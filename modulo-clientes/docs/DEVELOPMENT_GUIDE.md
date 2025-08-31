# Guia de Desenvolvimento - Módulo Clientes

## Visão Geral

Este guia fornece informações detalhadas para desenvolvedores que desejam contribuir ou estender o Módulo de Gestão de Clientes. Inclui padrões de código, arquitetura, fluxos de desenvolvimento e boas práticas.

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- Git
- Docker (opcional, mas recomendado)
- IDE recomendado: VS Code com extensões Python e React

### Configuração Inicial

1. **Clone e Configuração**:
   ```bash
   git clone <repository-url>
   cd sistema-gestao-lojas/modulo-clientes
   
   # Configurar hooks do Git
   cp .githooks/pre-commit .git/hooks/
   chmod +x .git/hooks/pre-commit
   ```

2. **Backend - Ambiente Python**:
   ```bash
   cd backend
   
   # Criar ambiente virtual
   python3.11 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou venv\Scripts\activate  # Windows
   
   # Instalar dependências
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # Configurar variáveis de ambiente
   cp .env.example .env
   ```

3. **Frontend - Ambiente Node.js**:
   ```bash
   cd frontend/cliente-frontend
   
   # Instalar dependências
   pnpm install
   # ou npm install
   
   # Configurar variáveis de ambiente
   cp .env.example .env
   ```

4. **Banco de Dados Local**:
   ```bash
   # Opção 1: Docker (recomendado)
   docker-compose up -d postgres redis
   
   # Opção 2: Instalação local
   sudo apt install postgresql-15 redis-server
   sudo -u postgres createdb clientes_dev
   ```

## Arquitetura do Sistema

### Backend (FastAPI)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação principal FastAPI
│   ├── database.py          # Configuração SQLAlchemy
│   ├── models.py            # Modelos ORM
│   ├── schemas.py           # Schemas Pydantic
│   ├── crud.py              # Operações CRUD
│   ├── dependencies.py      # Dependências FastAPI
│   ├── exceptions.py        # Exceções customizadas
│   ├── utils.py             # Utilitários
│   └── routers/
│       ├── __init__.py
│       └── clientes.py      # Endpoints de clientes
├── alembic/                 # Migrações
├── scripts/                 # Scripts utilitários
├── tests/                   # Testes automatizados
└── requirements.txt         # Dependências
```

### Frontend (React)

```
frontend/cliente-frontend/
├── src/
│   ├── components/          # Componentes React
│   │   ├── ClienteForm.jsx
│   │   ├── ClienteList.jsx
│   │   └── ClienteDetails.jsx
│   ├── services/            # Serviços de API
│   │   └── api.js
│   ├── utils/               # Utilitários
│   │   └── formatters.js
│   ├── hooks/               # Custom hooks
│   ├── contexts/            # React contexts
│   ├── styles/              # Estilos CSS
│   ├── App.jsx              # Componente principal
│   └── main.jsx             # Entry point
├── public/                  # Arquivos estáticos
└── package.json             # Dependências
```

## Padrões de Código

### Backend (Python)

#### Estilo de Código

- **PEP 8** com linha máxima de 100 caracteres
- **Type hints** obrigatórios
- **Docstrings** no formato Google
- **Imports** organizados com isort

```python
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Cliente
from app.schemas import ClienteCreate, ClienteUpdate


class ClienteCRUD:
    """Classe para operações CRUD de clientes."""
    
    def __init__(self, db: Session) -> None:
        """Inicializa o CRUD com sessão do banco.
        
        Args:
            db: Sessão do SQLAlchemy
        """
        self.db = db
    
    def create(self, cliente_data: ClienteCreate) -> Cliente:
        """Cria um novo cliente.
        
        Args:
            cliente_data: Dados do cliente a ser criado
            
        Returns:
            Cliente criado
            
        Raises:
            ValueError: Se CPF/CNPJ já existe
        """
        # Implementação...
