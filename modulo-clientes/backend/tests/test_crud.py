"""
Testes para as operações CRUD do módulo de clientes.
"""

import pytest
from uuid import uuid4
from app.crud import ClienteCRUD
from app.schemas import ClienteCreate, ClienteUpdate, ClienteFilter
from app.models import TipoCliente, StatusCliente

def test_criar_cliente(db_session):
    """Testa a criação de um cliente via CRUD."""
    crud = ClienteCRUD(db_session)
    
    cliente_data = ClienteCreate(
        nome="João Silva",
        tipo_cliente="pessoa_fisica",
        cpf_cnpj="12345678901",
        email="joao@email.com",
        telefone="11987654321"
    )
    
    cliente = crud.create(cliente_data)
    
    assert cliente.id is not None
    assert cliente.nome == "João Silva"
    assert cliente.cpf_cnpj == "12345678901"
    assert cliente.email == "joao@email.com"

def test_criar_cliente_cpf_duplicado(db_session):
    """Testa erro ao criar cliente com CPF duplicado."""
    crud = ClienteCRUD(db_session)
    
    # Primeiro cliente
    cliente_data1 = ClienteCreate(
        nome="João Silva",
        cpf_cnpj="12345678901",
        email="joao1@email.com"
    )
    crud.create(cliente_data1)
    
    # Segundo cliente com mesmo CPF
    cliente_data2 = ClienteCreate(
        nome="Maria Silva",
        cpf_cnpj="12345678901",
        email="maria@email.com"
    )
    
    with pytest.raises(ValueError, match="CPF/CNPJ.*já existe"):
        crud.create(cliente_data2)

def test_buscar_cliente_por_id(db_session):
    """Testa busca de cliente por ID."""
    crud = ClienteCRUD(db_session)
    
    # Criar cliente
    cliente_data = ClienteCreate(
        nome="Maria Santos",
        email="maria@email.com"
    )
    cliente_criado = crud.create(cliente_data)
    
    # Buscar por ID
    cliente_encontrado = crud.get_by_id(cliente_criado.id)
    
    assert cliente_encontrado is not None
    assert cliente_encontrado.id == cliente_criado.id
    assert cliente_encontrado.nome == "Maria Santos"

def test_buscar_cliente_por_cpf_cnpj(db_session):
    """Testa busca de cliente por CPF/CNPJ."""
    crud = ClienteCRUD(db_session)
    
    cliente_data = ClienteCreate(
        nome="Pedro Costa",
        cpf_cnpj="98765432109",
        email="pedro@email.com"
    )
    crud.create(cliente_data)
    
    cliente_encontrado = crud.get_by_cpf_cnpj("98765432109")
    
    assert cliente_encontrado is not None
    assert cliente_encontrado.cpf_cnpj == "98765432109"
    assert cliente_encontrado.nome == "Pedro Costa"

def test_buscar_cliente_por_email(db_session):
    """Testa busca de cliente por email."""
    crud = ClienteCRUD(db_session)
    
    cliente_data = ClienteCreate(
        nome="Ana Silva",
        email="ana@email.com"
    )
    crud.create(cliente_data)
    
    cliente_encontrado = crud.get_by_email("ana@email.com")
    
    assert cliente_encontrado is not None
    assert cliente_encontrado.email == "ana@email.com"
    assert cliente_encontrado.nome == "Ana Silva"

def test_listar_clientes(db_session):
    """Testa listagem de clientes com paginação."""
    crud = ClienteCRUD(db_session)
    
    # Criar múltiplos clientes
    for i in range(5):
        cliente_data = ClienteCreate(
            nome=f"Cliente {i}",
            email=f"cliente{i}@email.com",
            cpf_cnpj=f"1234567890{i}"
        )
        crud.create(cliente_data)
    
    # Listar com paginação
    clientes, total = crud.get_all(skip=0, limit=3)
    
    assert len(clientes) == 3
    assert total == 5

def test_listar_clientes_com_filtros(db_session):
    """Testa listagem de clientes com filtros."""
    crud = ClienteCRUD(db_session)
    
    # Criar clientes com dados diferentes
    cliente_data1 = ClienteCreate(
        nome="João Silva",
        tipo_cliente="pessoa_fisica",
        cidade="São Paulo",
        estado="SP"
    )
    crud.create(cliente_data1)
    
    cliente_data2 = ClienteCreate(
        nome="Empresa ABC",
        tipo_cliente="pessoa_juridica",
        cidade="Rio de Janeiro",
        estado="RJ"
    )
    crud.create(cliente_data2)
    
    # Filtrar por tipo
    filtros = ClienteFilter(tipo_cliente="pessoa_fisica")
    clientes, total = crud.get_all(filters=filtros)
    
    assert total == 1
    assert clientes[0].nome == "João Silva"
    
    # Filtrar por cidade
    filtros = ClienteFilter(cidade="Rio")
    clientes, total = crud.get_all(filters=filtros)
    
    assert total == 1
    assert clientes[0].nome == "Empresa ABC"

