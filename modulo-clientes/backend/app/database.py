"""
Configuração do banco de dados PostgreSQL para o módulo de clientes.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# URL de conexão com o banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:admin123@localhost:5432/gestao_lojas"
)

# Criação do engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False  # Mude para True para debug SQL
)

# Criação da sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db():
    """
    Dependency para obter uma sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Cria todas as tabelas no banco de dados.
    """
    Base.metadata.create_all(bind=engine)

