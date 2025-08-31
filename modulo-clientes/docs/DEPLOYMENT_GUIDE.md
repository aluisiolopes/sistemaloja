# Guia de Implantação - Módulo Clientes

## Visão Geral

Este guia fornece instruções detalhadas para implantação do Módulo de Gestão de Clientes em diferentes ambientes, desde desenvolvimento local até produção em nuvem.

## Ambientes de Implantação

### 1. Desenvolvimento Local

#### Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Git
- 4GB RAM disponível
- 10GB espaço em disco

#### Passos de Instalação

1. **Clone do Repositório**:
   ```bash
   git clone <repository-url>
   cd sistema-gestao-lojas/modulo-clientes
   ```

2. **Configuração de Ambiente**:
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   
   # Frontend
   cp frontend/cliente-frontend/.env.example frontend/cliente-frontend/.env
   ```

3. **Inicialização dos Serviços**:
   ```bash
   docker-compose up -d
   ```

4. **Verificação da Instalação**:
   ```bash
   # Verificar status dos containers
   docker-compose ps
   
   # Verificar logs
   docker-compose logs -f
   
   # Testar endpoints
   curl http://localhost:8000/health
   curl http://localhost:3000
   ```

5. **Inicialização do Banco de Dados**:
   ```bash
   # Executar migrações
   docker-compose exec backend alembic upgrade head
   
   # Inserir dados de exemplo (opcional)
   docker-compose exec backend python scripts/init_db.py
   ```

### 2. Ambiente de Teste/Staging

#### Infraestrutura Recomendada

- **Servidor**: 2 vCPUs, 4GB RAM, 50GB SSD
- **Sistema Operacional**: Ubuntu 22.04 LTS
- **Banco de Dados**: PostgreSQL 15
- **Proxy Reverso**: Nginx
- **SSL**: Let's Encrypt

#### Configuração do Servidor

1. **Preparação do Sistema**:
   ```bash
   # Atualizar sistema
   sudo apt update && sudo apt upgrade -y
   
   # Instalar dependências
   sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx
   
   # Configurar Docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   ```

2. **Configuração do Nginx**:
   ```nginx
   # /etc/nginx/sites-available/clientes-staging
   server {
       listen 80;
       server_name staging-clientes.exemplo.com;
   
       location /api/ {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Configuração SSL**:
   ```bash
   # Habilitar site
   sudo ln -s /etc/nginx/sites-available/clientes-staging /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   
   # Configurar SSL
   sudo certbot --nginx -d staging-clientes.exemplo.com
   ```

4. **Variáveis de Ambiente para Staging**:
   ```bash
   # backend/.env
   DATABASE_URL=postgresql://user:password@localhost:5432/clientes_staging
   ENVIRONMENT=staging
   DEBUG=False
   ALLOWED_ORIGINS=https://staging-clientes.exemplo.com
   
   # frontend/.env
   VITE_API_URL=https://staging-clientes.exemplo.com/api/v1
   VITE_ENVIRONMENT=staging
   ```

### 3. Ambiente de Produção

#### Infraestrutura Recomendada

**Opção 1: Servidor Único**
- **Servidor**: 4 vCPUs, 8GB RAM, 100GB SSD
- **Banco de Dados**: PostgreSQL 15 (dedicado)
- **Cache**: Redis 7
- **Load Balancer**: Nginx
- **Monitoramento**: Prometheus + Grafana

**Opção 2: Arquitetura em Nuvem (AWS)**
- **Aplicação**: ECS Fargate ou EC2
- **Banco de Dados**: RDS PostgreSQL
- **Cache**: ElastiCache Redis
- **Load Balancer**: Application Load Balancer
- **CDN**: CloudFront
- **Monitoramento**: CloudWatch

#### Configuração de Produção

1. **Configuração de Segurança**:
   ```bash
   # Firewall
   sudo ufw enable
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   
   # Fail2ban
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