def test_atualizar_cliente(db_session):
    """Testa atualização de cliente."""
    crud = ClienteCRUD(db_session)
    
    # Criar cliente
    cliente_data = ClienteCreate(
        nome="Carlos Santos",
        email="carlos@email.com"
    )
    cliente = crud.create(cliente_data)
    
    # Atualizar cliente
    update_data = ClienteUpdate(
        nome="Carlos Santos Silva",
        telefone="11999888777"
    )
    cliente_atualizado = crud.update(cliente.id, update_data)
    
    assert cliente_atualizado is not None
    assert cliente_atualizado.nome == "Carlos Santos Silva"
    assert cliente_atualizado.telefone == "11999888777"
    assert cliente_atualizado.email == "carlos@email.com"  # Não alterado

def test_remover_cliente(db_session):
    """Testa remoção de cliente."""
    crud = ClienteCRUD(db_session)
    
    # Criar cliente
    cliente_data = ClienteCreate(
        nome="Cliente para Remover",
        email="remover@email.com"
    )
    cliente = crud.create(cliente_data)
    
    # Remover cliente
    sucesso = crud.delete(cliente.id)
    
    assert sucesso is True
    
    # Verificar se foi removido
    cliente_removido = crud.get_by_id(cliente.id)
    assert cliente_removido is None

def test_inativar_cliente(db_session):
    """Testa inativação de cliente (soft delete)."""
    crud = ClienteCRUD(db_session)
    
    # Criar cliente
    cliente_data = ClienteCreate(
        nome="Cliente para Inativar",
        email="inativar@email.com"
    )
    cliente = crud.create(cliente_data)
    
    # Inativar cliente
    cliente_inativado = crud.soft_delete(cliente.id, "admin")
    
    assert cliente_inativado is not None
    assert cliente_inativado.status == StatusCliente.INATIVO
    assert cliente_inativado.atualizado_por == "admin"

def test_buscar_clientes(db_session):
    """Testa busca de clientes por termo."""
    crud = ClienteCRUD(db_session)
    
    # Criar clientes
    cliente_data1 = ClienteCreate(
        nome="João Silva",
        email="joao@email.com",
        cpf_cnpj="12345678901"
    )
    crud.create(cliente_data1)
    
    cliente_data2 = ClienteCreate(
        nome="Maria Santos",
        email="maria@email.com",
        cpf_cnpj="98765432109"
    )
    crud.create(cliente_data2)
    
    # Buscar por nome
    clientes = crud.search("João", limit=10)
    assert len(clientes) == 1
    assert clientes[0].nome == "João Silva"
    
    # Buscar por email
    clientes = crud.search("maria@email.com", limit=10)
    assert len(clientes) == 1
    assert clientes[0].nome == "Maria Santos"
    
    # Buscar por CPF
    clientes = crud.search("123456789", limit=10)
    assert len(clientes) == 1
    assert clientes[0].nome == "João Silva"

def test_estatisticas_clientes(db_session):
    """Testa obtenção de estatísticas de clientes."""
    crud = ClienteCRUD(db_session)
    
    # Criar clientes com diferentes tipos e status
    clientes_data = [
        ClienteCreate(nome="PF Ativo 1", tipo_cliente="pessoa_fisica", status="ativo"),
        ClienteCreate(nome="PF Ativo 2", tipo_cliente="pessoa_fisica", status="ativo"),
        ClienteCreate(nome="PF Inativo", tipo_cliente="pessoa_fisica", status="inativo"),
        ClienteCreate(nome="PJ Ativo", tipo_cliente="pessoa_juridica", status="ativo"),
        ClienteCreate(nome="PJ Bloqueado", tipo_cliente="pessoa_juridica", status="bloqueado"),
    ]
    
    for cliente_data in clientes_data:
        crud.create(cliente_data)
    
    stats = crud.get_stats()
    
    assert stats["total"] == 5
    assert stats["por_status"]["ativos"] == 3
    assert stats["por_status"]["inativos"] == 1
    assert stats["por_status"]["bloqueados"] == 1
    assert stats["por_tipo"]["pessoa_fisica"] == 3
    assert stats["por_tipo"]["pessoa_juridica"] == 2

