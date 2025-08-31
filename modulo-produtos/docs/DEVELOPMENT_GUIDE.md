# Guia de Desenvolvimento - Módulo de Produtos

Este guia fornece instruções detalhadas para desenvolvedores que desejam contribuir, modificar ou estender o Módulo de Produtos do Sistema de Gestão de Lojas.

## 📋 Visão Geral

O Módulo de Produtos é construído com uma arquitetura moderna e escalável:

- **Backend**: FastAPI com SQLAlchemy e PostgreSQL
- **Frontend**: React com Vite e TailwindCSS
- **Banco de Dados**: PostgreSQL com Redis para cache
- **Testes**: Pytest para backend, Jest para frontend
- **Documentação**: Swagger/OpenAPI automática

## 🛠️ Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

```bash
# Verificar versões
python3.11 --version  # >= 3.11
node --version         # >= 20.0
npm --version          # >= 9.0
docker --version       # >= 20.10
git --version          # >= 2.30
```

### Clonagem e Configuração Inicial

```bash
# 1. Clonar repositório
git clone <url-do-repositorio>
cd modulo-produtos

# 2. Configurar Git hooks (opcional)
cp scripts/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# 3. Criar estrutura de desenvolvimento
mkdir -p logs uploads temp
```

### Configuração do Backend

```bash
cd backend

# 1. Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Atualizar pip e instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dependências de desenvolvimento

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações locais

# 4. Configurar pre-commit hooks
pre-commit install

# 5. Verificar instalação
python -c "import fastapi, sqlalchemy, alembic; print('Backend OK')"
```

#### requirements-dev.txt

```txt
# Ferramentas de desenvolvimento
black==23.7.0
isort==5.12.0
flake8==6.0.0
mypy==1.5.1
pre-commit==3.3.3

# Testes
pytest==7.4.0
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.24.1
factory-boy==3.3.0

# Debugging
ipdb==0.13.13
rich==13.5.2

# Documentação
mkdocs==1.5.2
mkdocs-material==9.1.21
```

### Configuração do Frontend

```bash
cd frontend/produto-frontend

# 1. Instalar dependências
npm install

# 2. Instalar dependências de desenvolvimento
npm install --save-dev \
  @types/react \
  @types/react-dom \
  @typescript-eslint/eslint-plugin \
  @typescript-eslint/parser \
  eslint \
  eslint-plugin-react \
  eslint-plugin-react-hooks \
  prettier \
  @testing-library/react \
  @testing-library/jest-dom \
  @testing-library/user-event \
  jsdom \
  vitest

# 3. Configurar variáveis de ambiente
cp .env.example .env.local
# Editar .env.local com configurações locais

# 4. Verificar instalação
npm run build
npm run test
```

### Configuração do Banco de Dados

```bash
# 1. Iniciar PostgreSQL via Docker
docker run --name postgres-dev \
  -e POSTGRES_DB=gestao_lojas_produtos \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -p 5433:5432 \
  -d postgres:15-alpine

# 2. Iniciar Redis via Docker
docker run --name redis-dev \
  -p 6380:6379 \
  -d redis:7-alpine

# 3. Executar migrações
cd backend
alembic upgrade head

# 4. Inserir dados de exemplo
python scripts/init_db.py
```

## 🏗️ Arquitetura do Código

