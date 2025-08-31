# Guia de Implantação - Módulo de Produtos

Este guia fornece instruções detalhadas para implantar o Módulo de Produtos em diferentes ambientes, desde desenvolvimento local até produção em larga escala.

## 📋 Visão Geral

O Módulo de Produtos é uma aplicação containerizada que consiste em:
- **Backend FastAPI**: API RESTful com PostgreSQL
- **Frontend React**: Interface de usuário responsiva
- **Banco de Dados**: PostgreSQL com Redis para cache
- **Proxy Reverso**: Nginx para balanceamento de carga

## 🏗️ Arquiteturas de Implantação

### Desenvolvimento Local
- Docker Compose com hot reload
- Banco de dados local
- Sem SSL/HTTPS

### Staging/Homologação
- Docker Compose ou Kubernetes
- Banco de dados dedicado
- SSL com certificados auto-assinados
- Monitoramento básico

### Produção
- Kubernetes ou Docker Swarm
- Banco de dados gerenciado (RDS, Cloud SQL)
- SSL com certificados válidos
- Monitoramento completo
- Backup automatizado
- Alta disponibilidade

## 🐳 Implantação com Docker Compose

### Pré-requisitos

```bash
# Verificar versões mínimas
docker --version          # >= 20.10
docker-compose --version  # >= 1.29
```

### Configuração Básica

1. **Preparar Ambiente**

```bash
# Clonar/extrair projeto
cd modulo-produtos

# Criar diretórios necessários
mkdir -p data/postgres data/redis logs uploads

# Configurar permissões
chmod 755 data/postgres data/redis
chmod 777 uploads logs
```

2. **Configurar Variáveis de Ambiente**

```bash
# Backend
cat > backend/.env << EOF
DATABASE_URL=postgresql://admin:admin123@db-produtos:5432/gestao_lojas_produtos
REDIS_URL=redis://redis-produtos:6379/0
SECRET_KEY=$(openssl rand -hex 32)
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
ALLOWED_ORIGINS=https://seudominio.com,https://www.seudominio.com
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=5242880
ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/gif
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,PATCH,OPTIONS
CORS_ALLOW_HEADERS=*
EOF

# Frontend
cat > frontend/produto-frontend/.env << EOF
VITE_API_URL=https://api.seudominio.com/api/v1
VITE_APP_NAME=Sistema de Gestão de Lojas - Produtos
VITE_APP_VERSION=1.0.0
VITE_ENVIRONMENT=production
EOF
```

3. **Docker Compose para Produção**

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  db-produtos:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: gestao_lojas_produtos
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=pt_BR.UTF-8 --lc-ctype=pt_BR.UTF-8"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
      - ./database/init_produtos.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5433:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d gestao_lojas_produtos"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - produtos-network

  redis-produtos:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - ./data/redis:/data
    ports:
      - "6380:6379"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - produtos-network

  backend-produtos:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - DATABASE_URL=postgresql://admin:${DB_PASSWORD}@db-produtos:5432/gestao_lojas_produtos
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis-produtos:6379/0
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    ports:
      - "8001:8000"
    depends_on:
      db-produtos:
        condition: service_healthy
      redis-produtos:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - produtos-network

  frontend-produtos:
    build:
      context: ./frontend/produto-frontend
      dockerfile: Dockerfile.prod
    ports:
      - "3001:80"
    depends_on:
      - backend-produtos
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - produtos-network

  nginx-produtos:
    image: nginx:alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./uploads:/var/www/uploads
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend-produtos
      - frontend-produtos
    restart: unless-stopped
    networks:
      - produtos-network

networks:
  produtos-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

4. **Dockerfile de Produção - Backend**

```dockerfile
# backend/Dockerfile.prod
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicialização
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

5. **Dockerfile de Produção - Frontend**

```dockerfile
# frontend/produto-frontend/Dockerfile.prod
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

