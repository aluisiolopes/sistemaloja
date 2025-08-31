from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.crud import ProdutoCRUD, CategoriaCRUD, MarcaCRUD
from app.schemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse, ProdutoFilter, ProdutoSearch, ProdutoStats, PaginatedProductResponse, MessageResponse, CategoriaCreate, CategoriaUpdate, CategoriaResponse, MarcaCreate, MarcaUpdate, MarcaResponse
from app.database import get_db
from app.models import StatusProduto

import os
import shutil

router = APIRouter()

# --- Endpoints para Categorias ---
@router.post("/categorias/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    crud = CategoriaCRUD(db)
    db_categoria = crud.get_by_name(categoria.nome)
    if db_categoria:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Categoria já existe")
    return crud.create(categoria)

@router.get("/categorias/", response_model=List[CategoriaResponse])
def read_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crud = CategoriaCRUD(db)
    return crud.get_all(skip=skip, limit=limit)

@router.get("/categorias/{categoria_id}", response_model=CategoriaResponse)
def read_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    crud = CategoriaCRUD(db)
    db_categoria = crud.get_by_id(categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    return db_categoria

@router.put("/categorias/{categoria_id}", response_model=CategoriaResponse)
def update_categoria(categoria_id: UUID, categoria: CategoriaUpdate, db: Session = Depends(get_db)):
    crud = CategoriaCRUD(db)
    db_categoria = crud.update(categoria_id, categoria)
    if db_categoria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    return db_categoria

@router.delete("/categorias/{categoria_id}", response_model=MessageResponse)
def delete_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    crud = CategoriaCRUD(db)
    if not crud.delete(categoria_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")
    return MessageResponse(message="Categoria removida com sucesso")

# --- Endpoints para Marcas ---
@router.post("/marcas/", response_model=MarcaResponse, status_code=status.HTTP_201_CREATED)
def create_marca(marca: MarcaCreate, db: Session = Depends(get_db)):
    crud = MarcaCRUD(db)
    db_marca = crud.get_by_name(marca.nome)
    if db_marca:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Marca já existe")
    return crud.create(marca)

@router.get("/marcas/", response_model=List[MarcaResponse])
def read_marcas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crud = MarcaCRUD(db)
    return crud.get_all(skip=skip, limit=limit)

@router.get("/marcas/{marca_id}", response_model=MarcaResponse)
def read_marca(marca_id: UUID, db: Session = Depends(get_db)):
    crud = MarcaCRUD(db)
    db_marca = crud.get_by_id(marca_id)
    if db_marca is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marca não encontrada")
    return db_marca

@router.put("/marcas/{marca_id}", response_model=MarcaResponse)
def update_marca(marca_id: UUID, marca: MarcaUpdate, db: Session = Depends(get_db)):
    crud = MarcaCRUD(db)
    db_marca = crud.update(marca_id, marca)
    if db_marca is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marca não encontrada")
    return db_marca

@router.delete("/marcas/{marca_id}", response_model=MessageResponse)
def delete_marca(marca_id: UUID, db: Session = Depends(get_db)):
    crud = MarcaCRUD(db)
    if not crud.delete(marca_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marca não encontrada")
    return MessageResponse(message="Marca removida com sucesso")

# --- Endpoints para Produtos ---
@router.post("/produtos/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    if produto.codigo_barras and crud.get_by_codigo_barras(produto.codigo_barras):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Produto com este código de barras já existe")
    if produto.sku and crud.get_by_sku(produto.sku):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Produto com este SKU já existe")
    return crud.create(produto)

@router.get("/produtos/", response_model=PaginatedProductResponse)
def read_produtos(skip: int = 0, limit: int = 10, filters: ProdutoFilter = Depends(), db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    produtos, total = crud.get_all(skip=skip, limit=limit, filters=filters)
    return PaginatedProductResponse(
        produtos=produtos,
        total=total,
        pagina=skip // limit + 1,
        por_pagina=limit,
        total_paginas=(total + limit - 1) // limit
    )

@router.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def read_produto(produto_id: UUID, db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    db_produto = crud.get_by_id(produto_id)
    if db_produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return db_produto

@router.put("/produtos/{produto_id}", response_model=ProdutoResponse)
def update_produto(produto_id: UUID, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    db_produto = crud.update(produto_id, produto)
    if db_produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return db_produto

@router.delete("/produtos/{produto_id}", response_model=MessageResponse)
def delete_produto(produto_id: UUID, db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    if not crud.delete(produto_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return MessageResponse(message="Produto removido com sucesso")

@router.patch("/produtos/{produto_id}/inativar", response_model=ProdutoResponse)
def inativar_produto(produto_id: UUID, db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    db_produto = crud.soft_delete(produto_id, atualizado_por="API") # Exemplo de usuário
    if db_produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return db_produto

@router.get("/produtos/search/{termo}", response_model=List[ProdutoResponse])
def search_produtos(termo: str, limit: int = 10, db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    return crud.search(termo=termo, limit=limit)

@router.get("/produtos/stats/resumo", response_model=ProdutoStats)
def get_produto_stats(db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    return crud.get_stats()

# --- Endpoint para Upload de Imagem (Exemplo) ---
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 5242880)) # 5MB
ALLOWED_IMAGE_TYPES = os.getenv("ALLOWED_IMAGE_TYPES", "image/jpeg,image/png,image/gif").split(",")

@router.post("/produtos/{produto_id}/upload-imagem", response_model=ProdutoResponse)
async def upload_produto_imagem(produto_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    crud = ProdutoCRUD(db)
    db_produto = crud.get_by_id(produto_id)
    if db_produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de arquivo não permitido. Apenas JPEG, PNG ou GIF são aceitos.")

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tamanho do arquivo excede o limite de {MAX_FILE_SIZE / (1024 * 1024):.1f}MB.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_location = os.path.join(UPLOAD_DIR, f"{produto_id}_{file.filename}")

    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao salvar a imagem: {e}")

    db_produto.imagem_url = file_location # Em um ambiente real, isso seria uma URL pública
    db_produto.atualizado_por = "API_Upload"
    db.commit()
    db.refresh(db_produto)

    return db_produto


