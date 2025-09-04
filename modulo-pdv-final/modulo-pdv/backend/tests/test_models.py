"""
Testes para os modelos do módulo de clientes.
"""

import pytest
from datetime import date
from app.models import Cliente, TipoCliente, StatusCliente

def test_criar_cliente_pessoa_fisica(db_session):
    """Testa a criação de um cliente pessoa física."""
    cliente = Cliente(
        nome="João Silva",
        tipo_cliente=TipoCliente.PESSOA_FISICA,
        cpf_cnpj="12345678901",
        email="joao@email.com",
        status=StatusCliente.ATIVO
    )
    
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    
    assert cliente.id is not None
    assert cliente.nome == "João Silva"
    assert cliente.tipo_cliente == TipoCliente.PESSOA_FISICA
    assert cliente.cpf_cnpj == "12345678901"
    assert cliente.email == "joao@email.com"
    assert cliente.status == StatusCliente.ATIVO
    assert cliente.data_criacao is not None

def test_criar_cliente_pessoa_juridica(db_session):
    """Testa a criação de um cliente pessoa jurídica."""
    cliente = Cliente(
        nome="Empresa ABC Ltda",
        tipo_cliente=TipoCliente.PESSOA_JURIDICA,
        cpf_cnpj="12345678000123",
        email="contato@empresa.com",
        limite_credito=100000,
        status=StatusCliente.ATIVO
    )
    
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    
    assert cliente.id is not None
    assert cliente.nome == "Empresa ABC Ltda"
    assert cliente.tipo_cliente == TipoCliente.PESSOA_JURIDICA
    assert cliente.cpf_cnpj == "12345678000123"
    assert cliente.limite_credito == 100000

def test_cliente_to_dict(db_session):
    """Testa a conversão do modelo para dicionário."""
    cliente = Cliente(
        nome="Maria Santos",
        tipo_cliente=TipoCliente.PESSOA_FISICA,
        cpf_cnpj="98765432109",
        email="maria@email.com",
        data_nascimento=date(1990, 5, 15),
        status=StatusCliente.ATIVO
    )
    
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    
    cliente_dict = cliente.to_dict()
    
    assert isinstance(cliente_dict, dict)
    assert cliente_dict["nome"] == "Maria Santos"
    assert cliente_dict["tipo_cliente"] == "pessoa_fisica"
    assert cliente_dict["cpf_cnpj"] == "98765432109"
    assert cliente_dict["email"] == "maria@email.com"
    assert cliente_dict["data_nascimento"] == "1990-05-15"
    assert cliente_dict["status"] == "ativo"

def test_cliente_defaults(db_session):
    """Testa os valores padrão do modelo Cliente."""
    cliente = Cliente(nome="Teste Cliente")
    
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    
    assert cliente.tipo_cliente == TipoCliente.PESSOA_FISICA
    assert cliente.status == StatusCliente.ATIVO
    assert cliente.limite_credito == 0
    assert cliente.pontos_fidelidade == 0

def test_cliente_repr(db_session):
    """Testa a representação string do modelo Cliente."""
    cliente = Cliente(
        nome="Teste Cliente",
        tipo_cliente=TipoCliente.PESSOA_FISICA
    )
    
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    
    repr_str = repr(cliente)
    assert "Cliente" in repr_str
    assert "Teste Cliente" in repr_str
    assert "pessoa_fisica" in repr_str

