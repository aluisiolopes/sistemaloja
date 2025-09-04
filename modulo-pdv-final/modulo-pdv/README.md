# Sistema de Gestão de Lojas - Módulo Clientes

## Visão Geral

O **Módulo de Gestão de Clientes** é uma solução completa para gerenciamento de clientes em sistemas de gestão de lojas. Este módulo oferece funcionalidades abrangentes para cadastro, consulta, atualização e controle de clientes, tanto pessoas físicas quanto jurídicas.

### Características Principais

- **CRUD Completo**: Criação, leitura, atualização e exclusão de clientes
- **Suporte a Pessoa Física e Jurídica**: Campos específicos para CPF/CNPJ, RG/IE
- **Validação de Dados**: Validação robusta de CPF, CNPJ, email e outros campos
- **Busca Avançada**: Filtros por múltiplos critérios e busca textual
- **Interface Moderna**: Frontend React com componentes responsivos
- **API RESTful**: Backend FastAPI com documentação automática
- **Banco de Dados Robusto**: PostgreSQL com migrações Alembic
- **Testes Abrangentes**: Cobertura completa de testes unitários e de integração

## Arquitetura

### Stack Tecnológica

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: React 18 com Vite
- **Banco de Dados**: PostgreSQL 15
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0
- **Migrações**: Alembic
- **Testes**: Pytest
- **Containerização**: Docker & Docker Compose

### Estrutura do Projeto

```
modulo-clientes/
├── backend/                 # API FastAPI
│   ├── app/                # Código da aplicação
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   ├── schemas.py      # Schemas Pydantic
│   │   ├── crud.py         # Operações CRUD
│   │   ├── database.py     # Configuração do banco
│   │   ├── main.py         # Aplicação principal
│   │   └── routers/        # Endpoints da API
│   ├── alembic/            # Migrações do banco
│   ├── scripts/            # Scripts utilitários
│   ├── tests/              # Testes automatizados
│   └── requirements.txt    # Dependências Python
├── frontend/               # Aplicação React
│   └── cliente-frontend/   # Projeto React
│       ├── src/            # Código fonte
│       │   ├── components/ # Componentes React
│       │   ├── services/   # Serviços de API
│       │   └── utils/      # Utilitários
│       └── package.json    # Dependências Node.js
├── database/               # Scripts de banco
├── docs/                   # Documentação
└── docker-compose.yml      # Orquestração de containers
```

## Instalação e Configuração

### Pré-requisitos

- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)
- Node.js 20+ (para desenvolvimento local)
- PostgreSQL 15+ (para desenvolvimento local)

### Instalação com Docker (Recomendado)

1. **Clone o repositório**:
   ```bash
   git clone <repository-url>
   cd sistema-gestao-lojas/modulo-clientes
   ```

2. **Configure as variáveis de ambiente**:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/cliente-frontend/.env.example frontend/cliente-frontend/.env
   ```

3. **Inicie os serviços**:
   ```bash
   docker-compose up -d
   ```

4. **Execute as migrações**:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Acesse a aplicação**:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - Documentação da API: http://localhost:8000/docs

### Instalação Local

#### Backend

1. **Navegue para o diretório do backend**:
   ```bash
   cd backend
   ```

2. **Crie e ative o ambiente virtual**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**:
   ```bash
   # Certifique-se de que o PostgreSQL está rodando
   # Atualize a DATABASE_URL no arquivo .env
   
   # Execute as migrações
   alembic upgrade head
   ```

5. **Inicie o servidor**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend

1. **Navegue para o diretório do frontend**:
   ```bash
   cd frontend/cliente-frontend
   ```

2. **Instale as dependências**:
   ```bash
   pnpm install
   # ou
   npm install
   ```

3. **Inicie o servidor de desenvolvimento**:
   ```bash
   pnpm run dev --host
   # ou
   npm run dev -- --host
   ```

## Uso da Aplicação

### Interface Web

A interface web oferece uma experiência completa para gestão de clientes:

1. **Lista de Clientes**: Visualização paginada com filtros avançados
2. **Cadastro de Cliente**: Formulário completo com validação em tempo real
3. **Edição de Cliente**: Atualização de dados existentes
4. **Detalhes do Cliente**: Visualização completa das informações
5. **Busca Rápida**: Pesquisa por nome, email ou documento

### API REST

A API oferece endpoints completos para integração:

#### Endpoints Principais

- `GET /api/v1/clientes/` - Lista clientes com paginação e filtros
- `POST /api/v1/clientes/` - Cria novo cliente
- `GET /api/v1/clientes/{id}` - Busca cliente por ID
- `PUT /api/v1/clientes/{id}` - Atualiza cliente
- `DELETE /api/v1/clientes/{id}` - Remove cliente
- `PATCH /api/v1/clientes/{id}/inativar` - Inativa cliente

#### Exemplos de Uso

**Criar Cliente Pessoa Física**:
```bash
curl -X POST "http://localhost:8000/api/v1/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "tipo_cliente": "pessoa_fisica",
    "cpf_cnpj": "12345678901",
    "email": "joao@email.com",
    "telefone": "11987654321"
  }'