### Estrutura do Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação FastAPI principal
│   ├── database.py          # Configuração do banco
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Schemas Pydantic
│   ├── crud.py              # Operações CRUD
│   ├── dependencies.py      # Dependências FastAPI
│   ├── exceptions.py        # Exceções customizadas
│   ├── middleware.py        # Middlewares
│   ├── utils.py             # Utilitários
│   └── routers/
│       ├── __init__.py
│       ├── produtos.py      # Endpoints de produtos
│       ├── categorias.py    # Endpoints de categorias
│       └── marcas.py        # Endpoints de marcas
├── alembic/                 # Migrações do banco
├── scripts/                 # Scripts utilitários
├── tests/                   # Testes automatizados
├── requirements.txt         # Dependências de produção
├── requirements-dev.txt     # Dependências de desenvolvimento
└── .env.example            # Exemplo de configuração
```

### Estrutura do Frontend

```
frontend/produto-frontend/
├── public/                  # Arquivos estáticos
├── src/
│   ├── components/          # Componentes React
│   │   ├── common/         # Componentes reutilizáveis
│   │   ├── forms/          # Componentes de formulário
│   │   └── layout/         # Componentes de layout
│   ├── hooks/              # Custom hooks
│   ├── services/           # Serviços de API
│   ├── utils/              # Utilitários
│   ├── types/              # Definições TypeScript
│   ├── styles/             # Estilos CSS/SCSS
│   ├── App.tsx             # Componente principal
│   └── main.tsx            # Ponto de entrada
├── tests/                  # Testes do frontend
├── package.json            # Dependências Node.js
└── vite.config.ts          # Configuração do Vite
```

## 🔧 Padrões de Desenvolvimento

### Backend - FastAPI

#### Modelos SQLAlchemy

```python
# app/models.py
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

Base = declarative_base()

class StatusProduto(enum.Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    ESGOTADO = "esgotado"
    PROMOCAO = "promocao"

class Produto(Base):
    __tablename__ = "produtos"
    __table_args__ = {"schema": "produtos"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False, index=True)
    preco_venda = Column(Integer, nullable=False, default=0)
    status = Column(Enum(StatusProduto), nullable=False, default=StatusProduto.ATIVO)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    categoria = relationship("Categoria", back_populates="produtos")
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            "id": str(self.id),
            "nome": self.nome,
            "preco_venda": self.preco_venda,
            "status": self.status.value,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "categoria_nome": self.categoria.nome if self.categoria else None
        }
```

#### Schemas Pydantic

```python
# app/schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from .models import StatusProduto, UnidadeMedida

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255, description="Nome do produto")
    descricao: Optional[str] = Field(None, max_length=2000, description="Descrição detalhada")
    preco_venda: int = Field(..., ge=0, description="Preço de venda em centavos")
    preco_custo: int = Field(..., ge=0, description="Preço de custo em centavos")
    
    @validator('preco_venda', 'preco_custo')
    def validate_prices(cls, v):
        if v < 0:
            raise ValueError('Preços devem ser não negativos')
        return v

class ProdutoCreate(ProdutoBase):
    sku: Optional[str] = Field(None, max_length=255, description="SKU único")
    categoria_id: Optional[UUID] = None
    marca_id: Optional[UUID] = None
    status: StatusProduto = StatusProduto.ATIVO
    criado_por: str = Field(..., max_length=100)

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=255)
    preco_venda: Optional[int] = Field(None, ge=0)
    status: Optional[StatusProduto] = None
    atualizado_por: Optional[str] = Field(None, max_length=100)

class ProdutoResponse(ProdutoBase):
    id: UUID
    sku: Optional[str]
    categoria_nome: Optional[str]
    marca_nome: Optional[str]
    status: StatusProduto
    data_criacao: datetime
    data_atualizacao: Optional[datetime]
    
    class Config:
        from_attributes = True
```

#### Operações CRUD

```python
# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from .models import Produto, Categoria
from .schemas import ProdutoCreate, ProdutoUpdate