```

#### Estrutura de Modelos

```python
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class Cliente(Base):
    """Modelo de cliente."""
    
    __tablename__ = "clientes"
    __table_args__ = {"schema": "clientes"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    nome = Column(String(255), nullable=False, index=True)
    # ... outros campos
    
    def to_dict(self) -> dict:
        """Converte modelo para dicionário."""
        return {
            "id": str(self.id),
            "nome": self.nome,
            # ... outros campos
        }
    
    def __repr__(self) -> str:
        return f"<Cliente(id={self.id}, nome='{self.nome}')>"
```

#### Estrutura de Schemas

```python
from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator


class ClienteBase(BaseModel):
    """Schema base para cliente."""
    
    nome: str
    tipo_cliente: Optional[str] = "pessoa_fisica"
    email: Optional[EmailStr] = None
    
    @validator('nome')
    def validate_nome(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 caracteres')
        return v.strip().title()


class ClienteCreate(ClienteBase):
    """Schema para criação de cliente."""
    pass


class ClienteUpdate(BaseModel):
    """Schema para atualização de cliente."""
    
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    # ... outros campos opcionais


class ClienteResponse(ClienteBase):
    """Schema de resposta com dados completos."""
    
    id: UUID
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

### Frontend (React)

#### Estrutura de Componentes

```jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

import { api } from '../services/api';
import { formatCpfCnpj } from '../utils/formatters';

/**
 * Componente para listagem de clientes
 */
const ClienteList = ({ filters, onClienteSelect }) => {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadClientes();
  }, [filters]);

  const loadClientes = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.getClientes(filters);
      setClientes(response.clientes);
    } catch (err) {
      setError('Erro ao carregar clientes');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Carregando...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="cliente-list">
      {clientes.map(cliente => (
        <div 
          key={cliente.id} 
          className="cliente-item"
          onClick={() => onClienteSelect(cliente)}
        >
          <h3>{cliente.nome}</h3>
          <p>{formatCpfCnpj(cliente.cpf_cnpj)}</p>
          <p>{cliente.email}</p>
        </div>
      ))}
    </div>
  );
};

ClienteList.propTypes = {
  filters: PropTypes.object,
  onClienteSelect: PropTypes.func.isRequired
};

ClienteList.defaultProps = {
  filters: {}
};

export default ClienteList;
```

#### Serviços de API

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Métodos específicos
  async getClientes(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/clientes/?${params}`);
  }

  async createCliente(clienteData) {
    return this.request('/clientes/', {
      method: 'POST',
      body: JSON.stringify(clienteData)
    });
  }

  async updateCliente(id, clienteData) {
    return this.request(`/clientes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(clienteData)
    });
  }

  async deleteCliente(id) {
    return this.request(`/clientes/${id}`, {
      method: 'DELETE'
    });
  }
}

export const api = new ApiService();
```

## Fluxo de Desenvolvimento

### Git Workflow

1. **Branches**:
   - `main`: Código de produção
   - `develop`: Código de desenvolvimento
   - `feature/nome-da-feature`: Novas funcionalidades
   - `bugfix/nome-do-bug`: Correções de bugs
   - `hotfix/nome-do-hotfix`: Correções urgentes

2. **Processo**:
   ```bash
   # Criar feature branch
   git checkout develop
   git pull origin develop
   git checkout -b feature/nova-funcionalidade
   
   # Desenvolver e commitar
   git add .
   git commit -m "feat: adicionar nova funcionalidade"
   
   # Push e Pull Request
   git push origin feature/nova-funcionalidade
   # Criar PR no GitHub/GitLab
   ```

3. **Padrão de Commits** (Conventional Commits):
   ```
   feat: nova funcionalidade
   fix: correção de bug
   docs: atualização de documentação
   style: formatação de código
   refactor: refatoração
   test: adição de testes
   chore: tarefas de manutenção
   ```

### Desenvolvimento de Features

#### 1. Backend (API Endpoint)

```python
# 1. Adicionar modelo (se necessário)
# app/models.py

# 2. Criar schema
# app/schemas.py
class NovoSchema(BaseModel):
    campo: str

