import pytest
from app.models import Categoria, Marca, Produto, UnidadeMedida, StatusProduto

def test_categoria_creation(db_session):
    """Testa a criação de uma categoria."""
    categoria = Categoria(nome="Eletrônicos", descricao="Produtos eletrônicos")
    db_session.add(categoria)
    db_session.commit()
    
    assert categoria.id is not None
    assert categoria.nome == "Eletrônicos"
    assert categoria.descricao == "Produtos eletrônicos"
    assert categoria.data_criacao is not None

def test_categoria_to_dict(db_session):
    """Testa a conversão de categoria para dicionário."""
    categoria = Categoria(nome="Roupas", descricao="Vestuário")
    db_session.add(categoria)
    db_session.commit()
    
    categoria_dict = categoria.to_dict()
    
    assert "id" in categoria_dict
    assert categoria_dict["nome"] == "Roupas"
    assert categoria_dict["descricao"] == "Vestuário"
    assert "data_criacao" in categoria_dict

def test_marca_creation(db_session):
    """Testa a criação de uma marca."""
    marca = Marca(nome="Nike", descricao="Marca de artigos esportivos")
    db_session.add(marca)
    db_session.commit()
    
    assert marca.id is not None
    assert marca.nome == "Nike"
    assert marca.descricao == "Marca de artigos esportivos"
    assert marca.data_criacao is not None

def test_produto_creation(db_session):
    """Testa a criação de um produto."""
    # Criar categoria e marca primeiro
    categoria = Categoria(nome="Eletrônicos")
    marca = Marca(nome="Samsung")
    db_session.add(categoria)
    db_session.add(marca)
    db_session.commit()
    
    produto = Produto(
        nome="Smartphone",
        descricao="Celular moderno",
        codigo_barras="1234567890",
        sku="SMART-001",
        preco_venda=100000,
        preco_custo=70000,
        unidade_medida=UnidadeMedida.UNIDADE,
        categoria_id=categoria.id,
        marca_id=marca.id,
        status=StatusProduto.ATIVO,
        criado_por="teste"
    )
    db_session.add(produto)
    db_session.commit()
    
    assert produto.id is not None
    assert produto.nome == "Smartphone"
    assert produto.preco_venda == 100000
    assert produto.preco_custo == 70000
    assert produto.unidade_medida == UnidadeMedida.UNIDADE
    assert produto.status == StatusProduto.ATIVO
    assert produto.categoria_id == categoria.id
    assert produto.marca_id == marca.id

def test_produto_to_dict(db_session):
    """Testa a conversão de produto para dicionário."""
    categoria = Categoria(nome="Eletrônicos")
    marca = Marca(nome="Samsung")
    db_session.add(categoria)
    db_session.add(marca)
    db_session.commit()
    
    produto = Produto(
        nome="Tablet",
        preco_venda=50000,
        preco_custo=30000,
        categoria_id=categoria.id,
        marca_id=marca.id
    )
    db_session.add(produto)
    db_session.commit()
    
    # Recarregar para ter os relacionamentos
    db_session.refresh(produto)
    
    produto_dict = produto.to_dict()
    
    assert "id" in produto_dict
    assert produto_dict["nome"] == "Tablet"
    assert produto_dict["preco_venda"] == 50000
    assert produto_dict["preco_custo"] == 30000
    assert produto_dict["categoria_nome"] == "Eletrônicos"
    assert produto_dict["marca_nome"] == "Samsung"

def test_produto_relationships(db_session):
    """Testa os relacionamentos do produto."""
    categoria = Categoria(nome="Livros")
    marca = Marca(nome="Editora ABC")
    db_session.add(categoria)
    db_session.add(marca)
    db_session.commit()
    
    produto = Produto(
        nome="Livro de Python",
        preco_venda=5000,
        preco_custo=2500,
        categoria_id=categoria.id,
        marca_id=marca.id
    )
    db_session.add(produto)
    db_session.commit()
    
    # Testar relacionamentos
    assert produto.categoria.nome == "Livros"
    assert produto.marca.nome == "Editora ABC"
    assert produto in categoria.produtos
    assert produto in marca.produtos

def test_enums():
    """Testa os enums definidos."""
    # Testar UnidadeMedida
    assert UnidadeMedida.UNIDADE.value == "unidade"
    assert UnidadeMedida.KG.value == "kg"
    assert UnidadeMedida.L.value == "l"
    
    # Testar StatusProduto
    assert StatusProduto.ATIVO.value == "ativo"
    assert StatusProduto.INATIVO.value == "inativo"
    assert StatusProduto.ESGOTADO.value == "esgotado"
    assert StatusProduto.PROMOCAO.value == "promocao"