2. **Configuração do Banco de Dados**:
   ```sql
   -- Criar usuário específico para a aplicação
   CREATE USER clientes_app WITH PASSWORD 'senha_segura';
   CREATE DATABASE clientes_prod OWNER clientes_app;
   GRANT ALL PRIVILEGES ON DATABASE clientes_prod TO clientes_app;
   
   -- Configurações de performance
   ALTER SYSTEM SET shared_buffers = '256MB';
   ALTER SYSTEM SET effective_cache_size = '1GB';
   ALTER SYSTEM SET maintenance_work_mem = '64MB';
   SELECT pg_reload_conf();
   ```

3. **Docker Compose para Produção**:
   ```yaml
   # docker-compose.prod.yml
   version: '3.8'
   
   services:
     backend:
       build:
         context: ./backend
         dockerfile: Dockerfile.prod
       environment:
         - DATABASE_URL=${DATABASE_URL}
         - REDIS_URL=${REDIS_URL}
         - SECRET_KEY=${SECRET_KEY}
         - ENVIRONMENT=production
       restart: unless-stopped
       depends_on:
         - redis
   
     frontend:
       build:
         context: ./frontend/cliente-frontend
         dockerfile: Dockerfile.prod
       restart: unless-stopped
   
     redis:
       image: redis:7-alpine
       restart: unless-stopped
       command: redis-server --requirepass ${REDIS_PASSWORD}
   
     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx/prod.conf:/etc/nginx/nginx.conf
         - ./ssl:/etc/nginx/ssl
       restart: unless-stopped
       depends_on:
         - backend
         - frontend
   ```

4. **Configuração de Monitoramento**:
   ```yaml
   # Adicionar ao docker-compose.prod.yml
   prometheus:
     image: prom/prometheus
     volumes:
       - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
     ports:
       - "9090:9090"
   
   grafana:
     image: grafana/grafana
     environment:
       - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
     ports:
       - "3001:3000"
     volumes:
       - grafana-data:/var/lib/grafana
   ```

## Configurações de Ambiente

### Variáveis de Ambiente - Backend

```bash
# Banco de Dados
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://password@host:port

# Aplicação
ENVIRONMENT=production|staging|development
DEBUG=False
SECRET_KEY=chave_secreta_muito_segura

# CORS
ALLOWED_ORIGINS=https://exemplo.com,https://www.exemplo.com

# Logs
LOG_LEVEL=INFO
LOG_FORMAT=json

# Monitoramento
SENTRY_DSN=https://...
PROMETHEUS_ENABLED=true
```

### Variáveis de Ambiente - Frontend

```bash
# API
VITE_API_URL=https://api.exemplo.com/v1

# Aplicação
VITE_ENVIRONMENT=production
VITE_APP_NAME=Sistema de Gestão de Lojas - Clientes
VITE_APP_VERSION=1.0.0

# Analytics (opcional)
VITE_GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX
```

## Backup e Recuperação

### Backup do Banco de Dados

1. **Script de Backup Automático**:
   ```bash
   #!/bin/bash
   # backup_db.sh
   
   DATE=$(date +%Y%m%d_%H%M%S)
   BACKUP_DIR="/backups/clientes"
   DB_NAME="clientes_prod"
   
   mkdir -p $BACKUP_DIR
   
   # Backup completo
   pg_dump -h localhost -U clientes_app -d $DB_NAME \
     --no-password --verbose --format=custom \
     --file="$BACKUP_DIR/clientes_$DATE.backup"
   
   # Manter apenas últimos 7 dias
   find $BACKUP_DIR -name "*.backup" -mtime +7 -delete
   
   # Upload para S3 (opcional)
   aws s3 cp "$BACKUP_DIR/clientes_$DATE.backup" \
     s3://meu-bucket/backups/clientes/
   ```

2. **Agendamento via Cron**:
   ```bash
   # Backup diário às 2h da manhã
   0 2 * * * /scripts/backup_db.sh
   ```

