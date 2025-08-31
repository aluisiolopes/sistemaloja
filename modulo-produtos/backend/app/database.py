from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

load_dotenv()

# URL do banco de dados obtida das variáveis de ambiente
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/gestao_lojas_produtos")

# Configuração do engine
# Para testes, usamos NullPool para evitar problemas de conexão com o banco de dados de teste
if os.getenv("TESTING") == "true":
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, poolclass=NullPool, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos
Base = declarative_base()

def get_db():
    """Dependência para obter a sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Cria todas as tabelas definidas na Base."""
    Base.metadata.create_all(bind=engine)


