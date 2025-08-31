from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, case

from app.models import Produto, Categoria, Marca, StatusProduto, UnidadeMedida
from app.schemas import ProdutoCreate, ProdutoUpdate, ProdutoFilter, CategoriaCreate, CategoriaUpdate, MarcaCreate, MarcaUpdate


class CategoriaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, categoria: CategoriaCreate) -> Categoria:
        db_categoria = Categoria(nome=categoria.nome, descricao=categoria.descricao)
        self.db.add(db_categoria)
        self.db.commit()
        self.db.refresh(db_categoria)
        return db_categoria

    def get_by_id(self, categoria_id: UUID) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(Categoria.id == categoria_id).first()

    def get_by_name(self, nome: str) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(func.lower(Categoria.nome) == func.lower(nome)).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        return self.db.query(Categoria).offset(skip).limit(limit).all()

    def update(self, categoria_id: UUID, categoria: CategoriaUpdate) -> Optional[Categoria]:
        db_categoria = self.get_by_id(categoria_id)
        if db_categoria:
            for key, value in categoria.model_dump(exclude_unset=True).items():
                setattr(db_categoria, key, value)
            self.db.commit()
            self.db.refresh(db_categoria)
        return db_categoria

    def delete(self, categoria_id: UUID) -> bool:
        db_categoria = self.get_by_id(categoria_id)
        if db_categoria:
            self.db.delete(db_categoria)
            self.db.commit()
            return True
        return False


class MarcaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, marca: MarcaCreate) -> Marca:
        db_marca = Marca(nome=marca.nome, descricao=marca.descricao)
        self.db.add(db_marca)
        self.db.commit()
        self.db.refresh(db_marca)
        return db_marca

    def get_by_id(self, marca_id: UUID) -> Optional[Marca]:
        return self.db.query(Marca).filter(Marca.id == marca_id).first()

    def get_by_name(self, nome: str) -> Optional[Marca]:
        return self.db.query(Marca).filter(func.lower(Marca.nome) == func.lower(nome)).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Marca]:
        return self.db.query(Marca).offset(skip).limit(limit).all()

    def update(self, marca_id: UUID, marca: MarcaUpdate) -> Optional[Marca]:
        db_marca = self.get_by_id(marca_id)
        if db_marca:
            for key, value in marca.model_dump(exclude_unset=True).items():
                setattr(db_marca, key, value)
            self.db.commit()
            self.db.refresh(db_marca)
        return db_marca

    def delete(self, marca_id: UUID) -> bool:
        db_marca = self.get_by_id(marca_id)
        if db_marca:
            self.db.delete(db_marca)
            self.db.commit()
            return True
        return False


class ProdutoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, produto: ProdutoCreate) -> Produto:
        db_produto = Produto(**produto.model_dump(exclude_unset=True))
        self.db.add(db_produto)
        self.db.commit()
        self.db.refresh(db_produto)
        return db_produto

    def get_by_id(self, produto_id: UUID) -> Optional[Produto]:
        return self.db.query(Produto).options(joinedload(Produto.categoria), joinedload(Produto.marca)).filter(Produto.id == produto_id).first()

    def get_by_codigo_barras(self, codigo_barras: str) -> Optional[Produto]:
        return self.db.query(Produto).options(joinedload(Produto.categoria), joinedload(Produto.marca)).filter(Produto.codigo_barras == codigo_barras).first()

    def get_by_sku(self, sku: str) -> Optional[Produto]:
        return self.db.query(Produto).options(joinedload(Produto.categoria), joinedload(Produto.marca)).filter(Produto.sku == sku).first()

    def get_all(self, skip: int = 0, limit: int = 100, filters: Optional[ProdutoFilter] = None) -> Tuple[List[Produto], int]:
        query = self.db.query(Produto).options(joinedload(Produto.categoria), joinedload(Produto.marca))

        if filters:
            if filters.nome:
                query = query.filter(Produto.nome.ilike(f"%{filters.nome}%"))
            if filters.codigo_barras:
                query = query.filter(Produto.codigo_barras == filters.codigo_barras)
            if filters.sku:
                query = query.filter(Produto.sku == filters.sku)
            if filters.unidade_medida:
                query = query.filter(Produto.unidade_medida == filters.unidade_medida)
            if filters.categoria_id:
                query = query.filter(Produto.categoria_id == filters.categoria_id)
            if filters.marca_id:
                query = query.filter(Produto.marca_id == filters.marca_id)
            if filters.status:
                query = query.filter(Produto.status == filters.status)
            if filters.min_preco_venda is not None:
                query = query.filter(Produto.preco_venda >= filters.min_preco_venda)
            if filters.max_preco_venda is not None:
                query = query.filter(Produto.preco_venda <= filters.max_preco_venda)
            if filters.min_preco_custo is not None:
                query = query.filter(Produto.preco_custo >= filters.min_preco_custo)
            if filters.max_preco_custo is not None:
                query = query.filter(Produto.preco_custo <= filters.max_preco_custo)

        total = query.count()
        produtos = query.offset(skip).limit(limit).all()
        return produtos, total

    def update(self, produto_id: UUID, produto: ProdutoUpdate) -> Optional[Produto]:
        db_produto = self.get_by_id(produto_id)
        if db_produto:
            update_data = produto.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_produto, key, value)
            self.db.commit()
            self.db.refresh(db_produto)
        return db_produto

    def delete(self, produto_id: UUID) -> bool:
        db_produto = self.get_by_id(produto_id)
        if db_produto:
            self.db.delete(db_produto)
            self.db.commit()
            return True
        return False

    def soft_delete(self, produto_id: UUID, atualizado_por: Optional[str] = None) -> Optional[Produto]:
        db_produto = self.get_by_id(produto_id)
        if db_produto:
            db_produto.status = StatusProduto.INATIVO
            db_produto.atualizado_por = atualizado_por
            self.db.commit()
            self.db.refresh(db_produto)
        return db_produto

    def search(self, termo: str, limit: int = 10) -> List[Produto]:
        search_term = f"%{termo.lower()}%"
        return (
            self.db.query(Produto)
            .options(joinedload(Produto.categoria), joinedload(Produto.marca))
            .filter(
                or_(
                    func.lower(Produto.nome).like(search_term),
                    func.lower(Produto.descricao).like(search_term),
                    func.lower(Produto.codigo_barras).like(search_term),
                    func.lower(Produto.sku).like(search_term)
                )
            )
            .limit(limit)
            .all()
        )

    def get_stats(self):
        total_produtos = self.db.query(Produto).count()

        # Produtos por status
        por_status = self.db.query(
            Produto.status, func.count(Produto.id)
        ).group_by(Produto.status).all()
        stats_por_status = {status.value: count for status, count in por_status}

        # Produtos por categoria
        por_categoria = self.db.query(
            Categoria.nome, func.count(Produto.id)
        ).join(Produto.categoria).group_by(Categoria.nome).all()
        stats_por_categoria = {nome: count for nome, count in por_categoria}

        # Produtos por marca
        por_marca = self.db.query(
            Marca.nome, func.count(Produto.id)
        ).join(Produto.marca).group_by(Marca.nome).all()
        stats_por_marca = {nome: count for nome, count in por_marca}

        # Valor total de estoque (venda e custo)
        valor_total_estoque_venda = self.db.query(func.sum(Produto.preco_venda)).scalar() or 0
        valor_total_estoque_custo = self.db.query(func.sum(Produto.preco_custo)).scalar() or 0

        return {
            "total_produtos": total_produtos,
            "por_status": stats_por_status,
            "por_categoria": stats_por_categoria,
            "por_marca": stats_por_marca,
            "valor_total_estoque_venda": valor_total_estoque_venda,
            "valor_total_estoque_custo": valor_total_estoque_custo,
        }


