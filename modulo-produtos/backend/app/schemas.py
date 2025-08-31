from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.models import UnidadeMedida, StatusProduto


# Schemas para Categoria
class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    descricao: Optional[str] = Field(None, max_length=1000)

    @validator("nome")
    def validate_nome(cls, v):
        return v.strip().title()


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    nome: Optional[str] = Field(None, min_length=2, max_length=255)


class CategoriaResponse(CategoriaBase):
    id: UUID
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schemas para Marca
class MarcaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    descricao: Optional[str] = Field(None, max_length=1000)

    @validator("nome")
    def validate_nome(cls, v):
        return v.strip().title()


class MarcaCreate(MarcaBase):
    pass


class MarcaUpdate(MarcaBase):
    nome: Optional[str] = Field(None, min_length=2, max_length=255)


class MarcaResponse(MarcaBase):
    id: UUID
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schemas para Produto
class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    descricao: Optional[str] = Field(None, max_length=2000)
    codigo_barras: Optional[str] = Field(None, max_length=255)
    sku: Optional[str] = Field(None, max_length=255)
    preco_venda: int = Field(..., ge=0)  # Em centavos
    preco_custo: int = Field(..., ge=0)  # Em centavos
    unidade_medida: UnidadeMedida = Field(UnidadeMedida.UNIDADE)
    categoria_id: Optional[UUID] = None
    marca_id: Optional[UUID] = None
    status: StatusProduto = Field(StatusProduto.ATIVO)
    imagem_url: Optional[str] = Field(None, max_length=255)
    observacoes: Optional[str] = Field(None, max_length=2000)
    criado_por: Optional[str] = Field(None, max_length=100)
    atualizado_por: Optional[str] = Field(None, max_length=100)

    @validator("nome")
    def validate_nome(cls, v):
        return v.strip()

    @validator("codigo_barras", "sku", pre=True, always=True)
    def strip_optional_strings(cls, v):
        if isinstance(v, str):
            return v.strip() or None
        return v


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(ProdutoBase):
    nome: Optional[str] = Field(None, min_length=2, max_length=255)
    preco_venda: Optional[int] = Field(None, ge=0)
    preco_custo: Optional[int] = Field(None, ge=0)
    unidade_medida: Optional[UnidadeMedida] = None
    status: Optional[StatusProduto] = None


class ProdutoResponse(ProdutoBase):
    id: UUID
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    categoria_nome: Optional[str] = None
    marca_nome: Optional[str] = None

    class Config:
        from_attributes = True


class ProdutoFilter(BaseModel):
    nome: Optional[str] = None
    codigo_barras: Optional[str] = None
    sku: Optional[str] = None
    unidade_medida: Optional[UnidadeMedida] = None
    categoria_id: Optional[UUID] = None
    marca_id: Optional[UUID] = None
    status: Optional[StatusProduto] = None
    min_preco_venda: Optional[int] = None
    max_preco_venda: Optional[int] = None
    min_preco_custo: Optional[int] = None
    max_preco_custo: Optional[int] = None

    class Config:
        use_enum_values = True


class ProdutoSearch(BaseModel):
    termo: str
    limite: int = Field(10, ge=1, le=50)


class ProdutoStats(BaseModel):
    total_produtos: int
    por_status: dict
    por_categoria: dict
    por_marca: dict
    valor_total_estoque_venda: int
    valor_total_estoque_custo: int


class PaginatedProductResponse(BaseModel):
    produtos: List[ProdutoResponse]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int


class MessageResponse(BaseModel):
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


