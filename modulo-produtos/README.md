# Módulo 1.2 - Cadastro de Produtos

Sistema completo de gestão de produtos para o Sistema de Gestão de Lojas, desenvolvido com FastAPI (backend) e React (frontend).

## 📋 Visão Geral

Este módulo oferece funcionalidades completas para gerenciamento de produtos, categorias e marcas, incluindo:

- **CRUD Completo**: Criar, listar, atualizar e remover produtos
- **Gestão de Categorias**: Organização hierárquica de produtos
- **Gestão de Marcas**: Controle de fabricantes e fornecedores
- **Busca Avançada**: Filtros por múltiplos critérios
- **Validações Robustas**: Códigos de barras, SKUs únicos
- **Interface Responsiva**: Compatível com desktop e mobile
- **API RESTful**: Documentação automática com Swagger/OpenAPI

## 🏗️ Arquitetura

```
modulo-produtos/
├── backend/                 # API FastAPI
│   ├── app/                # Código da aplicação
│   │   ├── main.py        # Aplicação principal
│   │   ├── models.py      # Modelos SQLAlchemy
│   │   ├── schemas.py     # Schemas Pydantic
│   │   ├── crud.py        # Operações CRUD
│   │   ├── database.py    # Configuração do banco
│   │   └── routers/       # Endpoints da API
│   ├── alembic/           # Migrações do banco
│   ├── scripts/           # Scripts utilitários
│   ├── tests/             # Testes automatizados
│   └── requirements.txt   # Dependências Python
├── frontend/              # Aplicação React
│   └── produto-frontend/  # Projeto React
│       ├── src/           # Código fonte
│       │   ├── components/ # Componentes React
│       │   ├── services/  # Serviços de API
│       │   └── utils/     # Utilitários
│       └── package.json   # Dependências Node.js
├── database/              # Scripts de banco
├── docs/                  # Documentação técnica
└── docker-compose.yml     # Orquestração de containers
```

## 🚀 Instalação Rápida

### Pré-requisitos

- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)
- Node.js 20+ (para desenvolvimento local)

### Usando Docker (Recomendado)

```bash
# 1. Clonar/extrair o projeto
cd modulo-produtos

# 2. Configurar variáveis de ambiente
cp backend/.env.example backend/.env
cp frontend/produto-frontend/.env.example frontend/produto-frontend/.env

# 3. Iniciar todos os serviços
docker-compose up -d

# 4. Executar migrações do banco
docker-compose exec backend-produtos alembic upgrade head

# 5. Acessar a aplicação
# Frontend: http://localhost:3001
# API: http://localhost:8001
# Documentação: http://localhost:8001/docs
```

### Desenvolvimento Local

#### Backend

```bash
cd backend

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
python scripts/init_db.py

# Executar migrações
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --port 8001
```

#### Frontend

```bash
cd frontend/produto-frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

## 📊 Funcionalidades

### Gestão de Produtos

#### Campos Suportados
- **Identificação**: Nome, descrição, SKU, código de barras
- **Preços**: Venda e custo (em centavos para precisão)
- **Classificação**: Categoria, marca, unidade de medida
- **Status**: Ativo, inativo, esgotado, promoção
- **Mídia**: URL de imagem, upload de arquivos
- **Auditoria**: Criado por, atualizado por, timestamps

#### Validações Implementadas
- **SKU único**: Prevenção de duplicatas
- **Código de barras único**: Validação de formato
- **Preços válidos**: Valores não negativos
- **Campos obrigatórios**: Nome e preços mínimos

### API Endpoints

#### Produtos
- `GET /api/v1/produtos/` - Listar produtos (paginado)
- `POST /api/v1/produtos/` - Criar produto
- `GET /api/v1/produtos/{id}` - Buscar por ID
- `PUT /api/v1/produtos/{id}` - Atualizar produto
- `DELETE /api/v1/produtos/{id}` - Remover produto
- `PATCH /api/v1/produtos/{id}/inativar` - Inativar produto
- `GET /api/v1/produtos/search/{termo}` - Busca textual
- `GET /api/v1/produtos/stats/resumo` - Estatísticas

#### Categorias
- `GET /api/v1/categorias/` - Listar categorias
- `POST /api/v1/categorias/` - Criar categoria
- `GET /api/v1/categorias/{id}` - Buscar por ID
- `PUT /api/v1/categorias/{id}` - Atualizar categoria
- `DELETE /api/v1/categorias/{id}` - Remover categoria

#### Marcas
- `GET /api/v1/marcas/` - Listar marcas
- `POST /api/v1/marcas/` - Criar marca
- `GET /api/v1/marcas/{id}` - Buscar por ID
- `PUT /api/v1/marcas/{id}` - Atualizar marca
- `DELETE /api/v1/marcas/{id}` - Remover marca

### Interface do Usuário

#### Componentes Principais
- **ProdutoList**: Listagem com paginação e filtros
- **ProdutoForm**: Formulário de cadastro/edição
- **ProdutoDetails**: Visualização detalhada

#### Funcionalidades da Interface
- **Busca em tempo real**: Pesquisa instantânea
- **Filtros avançados**: Por status, categoria, marca
- **Paginação eficiente**: Navegação otimizada
- **Validação de formulários**: Feedback imediato
- **Formatação automática**: Preços, datas, enums

## 🧪 Testes

### Executar Testes

```bash
cd backend

