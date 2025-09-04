"""
Schemas Pydantic para validação de dados do módulo de clientes.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import re
import uuid

class TipoClienteEnum(str, Enum):
    """Enum para tipos de cliente"""
    PESSOA_FISICA = "pessoa_fisica"
    PESSOA_JURIDICA = "pessoa_juridica"

class StatusClienteEnum(str, Enum):
    """Enum para status do cliente"""
    ATIVO = "ativo"
    INATIVO = "inativo"
    BLOQUEADO = "bloqueado"

class ClienteBase(BaseModel):
    """Schema base para cliente"""
    nome: str = Field(..., min_length=2, max_length=255, description="Nome do cliente")
    tipo_cliente: TipoClienteEnum = Field(default=TipoClienteEnum.PESSOA_FISICA, description="Tipo do cliente")
    cpf_cnpj: Optional[str] = Field(None, max_length=18, description="CPF ou CNPJ do cliente")
    rg_ie: Optional[str] = Field(None, max_length=20, description="RG ou Inscrição Estadual")
    email: Optional[str] = Field(None, max_length=255, description="Email do cliente")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone fixo")
    celular: Optional[str] = Field(None, max_length=20, description="Telefone celular")
    endereco: Optional[str] = Field(None, max_length=255, description="Endereço")
    numero: Optional[str] = Field(None, max_length=10, description="Número do endereço")
    complemento: Optional[str] = Field(None, max_length=100, description="Complemento do endereço")
    bairro: Optional[str] = Field(None, max_length=100, description="Bairro")
    cidade: Optional[str] = Field(None, max_length=100, description="Cidade")
    estado: Optional[str] = Field(None, max_length=2, description="Estado (UF)")
    cep: Optional[str] = Field(None, max_length=10, description="CEP")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")
    profissao: Optional[str] = Field(None, max_length=100, description="Profissão")
    observacoes: Optional[str] = Field(None, description="Observações sobre o cliente")
    status: StatusClienteEnum = Field(default=StatusClienteEnum.ATIVO, description="Status do cliente")
    limite_credito: int = Field(default=0, ge=0, description="Limite de crédito em centavos")
    pontos_fidelidade: int = Field(default=0, ge=0, description="Pontos de fidelidade")

    @validator('cpf_cnpj')
    def validar_cpf_cnpj(cls, v, values):
        """Valida CPF ou CNPJ baseado no tipo de cliente"""
        if v is None:
            return v
        
        # Remove caracteres especiais
        documento = re.sub(r'[^0-9]', '', v)
        
        tipo_cliente = values.get('tipo_cliente')
        
        if tipo_cliente == TipoClienteEnum.PESSOA_FISICA:
            if len(documento) != 11:
                raise ValueError('CPF deve ter 11 dígitos')
            # Aqui poderia adicionar validação de CPF mais rigorosa
        elif tipo_cliente == TipoClienteEnum.PESSOA_JURIDICA:
            if len(documento) != 14:
                raise ValueError('CNPJ deve ter 14 dígitos')
            # Aqui poderia adicionar validação de CNPJ mais rigorosa
        
        return documento

    @validator('email')
    def validar_email(cls, v):
        """Valida formato do email"""
        if v is None:
            return v
        
        # Validação básica de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Email inválido')
        
        return v.lower()

    @validator('cep')
    def validar_cep(cls, v):
        """Valida formato do CEP"""
        if v is None:
            return v
        
        # Remove caracteres especiais
        cep = re.sub(r'[^0-9]', '', v)
        
        if len(cep) != 8:
            raise ValueError('CEP deve ter 8 dígitos')
        
        return cep

    @validator('estado')
    def validar_estado(cls, v):
        """Valida UF do estado"""
        if v is None:
            return v
        
        estados_validos = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
        
        if v.upper() not in estados_validos:
            raise ValueError('Estado inválido')
        
        return v.upper()

class ClienteCreate(ClienteBase):
    """Schema para criação de cliente"""
    criado_por: Optional[str] = Field(None, max_length=100, description="Usuário que criou o registro")

class ClienteUpdate(BaseModel):
    """Schema para atualização de cliente"""
    nome: Optional[str] = Field(None, min_length=2, max_length=255)
    tipo_cliente: Optional[TipoClienteEnum] = None
    cpf_cnpj: Optional[str] = Field(None, max_length=18)
    rg_ie: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    telefone: Optional[str] = Field(None, max_length=20)
    celular: Optional[str] = Field(None, max_length=20)
    endereco: Optional[str] = Field(None, max_length=255)
    numero: Optional[str] = Field(None, max_length=10)
    complemento: Optional[str] = Field(None, max_length=100)
    bairro: Optional[str] = Field(None, max_length=100)
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=2)
    cep: Optional[str] = Field(None, max_length=10)
    data_nascimento: Optional[date] = None
    profissao: Optional[str] = Field(None, max_length=100)
    observacoes: Optional[str] = None
    status: Optional[StatusClienteEnum] = None
    limite_credito: Optional[int] = Field(None, ge=0)
    pontos_fidelidade: Optional[int] = Field(None, ge=0)
    atualizado_por: Optional[str] = Field(None, max_length=100, description="Usuário que atualizou o registro")

class ClienteResponse(ClienteBase):
    """Schema para resposta de cliente"""
    id: uuid.UUID
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    criado_por: Optional[str] = None
    atualizado_por: Optional[str] = None

    class Config:
        from_attributes = True

class ClienteList(BaseModel):
    """Schema para listagem de clientes"""
    clientes: List[ClienteResponse]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int

class ClienteFilter(BaseModel):
    """Schema para filtros de busca de clientes"""
    nome: Optional[str] = Field(None, description="Filtro por nome (busca parcial)")
    tipo_cliente: Optional[TipoClienteEnum] = Field(None, description="Filtro por tipo de cliente")
    status: Optional[StatusClienteEnum] = Field(None, description="Filtro por status")
    cidade: Optional[str] = Field(None, description="Filtro por cidade")
    estado: Optional[str] = Field(None, description="Filtro por estado")
    cpf_cnpj: Optional[str] = Field(None, description="Filtro por CPF/CNPJ")
    email: Optional[str] = Field(None, description="Filtro por email")

class ErrorResponse(BaseModel):
    """Schema para respostas de erro"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class SuccessResponse(BaseModel):
    """Schema para respostas de sucesso"""
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)



