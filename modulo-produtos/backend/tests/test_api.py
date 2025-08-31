import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client):
    """Testa o endpoint raiz."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_categoria(client, sample_categoria_data):
    """Testa a criação de categoria via API."""
    response = client.post("/api/v1/categorias/", json=sample_categoria_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["nome"] == sample_categoria_data["nome"]
    assert data["descricao"] == sample_categoria_data["descricao"]
    assert "id" in data

def test_get_categorias(client, sample_categoria_data):
    """Testa a listagem de categorias."""
    # Criar uma categoria primeiro
    client.post("/api/v1/categorias/", json=sample_categoria_data)
    
    response = client.get("/api/v1/categorias/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_create_marca(client, sample_marca_data):
    """Testa a criação de marca via API."""
    response = client.post("/api/v1/marcas/", json=sample_marca_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["nome"] == sample_marca_data["nome"]
    assert data["descricao"] == sample_marca_data["descricao"]
    assert "id" in data

def test_get_marcas(client, sample_marca_data):
    """Testa a listagem de marcas."""
    # Criar uma marca primeiro
    client.post("/api/v1/marcas/", json=sample_marca_data)
    
    response = client.get("/api/v1/marcas/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_create_produto(client, sample_produto_data):
    """Testa a criação de produto via API."""
    response = client.post("/api/v1/produtos/", json=sample_produto_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["nome"] == sample_produto_data["nome"]
    assert data["preco_venda"] == sample_produto_data["preco_venda"]
    assert data["sku"] == sample_produto_data["sku"]
    assert "id" in data

def test_get_produtos(client, sample_produto_data):
    """Testa a listagem de produtos."""
    # Criar um produto primeiro
    client.post("/api/v1/produtos/", json=sample_produto_data)
    
    response = client.get("/api/v1/produtos/")
    assert response.status_code == 200
    
    data = response.json()
    assert "produtos" in data
    assert "total" in data
    assert "pagina" in data
    assert isinstance(data["produtos"], list)
    assert len(data["produtos"]) >= 1

def test_get_produto_by_id(client, sample_produto_data):
    """Testa a busca de produto por ID."""
    # Criar um produto primeiro
    create_response = client.post("/api/v1/produtos/", json=sample_produto_data)
    produto_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/produtos/{produto_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == sample_produto_data["nome"]

def test_update_produto(client, sample_produto_data):
    """Testa a atualização de produto."""
    # Criar um produto primeiro
    create_response = client.post("/api/v1/produtos/", json=sample_produto_data)
    produto_id = create_response.json()["id"]
    
    # Dados para atualização
    update_data = {
        "nome": "Produto Atualizado",
        "preco_venda": 600000
    }
    
    response = client.put(f"/api/v1/produtos/{produto_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["nome"] == "Produto Atualizado"
    assert data["preco_venda"] == 600000

def test_inativar_produto(client, sample_produto_data):
    """Testa a inativação de produto."""
    # Criar um produto primeiro
    create_response = client.post("/api/v1/produtos/", json=sample_produto_data)
    produto_id = create_response.json()["id"]
    
    response = client.patch(f"/api/v1/produtos/{produto_id}/inativar")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "inativo"

def test_search_produtos(client, sample_produto_data):
    """Testa a busca de produtos por termo."""
    # Criar um produto primeiro
    client.post("/api/v1/produtos/", json=sample_produto_data)
    
    response = client.get("/api/v1/produtos/search/Galaxy")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "Galaxy" in data[0]["nome"]

def test_delete_produto(client, sample_produto_data):
    """Testa a remoção de produto."""
    # Criar um produto primeiro
    create_response = client.post("/api/v1/produtos/", json=sample_produto_data)
    produto_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/produtos/{produto_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    
    # Verificar se foi removido
    get_response = client.get(f"/api/v1/produtos/{produto_id}")
    assert get_response.status_code == 404

def test_get_produto_stats(client, sample_produto_data):
    """Testa as estatísticas de produtos."""
    # Criar alguns produtos primeiro
    client.post("/api/v1/produtos/", json=sample_produto_data)
    
    response = client.get("/api/v1/produtos/stats/resumo")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_produtos" in data
    assert "por_status" in data
    assert "por_categoria" in data
    assert "por_marca" in data
    assert data["total_produtos"] >= 1

def test_create_produto_duplicate_sku(client, sample_produto_data):
    """Testa a criação de produto com SKU duplicado."""
    # Criar um produto primeiro
    client.post("/api/v1/produtos/", json=sample_produto_data)
    
    # Tentar criar outro com o mesmo SKU
    response = client.post("/api/v1/produtos/", json=sample_produto_data)
    assert response.status_code == 409  # Conflict

def test_create_produto_duplicate_codigo_barras(client, sample_produto_data):
    """Testa a criação de produto com código de barras duplicado."""
    # Criar um produto primeiro
    client.post("/api/v1/produtos/", json=sample_produto_data)
    
    # Tentar criar outro com o mesmo código de barras mas SKU diferente
    duplicate_data = sample_produto_data.copy()
    duplicate_data["sku"] = "OUTRO-SKU"
    
    response = client.post("/api/v1/produtos/", json=duplicate_data)
    assert response.status_code == 409  # Conflict

def test_get_produto_not_found(client):
    """Testa a busca de produto inexistente."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/produtos/{fake_id}")
    assert response.status_code == 404

def test_update_produto_not_found(client):
    """Testa a atualização de produto inexistente."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    update_data = {"nome": "Produto Inexistente"}
    
    response = client.put(f"/api/v1/produtos/{fake_id}", json=update_data)
    assert response.status_code == 404

def test_delete_produto_not_found(client):
    """Testa a remoção de produto inexistente."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/api/v1/produtos/{fake_id}")
    assert response.status_code == 404

