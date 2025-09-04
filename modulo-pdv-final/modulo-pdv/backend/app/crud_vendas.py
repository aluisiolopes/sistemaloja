"""
Operações CRUD para o módulo de vendas (PDV).
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import uuid

from app.models import Venda, ItemVenda, PagamentoVenda, StatusVenda, FormaPagamento
from app.schemas import (
    VendaCreate, VendaUpdate, VendaFilter, ItemVendaCreate, 
    PagamentoVendaCreate, StatusVendaEnum
)

class CRUDVenda:
    """Classe para operações CRUD de vendas"""

    def __init__(self):
        pass

    def gerar_numero_venda(self, db: Session) -> str:
        """Gera um número único para a venda"""
        # Busca o último número de venda do dia
        hoje = datetime.now().date()
        ultimo_numero = db.query(Venda).filter(
            func.date(Venda.data_criacao) == hoje
        ).count()
        
        # Formato: YYYYMMDD-NNNN
        numero = f"{hoje.strftime('%Y%m%d')}-{(ultimo_numero + 1):04d}"
        return numero

    def create(self, db: Session, obj_in: VendaCreate) -> Venda:
        """Cria uma nova venda com itens e pagamentos"""
        try:
            # Calcula totais
            subtotal = sum(
                item.quantidade * item.preco_unitario - item.desconto_item 
                for item in obj_in.itens
            )
            total_venda = subtotal - obj_in.desconto_total
            
            # Valida se o total dos pagamentos corresponde ao total da venda
            total_pagamentos = sum(pagamento.valor_pago for pagamento in obj_in.pagamentos)
            if total_pagamentos != total_venda:
                raise ValueError(f"Total dos pagamentos ({total_pagamentos}) não corresponde ao total da venda ({total_venda})")

            # Cria a venda
            db_venda = Venda(
                numero_venda=self.gerar_numero_venda(db),
                cliente_id=obj_in.cliente_id,
                vendedor_id=obj_in.vendedor_id,
                subtotal=subtotal,
                desconto_total=obj_in.desconto_total,
                total_venda=total_venda,
                status=StatusVenda.CONCLUIDA,
                observacoes=obj_in.observacoes,
                criado_por=obj_in.criado_por
            )
            
            db.add(db_venda)
            db.flush()  # Para obter o ID da venda

            # Cria os itens da venda
            for item_data in obj_in.itens:
                # Aqui deveria buscar os dados do produto para fazer snapshot
                # Por simplicidade, vamos usar dados básicos
                subtotal_item = item_data.quantidade * item_data.preco_unitario - item_data.desconto_item
                
                db_item = ItemVenda(
                    venda_id=db_venda.id,
                    produto_id=item_data.produto_id,
                    quantidade=item_data.quantidade,
                    preco_unitario=item_data.preco_unitario,
                    desconto_item=item_data.desconto_item,
                    subtotal_item=subtotal_item,
                    nome_produto=f"Produto {item_data.produto_id}",  # Deveria vir do banco
                    codigo_barras=None,  # Deveria vir do banco
                    sku=None  # Deveria vir do banco
                )
                db.add(db_item)

            # Cria os pagamentos da venda
            for pagamento_data in obj_in.pagamentos:
                troco = 0
                if (pagamento_data.forma_pagamento == FormaPagamento.DINHEIRO and 
                    pagamento_data.valor_recebido):
                    troco = pagamento_data.valor_recebido - pagamento_data.valor_pago

                db_pagamento = PagamentoVenda(
                    venda_id=db_venda.id,
                    forma_pagamento=pagamento_data.forma_pagamento,
                    valor_pago=pagamento_data.valor_pago,
                    valor_recebido=pagamento_data.valor_recebido,
                    troco=troco,
                    numero_transacao=pagamento_data.numero_transacao,
                    numero_autorizacao=pagamento_data.numero_autorizacao
                )
                db.add(db_pagamento)

            db.commit()
            db.refresh(db_venda)
            return db_venda

        except Exception as e:
            db.rollback()
            raise e

    def get(self, db: Session, id: uuid.UUID) -> Optional[Venda]:
        """Busca uma venda por ID"""
        return db.query(Venda).filter(Venda.id == id).first()

    def get_by_numero(self, db: Session, numero_venda: str) -> Optional[Venda]:
        """Busca uma venda por número"""
        return db.query(Venda).filter(Venda.numero_venda == numero_venda).first()

    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filtros: Optional[VendaFilter] = None
    ) -> tuple[List[Venda], int]:
        """Lista vendas com filtros e paginação"""
        query = db.query(Venda)

        # Aplica filtros
        if filtros:
            if filtros.data_inicio:
                query = query.filter(func.date(Venda.data_criacao) >= filtros.data_inicio)
            if filtros.data_fim:
                query = query.filter(func.date(Venda.data_criacao) <= filtros.data_fim)
            if filtros.cliente_id:
                query = query.filter(Venda.cliente_id == filtros.cliente_id)
            if filtros.vendedor_id:
                query = query.filter(Venda.vendedor_id == filtros.vendedor_id)
            if filtros.status:
                query = query.filter(Venda.status == StatusVenda(filtros.status.value))
            if filtros.numero_venda:
                query = query.filter(Venda.numero_venda.ilike(f"%{filtros.numero_venda}%"))

        # Conta total de registros
        total = query.count()

        # Aplica ordenação e paginação
        vendas = query.order_by(desc(Venda.data_criacao)).offset(skip).limit(limit).all()

        return vendas, total

    def update(self, db: Session, db_obj: Venda, obj_in: VendaUpdate) -> Venda:
        """Atualiza uma venda"""
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "status" and value:
                setattr(db_obj, field, StatusVenda(value.value))
            else:
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: uuid.UUID) -> Optional[Venda]:
        """Remove uma venda (soft delete - muda status para cancelada)"""
        db_obj = self.get(db, id)
        if db_obj:
            db_obj.status = StatusVenda.CANCELADA
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def get_resumo_vendas(
        self, 
        db: Session, 
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None
    ) -> Dict[str, Any]:
        """Gera resumo de vendas por período"""
        query = db.query(Venda).filter(Venda.status == StatusVenda.CONCLUIDA)

        if data_inicio:
            query = query.filter(func.date(Venda.data_criacao) >= data_inicio)
        if data_fim:
            query = query.filter(func.date(Venda.data_criacao) <= data_fim)

        vendas = query.all()
        
        if not vendas:
            return {
                "total_vendas": 0,
                "valor_total": 0,
                "ticket_medio": 0.0,
                "vendas_por_status": {},
                "vendas_por_forma_pagamento": {}
            }

        total_vendas = len(vendas)
        valor_total = sum(venda.total_venda for venda in vendas)
        ticket_medio = valor_total / total_vendas if total_vendas > 0 else 0

        # Vendas por status
        vendas_por_status = {}
        for status in StatusVenda:
            count = len([v for v in vendas if v.status == status])
            if count > 0:
                vendas_por_status[status.value] = count

        # Vendas por forma de pagamento (seria necessário fazer join com pagamentos)
        vendas_por_forma_pagamento = {}

        return {
            "total_vendas": total_vendas,
            "valor_total": valor_total,
            "ticket_medio": ticket_medio,
            "vendas_por_status": vendas_por_status,
            "vendas_por_forma_pagamento": vendas_por_forma_pagamento
        }

    def buscar_vendas_cliente(self, db: Session, cliente_id: uuid.UUID) -> List[Venda]:
        """Busca todas as vendas de um cliente"""
        return db.query(Venda).filter(
            and_(
                Venda.cliente_id == cliente_id,
                Venda.status == StatusVenda.CONCLUIDA
            )
        ).order_by(desc(Venda.data_criacao)).all()

    def buscar_vendas_vendedor(
        self, 
        db: Session, 
        vendedor_id: uuid.UUID,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None
    ) -> List[Venda]:
        """Busca vendas de um vendedor por período"""
        query = db.query(Venda).filter(
            and_(
                Venda.vendedor_id == vendedor_id,
                Venda.status == StatusVenda.CONCLUIDA
            )
        )

        if data_inicio:
            query = query.filter(func.date(Venda.data_criacao) >= data_inicio)
        if data_fim:
            query = query.filter(func.date(Venda.data_criacao) <= data_fim)

        return query.order_by(desc(Venda.data_criacao)).all()

# Instância global do CRUD
crud_venda = CRUDVenda()