# Schemas para o Módulo de Gestão de Vendas (PDV)

class StatusVendaEnum(str, Enum):
    """Enum para status da venda"""
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"
    ESTORNADA = "estornada"

class FormaPagamentoEnum(str, Enum):
    """Enum para formas de pagamento"""
    DINHEIRO = "dinheiro"
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    VALE_PRESENTE = "vale_presente"
    CREDIARIO = "crediario"

class ItemVendaBase(BaseModel):
    """Schema base para item de venda"""
    produto_id: uuid.UUID = Field(..., description="ID do produto")
    quantidade: int = Field(..., gt=0, description="Quantidade do produto")
    preco_unitario: int = Field(..., ge=0, description="Preço unitário em centavos")
    desconto_item: int = Field(default=0, ge=0, description="Desconto do item em centavos")

class ItemVendaCreate(ItemVendaBase):
    """Schema para criação de item de venda"""
    pass

class ItemVendaResponse(ItemVendaBase):
    """Schema para resposta de item de venda"""
    id: uuid.UUID
    venda_id: uuid.UUID
    subtotal_item: int
    nome_produto: str
    codigo_barras: Optional[str] = None
    sku: Optional[str] = None
    data_criacao: datetime

    class Config:
        from_attributes = True

class PagamentoVendaBase(BaseModel):
    """Schema base para pagamento de venda"""
    forma_pagamento: FormaPagamentoEnum = Field(..., description="Forma de pagamento")
    valor_pago: int = Field(..., gt=0, description="Valor pago em centavos")
    valor_recebido: Optional[int] = Field(None, description="Valor recebido em centavos (para dinheiro)")
    numero_transacao: Optional[str] = Field(None, max_length=100, description="Número da transação")
    numero_autorizacao: Optional[str] = Field(None, max_length=100, description="Número de autorização")

