"""
Router para endpoints de vendas (PDV).
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import uuid

from app.database import get_db
from app.crud_vendas import crud_venda
from app.schemas import (
    VendaCreate, VendaUpdate, VendaResponse, VendaList, VendaFilter,
    VendaResumo, ErrorResponse, SuccessResponse, StatusVendaEnum
)

router = APIRouter(prefix="/api/v1/vendas", tags=["vendas"])

@router.post("/", response_model=VendaResponse, status_code=status.HTTP_201_CREATED)
async def criar_venda(
    venda: VendaCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova venda no PDV.
    
    - **venda**: Dados da venda incluindo itens e pagamentos
    """
    try:
        db_venda = crud_venda.create(db=db, obj_in=venda)
        return db_venda
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/", response_model=VendaList)
async def listar_vendas(
    pagina: int = Query(1, ge=1, description="Número da página"),
    por_pagina: int = Query(20, ge=1, le=100, description="Itens por página"),
    data_inicio: Optional[date] = Query(None, description="Data de início do período"),
    data_fim: Optional[date] = Query(None, description="Data de fim do período"),
    cliente_id: Optional[uuid.UUID] = Query(None, description="ID do cliente"),
    vendedor_id: Optional[uuid.UUID] = Query(None, description="ID do vendedor"),
    status: Optional[StatusVendaEnum] = Query(None, description="Status da venda"),
    numero_venda: Optional[str] = Query(None, description="Número da venda"),
    db: Session = Depends(get_db)
):
    """
    Lista vendas com filtros e paginação.
    
    - **pagina**: Número da página (padrão: 1)
    - **por_pagina**: Itens por página (padrão: 20, máximo: 100)
    - **data_inicio**: Filtro por data de início
    - **data_fim**: Filtro por data de fim
    - **cliente_id**: Filtro por cliente
    - **vendedor_id**: Filtro por vendedor
    - **status**: Filtro por status
    - **numero_venda**: Filtro por número da venda
    """
    skip = (pagina - 1) * por_pagina
    
    filtros = VendaFilter(
        data_inicio=data_inicio,
        data_fim=data_fim,
        cliente_id=cliente_id,
        vendedor_id=vendedor_id,
        status=status,
        numero_venda=numero_venda
    )
    
    vendas, total = crud_venda.get_multi(
        db=db, 
        skip=skip, 
        limit=por_pagina,
        filtros=filtros
    )
    
    total_paginas = (total + por_pagina - 1) // por_pagina
    
    return VendaList(
        vendas=vendas,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        total_paginas=total_paginas
    )

@router.get("/{venda_id}", response_model=VendaResponse)
async def buscar_venda(
    venda_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Busca uma venda específica por ID.
    
    - **venda_id**: ID único da venda
    """
    db_venda = crud_venda.get(db=db, id=venda_id)
    if not db_venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada"
        )
    return db_venda

@router.get("/numero/{numero_venda}", response_model=VendaResponse)
async def buscar_venda_por_numero(
    numero_venda: str,
    db: Session = Depends(get_db)
):
    """
    Busca uma venda específica por número.
    
    - **numero_venda**: Número único da venda
    """
    db_venda = crud_venda.get_by_numero(db=db, numero_venda=numero_venda)
    if not db_venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada"
        )
    return db_venda

@router.put("/{venda_id}", response_model=VendaResponse)
async def atualizar_venda(
    venda_id: uuid.UUID,
    venda: VendaUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma venda existente.
    
    - **venda_id**: ID único da venda
    - **venda**: Dados para atualização
    """
    db_venda = crud_venda.get(db=db, id=venda_id)
    if not db_venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada"
        )
    
    try:
        db_venda = crud_venda.update(db=db, db_obj=db_venda, obj_in=venda)
        return db_venda
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar venda: {str(e)}"
        )

@router.delete("/{venda_id}", response_model=SuccessResponse)
async def cancelar_venda(
    venda_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Cancela uma venda (soft delete).
    
    - **venda_id**: ID único da venda
    """
    db_venda = crud_venda.get(db=db, id=venda_id)
    if not db_venda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada"
        )
    
    try:
        crud_venda.delete(db=db, id=venda_id)
        return SuccessResponse(message="Venda cancelada com sucesso")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cancelar venda: {str(e)}"
        )

@router.get("/resumo/vendas", response_model=VendaResumo)
async def resumo_vendas(
    data_inicio: Optional[date] = Query(None, description="Data de início do período"),
    data_fim: Optional[date] = Query(None, description="Data de fim do período"),
    db: Session = Depends(get_db)
):
    """
    Gera resumo de vendas por período.
    
    - **data_inicio**: Data de início do período
    - **data_fim**: Data de fim do período
    """
    try:
        resumo = crud_venda.get_resumo_vendas(
            db=db,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return VendaResumo(**resumo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar resumo: {str(e)}"
        )

@router.get("/cliente/{cliente_id}/historico", response_model=List[VendaResponse])
async def historico_vendas_cliente(
    cliente_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Busca histórico de vendas de um cliente.
    
    - **cliente_id**: ID único do cliente
    """
    try:
        vendas = crud_venda.buscar_vendas_cliente(db=db, cliente_id=cliente_id)
        return vendas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar histórico: {str(e)}"
        )

@router.get("/vendedor/{vendedor_id}/vendas", response_model=List[VendaResponse])
async def vendas_por_vendedor(
    vendedor_id: uuid.UUID,
    data_inicio: Optional[date] = Query(None, description="Data de início do período"),
    data_fim: Optional[date] = Query(None, description="Data de fim do período"),
    db: Session = Depends(get_db)
):
    """
    Busca vendas de um vendedor por período.
    
    - **vendedor_id**: ID único do vendedor
    - **data_inicio**: Data de início do período
    - **data_fim**: Data de fim do período
    """
    try:
        vendas = crud_venda.buscar_vendas_vendedor(
            db=db,
            vendedor_id=vendedor_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return vendas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar vendas do vendedor: {str(e)}"
        )