6. **Configuração do Nginx**

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend-produtos:8000;
    }

    upstream frontend {
        server frontend-produtos:80;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=static:10m rate=30r/s;

    server {
        listen 80;
        server_name seudominio.com www.seudominio.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name seudominio.com www.seudominio.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Upload files
        location /uploads/ {
            alias /var/www/uploads/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Frontend
        location / {
            limit_req zone=static burst=50 nodelay;
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Implantação

```bash
# 1. Definir senhas seguras
export DB_PASSWORD=$(openssl rand -base64 32)
export REDIS_PASSWORD=$(openssl rand -base64 32)

# 2. Construir e iniciar serviços
docker-compose -f docker-compose.prod.yml up -d --build

# 3. Executar migrações
docker-compose -f docker-compose.prod.yml exec backend-produtos alembic upgrade head

# 4. Verificar saúde dos serviços
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

## ☸️ Implantação com Kubernetes

### Pré-requisitos

```bash
# Verificar cluster Kubernetes
kubectl version --client
kubectl cluster-info

# Instalar Helm (opcional)
curl https://get.helm.sh/helm-v3.12.0-linux-amd64.tar.gz | tar xz
sudo mv linux-amd64/helm /usr/local/bin/
```

### Configuração de Namespace

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: produtos
  labels:
    name: produtos
```

### Secrets e ConfigMaps

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: produtos-secrets
  namespace: produtos
type: Opaque
data:
  db-password: <base64-encoded-password>
  redis-password: <base64-encoded-password>
  secret-key: <base64-encoded-secret>

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: produtos-config
  namespace: produtos
data:
  DATABASE_URL: "postgresql://admin:$(DB_PASSWORD)@postgres-service:5432/gestao_lojas_produtos"
  REDIS_URL: "redis://:$(REDIS_PASSWORD)@redis-service:6379/0"
  ENVIRONMENT: "production"
  DEBUG: "False"
  LOG_LEVEL: "INFO"
```

### Banco de Dados PostgreSQL

```yaml
# k8s/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: produtos
spec:
  serviceName: postgres-service
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
        - name: POSTGRES_DB
          value: gestao_lojas_produtos
        - name: POSTGRES_USER
          value: admin
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: produtos-secrets
              key: db-password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: produtos
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

### Backend FastAPI

```yaml
# k8s/backend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: produtos
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: produtos-backend:latest
        envFrom:
        - configMapRef:
            name: produtos-config
        - secretRef:
            name: produtos-secrets
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: produtos
spec:
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

### Frontend React

```yaml
# k8s/frontend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: produtos
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: produtos-frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"

---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: produtos
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

### Ingress

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: produtos-ingress
  namespace: produtos
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - seudominio.com
    - api.seudominio.com
    secretName: produtos-tls
  rules:
  - host: seudominio.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
  - host: api.seudominio.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
```

### Implantação no Kubernetes

```bash
# 1. Aplicar configurações
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/ingress.yaml

# 2. Verificar implantação
kubectl get pods -n produtos
kubectl get services -n produtos
kubectl get ingress -n produtos

# 3. Executar migrações
kubectl exec -it deployment/backend -n produtos -- alembic upgrade head

# 4. Monitorar logs
kubectl logs -f deployment/backend -n produtos
kubectl logs -f deployment/frontend -n produtos
```

## 🌐 Configuração de Domínio e SSL

### Certificados SSL com Let's Encrypt

```bash
# 1. Instalar cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml

# 2. Configurar ClusterIssuer
cat << EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@seudominio.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### Configuração de DNS

```bash
# Registros DNS necessários
# A    seudominio.com      -> IP_DO_CLUSTER
# A    api.seudominio.com  -> IP_DO_CLUSTER
# AAAA seudominio.com      -> IPv6_DO_CLUSTER (opcional)
```

## 📊 Monitoramento e Observabilidade

### Prometheus e Grafana

```yaml
# k8s/monitoring.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: produtos
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'backend'
      static_configs:
      - targets: ['backend-service:8000']
      metrics_path: /metrics
    - job_name: 'postgres'
      static_configs:
      - targets: ['postgres-service:5432']

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: produtos
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
      volumes:
      - name: config
        configMap:
          name: prometheus-config
```

### Logs Centralizados

```yaml
# k8s/logging.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: produtos
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch-service"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## 🔄 Backup e Recuperação

### Backup Automatizado

```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/produtos"
DB_NAME="gestao_lojas_produtos"

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
kubectl exec -n produtos deployment/postgres -- pg_dump -U admin $DB_NAME > $BACKUP_DIR/db_$DATE.sql

# Backup dos uploads
kubectl cp produtos/backend-deployment-xxx:/app/uploads $BACKUP_DIR/uploads_$DATE

# Compactar backup
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz $BACKUP_DIR/db_$DATE.sql $BACKUP_DIR/uploads_$DATE

# Limpar arquivos temporários
rm -rf $BACKUP_DIR/db_$DATE.sql $BACKUP_DIR/uploads_$DATE

# Manter apenas últimos 30 backups
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "Backup concluído: backup_$DATE.tar.gz"
```

### Cron Job para Backup

```yaml
# k8s/backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
  namespace: produtos
spec:
  schedule: "0 2 * * *"  # Todo dia às 2h
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15-alpine
            command:
            - /bin/sh
            - -c
            - |
              DATE=$(date +%Y%m%d_%H%M%S)
              pg_dump -h postgres-service -U admin gestao_lojas_produtos > /backup/db_$DATE.sql
              echo "Backup concluído: db_$DATE.sql"
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: produtos-secrets
                  key: db-password
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

## 🚀 Estratégias de Deploy

### Blue-Green Deployment

```bash
#!/bin/bash
# scripts/blue-green-deploy.sh

NAMESPACE="produtos"
NEW_VERSION=$1

if [ -z "$NEW_VERSION" ]; then
    echo "Uso: $0 <nova-versao>"
    exit 1
fi

# Verificar versão atual
CURRENT_VERSION=$(kubectl get deployment backend -n $NAMESPACE -o jsonpath='{.spec.template.spec.containers[0].image}' | cut -d':' -f2)

echo "Versão atual: $CURRENT_VERSION"
echo "Nova versão: $NEW_VERSION"

# Deploy da nova versão (green)
kubectl set image deployment/backend -n $NAMESPACE backend=produtos-backend:$NEW_VERSION

# Aguardar rollout
kubectl rollout status deployment/backend -n $NAMESPACE

# Verificar saúde
sleep 30
HEALTH_CHECK=$(kubectl exec -n $NAMESPACE deployment/backend -- curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$HEALTH_CHECK" = "200" ]; then
    echo "Deploy bem-sucedido!"
    # Limpar versão anterior se necessário
    # kubectl delete deployment backend-$CURRENT_VERSION -n $NAMESPACE
else
    echo "Deploy falhou! Fazendo rollback..."
    kubectl rollout undo deployment/backend -n $NAMESPACE
    exit 1
fi
```

### Canary Deployment

```yaml
# k8s/canary-deployment.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: backend-rollout
  namespace: produtos
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 10m}
      - setWeight: 40
      - pause: {duration: 10m}
      - setWeight: 60
      - pause: {duration: 10m}
      - setWeight: 80
      - pause: {duration: 10m}
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: produtos-backend:latest
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Banco de Dados Não Conecta

```bash
# Verificar status do PostgreSQL
kubectl logs -n produtos deployment/postgres

# Testar conectividade
kubectl exec -it -n produtos deployment/backend -- psql -h postgres-service -U admin -d gestao_lojas_produtos

# Verificar secrets
kubectl get secret produtos-secrets -n produtos -o yaml
```

#### 2. Frontend Não Carrega

```bash
# Verificar logs do frontend
kubectl logs -n produtos deployment/frontend

# Verificar configuração do Nginx
kubectl exec -it -n produtos deployment/frontend -- nginx -t

# Testar conectividade com backend
kubectl exec -it -n produtos deployment/frontend -- curl http://backend-service:8000/health
```

#### 3. SSL/TLS Issues

```bash
# Verificar certificados
kubectl describe certificate produtos-tls -n produtos

# Verificar cert-manager
kubectl logs -n cert-manager deployment/cert-manager

# Renovar certificado manualmente
kubectl delete certificate produtos-tls -n produtos
kubectl apply -f k8s/ingress.yaml
```

### Comandos Úteis

```bash
# Verificar recursos
kubectl top pods -n produtos
kubectl top nodes

# Escalar aplicação
kubectl scale deployment backend -n produtos --replicas=5

# Verificar eventos
kubectl get events -n produtos --sort-by=.metadata.creationTimestamp

# Debug de pod
kubectl describe pod <pod-name> -n produtos
kubectl exec -it <pod-name> -n produtos -- /bin/bash

# Verificar configuração
kubectl get configmap produtos-config -n produtos -o yaml
kubectl get secret produtos-secrets -n produtos -o yaml
```

## 📈 Otimização de Performance

### Configurações de Produção

```yaml
# Recursos otimizados para produção
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"

# HPA (Horizontal Pod Autoscaler)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: produtos
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Cache e CDN

```yaml
# Redis para cache
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: produtos
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        command: ["redis-server", "--appendonly", "yes", "--maxmemory", "256mb", "--maxmemory-policy", "allkeys-lru"]
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

## 🔐 Segurança

### Network Policies

```yaml
# k8s/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: produtos-network-policy
  namespace: produtos
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 5432
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
```

### Pod Security Standards

```yaml
# k8s/pod-security.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: produtos
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

Este guia fornece uma base sólida para implantar o Módulo de Produtos em diferentes ambientes. Adapte as configurações conforme suas necessidades específicas de infraestrutura e segurança.