# Todos os testes
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/test_models.py -v
python -m pytest tests/test_crud.py -v
python -m pytest tests/test_api.py -v

# Com cobertura de código
pip install coverage
coverage run -m pytest tests/
coverage report
coverage html  # Relatório HTML em htmlcov/

# Script interativo
python scripts/test_runner.py
```

### Cobertura de Testes
- **Modelos**: Validações e relacionamentos
- **CRUD**: Operações de banco de dados
- **API**: Endpoints e integração
- **Cobertura**: > 80% do código

## 🔧 Configuração

### Variáveis de Ambiente

#### Backend (.env)
```env
DATABASE_URL=postgresql://admin:admin123@db-produtos:5432/gestao_lojas_produtos
REDIS_URL=redis://redis-produtos:6379/0
SECRET_KEY=sua_chave_secreta_aqui
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:3001,http://localhost:8001
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE=5242880
ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/gif
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8001/api/v1
VITE_APP_NAME=Sistema de Gestão de Lojas - Produtos
VITE_APP_VERSION=1.0.0
```

### Banco de Dados

#### Schema
- **Schema**: `produtos`
- **Tabelas**: `produtos`, `categorias`, `marcas`
- **Enums**: `unidademedida`, `statusproduto`
- **Índices**: Otimizados para consultas frequentes

#### Migrações
```bash
# Verificar status
alembic current

# Executar migrações
alembic upgrade head

# Criar nova migração
alembic revision --autogenerate -m "Descrição"

# Script interativo
python scripts/run_migrations.py
```

## 📈 Performance

### Otimizações Implementadas
- **Índices de banco**: Campos de busca frequente
- **Paginação eficiente**: Consultas limitadas
- **Lazy loading**: Relacionamentos sob demanda
- **Cache Redis**: Dados frequentemente acessados
- **Compressão**: Assets do frontend

### Métricas Esperadas
- **Listagem**: < 200ms para 1000 produtos
- **Busca**: < 100ms para consultas simples
- **Criação**: < 50ms para novos produtos
- **Atualização**: < 30ms para modificações

## 🔒 Segurança

### Medidas Implementadas
- **Validação de entrada**: Sanitização em todas as camadas
- **SQL Injection**: Proteção via ORM
- **CORS configurado**: Origens permitidas
- **Headers de segurança**: X-Frame-Options, CSP
- **Logs de auditoria**: Rastreamento de alterações

### Validações de Dados
- **Produtos**: SKU e código de barras únicos
- **Preços**: Valores não negativos
- **Uploads**: Tipos e tamanhos de arquivo
- **Entrada**: Sanitização de strings

## 🚀 Deploy

### Desenvolvimento
```bash
docker-compose up -d
```

### Produção
Consulte `docs/DEPLOYMENT_GUIDE.md` para instruções detalhadas de implantação em ambiente de produção.

## 📚 Documentação

- **API**: http://localhost:8001/docs (Swagger UI)
- **Redoc**: http://localhost:8001/redoc
- **Guia de Desenvolvimento**: `docs/DEVELOPMENT_GUIDE.md`
- **Guia de Implantação**: `docs/DEPLOYMENT_GUIDE.md`

## 🤝 Contribuição

### Estrutura de Desenvolvimento
1. **Fork** do repositório
2. **Branch** para nova funcionalidade
3. **Testes** para código novo
4. **Pull Request** com descrição detalhada

### Padrões de Código
- **Python**: PEP 8, type hints
- **JavaScript**: ES6+, JSDoc
- **Commits**: Conventional Commits
- **Testes**: Cobertura > 80%

## 📋 Roadmap

### Versão 1.1.0
- [ ] Gestão de variações de produtos
- [ ] Importação/exportação CSV
- [ ] Integração com código de barras
- [ ] Histórico de alterações

### Versão 1.2.0
- [ ] API GraphQL
- [ ] Websockets para tempo real
- [ ] Relatórios avançados
- [ ] Mobile app (React Native)

## 🐛 Problemas Conhecidos

Nenhum problema crítico conhecido. Para reportar bugs:
1. Verificar issues existentes
2. Criar nova issue com detalhes
3. Incluir logs e passos para reproduzir

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Equipe

- **Desenvolvedor Principal**: Manus AI
- **Arquitetura**: Sistema modular escalável
- **Tecnologias**: FastAPI, React, PostgreSQL

## 📞 Suporte

- **Documentação**: README.md e docs/
- **Issues**: GitHub Issues
- **Email**: suporte@gestaolojas.com

---

**Desenvolvido com ❤️ por Manus AI**