# 3. Implementar CRUD
# app/crud.py
def nova_operacao(db: Session, data: NovoSchema):
    # Implementação
    pass

# 4. Criar endpoint
# app/routers/clientes.py
@router.post("/nova-operacao/")
async def nova_operacao(
    data: NovoSchema,
    db: Session = Depends(get_db)
):
    result = crud.nova_operacao(db, data)
    return result

# 5. Adicionar testes
# tests/test_nova_feature.py
def test_nova_operacao(client, db_session):
    response = client.post("/api/v1/clientes/nova-operacao/", json={...})
    assert response.status_code == 200
```

#### 2. Frontend (Componente)

```jsx
// 1. Criar componente
// src/components/NovoComponente.jsx
const NovoComponente = () => {
  // Implementação
};

// 2. Adicionar ao serviço de API
// src/services/api.js
async novaOperacao(data) {
  return this.request('/clientes/nova-operacao/', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

// 3. Integrar no App
// src/App.jsx
import NovoComponente from './components/NovoComponente';

// 4. Adicionar testes
// src/components/__tests__/NovoComponente.test.jsx
test('renderiza novo componente', () => {
  render(<NovoComponente />);
  // Assertions
});
```

### Testes

#### Backend - Pytest

```python
# tests/test_clientes.py
import pytest
from fastapi.testclient import TestClient

def test_criar_cliente_sucesso(client: TestClient, cliente_data: dict):
    """Testa criação de cliente com dados válidos."""
    response = client.post("/api/v1/clientes/", json=cliente_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == cliente_data["nome"]
    assert "id" in data

def test_criar_cliente_cpf_duplicado(client: TestClient, cliente_data: dict):
    """Testa erro ao criar cliente com CPF duplicado."""
    # Criar primeiro cliente
    client.post("/api/v1/clientes/", json=cliente_data)
    
    # Tentar criar segundo com mesmo CPF
    response = client.post("/api/v1/clientes/", json=cliente_data)
    
    assert response.status_code == 400
    assert "já existe" in response.json()["detail"]

@pytest.mark.parametrize("campo,valor,erro_esperado", [
    ("nome", "", "Nome deve ter pelo menos 2 caracteres"),
    ("email", "email_invalido", "Email inválido"),
    ("cpf_cnpj", "123", "CPF/CNPJ inválido"),
])
def test_validacao_campos(client: TestClient, campo: str, valor: str, erro_esperado: str):
    """Testa validação de campos."""
    data = {"nome": "Teste", campo: valor}
    response = client.post("/api/v1/clientes/", json=data)
    
    assert response.status_code == 422
    # Verificar mensagem de erro específica
```

#### Frontend - Jest/React Testing Library

```jsx
// src/components/__tests__/ClienteForm.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ClienteForm from '../ClienteForm';

describe('ClienteForm', () => {
  test('renderiza formulário vazio', () => {
    render(<ClienteForm />);
    
    expect(screen.getByLabelText(/nome/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /salvar/i })).toBeInTheDocument();
  });

  test('submete formulário com dados válidos', async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();
    
    render(<ClienteForm onSubmit={onSubmit} />);
    
    await user.type(screen.getByLabelText(/nome/i), 'João Silva');
    await user.type(screen.getByLabelText(/email/i), 'joao@email.com');
    await user.click(screen.getByRole('button', { name: /salvar/i }));
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        nome: 'João Silva',
        email: 'joao@email.com'
      });
    });
  });

  test('exibe erro para nome vazio', async () => {
    const user = userEvent.setup();
    
    render(<ClienteForm />);
    
    await user.click(screen.getByRole('button', { name: /salvar/i }));
    
    expect(screen.getByText(/nome é obrigatório/i)).toBeInTheDocument();
  });
});
```

### Executando Testes

```bash
# Backend
cd backend
python -m pytest tests/ -v --cov=app --cov-report=html

