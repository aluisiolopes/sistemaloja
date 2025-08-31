"""
Modelos SQLAlchemy para o módulo de gestão de clientes.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid
import enum

class TipoCliente(enum.Enum):
    """Enum para tipos de cliente"""
    PESSOA_FISICA = "pessoa_fisica"
    PESSOA_JURIDICA = "pessoa_juridica"

class StatusCliente(enum.Enum):
    """Enum para status do cliente"""
    ATIVO = "ativo"
    INATIVO = "inativo"
    BLOQUEADO = "bloqueado"

class Cliente(Base):
    """
    Modelo para a tabela de clientes.
    
    Representa um cliente do sistema, podendo ser pessoa física ou jurídica.
    Inclui informações de contato, endereço e dados para fidelidade.
    """
    __tablename__ = "clientes"
    __table_args__ = {"schema": "clientes"}

    # Identificação única
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Dados básicos
    nome = Column(String(255), nullable=False, index=True)
    
    # --- INÍCIO DA CORREÇÃO ---
    tipo_cliente = Column(
        Enum(TipoCliente, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=TipoCliente.PESSOA_FISICA.value
    )
    # --- FIM DA CORREÇÃO ---

    # Documentos
    cpf_cnpj = Column(String(18), unique=True, nullable=True, index=True)
    rg_ie = Column(String(20), nullable=True)
    
    # Dados de contato
    email = Column(String(255), nullable=True, index=True)
    telefone = Column(String(20), nullable=True)
    celular = Column(String(20), nullable=True)
    
    # Endereço
    endereco = Column(String(255), nullable=True)
    numero = Column(String(10), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    cep = Column(String(10), nullable=True)
    
    # Dados adicionais
    data_nascimento = Column(Date, nullable=True)
    profissao = Column(String(100), nullable=True)
    observacoes = Column(Text, nullable=True)
    
    # Status e controle
    # --- INÍCIO DA CORREÇÃO ---
    status = Column(
        Enum(StatusCliente, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=StatusCliente.ATIVO.value
    )
    # --- FIM DA CORREÇÃO ---
    
    limite_credito = Column(Integer, default=0)  # Em centavos
    pontos_fidelidade = Column(Integer, default=0)
    
    # Auditoria
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    criado_por = Column(String(100), nullable=True)
    atualizado_por = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', tipo='{self.tipo_cliente.value}')>"

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            "id": str(self.id),
            "nome": self.nome,
            "tipo_cliente": self.tipo_cliente.value,
            "cpf_cnpj": self.cpf_cnpj,
            "rg_ie": self.rg_ie,
            "email": self.email,
            "telefone": self.telefone,
            "celular": self.celular,
            "endereco": self.endereco,
            "numero": self.numero,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "estado": self.estado,
            "cep": self.cep,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "profissao": self.profissao,
            "observacoes": self.observacoes,
            "status": self.status.value,
            "limite_credito": self.limite_credito,
            "pontos_fidelidade": self.pontos_fidelidade,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            "criado_por": self.criado_por,
            "atualizado_por": self.atualizado_por
        }
