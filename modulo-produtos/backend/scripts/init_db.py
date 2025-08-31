#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do módulo de produtos.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.database import SQLALCHEMY_DATABASE_URL, Base
from app.models import Categoria, Marca, Produto
from dotenv import load_dotenv

load_dotenv()

def create_database_if_not_exists():
    """Cria o banco de dados se ele não existir."""
    try:
        # Conectar ao PostgreSQL sem especificar o banco
        base_url = SQLALCHEMY_DATABASE_URL.rsplit('/', 1)[0]
        db_name = SQLALCHEMY_DATABASE_URL.rsplit('/', 1)[1]
        
        engine = create_engine(f"{base_url}/postgres")
        
        with engine.connect() as conn:
            # Verificar se o banco existe
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            if not result.fetchone():
                # Criar o banco se não existir
                conn.execute(text("COMMIT"))
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Banco de dados '{db_name}' criado com sucesso!")
            else:
                print(f"Banco de dados '{db_name}' já existe.")
                
    except OperationalError as e:
        print(f"Erro ao conectar com PostgreSQL: {e}")
        print("Certifique-se de que o PostgreSQL está rodando e as credenciais estão corretas.")
        return False
    
    return True

def create_tables():
    """Cria as tabelas no banco de dados."""
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        
        # Criar schema produtos se não existir
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS produtos"))
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
            conn.commit()
        
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        return False

def insert_sample_data():
    """Insere dados de exemplo no banco."""
    try:
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        db = SessionLocal()
        
        # Verificar se já existem dados
        if db.query(Categoria).count() > 0:
            print("Dados de exemplo já existem no banco.")
            db.close()
            return True
        
        # Inserir categorias de exemplo
        categorias = [
            Categoria(nome="Eletrônicos", descricao="Produtos eletrônicos em geral"),
            Categoria(nome="Roupas", descricao="Vestuário e acessórios"),
            Categoria(nome="Alimentos", descricao="Produtos alimentícios"),
            Categoria(nome="Livros", descricao="Livros e materiais de leitura"),
            Categoria(nome="Casa e Jardim", descricao="Produtos para casa e jardim"),
        ]
        
        for categoria in categorias:
            db.add(categoria)
        
        # Inserir marcas de exemplo
        marcas = [
            Marca(nome="Samsung", descricao="Marca sul-coreana de eletrônicos"),
            Marca(nome="Apple", descricao="Marca americana de tecnologia"),
            Marca(nome="Nike", descricao="Marca americana de artigos esportivos"),
            Marca(nome="Nestlé", descricao="Marca suíça de alimentos"),
            Marca(nome="Editora Globo", descricao="Editora brasileira"),
        ]
        
        for marca in marcas:
            db.add(marca)
        
        db.commit()
        
        # Buscar IDs das categorias e marcas inseridas
        categoria_eletronicos = db.query(Categoria).filter_by(nome="Eletrônicos").first()
        categoria_roupas = db.query(Categoria).filter_by(nome="Roupas").first()
        categoria_alimentos = db.query(Categoria).filter_by(nome="Alimentos").first()
        
        marca_samsung = db.query(Marca).filter_by(nome="Samsung").first()
        marca_nike = db.query(Marca).filter_by(nome="Nike").first()
        marca_nestle = db.query(Marca).filter_by(nome="Nestlé").first()
        
        # Inserir produtos de exemplo
        produtos = [
            Produto(
                nome="Smartphone Galaxy S23",
                descricao="Celular de última geração com câmera de alta resolução",
                codigo_barras="7891234567890",
                sku="SMART-S23",
                preco_venda=500000,  # R$ 5000,00 em centavos
                preco_custo=350000,  # R$ 3500,00 em centavos
                categoria_id=categoria_eletronicos.id if categoria_eletronicos else None,
                marca_id=marca_samsung.id if marca_samsung else None,
                criado_por="sistema"
            ),
            Produto(
                nome="Camiseta Esportiva Dry-Fit",
                descricao="Camiseta leve e respirável para atividades físicas",
                codigo_barras="7890987654321",
                sku="CAMI-DRYFIT-M",
                preco_venda=12000,  # R$ 120,00 em centavos
                preco_custo=6000,   # R$ 60,00 em centavos
                categoria_id=categoria_roupas.id if categoria_roupas else None,
                marca_id=marca_nike.id if marca_nike else None,
                criado_por="sistema"
            ),
            Produto(
                nome="Chocolate ao Leite 100g",
                descricao="Delicioso chocolate ao leite, ideal para sobremesas",
                codigo_barras="7894561237890",
                sku="CHOC-LEITE-100G",
                preco_venda=800,    # R$ 8,00 em centavos
                preco_custo=400,    # R$ 4,00 em centavos
                categoria_id=categoria_alimentos.id if categoria_alimentos else None,
                marca_id=marca_nestle.id if marca_nestle else None,
                criado_por="sistema"
            ),
        ]
        
        for produto in produtos:
            db.add(produto)
        
        db.commit()
        db.close()
        
        print("Dados de exemplo inseridos com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao inserir dados de exemplo: {e}")
        return False

def main():
    """Função principal do script."""
    print("=== Inicialização do Banco de Dados - Módulo de Produtos ===")
    
    # Passo 1: Criar banco de dados se não existir
    print("\n1. Verificando/criando banco de dados...")
    if not create_database_if_not_exists():
        print("Falha ao criar/verificar banco de dados. Abortando.")
        return False
    
    # Passo 2: Criar tabelas
    print("\n2. Criando tabelas...")
    if not create_tables():
        print("Falha ao criar tabelas. Abortando.")
        return False
    
    # Passo 3: Inserir dados de exemplo
    print("\n3. Inserindo dados de exemplo...")
    if not insert_sample_data():
        print("Falha ao inserir dados de exemplo.")
        return False
    
    print("\n=== Inicialização concluída com sucesso! ===")
    print("\nVocê pode agora:")
    print("- Iniciar o servidor FastAPI: uvicorn app.main:app --reload")
    print("- Acessar a documentação da API: http://localhost:8000/docs")
    print("- Executar migrações: alembic upgrade head")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

