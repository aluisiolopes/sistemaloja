from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class UnidadeMedida(enum.Enum):
    UNIDADE = "unidade"
    KG = "kg"
    G = "g"
    M = "m"
    CM = "cm"
    MM = "mm"
    L = "l"
    ML = "ml"
    CAIXA = "caixa"
    PACOTE = "pacote"


class StatusProduto(enum.Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    ESGOTADO = "esgotado"
    PROMOCAO = "promocao"


class Categoria(Base):
    __tablename__ = "categorias"
    __table_args__ = {"schema": "produtos"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    nome = Column(String(255), nullable=False, unique=True)
    descricao = Column(Text)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    produtos = relationship("Produto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id={self.id}, nome=\'{self.nome}\')>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "descricao": self.descricao,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None,
        }


class Marca(Base):
    __tablename__ = "marcas"
    __table_args__ = {"schema": "produtos"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    nome = Column(String(255), nullable=False, unique=True)
    descricao = Column(Text)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    produtos = relationship("Produto", back_populates="marca")

    def __repr__(self):
        return f"<Marca(id={self.id}, nome=\'{self.nome}\')>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "descricao": self.descricao,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None,
        }


class Produto(Base):
    __tablename__ = "produtos"
    __table_args__ = {"schema": "produtos"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    nome = Column(String(255), nullable=False, index=True)
    descricao = Column(Text)
    codigo_barras = Column(String(255), unique=True, index=True)
    sku = Column(String(255), unique=True, index=True)
    preco_venda = Column(Integer, nullable=False, default=0)  # Preço em centavos
    preco_custo = Column(Integer, nullable=False, default=0)  # Preço em centavos
    unidade_medida = Column(Enum(UnidadeMedida, name="unidademedida", schema="produtos"),
                            nullable=False, server_default=UnidadeMedida.UNIDADE.value)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("produtos.categorias.id"), nullable=True)
    marca_id = Column(UUID(as_uuid=True), ForeignKey("produtos.marcas.id"), nullable=True)
    status = Column(Enum(StatusProduto, name="statusproduto", schema="produtos"),
                    nullable=False, server_default=StatusProduto.ATIVO.value)
    imagem_url = Column(String(255))
    observacoes = Column(Text)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    criado_por = Column(String(100))
    atualizado_por = Column(String(100))

    categoria = relationship("Categoria", back_populates="produtos")
    marca = relationship("Marca", back_populates="produtos")

    def __repr__(self):
        return f"<Produto(id={self.id}, nome=\'{self.nome}\', sku=\'{self.sku}\')>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "descricao": self.descricao,
            "codigo_barras": self.codigo_barras,
            "sku": self.sku,
            "preco_venda": self.preco_venda,
            "preco_custo": self.preco_custo,
            "unidade_medida": self.unidade_medida.value if self.unidade_medida else None,
            "categoria_id": str(self.categoria_id) if self.categoria_id else None,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "marca_id": str(self.marca_id) if self.marca_id else None,
            "marca_nome": self.marca.nome if self.marca else None,
            "status": self.status.value if self.status else None,
            "imagem_url": self.imagem_url,
            "observacoes": self.observacoes,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            "criado_por": self.criado_por,
            "atualizado_por": self.atualizado_por,
        }