class PagamentoVendaCreate(PagamentoVendaBase):
    """Schema para criação de pagamento de venda"""
    pass

class PagamentoVendaResponse(PagamentoVendaBase):
    """Schema para resposta de pagamento de venda"""
    id: uuid.UUID
    venda_id: uuid.UUID
    troco: int
    data_criacao: datetime

    class Config:
        from_attributes = True

class VendaBase(BaseModel):
    """Schema base para venda"""
    cliente_id: Optional[uuid.UUID] = Field(None, description="ID do cliente (opcional)")
    vendedor_id: Optional[uuid.UUID] = Field(None, description="ID do vendedor")
    desconto_total: int = Field(default=0, ge=0, description="Desconto total em centavos")
    observacoes: Optional[str] = Field(None, description="Observações da venda")

class VendaCreate(VendaBase):
    """Schema para criação de venda"""
    itens: List[ItemVendaCreate] = Field(..., min_items=1, description="Itens da venda")
    pagamentos: List[PagamentoVendaCreate] = Field(..., min_items=1, description="Pagamentos da venda")
    criado_por: Optional[str] = Field(None, max_length=100, description="Usuário que criou a venda")

    @validator('pagamentos')
    def validar_pagamentos(cls, v, values):
        """Valida se o total dos pagamentos corresponde ao total da venda"""
        if not v:
            raise ValueError('Pelo menos uma forma de pagamento deve ser informada')
        
        # Aqui poderia adicionar validação mais complexa se necessário
        return v

class VendaUpdate(BaseModel):
    """Schema para atualização de venda"""
    status: Optional[StatusVendaEnum] = None
    observacoes: Optional[str] = None
    atualizado_por: Optional[str] = Field(None, max_length=100, description="Usuário que atualizou a venda")

class VendaResponse(VendaBase):
    """Schema para resposta de venda"""
    id: uuid.UUID
    numero_venda: str
    subtotal: int
    total_venda: int
    status: StatusVendaEnum
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    criado_por: Optional[str] = None
    atualizado_por: Optional[str] = None
    itens: List[ItemVendaResponse] = []
    pagamentos: List[PagamentoVendaResponse] = []

    class Config:
        from_attributes = True

class VendaList(BaseModel):
    """Schema para listagem de vendas"""
    vendas: List[VendaResponse]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int

class VendaFilter(BaseModel):
    """Schema para filtros de busca de vendas"""
    data_inicio: Optional[date] = Field(None, description="Data de início do período")
    data_fim: Optional[date] = Field(None, description="Data de fim do período")
    cliente_id: Optional[uuid.UUID] = Field(None, description="Filtro por cliente")
    vendedor_id: Optional[uuid.UUID] = Field(None, description="Filtro por vendedor")
    status: Optional[StatusVendaEnum] = Field(None, description="Filtro por status")
    numero_venda: Optional[str] = Field(None, description="Filtro por número da venda")

class VendaResumo(BaseModel):
    """Schema para resumo de vendas"""
    total_vendas: int
    valor_total: int
    ticket_medio: float
    vendas_por_status: dict
    vendas_por_forma_pagamento: dict

class ProdutoVenda(BaseModel):
    """Schema simplificado de produto para o PDV"""
    id: uuid.UUID
    nome: str
    codigo_barras: Optional[str] = None
    sku: Optional[str] = None
    preco_venda: int
    estoque_atual: int

    class Config:
        from_attributes = True