class ProdutoCRUD:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, produto_data: ProdutoCreate) -> Produto:
        """Cria um novo produto."""
        # Verificar duplicatas
        if produto_data.sku:
            existing = self.get_by_sku(produto_data.sku)
            if existing:
                raise ValueError(f"SKU '{produto_data.sku}' já existe")
        
        produto = Produto(**produto_data.dict())
        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto
    
    def get_by_id(self, produto_id: str) -> Optional[Produto]:
        """Busca produto por ID."""
        return self.db.query(Produto).filter(Produto.id == produto_id).first()
    
    def get_by_sku(self, sku: str) -> Optional[Produto]:
        """Busca produto por SKU."""
        return self.db.query(Produto).filter(Produto.sku == sku).first()
    
    def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 10,
        filters: dict = None
    ) -> tuple[List[Produto], int]:
        """Lista produtos com paginação e filtros."""
        query = self.db.query(Produto)
        
        # Aplicar filtros
        if filters:
            if filters.get('nome'):
                query = query.filter(Produto.nome.ilike(f"%{filters['nome']}%"))
            if filters.get('status'):
                query = query.filter(Produto.status == filters['status'])
            if filters.get('categoria_id'):
                query = query.filter(Produto.categoria_id == filters['categoria_id'])
        
        total = query.count()
        produtos = query.offset(skip).limit(limit).all()
        
        return produtos, total
    
    def update(self, produto_id: str, produto_data: ProdutoUpdate) -> Optional[Produto]:
        """Atualiza um produto."""
        produto = self.get_by_id(produto_id)
        if not produto:
            return None
        
        update_data = produto_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(produto, field, value)
        
        self.db.commit()
        self.db.refresh(produto)
        return produto
    
    def delete(self, produto_id: str) -> bool:
        """Remove um produto permanentemente."""
        produto = self.get_by_id(produto_id)
        if not produto:
            return False
        
        self.db.delete(produto)
        self.db.commit()
        return True
    
    def search(self, termo: str, limit: int = 10) -> List[Produto]:
        """Busca produtos por termo textual."""
        return self.db.query(Produto).filter(
            or_(
                Produto.nome.ilike(f"%{termo}%"),
                Produto.descricao.ilike(f"%{termo}%"),
                Produto.sku.ilike(f"%{termo}%")
            )
        ).limit(limit).all()
