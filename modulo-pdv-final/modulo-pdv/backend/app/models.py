"""
Modelos SQLAlchemy para o módulo de gestão de clientes.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
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

    # Identificação única
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Dados básicos
    nome = Column(String(255), nullable=False, index=True)
    tipo_cliente = Column(Enum(TipoCliente), nullable=False, default=TipoCliente.PESSOA_FISICA)
    
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
    status = Column(Enum(StatusCliente), nullable=False, default=StatusCliente.ATIVO)
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



# Modelos para o Módulo de Gestão de Vendas (PDV)

class StatusVenda(enum.Enum):
    """Enum para status da venda"""
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"
    ESTORNADA = "estornada"

class FormaPagamento(enum.Enum):
    """Enum para formas de pagamento"""
    DINHEIRO = "dinheiro"
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    VALE_PRESENTE = "vale_presente"
    CREDIARIO = "crediario"

class Venda(Base):
    """
    Modelo para a tabela de vendas.
    
    Representa uma transação de venda no PDV, incluindo informações
    do cliente, vendedor, totais e status da venda.
    """
    __tablename__ = "vendas"

    # Identificação única
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    numero_venda = Column(String(20), unique=True, nullable=False, index=True)
    
    # Relacionamentos
    cliente_id = Column(UUID(as_uuid=True), nullable=True, index=True)  # FK para clientes
    vendedor_id = Column(UUID(as_uuid=True), nullable=True, index=True)  # FK para usuários
    
    # Dados da venda
    subtotal = Column(Integer, nullable=False, default=0)  # Em centavos
    desconto_total = Column(Integer, nullable=False, default=0)  # Em centavos
    total_venda = Column(Integer, nullable=False, default=0)  # Em centavos
    
    # Status e controle
    status = Column(Enum(StatusVenda), nullable=False, default=StatusVenda.PENDENTE)
    observacoes = Column(Text, nullable=True)
    
    # Auditoria
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())
    criado_por = Column(String(100), nullable=True)
    atualizado_por = Column(String(100), nullable=True)

    # Relacionamentos
    itens = relationship("ItemVenda", back_populates="venda")
    pagamentos = relationship("PagamentoVenda", back_populates="venda")

    def __repr__(self):
        return f"<Venda(id={self.id}, numero='{self.numero_venda}', total={self.total_venda})>"

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            "id": str(self.id),
            "numero_venda": self.numero_venda,
            "cliente_id": str(self.cliente_id) if self.cliente_id else None,
            "vendedor_id": str(self.vendedor_id) if self.vendedor_id else None,
            "subtotal": self.subtotal,
            "desconto_total": self.desconto_total,
            "total_venda": self.total_venda,
            "status": self.status.value,
            "observacoes": self.observacoes,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "data_atualizacao": self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            "criado_por": self.criado_por,
            "atualizado_por": self.atualizado_por
        }

class ItemVenda(Base):
    """
    Modelo para a tabela de itens de venda.
    
    Representa cada produto vendido em uma transação,
    incluindo quantidade, preços e descontos aplicados.
    """
    __tablename__ = "itens_venda"

    # Identificação única
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relacionamentos
    venda_id = Column(UUID(as_uuid=True), ForeignKey('vendas.id'), nullable=False, index=True)  # FK para vendas
    produto_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # FK para produtos
    
    # Dados do item
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Integer, nullable=False)  # Em centavos
    desconto_item = Column(Integer, nullable=False, default=0)  # Em centavos
    subtotal_item = Column(Integer, nullable=False)  # Em centavos
    
    # Dados do produto no momento da venda (snapshot)
    nome_produto = Column(String(255), nullable=False)
    codigo_barras = Column(String(50), nullable=True)
    sku = Column(String(50), nullable=True)
    
    # Auditoria
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    venda = relationship("Venda", back_populates="itens")

    def __repr__(self):
        return f"<ItemVenda(id={self.id}, produto='{self.nome_produto}', qtd={self.quantidade})>"

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            "id": str(self.id),
            "venda_id": str(self.venda_id),
            "produto_id": str(self.produto_id),
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "desconto_item": self.desconto_item,
            "subtotal_item": self.subtotal_item,
            "nome_produto": self.nome_produto,
            "codigo_barras": self.codigo_barras,
            "sku": self.sku,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None
        }

class PagamentoVenda(Base):
    """
    Modelo para a tabela de pagamentos de venda.
    
    Representa as formas de pagamento utilizadas em uma venda,
    permitindo pagamentos mistos.
    """
    __tablename__ = "pagamentos_venda"

    # Identificação única
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relacionamentos
    venda_id = Column(UUID(as_uuid=True), ForeignKey('vendas.id'), nullable=False, index=True)  # FK para vendas
    
    # Dados do pagamento
    forma_pagamento = Column(Enum(FormaPagamento), nullable=False)
    valor_pago = Column(Integer, nullable=False)  # Em centavos
    valor_recebido = Column(Integer, nullable=True)  # Em centavos (para dinheiro)
    troco = Column(Integer, nullable=True, default=0)  # Em centavos
    
    # Dados adicionais por forma de pagamento
    numero_transacao = Column(String(100), nullable=True)  # Para cartões/PIX
    numero_autorizacao = Column(String(100), nullable=True)  # Para cartões
    
    # Auditoria
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relacionamentos
    venda = relationship("Venda", back_populates="pagamentos")

    def __repr__(self):
        return f"<PagamentoVenda(id={self.id}, forma='{self.forma_pagamento.value}', valor={self.valor_pago})>"

    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            "id": str(self.id),
            "venda_id": str(self.venda_id),
            "forma_pagamento": self.forma_pagamento.value,
            "valor_pago": self.valor_pago,
            "valor_recebido": self.valor_recebido,
            "troco": self.troco,
            "numero_transacao": self.numero_transacao,
            "numero_autorizacao": self.numero_autorizacao,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None
        }

