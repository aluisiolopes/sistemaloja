"""
Endpoints da API para gestão de clientes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import math

from app.database import get_db
from app.crud import ClienteCRUD
from app.schemas import (
    ClienteCreate, 
    ClienteUpdate, 
    ClienteResponse, 
    ClienteList, 
    ClienteFilter,
    ErrorResponse,
    SuccessResponse,
    TipoClienteEnum,
    StatusClienteEnum
)

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    responses={404: {"model": ErrorResponse}}
)

@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente",
    description="Cria um novo cliente no sistema"
)
async def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo cliente no sistema.
    
    - **nome**: Nome completo do cliente (obrigatório)
    - **tipo_cliente**: Tipo do cliente (pessoa_fisica ou pessoa_juridica)
    - **cpf_cnpj**: CPF (11 dígitos) ou CNPJ (14 dígitos)
    - **email**: Email válido do cliente
    - **telefone**: Telefone de contato
    - **endereco**: Endereço completo
    """
    try:
        crud = ClienteCRUD(db)
        db_cliente = crud.create(cliente)
        return db_cliente
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get(
    "/",
    response_model=ClienteList,
    summary="Listar clientes",
    description="Lista clientes com paginação e filtros"
)
async def listar_clientes(
    pagina: int = Query(1, ge=1, description="Número da página"),
    por_pagina: int = Query(20, ge=1, le=100, description="Itens por página"),
    nome: Optional[str] = Query(None, description="Filtro por nome"),
    tipo_cliente: Optional[TipoClienteEnum] = Query(None, description="Filtro por tipo"),
    status: Optional[StatusClienteEnum] = Query(None, description="Filtro por status"),
    cidade: Optional[str] = Query(None, description="Filtro por cidade"),
    estado: Optional[str] = Query(None, description="Filtro por estado"),
    cpf_cnpj: Optional[str] = Query(None, description="Filtro por CPF/CNPJ"),
    email: Optional[str] = Query(None, description="Filtro por email"),
    db: Session = Depends(get_db)
):
    """
    Lista clientes com paginação e filtros opcionais.
    
    Parâmetros de paginação:
    - **pagina**: Número da página (inicia em 1)
    - **por_pagina**: Número de itens por página (máximo 100)
    
    Filtros disponíveis:
    - **nome**: Busca parcial por nome
    - **tipo_cliente**: pessoa_fisica ou pessoa_juridica
    - **status**: ativo, inativo ou bloqueado
    - **cidade**: Busca parcial por cidade
    - **estado**: UF do estado
    - **cpf_cnpj**: CPF ou CNPJ exato
    - **email**: Busca parcial por email
    """
    try:
        crud = ClienteCRUD(db)
        
        # Cria filtros
        filters = ClienteFilter(
            nome=nome,
            tipo_cliente=tipo_cliente,
            status=status,
            cidade=cidade,
            estado=estado,
            cpf_cnpj=cpf_cnpj,
            email=email
        )
        
        # Calcula offset
        skip = (pagina - 1) * por_pagina
        
        # Busca clientes
        clientes, total = crud.get_all(skip=skip, limit=por_pagina, filters=filters)
        
        # Calcula total de páginas
        total_paginas = math.ceil(total / por_pagina) if total > 0 else 1
        
        return ClienteList(
            clientes=clientes,
            total=total,
            pagina=pagina,
            por_pagina=por_pagina,
            total_paginas=total_paginas
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Buscar cliente por ID",
    description="Retorna os dados de um cliente específico"
)
async def buscar_cliente(
    cliente_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Busca um cliente específico pelo ID.
    
    - **cliente_id**: ID único do cliente (UUID)
    """
    crud = ClienteCRUD(db)
    cliente = crud.get_by_id(cliente_id)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    return cliente

@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse,
    summary="Atualizar cliente",
    description="Atualiza os dados de um cliente existente"
)
async def atualizar_cliente(
    cliente_id: UUID,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um cliente existente.
    
    - **cliente_id**: ID único do cliente (UUID)
    - Apenas os campos fornecidos serão atualizados
    """
    try:
        crud = ClienteCRUD(db)
        cliente = crud.update(cliente_id, cliente_update)
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        
        return cliente
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete(
    "/{cliente_id}",
    response_model=SuccessResponse,
    summary="Remover cliente",
    description="Remove um cliente do sistema"
)
async def remover_cliente(
    cliente_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Remove um cliente do sistema.
    
    - **cliente_id**: ID único do cliente (UUID)
    
    **Atenção**: Esta operação é irreversível!
    """
    crud = ClienteCRUD(db)
    sucesso = crud.delete(cliente_id)
    
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    return SuccessResponse(message="Cliente removido com sucesso")

@router.patch(
    "/{cliente_id}/inativar",
    response_model=ClienteResponse,
    summary="Inativar cliente",
    description="Marca um cliente como inativo (soft delete)"
)
async def inativar_cliente(
    cliente_id: UUID,
    usuario: Optional[str] = Query(None, description="Usuário responsável pela operação"),
    db: Session = Depends(get_db)
):
    """
    Marca um cliente como inativo (soft delete).
    
    - **cliente_id**: ID único do cliente (UUID)
    - **usuario**: Usuário responsável pela operação (opcional)
    """
    crud = ClienteCRUD(db)
    cliente = crud.soft_delete(cliente_id, usuario)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    return cliente

@router.get(
    "/buscar/{termo}",
    response_model=List[ClienteResponse],
    summary="Buscar clientes",
    description="Busca clientes por termo (nome, email, CPF/CNPJ)"
)
async def buscar_clientes(
    termo: str,
    limite: int = Query(10, ge=1, le=50, description="Número máximo de resultados"),
    db: Session = Depends(get_db)
):
    """
    Busca clientes por termo de pesquisa.
    
    - **termo**: Termo para busca (nome, email ou CPF/CNPJ)
    - **limite**: Número máximo de resultados (máximo 50)
    
    A busca é feita nos campos: nome, email e CPF/CNPJ
    """
    crud = ClienteCRUD(db)
    clientes = crud.search(termo, limite)
    return clientes

@router.get(
    "/stats/resumo",
    summary="Estatísticas de clientes",
    description="Retorna estatísticas gerais dos clientes"
)
async def estatisticas_clientes(
    db: Session = Depends(get_db)
):
    """
    Retorna estatísticas gerais dos clientes.
    
    Inclui:
    - Total de clientes
    - Distribuição por status (ativo, inativo, bloqueado)
    - Distribuição por tipo (pessoa física, pessoa jurídica)
    """
    crud = ClienteCRUD(db)
    stats = crud.get_stats()
    return stats

@router.get(
    "/cpf-cnpj/{documento}",
    response_model=ClienteResponse,
    summary="Buscar cliente por CPF/CNPJ",
    description="Busca um cliente pelo CPF ou CNPJ"
)
async def buscar_por_cpf_cnpj(
    documento: str,
    db: Session = Depends(get_db)
):
    """
    Busca um cliente pelo CPF ou CNPJ.
    
    - **documento**: CPF (11 dígitos) ou CNPJ (14 dígitos)
    """
    crud = ClienteCRUD(db)
    cliente = crud.get_by_cpf_cnpj(documento)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    return cliente

@router.get(
    "/email/{email}",
    response_model=ClienteResponse,
    summary="Buscar cliente por email",
    description="Busca um cliente pelo email"
)
async def buscar_por_email(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Busca um cliente pelo email.
    
    - **email**: Email do cliente
    """
    crud = ClienteCRUD(db)
    cliente = crud.get_by_email(email)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    
    return cliente