```

#### Endpoints da API

```python
# app/routers/produtos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..crud import ProdutoCRUD
from ..schemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.post("/", response_model=ProdutoResponse, status_code=201)
async def create_produto(
    produto_data: ProdutoCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo produto."""
    try:
        crud = ProdutoCRUD(db)
        produto = crud.create(produto_data)
        return produto
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/", response_model=dict)
async def list_produtos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    nome: Optional[str] = Query(None, description="Filtro por nome"),
    status: Optional[str] = Query(None, description="Filtro por status"),
    db: Session = Depends(get_db)
):
    """Lista produtos com paginação e filtros."""
    crud = ProdutoCRUD(db)
    filters = {k: v for k, v in {"nome": nome, "status": status}.items() if v}
    
    produtos, total = crud.get_multi(skip=skip, limit=limit, filters=filters)
    
    return {
        "produtos": [produto.to_dict() for produto in produtos],
        "total": total,
        "pagina": (skip // limit) + 1,
        "limite": limit,
        "total_paginas": (total + limit - 1) // limit
    }

@router.get("/{produto_id}", response_model=ProdutoResponse)
async def get_produto(
    produto_id: str,
    db: Session = Depends(get_db)
):
    """Busca produto por ID."""
    crud = ProdutoCRUD(db)
    produto = crud.get_by_id(produto_id)
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto

@router.put("/{produto_id}", response_model=ProdutoResponse)
async def update_produto(
    produto_id: str,
    produto_data: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um produto."""
    crud = ProdutoCRUD(db)
    produto = crud.update(produto_id, produto_data)
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto

@router.delete("/{produto_id}")
async def delete_produto(
    produto_id: str,
    db: Session = Depends(get_db)
):
    """Remove um produto."""
    crud = ProdutoCRUD(db)
    success = crud.delete(produto_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return {"message": "Produto removido com sucesso"}
```

### Frontend - React

#### Componentes Funcionais

```tsx
// src/components/ProdutoCard.tsx
import React from 'react';
import { Produto } from '../types/produto';
import { formatCurrency } from '../utils/formatters';

interface ProdutoCardProps {
  produto: Produto;
  onEdit: (produto: Produto) => void;
  onDelete: (id: string) => void;
  onView: (produto: Produto) => void;
}

export const ProdutoCard: React.FC<ProdutoCardProps> = ({
  produto,
  onEdit,
  onDelete,
  onView
}) => {
  const handleDelete = () => {
    if (window.confirm(`Tem certeza que deseja remover "${produto.nome}"?`)) {
      onDelete(produto.id);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-semibold text-gray-900 truncate">
          {produto.nome}
        </h3>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          produto.status === 'ativo' ? 'bg-green-100 text-green-800' :
          produto.status === 'promocao' ? 'bg-yellow-100 text-yellow-800' :
          'bg-red-100 text-red-800'
        }`}>
          {produto.status}
        </span>
      </div>
      
      <div className="space-y-2 mb-4">
        <p className="text-sm text-gray-600">
          <span className="font-medium">SKU:</span> {produto.sku || 'N/A'}
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-medium">Preço:</span> {formatCurrency(produto.preco_venda)}
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-medium">Categoria:</span> {produto.categoria_nome || 'N/A'}
        </p>
      </div>
      
      <div className="flex space-x-2">
        <button
          onClick={() => onView(produto)}
          className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
        >
          Ver
        </button>
        <button
          onClick={() => onEdit(produto)}
          className="flex-1 bg-gray-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700 transition-colors"
        >
          Editar
        </button>
        <button
          onClick={handleDelete}
          className="flex-1 bg-red-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-red-700 transition-colors"
        >
          Remover
        </button>
      </div>
    </div>
  );
};
```

#### Custom Hooks

```tsx
// src/hooks/useProdutos.ts
import { useState, useEffect, useCallback } from 'react';
import { getProdutos, createProduto, updateProduto, deleteProduto } from '../services/api';
import { Produto, ProdutoCreate, ProdutoUpdate } from '../types/produto';

interface UseProdutosReturn {
  produtos: Produto[];
  loading: boolean;
  error: string | null;
  total: number;
  page: number;
  totalPages: number;
  fetchProdutos: (params?: any) => Promise<void>;
  createProdutoHandler: (data: ProdutoCreate) => Promise<Produto>;
  updateProdutoHandler: (id: string, data: ProdutoUpdate) => Promise<Produto>;
  deleteProdutoHandler: (id: string) => Promise<void>;
  setPage: (page: number) => void;
}

export const useProdutos = (initialParams = {}): UseProdutosReturn => {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  const fetchProdutos = useCallback(async (params = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await getProdutos({
        skip: (page - 1) * 10,
        limit: 10,
        ...initialParams,
        ...params
      });
      
      setProdutos(response.produtos);
      setTotal(response.total);
      setTotalPages(response.total_paginas);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar produtos');
    } finally {
      setLoading(false);
    }
  }, [page, initialParams]);

  const createProdutoHandler = async (data: ProdutoCreate): Promise<Produto> => {
    try {
      const produto = await createProduto(data);
      await fetchProdutos();
      return produto;
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : 'Erro ao criar produto');
    }
  };

  const updateProdutoHandler = async (id: string, data: ProdutoUpdate): Promise<Produto> => {
    try {
      const produto = await updateProduto(id, data);
      await fetchProdutos();
      return produto;
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : 'Erro ao atualizar produto');
    }
  };

  const deleteProdutoHandler = async (id: string): Promise<void> => {
    try {
      await deleteProduto(id);
      await fetchProdutos();
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : 'Erro ao remover produto');
    }
  };

  useEffect(() => {
    fetchProdutos();
  }, [fetchProdutos]);

  return {
    produtos,
    loading,
    error,
    total,
    page,
    totalPages,
    fetchProdutos,
    createProdutoHandler,
    updateProdutoHandler,
    deleteProdutoHandler,
    setPage
  };
};
```

#### Tipos TypeScript

```typescript
// src/types/produto.ts
export interface Produto {
  id: string;
  nome: string;
  descricao?: string;
  codigo_barras?: string;
  sku?: string;
  preco_venda: number;
  preco_custo: number;
  unidade_medida: UnidadeMedida;
  categoria_id?: string;
  categoria_nome?: string;
  marca_id?: string;
  marca_nome?: string;
  status: StatusProduto;
  imagem_url?: string;
  observacoes?: string;
  data_criacao: string;
  data_atualizacao?: string;
  criado_por?: string;
  atualizado_por?: string;
}

export interface ProdutoCreate {
  nome: string;
  descricao?: string;
  codigo_barras?: string;
  sku?: string;
  preco_venda: number;
  preco_custo: number;
  unidade_medida: UnidadeMedida;
  categoria_id?: string;
  marca_id?: string;
  status: StatusProduto;
  imagem_url?: string;
  observacoes?: string;
  criado_por: string;
}

export interface ProdutoUpdate {
  nome?: string;
  descricao?: string;
  preco_venda?: number;
  preco_custo?: number;
  status?: StatusProduto;
  imagem_url?: string;
  observacoes?: string;
  atualizado_por?: string;
}

export enum UnidadeMedida {
  UNIDADE = 'unidade',
  KG = 'kg',
  G = 'g',
  M = 'm',
  CM = 'cm',
  MM = 'mm',
  L = 'l',
  ML = 'ml',
  CAIXA = 'caixa',
  PACOTE = 'pacote'
}

export enum StatusProduto {
  ATIVO = 'ativo',
  INATIVO = 'inativo',
  ESGOTADO = 'esgotado',
  PROMOCAO = 'promocao'
}

export interface ProdutosResponse {
  produtos: Produto[];
  total: number;
  pagina: number;
  limite: number;
  total_paginas: number;
}
```

## 🧪 Testes

### Testes do Backend

#### Configuração de Testes

```python
# tests/conftest.py
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

os.environ["TESTING"] = "true"

from app.main import app
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_produto():
    return {
        "nome": "Produto Teste",
        "preco_venda": 10000,
        "preco_custo": 6000,
        "sku": "TEST-001",
        "criado_por": "teste"
    }
```

#### Testes de Unidade

```python
# tests/test_crud.py
import pytest
from app.crud import ProdutoCRUD
from app.schemas import ProdutoCreate, ProdutoUpdate
from app.models import StatusProduto

def test_create_produto(db_session):
    crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Produto Teste",
        preco_venda=10000,
        preco_custo=6000,
        criado_por="teste"
    )
    
    produto = crud.create(produto_data)
    
    assert produto.id is not None
    assert produto.nome == "Produto Teste"
    assert produto.preco_venda == 10000

def test_get_produto_by_id(db_session):
    crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Produto Teste",
        preco_venda=10000,
        preco_custo=6000,
        criado_por="teste"
    )
    produto = crud.create(produto_data)
    
    found_produto = crud.get_by_id(str(produto.id))
    
    assert found_produto is not None
    assert found_produto.id == produto.id

def test_update_produto(db_session):
    crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Produto Original",
        preco_venda=10000,
        preco_custo=6000,
        criado_por="teste"
    )
    produto = crud.create(produto_data)
    
    update_data = ProdutoUpdate(
        nome="Produto Atualizado",
        preco_venda=12000
    )
    updated_produto = crud.update(str(produto.id), update_data)
    
    assert updated_produto.nome == "Produto Atualizado"
    assert updated_produto.preco_venda == 12000

def test_delete_produto(db_session):
    crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Produto para Deletar",
        preco_venda=10000,
        preco_custo=6000,
        criado_por="teste"
    )
    produto = crud.create(produto_data)
    produto_id = str(produto.id)
    
    success = crud.delete(produto_id)
    
    assert success is True
    assert crud.get_by_id(produto_id) is None
```

#### Testes de Integração

```python
# tests/test_api.py
def test_create_produto_api(client, sample_produto):
    response = client.post("/api/v1/produtos/", json=sample_produto)
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == sample_produto["nome"]
    assert "id" in data

def test_list_produtos_api(client, sample_produto):
    # Criar produto primeiro
    client.post("/api/v1/produtos/", json=sample_produto)
    
    response = client.get("/api/v1/produtos/")
    
    assert response.status_code == 200
    data = response.json()
    assert "produtos" in data
    assert len(data["produtos"]) >= 1

def test_get_produto_by_id_api(client, sample_produto):
    create_response = client.post("/api/v1/produtos/", json=sample_produto)
    produto_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/produtos/{produto_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produto_id

def test_update_produto_api(client, sample_produto):
    create_response = client.post("/api/v1/produtos/", json=sample_produto)
    produto_id = create_response.json()["id"]
    
    update_data = {"nome": "Produto Atualizado"}
    response = client.put(f"/api/v1/produtos/{produto_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Produto Atualizado"

def test_delete_produto_api(client, sample_produto):
    create_response = client.post("/api/v1/produtos/", json=sample_produto)
    produto_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/produtos/{produto_id}")
    
    assert response.status_code == 200
    
    # Verificar se foi removido
    get_response = client.get(f"/api/v1/produtos/{produto_id}")
    assert get_response.status_code == 404
```

### Testes do Frontend

#### Configuração do Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock do fetch
global.fetch = vi.fn();

// Mock do localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
global.localStorage = localStorageMock;
```

#### Testes de Componentes

```typescript
// src/components/__tests__/ProdutoCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import { ProdutoCard } from '../ProdutoCard';
import { Produto, StatusProduto, UnidadeMedida } from '../../types/produto';

const mockProduto: Produto = {
  id: '1',
  nome: 'Produto Teste',
  preco_venda: 10000,
  preco_custo: 6000,
  unidade_medida: UnidadeMedida.UNIDADE,
  status: StatusProduto.ATIVO,
  data_criacao: '2024-01-01T00:00:00Z',
  sku: 'TEST-001'
};

describe('ProdutoCard', () => {
  const mockOnEdit = vi.fn();
  const mockOnDelete = vi.fn();
  const mockOnView = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders produto information correctly', () => {
    render(
      <ProdutoCard
        produto={mockProduto}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onView={mockOnView}
      />
    );

    expect(screen.getByText('Produto Teste')).toBeInTheDocument();
    expect(screen.getByText('TEST-001')).toBeInTheDocument();
    expect(screen.getByText('R$ 100,00')).toBeInTheDocument();
    expect(screen.getByText('ativo')).toBeInTheDocument();
  });

  it('calls onView when view button is clicked', () => {
    render(
      <ProdutoCard
        produto={mockProduto}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onView={mockOnView}
      />
    );

    fireEvent.click(screen.getByText('Ver'));
    expect(mockOnView).toHaveBeenCalledWith(mockProduto);
  });

  it('calls onEdit when edit button is clicked', () => {
    render(
      <ProdutoCard
        produto={mockProduto}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onView={mockOnView}
      />
    );

    fireEvent.click(screen.getByText('Editar'));
    expect(mockOnEdit).toHaveBeenCalledWith(mockProduto);
  });

  it('shows confirmation dialog when delete button is clicked', () => {
    const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(true);
    
    render(
      <ProdutoCard
        produto={mockProduto}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        onView={mockOnView}
      />
    );

    fireEvent.click(screen.getByText('Remover'));
    
    expect(confirmSpy).toHaveBeenCalledWith('Tem certeza que deseja remover "Produto Teste"?');
    expect(mockOnDelete).toHaveBeenCalledWith('1');
  });
});
```

#### Testes de Hooks

```typescript
// src/hooks/__tests__/useProdutos.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { useProdutos } from '../useProdutos';
import * as api from '../../services/api';

vi.mock('../../services/api');

describe('useProdutos', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('fetches produtos on mount', async () => {
    const mockResponse = {
      produtos: [{ id: '1', nome: 'Produto 1' }],
      total: 1,
      total_paginas: 1
    };
    
    vi.mocked(api.getProdutos).mockResolvedValue(mockResponse);

    const { result } = renderHook(() => useProdutos());

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.produtos).toEqual(mockResponse.produtos);
    expect(result.current.total).toBe(1);
  });

  it('handles error when fetching produtos fails', async () => {
    vi.mocked(api.getProdutos).mockRejectedValue(new Error('API Error'));

    const { result } = renderHook(() => useProdutos());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBe('API Error');
    expect(result.current.produtos).toEqual([]);
  });
});
```

## 🔧 Ferramentas de Desenvolvimento

### Linting e Formatação

#### Backend - Python

```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

