"""Criar tabela de clientes

Revision ID: c19e371d017c
Revises: 
Create Date: 2025-08-23 02:44:41.301414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c19e371d017c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Criar schema clientes se não existir (mantido por segurança)
    op.execute("CREATE SCHEMA IF NOT EXISTS clientes")
    
    # Criar extensão UUID se não existir (mantido por segurança)
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Define os tipos ENUM para o SQLAlchemy, mas não os cria no banco
    # A criação agora é responsabilidade do init.sql
    tipo_cliente_enum = postgresql.ENUM('pessoa_fisica', 'pessoa_juridica', name='tipocliente', schema='clientes')
    # tipo_cliente_enum.create(op.get_bind()) # <-- GARANTIR QUE ESTA LINHA ESTÁ COMENTADA

    status_cliente_enum = postgresql.ENUM('ativo', 'inativo', 'bloqueado', name='statuscliente', schema='clientes')
    # status_cliente_enum.create(op.get_bind()) # <-- GARANTIR QUE ESTA LINHA ESTÁ COMENTADA
    
    # Criar tabela de clientes
    op.create_table(
        'clientes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('nome', sa.String(255), nullable=False, index=True),
        sa.Column('tipo_cliente', tipo_cliente_enum, nullable=False, server_default='pessoa_fisica'),
        sa.Column('cpf_cnpj', sa.String(18), nullable=True, unique=True, index=True),
        sa.Column('rg_ie', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True, index=True),
        sa.Column('telefone', sa.String(20), nullable=True),
        sa.Column('celular', sa.String(20), nullable=True),
        sa.Column('endereco', sa.String(255), nullable=True),
        sa.Column('numero', sa.String(10), nullable=True),
        sa.Column('complemento', sa.String(100), nullable=True),
        sa.Column('bairro', sa.String(100), nullable=True),
        sa.Column('cidade', sa.String(100), nullable=True),
        sa.Column('estado', sa.String(2), nullable=True),
        sa.Column('cep', sa.String(10), nullable=True),
        sa.Column('data_nascimento', sa.Date, nullable=True),
        sa.Column('profissao', sa.String(100), nullable=True),
        sa.Column('observacoes', sa.Text, nullable=True),
        sa.Column('status', status_cliente_enum, nullable=False, server_default='ativo'),
        sa.Column('limite_credito', sa.Integer, nullable=False, server_default='0'),
        sa.Column('pontos_fidelidade', sa.Integer, nullable=False, server_default='0'),
        sa.Column('data_criacao', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('data_atualizacao', sa.DateTime(timezone=True), nullable=True),
        sa.Column('criado_por', sa.String(100), nullable=True),
        sa.Column('atualizado_por', sa.String(100), nullable=True),
        schema='clientes'
    )
    
    # Criar índices adicionais
    op.create_index('idx_clientes_nome', 'clientes', ['nome'], schema='clientes')
    op.create_index('idx_clientes_cpf_cnpj', 'clientes', ['cpf_cnpj'], schema='clientes')
    op.create_index('idx_clientes_email', 'clientes', ['email'], schema='clientes')
    op.create_index('idx_clientes_status', 'clientes', ['status'], schema='clientes')
    op.create_index('idx_clientes_tipo', 'clientes', ['tipo_cliente'], schema='clientes')
    op.create_index('idx_clientes_cidade_estado', 'clientes', ['cidade', 'estado'], schema='clientes')

def downgrade() -> None:
    """Downgrade schema."""
    # Remover tabela
    op.drop_table('clientes', schema='clientes')
    
    # Remover enums
    op.execute('DROP TYPE IF EXISTS clientes.statuscliente')
    op.execute('DROP TYPE IF EXISTS clientes.tipocliente')
    
    # Remover schema (apenas se estiver vazio)
    op.execute('DROP SCHEMA IF EXISTS clientes')