```

**Listar Clientes com Filtros**:
```bash
curl "http://localhost:8000/api/v1/clientes/?tipo_cliente=pessoa_fisica&status=ativo&pagina=1&por_pagina=20"
```

## Desenvolvimento

### Estrutura do Código

#### Backend (FastAPI)

- **models.py**: Define os modelos SQLAlchemy para o banco de dados
- **schemas.py**: Schemas Pydantic para validação de entrada e saída
- **crud.py**: Operações de banco de dados (Create, Read, Update, Delete)
- **routers/**: Endpoints da API organizados por funcionalidade
- **database.py**: Configuração de conexão com o banco de dados

#### Frontend (React)

- **components/**: Componentes React reutilizáveis
- **services/**: Serviços para comunicação com a API
- **utils/**: Funções utilitárias e formatadores
- **hooks/**: Custom hooks do React

### Executando Testes

#### Backend

```bash
cd backend

# Executar todos os testes
python -m pytest tests/ -v

# Executar com cobertura
python -m pytest tests/ --cov=app --cov-report=html

# Executar script de testes interativo
python scripts/test_runner.py
```

#### Frontend

```bash
cd frontend/cliente-frontend

# Executar testes
npm test

# Executar testes com cobertura
npm run test:coverage
```

### Scripts Utilitários

O projeto inclui vários scripts para facilitar o desenvolvimento:

- **scripts/init_db.py**: Inicializa o banco de dados com dados de exemplo
- **scripts/run_migrations.py**: Interface interativa para gerenciar migrações
- **scripts/test_runner.py**: Executa testes com diferentes opções

## Banco de Dados

### Modelo de Dados

O módulo utiliza um modelo de dados robusto para clientes:

#### Tabela: clientes.clientes

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | UUID | Identificador único |
| nome | VARCHAR(255) | Nome completo |
| tipo_cliente | ENUM | pessoa_fisica ou pessoa_juridica |
| cpf_cnpj | VARCHAR(18) | CPF ou CNPJ |
| rg_ie | VARCHAR(20) | RG ou Inscrição Estadual |
| email | VARCHAR(255) | Email de contato |
| telefone | VARCHAR(20) | Telefone fixo |
| celular | VARCHAR(20) | Telefone celular |
| endereco | VARCHAR(255) | Logradouro |
| numero | VARCHAR(10) | Número do endereço |
| complemento | VARCHAR(100) | Complemento |
| bairro | VARCHAR(100) | Bairro |
| cidade | VARCHAR(100) | Cidade |
| estado | VARCHAR(2) | UF do estado |
| cep | VARCHAR(10) | CEP |
| data_nascimento | DATE | Data de nascimento |
| profissao | VARCHAR(100) | Profissão |
| observacoes | TEXT | Observações |
| status | ENUM | ativo, inativo, bloqueado |
| limite_credito | INTEGER | Limite em centavos |
| pontos_fidelidade | INTEGER | Pontos acumulados |
| data_criacao | TIMESTAMP | Data de criação |
| data_atualizacao | TIMESTAMP | Data da última atualização |
| criado_por | VARCHAR(100) | Usuário que criou |
| atualizado_por | VARCHAR(100) | Usuário que atualizou |

### Migrações

O sistema utiliza Alembic para controle de versão do banco de dados:

```bash
# Criar nova migração
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

## Segurança

### Validações Implementadas

- **CPF/CNPJ**: Validação de formato e dígitos verificadores
- **Email**: Validação de formato RFC compliant
- **CEP**: Validação de formato brasileiro
- **Estados**: Validação contra lista de UFs válidas
- **Dados Obrigatórios**: Validação de campos requeridos

### Boas Práticas

- Sanitização de entrada de dados
- Validação tanto no frontend quanto no backend
- Logs de auditoria para operações críticas
- Tratamento seguro de erros sem exposição de dados sensíveis

## Monitoramento e Logs

### Logs da Aplicação

O sistema gera logs estruturados para:
- Operações CRUD de clientes
- Erros de validação
- Falhas de conexão com banco de dados
- Tentativas de acesso inválido

### Métricas

- Número de clientes cadastrados
- Distribuição por tipo (PF/PJ)
- Distribuição por status
- Operações por endpoint

## Contribuição

### Padrões de Código

- **Python**: Seguir PEP 8 com linha máxima de 100 caracteres
- **JavaScript**: Usar ESLint e Prettier
- **Commits**: Seguir Conventional Commits
- **Testes**: Manter cobertura mínima de 80%

### Fluxo de Desenvolvimento

1. Criar branch feature a partir de main
2. Implementar funcionalidade com testes
3. Executar validações locais
4. Criar Pull Request
5. Revisar código
6. Merge após aprovação

## Troubleshooting

### Problemas Comuns

**Erro de Conexão com Banco**:
```
sqlalchemy.exc.OperationalError: connection refused
```
- Verificar se PostgreSQL está rodando
- Confirmar configurações de conexão no .env
- Verificar firewall e permissões de rede

**Erro de Migração**:
```
alembic.util.exc.CommandError: Can't locate revision
```
- Verificar se o banco está inicializado
- Executar `alembic stamp head` se necessário
- Verificar integridade dos arquivos de migração

**Erro de CORS no Frontend**:
```
Access to fetch blocked by CORS policy
```
- Verificar configuração de CORS no backend
- Confirmar URL da API no frontend
- Verificar se o backend está rodando

### Logs de Debug

Para habilitar logs detalhados:

```bash
# Backend
export DEBUG=True
export LOG_LEVEL=DEBUG

# Executar com logs SQL
export SQLALCHEMY_ECHO=True
```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para detalhes.

## Suporte

Para suporte técnico ou dúvidas:
- Documentação da API: http://localhost:8000/docs
- Issues: Criar issue no repositório
- Email: suporte@gestaolojas.com

---

**Desenvolvido por**: Manus AI  
**Versão**: 1.0.0  
**Data**: 2024