```ini
# setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,venv,alembic

[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

#### Frontend - TypeScript/React

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint", "react", "react-hooks"],
  "rules": {
    "react/react-in-jsx-scope": "off",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn"
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
```

```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

### Scripts de Desenvolvimento

```json
// package.json scripts
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint src --ext ts,tsx --fix",
    "format": "prettier --write src/**/*.{ts,tsx,css,md}",
    "type-check": "tsc --noEmit"
  }
}
```

### Makefile para Automação

```makefile
# Makefile
.PHONY: help install dev test lint format clean

help:
	@echo "Comandos disponíveis:"
	@echo "  install     - Instalar dependências"
	@echo "  dev         - Iniciar ambiente de desenvolvimento"
	@echo "  test        - Executar testes"
	@echo "  lint        - Verificar código"
	@echo "  format      - Formatar código"
	@echo "  clean       - Limpar arquivos temporários"

install:
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	cd frontend/produto-frontend && npm install

dev:
	docker-compose up -d db-produtos redis-produtos
	cd backend && uvicorn app.main:app --reload --port 8001 &
	cd frontend/produto-frontend && npm run dev

test:
	cd backend && python -m pytest tests/ -v --cov=app
	cd frontend/produto-frontend && npm run test

lint:
	cd backend && flake8 app tests
	cd backend && mypy app
	cd frontend/produto-frontend && npm run lint

