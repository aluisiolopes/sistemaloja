"""
Operações CRUD (Create, Read, Update, Delete) para o módulo de clientes.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from uuid import UUID
import uuid

from app.models import Cliente, TipoCliente, StatusCliente
from app.schemas import ClienteCreate, ClienteUpdate, ClienteFilter

class ClienteCRUD:
    """Classe para operações CRUD de clientes"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente_data: ClienteCreate) -> Cliente:
        """
        Cria um novo cliente no banco de dados.
        
        Args:
            cliente_data: Dados do cliente a ser criado
            
        Returns:
            Cliente criado
            
        Raises:
            ValueError: Se CPF/CNPJ já existe
        """
        # Verifica se CPF/CNPJ já existe
        if cliente_data.cpf_cnpj:
            existing = self.get_by_cpf_cnpj(cliente_data.cpf_cnpj)
            if existing:
                raise ValueError(f"Cliente com CPF/CNPJ {cliente_data.cpf_cnpj} já existe")

        # Verifica se email já existe
        if cliente_data.email:
            existing = self.get_by_email(cliente_data.email)
            if existing:
                raise ValueError(f"Cliente com email {cliente_data.email} já existe")

        # Converte enum strings para enums do SQLAlchemy
        cliente_dict = cliente_data.model_dump()
        if cliente_dict.get('tipo_cliente'):
            cliente_dict['tipo_cliente'] = TipoCliente(cliente_dict['tipo_cliente'])
        if cliente_dict.get('status'):
            cliente_dict['status'] = StatusCliente(cliente_dict['status'])

        # Cria o cliente
        db_cliente = Cliente(**cliente_dict)
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        
        return db_cliente

    def get_by_id(self, cliente_id: UUID) -> Optional[Cliente]:
        """
        Busca um cliente pelo ID.
        
        Args:
            cliente_id: ID do cliente
            
        Returns:
            Cliente encontrado ou None
        """
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_by_cpf_cnpj(self, cpf_cnpj: str) -> Optional[Cliente]:
        """
        Busca um cliente pelo CPF/CNPJ.
        
        Args:
            cpf_cnpj: CPF ou CNPJ do cliente
            
        Returns:
            Cliente encontrado ou None
        """
        return self.db.query(Cliente).filter(Cliente.cpf_cnpj == cpf_cnpj).first()

    def get_by_email(self, email: str) -> Optional[Cliente]:
        """
        Busca um cliente pelo email.
        
        Args:
            email: Email do cliente
            
        Returns:
            Cliente encontrado ou None
        """
        return self.db.query(Cliente).filter(Cliente.email == email.lower()).first()

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[ClienteFilter] = None
    ) -> tuple[List[Cliente], int]:
        """
        Lista clientes com paginação e filtros.
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            filters: Filtros de busca
            
        Returns:
            Tupla com (lista de clientes, total de registros)
        """
        query = self.db.query(Cliente)
        
        # Aplica filtros se fornecidos
        if filters:
            if filters.nome:
                query = query.filter(Cliente.nome.ilike(f"%{filters.nome}%"))
            
            if filters.tipo_cliente:
                query = query.filter(Cliente.tipo_cliente == TipoCliente(filters.tipo_cliente))
            
            if filters.status:
                query = query.filter(Cliente.status == StatusCliente(filters.status))
            
            if filters.cidade:
                query = query.filter(Cliente.cidade.ilike(f"%{filters.cidade}%"))
            
            if filters.estado:
                query = query.filter(Cliente.estado == filters.estado.upper())
            
            if filters.cpf_cnpj:
                query = query.filter(Cliente.cpf_cnpj == filters.cpf_cnpj)
            
            if filters.email:
                query = query.filter(Cliente.email.ilike(f"%{filters.email.lower()}%"))

        # Conta total de registros
        total = query.count()
        
        # Aplica paginação e ordena por nome
        clientes = query.order_by(Cliente.nome).offset(skip).limit(limit).all()
        
        return clientes, total

    def update(self, cliente_id: UUID, cliente_data: ClienteUpdate) -> Optional[Cliente]:
        """
        Atualiza um cliente existente.
        
        Args:
            cliente_id: ID do cliente a ser atualizado
            cliente_data: Dados para atualização
            
        Returns:
            Cliente atualizado ou None se não encontrado
            
        Raises:
            ValueError: Se CPF/CNPJ já existe para outro cliente
        """
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return None

        # Dados para atualização (apenas campos não nulos)
        update_data = cliente_data.model_dump(exclude_unset=True)
        
        # Verifica se CPF/CNPJ já existe para outro cliente
        if 'cpf_cnpj' in update_data and update_data['cpf_cnpj']:
            existing = self.get_by_cpf_cnpj(update_data['cpf_cnpj'])
            if existing and existing.id != cliente_id:
                raise ValueError(f"Cliente com CPF/CNPJ {update_data['cpf_cnpj']} já existe")

        # Verifica se email já existe para outro cliente
        if 'email' in update_data and update_data['email']:
            existing = self.get_by_email(update_data['email'])
            if existing and existing.id != cliente_id:
                raise ValueError(f"Cliente com email {update_data['email']} já existe")

        # Converte enum strings para enums do SQLAlchemy
        if 'tipo_cliente' in update_data:
            update_data['tipo_cliente'] = TipoCliente(update_data['tipo_cliente'])
        if 'status' in update_data:
            update_data['status'] = StatusCliente(update_data['status'])

        # Atualiza os campos
        for field, value in update_data.items():
            setattr(db_cliente, field, value)

        self.db.commit()
        self.db.refresh(db_cliente)
        
        return db_cliente

    def delete(self, cliente_id: UUID) -> bool:
        """
        Remove um cliente do banco de dados.
        
        Args:
            cliente_id: ID do cliente a ser removido
            
        Returns:
            True se removido com sucesso, False se não encontrado
        """
        db_cliente = self.get_by_id(cliente_id)
        if not db_cliente:
            return False

        self.db.delete(db_cliente)
        self.db.commit()
        
        return True

    def soft_delete(self, cliente_id: UUID, usuario: str = None) -> Optional[Cliente]:
        """
        Marca um cliente como inativo (soft delete).
        
        Args:
            cliente_id: ID do cliente
            usuario: Usuário que está fazendo a operação
            
        Returns:
            Cliente atualizado ou None se não encontrado
        """
        update_data = ClienteUpdate(
            status=StatusCliente.INATIVO,
            atualizado_por=usuario
        )
        return self.update(cliente_id, update_data)

    def search(self, termo: str, limit: int = 10) -> List[Cliente]:
        """
        Busca clientes por termo (nome, email, CPF/CNPJ).
        
        Args:
            termo: Termo de busca
            limit: Número máximo de resultados
            
        Returns:
            Lista de clientes encontrados
        """
        return self.db.query(Cliente).filter(
            or_(
                Cliente.nome.ilike(f"%{termo}%"),
                Cliente.email.ilike(f"%{termo}%"),
                Cliente.cpf_cnpj.ilike(f"%{termo}%")
            )
        ).order_by(Cliente.nome).limit(limit).all()

    def get_stats(self) -> dict:
        """
        Retorna estatísticas dos clientes.
        
        Returns:
            Dicionário com estatísticas
        """
        total = self.db.query(Cliente).count()
        ativos = self.db.query(Cliente).filter(Cliente.status == StatusCliente.ATIVO).count()
        inativos = self.db.query(Cliente).filter(Cliente.status == StatusCliente.INATIVO).count()
        bloqueados = self.db.query(Cliente).filter(Cliente.status == StatusCliente.BLOQUEADO).count()
        
        pessoa_fisica = self.db.query(Cliente).filter(Cliente.tipo_cliente == TipoCliente.PESSOA_FISICA).count()
        pessoa_juridica = self.db.query(Cliente).filter(Cliente.tipo_cliente == TipoCliente.PESSOA_JURIDICA).count()

        return {
            "total": total,
            "por_status": {
                "ativos": ativos,
                "inativos": inativos,
                "bloqueados": bloqueados
            },
            "por_tipo": {
                "pessoa_fisica": pessoa_fisica,
                "pessoa_juridica": pessoa_juridica
            }
        }