### Recuperação de Backup

```bash
# Restaurar backup
pg_restore -h localhost -U clientes_app -d clientes_prod \
  --verbose --clean --if-exists \
  /backups/clientes/clientes_20240121_020000.backup
```

## Monitoramento e Alertas

### Métricas Importantes

1. **Aplicação**:
   - Tempo de resposta da API
   - Taxa de erro (4xx, 5xx)
   - Throughput (requests/segundo)
   - Uso de CPU e memória

2. **Banco de Dados**:
   - Conexões ativas
   - Tempo de query
   - Tamanho do banco
   - Locks e deadlocks

3. **Sistema**:
   - Uso de CPU
   - Uso de memória
   - Espaço em disco
   - Rede (I/O)

### Configuração do Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'clientes-api'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Alertas Críticos

```yaml
# alerts.yml
groups:
  - name: clientes-api
    rules:
      - alert: APIHighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        annotations:
          summary: "Alta taxa de erro na API"

      - alert: DatabaseConnectionsHigh
        expr: pg_stat_activity_count > 80
        for: 2m
        annotations:
          summary: "Muitas conexões no banco de dados"

      - alert: DiskSpaceLow
        expr: disk_free_percent < 10
        for: 1m
        annotations:
          summary: "Pouco espaço em disco"
```

## Segurança

### Checklist de Segurança

- [ ] HTTPS configurado com certificado válido
- [ ] Firewall configurado (apenas portas necessárias)
- [ ] Senhas fortes para banco de dados
- [ ] Backup criptografado
- [ ] Logs de auditoria habilitados
- [ ] Rate limiting configurado
- [ ] Headers de segurança configurados
- [ ] Dependências atualizadas
- [ ] Monitoramento de segurança ativo

### Headers de Segurança (Nginx)

```nginx
# Adicionar ao bloco server
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

## Troubleshooting

### Problemas Comuns

1. **Container não inicia**:
   ```bash
   # Verificar logs
   docker-compose logs backend
   
   # Verificar recursos
   docker system df
   docker system prune
   ```

2. **Erro de conexão com banco**:
   ```bash
   # Testar conexão
   docker-compose exec backend python -c "
   from app.database import engine
   with engine.connect() as conn:
       print('Conexão OK')
   "
   ```

3. **Performance lenta**:
   ```bash
   # Verificar queries lentas
   docker-compose exec postgres psql -U clientes_app -d clientes_prod -c "
   SELECT query, mean_time, calls 
   FROM pg_stat_statements 
   ORDER BY mean_time DESC 
   LIMIT 10;
   "
   ```

### Logs Importantes

```bash
# Logs da aplicação
docker-compose logs -f backend

# Logs do banco
docker-compose logs -f postgres

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs do sistema
sudo journalctl -f -u docker
```

## Atualizações

### Processo de Atualização

1. **Backup completo**
2. **Teste em staging**
3. **Janela de manutenção**
4. **Deploy gradual**
5. **Verificação pós-deploy**
6. **Rollback se necessário**

### Script de Deploy

```bash
#!/bin/bash
# deploy.sh

set -e

echo "Iniciando deploy..."

# Backup
./scripts/backup_db.sh

# Pull das imagens
docker-compose -f docker-compose.prod.yml pull

# Parar serviços
docker-compose -f docker-compose.prod.yml down

# Executar migrações
docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head

# Iniciar serviços
docker-compose -f docker-compose.prod.yml up -d

# Verificar saúde
sleep 30
curl -f http://localhost:8000/health || exit 1

echo "Deploy concluído com sucesso!"
```

## Suporte

Para suporte na implantação:
- Documentação: [README.md](../README.md)
- Issues: Repositório GitHub
- Email: devops@gestaolojas.com

---

**Versão**: 1.0.0  
**Última Atualização**: 2024-01-21

