"""
Configurações para os testes do módulo de clientes.
"""

import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db, Base
from app.models import Cliente

# URL do banco de dados de teste (SQLite em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Engine de teste
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Session de teste
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override da função get_db para usar o banco de teste."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override da dependência
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para toda a sessão de testes."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados para cada teste."""
    # Cria as tabelas
    Base.metadata.create_all(bind=engine)
    
    # Cria a sessão
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Remove as tabelas após o teste
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    """Cria um cliente de teste para a API."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def cliente_data():
    """Dados de exemplo para criar um cliente."""
    return {
        "nome": "João Silva",
        "tipo_cliente": "pessoa_fisica",
        "cpf_cnpj": "12345678901",
        "email": "joao.silva@email.com",
        "telefone": "11987654321",
        "endereco": "Rua das Flores, 123",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01234567",
        "status": "ativo"
    }

@pytest.fixture
def cliente_juridica_data():
    """Dados de exemplo para criar um cliente pessoa jurídica."""
    return {
        "nome": "Empresa ABC Ltda",
        "tipo_cliente": "pessoa_juridica",
        "cpf_cnpj": "12345678000123",
        "email": "contato@empresaabc.com",
        "telefone": "1133334444",
        "endereco": "Av. Paulista, 1000",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01310100",
        "status": "ativo",
        "limite_credito": 500000
    }