format:
	cd backend && black app tests
	cd backend && isort app tests
	cd frontend/produto-frontend && npm run format

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	cd frontend/produto-frontend && rm -rf node_modules/.cache
```

## 📚 Documentação

### Gerando Documentação

```bash
# Backend - Swagger/OpenAPI automático
# Disponível em: http://localhost:8001/docs

# Frontend - Storybook (opcional)
cd frontend/produto-frontend
npx storybook init
npm run storybook

# Documentação com MkDocs
pip install mkdocs mkdocs-material
mkdocs serve
```

### Estrutura da Documentação

```
docs/
├── index.md                 # Página inicial
├── api/
│   ├── endpoints.md         # Documentação dos endpoints
│   ├── schemas.md           # Schemas de dados
│   └── examples.md          # Exemplos de uso
├── frontend/
│   ├── components.md        # Documentação dos componentes
│   ├── hooks.md             # Custom hooks
│   └── utils.md             # Utilitários
├── deployment/
│   ├── docker.md            # Deploy com Docker
│   ├── kubernetes.md        # Deploy com Kubernetes
│   └── production.md        # Configurações de produção
└── contributing/
    ├── setup.md             # Configuração do ambiente
    ├── guidelines.md        # Diretrizes de contribuição
    └── testing.md           # Guia de testes
```

## 🚀 Workflow de Desenvolvimento

### Git Flow

```bash
# 1. Criar branch para nova funcionalidade
git checkout -b feature/nova-funcionalidade

# 2. Fazer commits pequenos e descritivos
git add .
git commit -m "feat: adicionar validação de SKU único"

# 3. Executar testes antes do push
make test

# 4. Push da branch
git push origin feature/nova-funcionalidade

# 5. Criar Pull Request
# 6. Code review
# 7. Merge para main
```

### Conventional Commits

```
feat: nova funcionalidade
fix: correção de bug
docs: atualização de documentação
style: formatação de código
refactor: refatoração sem mudança de funcionalidade
test: adição ou correção de testes
chore: tarefas de manutenção
```

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt -r requirements-dev.txt
      - name: Run tests
        run: |
          cd backend
          python -m pytest tests/ -v --cov=app

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend/produto-frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend/produto-frontend
          npm run test

  build:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker images
        run: |
          docker build -t produtos-backend ./backend
          docker build -t produtos-frontend ./frontend/produto-frontend
```

Este guia fornece uma base sólida para desenvolver e contribuir com o Módulo de Produtos. Siga as práticas recomendadas e mantenha a qualidade do código através de testes e revisões regulares.