# Frontend
cd frontend/cliente-frontend
npm test
npm run test:coverage
```

## Debugging

### Backend

```python
# Configurar logging detalhado
import logging
logging.basicConfig(level=logging.DEBUG)

# Usar debugger
import pdb; pdb.set_trace()

# Ou com IPython
import IPython; IPython.embed()

# Logs estruturados
import structlog
logger = structlog.get_logger()
logger.info("Operação realizada", cliente_id=cliente.id, operacao="create")
```

### Frontend

```javascript
// Console debugging
console.log('Estado atual:', state);
console.table(clientes);

// React DevTools
// Instalar extensão React Developer Tools

// Debugging de API
const api = {
  async request(endpoint, options) {
    console.log('API Request:', endpoint, options);
    const response = await fetch(endpoint, options);
    console.log('API Response:', response);
    return response;
  }
};
```

## Performance

### Backend

```python
# Otimização de queries
from sqlalchemy.orm import selectinload

# Eager loading
clientes = db.query(Cliente).options(
    selectinload(Cliente.enderecos)
).all()

# Paginação eficiente
def get_clientes_paginated(db: Session, skip: int, limit: int):
    return db.query(Cliente).offset(skip).limit(limit).all()

# Cache com Redis
import redis
cache = redis.Redis()

def get_cliente_cached(cliente_id: str):
    cached = cache.get(f"cliente:{cliente_id}")
    if cached:
        return json.loads(cached)
    
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    cache.setex(f"cliente:{cliente_id}", 3600, json.dumps(cliente.to_dict()))
    return cliente
```

### Frontend

```jsx
// Lazy loading de componentes
const ClienteDetails = React.lazy(() => import('./ClienteDetails'));

// Memoização
const ClienteList = React.memo(({ clientes }) => {
  return (
    <div>
      {clientes.map(cliente => (
        <ClienteItem key={cliente.id} cliente={cliente} />
      ))}
    </div>
  );
});

// Debounce para busca
import { useMemo } from 'react';
import { debounce } from 'lodash';

const SearchInput = ({ onSearch }) => {
  const debouncedSearch = useMemo(
    () => debounce(onSearch, 300),
    [onSearch]
  );

  return (
    <input
      type="text"
      onChange={(e) => debouncedSearch(e.target.value)}
      placeholder="Buscar clientes..."
    />
  );
};
```

## Ferramentas de Desenvolvimento

### VS Code Extensions

```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.pylint",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-json"
  ]
}
```

### Configuração do VS Code

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

### Scripts Úteis

```bash
# backend/scripts/dev.sh
#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$PWD
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# frontend/scripts/dev.sh
#!/bin/bash
cd cliente-frontend
npm run dev -- --host

# scripts/test-all.sh
#!/bin/bash
echo "Executando testes do backend..."
cd backend && python -m pytest tests/ -v

echo "Executando testes do frontend..."
cd ../frontend/cliente-frontend && npm test -- --watchAll=false

echo "Verificando qualidade do código..."
cd ../../backend && python -m flake8 app/
cd ../frontend/cliente-frontend && npm run lint
```

## Contribuição

### Checklist para Pull Requests

- [ ] Código segue os padrões estabelecidos
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Commits seguem padrão conventional
- [ ] CI/CD passa sem erros
- [ ] Code review aprovado

### Revisão de Código

#### O que verificar:

1. **Funcionalidade**: O código faz o que deveria fazer?
2. **Legibilidade**: O código é fácil de entender?
3. **Performance**: Há gargalos ou ineficiências?
4. **Segurança**: Há vulnerabilidades potenciais?
5. **Testes**: A cobertura é adequada?
6. **Documentação**: Está atualizada e clara?

## Recursos Adicionais

### Documentação de Referência

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Library](https://testing-library.com/)

### Ferramentas Recomendadas

- **API Testing**: Postman, Insomnia
- **Database**: pgAdmin, DBeaver
- **Monitoring**: Sentry, DataDog
- **Documentation**: Swagger, Redoc

---

**Versão**: 1.0.0  
**Última Atualização**: 2024-01-21

