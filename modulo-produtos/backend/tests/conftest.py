import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Configurar variável de ambiente para testes
os.environ["TESTING"] = "true"

from app.main import app
from app.database import get_db, Base

# URL do banco de dados de teste (usar SQLite em memória para testes)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados para testes."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste FastAPI."""
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
def sample_categoria_data():
    """Dados de exemplo para categoria."""
    return {
        "nome": "Eletrônicos",
        "descricao": "Produtos eletrônicos em geral"
    }

@pytest.fixture
def sample_marca_data():
    """Dados de exemplo para marca."""
    return {
        "nome": "Samsung",
        "descricao": "Marca sul-coreana de eletrônicos"
    }

@pytest.fixture
def sample_produto_data():
    """Dados de exemplo para produto."""
    return {
        "nome": "Smartphone Galaxy S23",
        "descricao": "Celular de última geração",
        "codigo_barras": "7891234567890",
        "sku": "SMART-S23",
        "preco_venda": 500000,
        "preco_custo": 350000,
        "unidade_medida": "unidade",
        "status": "ativo",
        "criado_por": "teste"
    }

