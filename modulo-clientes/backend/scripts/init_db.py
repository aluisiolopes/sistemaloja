#!/usr/bin/env python3
"""
Script para inicialização do banco de dados do módulo de clientes.
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine, Base, create_tables
from app.models import Cliente
from sqlalchemy import text

def create_database_schema():
    """Cria o schema do banco de dados se não existir."""
    print("🔧 Criando schema do banco de dados...")
    
    with engine.connect() as conn:
        # Criar extensão UUID
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        
        # Criar schema clientes
        conn.execute(text('CREATE SCHEMA IF NOT EXISTS clientes'))
        
        conn.commit()
    
    print("✅ Schema criado com sucesso!")

def create_tables_if_not_exist():
    """Cria as tabelas se não existirem."""
    print("🔧 Criando tabelas...")
    
    try:
        create_tables()
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        raise

def insert_sample_data():
    """Insere dados de exemplo (opcional)."""
    from sqlalchemy.orm import sessionmaker
    from app.models import TipoCliente, StatusCliente
    
    print("🔧 Inserindo dados de exemplo...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Verifica se já existem clientes
        existing_count = session.query(Cliente).count()
        if existing_count > 0:
            print(f"ℹ️  Já existem {existing_count} clientes no banco. Pulando inserção de dados de exemplo.")
            return
        
        # Dados de exemplo
        clientes_exemplo = [
            {
                "nome": "João Silva",
                "tipo_cliente": TipoCliente.PESSOA_FISICA,
                "cpf_cnpj": "12345678901",
                "email": "joao.silva@email.com",
                "telefone": "11987654321",
                "endereco": "Rua das Flores, 123",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01234567",
                "status": StatusCliente.ATIVO,
                "criado_por": "sistema"
            },
            {
                "nome": "Empresa ABC Ltda",
                "tipo_cliente": TipoCliente.PESSOA_JURIDICA,
                "cpf_cnpj": "12345678000123",
                "email": "contato@empresaabc.com",
                "telefone": "1133334444",
                "endereco": "Av. Paulista, 1000",
                "bairro": "Bela Vista",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01310100",
                "status": StatusCliente.ATIVO,
                "limite_credito": 500000,  # R$ 5.000,00 em centavos
                "criado_por": "sistema"
            },
            {
                "nome": "Maria Santos",
                "tipo_cliente": TipoCliente.PESSOA_FISICA,
                "cpf_cnpj": "98765432109",
                "email": "maria.santos@email.com",
                "celular": "11999887766",
                "endereco": "Rua dos Jardins, 456",
                "bairro": "Jardins",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01234567",
                "status": StatusCliente.ATIVO,
                "pontos_fidelidade": 1500,
                "criado_por": "sistema"
            }
        ]
        
        for cliente_data in clientes_exemplo:
            cliente = Cliente(**cliente_data)
            session.add(cliente)
        
        session.commit()
        print(f"✅ {len(clientes_exemplo)} clientes de exemplo inseridos com sucesso!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao inserir dados de exemplo: {e}")
        raise
    finally:
        session.close()

def main():
    """Função principal."""
    print("🚀 Inicializando banco de dados do módulo de clientes...")
    
    try:
        # 1. Criar schema
        create_database_schema()
        
        # 2. Criar tabelas
        create_tables_if_not_exist()
        
        # 3. Inserir dados de exemplo (opcional)
        resposta = input("Deseja inserir dados de exemplo? (s/N): ").lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            insert_sample_data()
        
        print("🎉 Inicialização concluída com sucesso!")
        
    except Exception as e:
        print(f"💥 Erro durante a inicialização: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

