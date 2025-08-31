import pytest
from app.crud import ProdutoCRUD, CategoriaCRUD, MarcaCRUD
from app.schemas import ProdutoCreate, ProdutoUpdate, CategoriaCreate, MarcaCreate
from app.models import StatusProduto, UnidadeMedida

def test_categoria_crud_create(db_session):
    """Testa a criação de categoria via CRUD."""
    crud = CategoriaCRUD(db_session)
    categoria_data = CategoriaCreate(nome="Eletrônicos", descricao="Produtos eletrônicos")
    
    categoria = crud.create(categoria_data)
    
    assert categoria.id is not None
    assert categoria.nome == "Eletrônicos"
    assert categoria.descricao == "Produtos eletrônicos"

def test_categoria_crud_get_by_id(db_session):
    """Testa a busca de categoria por ID."""
    crud = CategoriaCRUD(db_session)
    categoria_data = CategoriaCreate(nome="Roupas")
    categoria = crud.create(categoria_data)
    
    found_categoria = crud.get_by_id(categoria.id)
    
    assert found_categoria is not None
    assert found_categoria.id == categoria.id
    assert found_categoria.nome == "Roupas"

def test_categoria_crud_get_by_name(db_session):
    """Testa a busca de categoria por nome."""
    crud = CategoriaCRUD(db_session)
    categoria_data = CategoriaCreate(nome="Livros")
    crud.create(categoria_data)
    
    found_categoria = crud.get_by_name("Livros")
    
    assert found_categoria is not None
    assert found_categoria.nome == "Livros"

def test_marca_crud_create(db_session):
    """Testa a criação de marca via CRUD."""
    crud = MarcaCRUD(db_session)
    marca_data = MarcaCreate(nome="Samsung", descricao="Marca sul-coreana")
    
    marca = crud.create(marca_data)
    
    assert marca.id is not None
    assert marca.nome == "Samsung"
    assert marca.descricao == "Marca sul-coreana"

def test_produto_crud_create(db_session):
    """Testa a criação de produto via CRUD."""
    # Criar categoria e marca primeiro
    categoria_crud = CategoriaCRUD(db_session)
    marca_crud = MarcaCRUD(db_session)
    
    categoria = categoria_crud.create(CategoriaCreate(nome="Eletrônicos"))
    marca = marca_crud.create(MarcaCreate(nome="Apple"))
    
    # Criar produto
    produto_crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="iPhone 15",
        descricao="Smartphone da Apple",
        codigo_barras="1234567890123",
        sku="IPHONE-15",
        preco_venda=600000,
        preco_custo=400000,
        unidade_medida=UnidadeMedida.UNIDADE,
        categoria_id=categoria.id,
        marca_id=marca.id,
        status=StatusProduto.ATIVO,
        criado_por="teste"
    )
    
    produto = produto_crud.create(produto_data)
    
    assert produto.id is not None
    assert produto.nome == "iPhone 15"
    assert produto.preco_venda == 600000
    assert produto.categoria_id == categoria.id
    assert produto.marca_id == marca.id

def test_produto_crud_get_by_codigo_barras(db_session):
    """Testa a busca de produto por código de barras."""
    categoria_crud = CategoriaCRUD(db_session)
    categoria = categoria_crud.create(CategoriaCreate(nome="Eletrônicos"))
    
    produto_crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Tablet",
        codigo_barras="9876543210987",
        sku="TAB-001",
        preco_venda=30000,
        preco_custo=20000,
        categoria_id=categoria.id
    )
    produto = produto_crud.create(produto_data)
    
    found_produto = produto_crud.get_by_codigo_barras("9876543210987")
    
    assert found_produto is not None
    assert found_produto.id == produto.id
    assert found_produto.codigo_barras == "9876543210987"

def test_produto_crud_get_by_sku(db_session):
    """Testa a busca de produto por SKU."""
    produto_crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Mouse",
        sku="MOUSE-001",
        preco_venda=5000,
        preco_custo=2500
    )
    produto = produto_crud.create(produto_data)
    
    found_produto = produto_crud.get_by_sku("MOUSE-001")
    
    assert found_produto is not None
    assert found_produto.id == produto.id
    assert found_produto.sku == "MOUSE-001"

def test_produto_crud_update(db_session):
    """Testa a atualização de produto."""
    produto_crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Teclado",
        preco_venda=8000,
        preco_custo=4000
    )
    produto = produto_crud.create(produto_data)
    
    # Atualizar produto
    update_data = ProdutoUpdate(
        nome="Teclado Mecânico",
        preco_venda=12000,
        status=StatusProduto.PROMOCAO
    )
    updated_produto = produto_crud.update(produto.id, update_data)
    
    assert updated_produto is not None
    assert updated_produto.nome == "Teclado Mecânico"
    assert updated_produto.preco_venda == 12000
    assert updated_produto.status == StatusProduto.PROMOCAO

def test_produto_crud_search(db_session):
    """Testa a busca de produtos por termo."""
    produto_crud = ProdutoCRUD(db_session)
    
    # Criar alguns produtos
    produtos_data = [
        ProdutoCreate(nome="Smartphone Samsung", sku="SMART-SAM", preco_venda=50000, preco_custo=30000),
        ProdutoCreate(nome="Tablet Apple", sku="TAB-APP", preco_venda=40000, preco_custo=25000),
        ProdutoCreate(nome="Notebook Dell", sku="NOTE-DELL", preco_venda=200000, preco_custo=150000),
    ]
    
    for produto_data in produtos_data:
        produto_crud.create(produto_data)
    
    # Buscar por "Samsung"
    resultados = produto_crud.search("Samsung")
    assert len(resultados) == 1
    assert resultados[0].nome == "Smartphone Samsung"
    
    # Buscar por "Apple"
    resultados = produto_crud.search("Apple")
    assert len(resultados) == 1
    assert resultados[0].nome == "Tablet Apple"
    
    # Buscar por termo que não existe
    resultados = produto_crud.search("Xbox")
    assert len(resultados) == 0

def test_produto_crud_soft_delete(db_session):
    """Testa a inativação (soft delete) de produto."""
    produto_crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Produto para inativar",
        preco_venda=1000,
        preco_custo=500
    )
    produto = produto_crud.create(produto_data)
    
    # Inativar produto
    inativado = produto_crud.soft_delete(produto.id, "teste_user")
    
    assert inativado is not None
    assert inativado.status == StatusProduto.INATIVO
    assert inativado.atualizado_por == "teste_user"

def test_produto_crud_delete(db_session):
    """Testa a remoção permanente de produto."""
    produto_crud = ProdutoCRUD(db_session)
    produto_data = ProdutoCreate(
        nome="Produto para remover",
        preco_venda=1000,
        preco_custo=500
    )
    produto = produto_crud.create(produto_data)
    produto_id = produto.id
    
    # Remover produto
    deleted = produto_crud.delete(produto_id)
    
    assert deleted is True
    
    # Verificar se foi removido
    found_produto = produto_crud.get_by_id(produto_id)
    assert found_produto is None

