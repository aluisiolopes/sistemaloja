"""
Testes para os endpoints da API do módulo de clientes.
"""

import pytest
from fastapi.testclient import TestClient

def test_health_check(client):
    """Testa o endpoint de health check."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data

def test_criar_cliente_sucesso(client, cliente_data):
    """Testa criação de cliente com sucesso."""
    response = client.post("/api/v1/clientes/", json=cliente_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["nome"] == cliente_data["nome"]
    assert data["cpf_cnpj"] == cliente_data["cpf_cnpj"]
    assert data["email"] == cliente_data["email"]
    assert "id" in data

def test_criar_cliente_dados_invalidos(client):
    """Testa criação de cliente com dados inválidos."""
    cliente_invalido = {
        "nome": "",  # Nome vazio
        "email": "email_invalido",  # Email inválido
        "cpf_cnpj": "123"  # CPF inválido
    }
    
    response = client.post("/api/v1/clientes/", json=cliente_invalido)
    assert response.status_code == 422  # Validation Error

def test_listar_clientes(client, cliente_data):
    """Testa listagem de clientes."""
    # Criar um cliente primeiro
    client.post("/api/v1/clientes/", json=cliente_data)
    
    # Listar clientes
    response = client.get("/api/v1/clientes/")
    assert response.status_code == 200
    
    data = response.json()
    assert "clientes" in data
    assert "total" in data
    assert "pagina" in data
    assert len(data["clientes"]) >= 1

def test_listar_clientes_com_filtros(client, cliente_data, cliente_juridica_data):
    """Testa listagem de clientes com filtros."""
    # Criar clientes
    client.post("/api/v1/clientes/", json=cliente_data)
    client.post("/api/v1/clientes/", json=cliente_juridica_data)
    
    # Filtrar por tipo pessoa física
    response = client.get("/api/v1/clientes/?tipo_cliente=pessoa_fisica")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 1
    assert data["clientes"][0]["tipo_cliente"] == "pessoa_fisica"
    
    # Filtrar por cidade
    response = client.get("/api/v1/clientes/?cidade=São Paulo")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 2  # Ambos são de São Paulo

def test_buscar_cliente_por_id(client, cliente_data):
    """Testa busca de cliente por ID."""
    # Criar cliente
    response_create = client.post("/api/v1/clientes/", json=cliente_data)
    cliente_criado = response_create.json()
    cliente_id = cliente_criado["id"]
    
    # Buscar por ID
    response = client.get(f"/api/v1/clientes/{cliente_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == cliente_id
    assert data["nome"] == cliente_data["nome"]

def test_buscar_cliente_inexistente(client):
    """Testa busca de cliente que não existe."""
    cliente_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/clientes/{cliente_id}")
    assert response.status_code == 404

def test_atualizar_cliente(client, cliente_data):
    """Testa atualização de cliente."""
    # Criar cliente
    response_create = client.post("/api/v1/clientes/", json=cliente_data)
    cliente_criado = response_create.json()
    cliente_id = cliente_criado["id"]
    
    # Dados para atualização
    update_data = {
        "nome": "João Silva Santos",
        "telefone": "11999888777"
    }
    
    # Atualizar cliente
    response = client.put(f"/api/v1/clientes/{cliente_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["nome"] == "João Silva Santos"
    assert data["telefone"] == "11999888777"
    assert data["email"] == cliente_data["email"]  # Não alterado

def test_remover_cliente(client, cliente_data):
    """Testa remoção de cliente."""
    # Criar cliente
    response_create = client.post("/api/v1/clientes/", json=cliente_data)
    cliente_criado = response_create.json()
    cliente_id = cliente_criado["id"]
    
    # Remover cliente
    response = client.delete(f"/api/v1/clientes/{cliente_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    
    # Verificar se foi removido
    response_get = client.get(f"/api/v1/clientes/{cliente_id}")
    assert response_get.status_code == 404

def test_inativar_cliente(client, cliente_data):
    """Testa inativação de cliente."""
    # Criar cliente
    response_create = client.post("/api/v1/clientes/", json=cliente_data)
    cliente_criado = response_create.json()
    cliente_id = cliente_criado["id"]
    
    # Inativar cliente
    response = client.patch(f"/api/v1/clientes/{cliente_id}/inativar")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "inativo"

def test_buscar_clientes_por_termo(client, cliente_data):
    """Testa busca de clientes por termo."""
    # Criar cliente
    client.post("/api/v1/clientes/", json=cliente_data)
    
    # Buscar por nome
    response = client.get("/api/v1/clientes/buscar/João")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= 1
    assert data[0]["nome"] == cliente_data["nome"]

def test_buscar_cliente_por_cpf_cnpj(client, cliente_data):
    """Testa busca de cliente por CPF/CNPJ."""
    # Criar cliente
    client.post("/api/v1/clientes/", json=cliente_data)
    
    # Buscar por CPF
    response = client.get(f"/api/v1/clientes/cpf-cnpj/{cliente_data['cpf_cnpj']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["cpf_cnpj"] == cliente_data["cpf_cnpj"]

def test_buscar_cliente_por_email(client, cliente_data):
    """Testa busca de cliente por email."""
    # Criar cliente
    client.post("/api/v1/clientes/", json=cliente_data)
    
    # Buscar por email
    response = client.get(f"/api/v1/clientes/email/{cliente_data['email']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == cliente_data["email"]

def test_estatisticas_clientes(client, cliente_data, cliente_juridica_data):
    """Testa endpoint de estatísticas."""
    # Criar clientes
    client.post("/api/v1/clientes/", json=cliente_data)
    client.post("/api/v1/clientes/", json=cliente_juridica_data)
    
    # Obter estatísticas
    response = client.get("/api/v1/clientes/stats/resumo")
    assert response.status_code == 200
    
    data = response.json()
    assert "total" in data
    assert "por_status" in data
    assert "por_tipo" in data
    assert data["total"] >= 2

def test_paginacao(client):
    """Testa paginação da listagem de clientes."""
    # Criar múltiplos clientes
    for i in range(5):
        cliente_data = {
            "nome": f"Cliente {i}",
            "email": f"cliente{i}@email.com",
            "cpf_cnpj": f"1234567890{i}"
        }
        client.post("/api/v1/clientes/", json=cliente_data)
    
    # Primeira página
    response = client.get("/api/v1/clientes/?pagina=1&por_pagina=2")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["clientes"]) == 2
    assert data["pagina"] == 1
    assert data["total"] >= 5
    
    # Segunda página
    response = client.get("/api/v1/clientes/?pagina=2&por_pagina=2")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["clientes"]) == 2
    assert data["pagina"] == 2

