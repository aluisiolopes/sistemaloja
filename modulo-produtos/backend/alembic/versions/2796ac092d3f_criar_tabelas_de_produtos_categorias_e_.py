"""Criar tabelas de produtos, categorias e marcas

Revision ID: 2796ac092d3f
Revises: 
Create Date: 2025-08-29 07:30:03.110340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2796ac092d3f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Criar schema produtos se não existir
    op.execute("CREATE SCHEMA IF NOT EXISTS produtos")
    
    # Criar extensão UUID se não existir
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Criar ENUMs
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'unidademedida') THEN
                CREATE TYPE produtos.unidademedida AS ENUM (
                    'unidade', 'kg', 'g', 'm', 'cm', 'mm', 'l', 'ml', 'caixa', 'pacote'
                );
            END IF;
        END
        $$;
    """)
    
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statusproduto') THEN
                CREATE TYPE produtos.statusproduto AS ENUM (
                    'ativo', 'inativo', 'esgotado', 'promocao'
                );
            END IF;
        END
        $$;
    """)
    
    # Criar tabela de categorias
    op.create_table('categorias',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('data_criacao', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('data_atualizacao', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome'),
        schema='produtos'
    )
    
    # Criar tabela de marcas
    op.create_table('marcas',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('data_criacao', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('data_atualizacao', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome'),
        schema='produtos'
    )
    
    # Criar tabela de produtos
    op.create_table('produtos',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('codigo_barras', sa.String(length=255), nullable=True),
        sa.Column('sku', sa.String(length=255), nullable=True),
        sa.Column('preco_venda', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('preco_custo', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('unidade_medida', postgresql.ENUM('unidade', 'kg', 'g', 'm', 'cm', 'mm', 'l', 'ml', 'caixa', 'pacote', name='unidademedida', schema='produtos'), nullable=False, server_default='unidade'),
        sa.Column('categoria_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('marca_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('status', postgresql.ENUM('ativo', 'inativo', 'esgotado', 'promocao', name='statusproduto', schema='produtos'), nullable=False, server_default='ativo'),
        sa.Column('imagem_url', sa.String(length=255), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('data_criacao', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('data_atualizacao', sa.DateTime(timezone=True), nullable=True),
        sa.Column('criado_por', sa.String(length=100), nullable=True),
        sa.Column('atualizado_por', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['categoria_id'], ['produtos.categorias.id'], ),
        sa.ForeignKeyConstraint(['marca_id'], ['produtos.marcas.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo_barras'),
        sa.UniqueConstraint('sku'),
        schema='produtos'
    )
    
    # Criar índices
    op.create_index('idx_produtos_nome', 'produtos', ['nome'], schema='produtos')
    op.create_index('idx_produtos_codigo_barras', 'produtos', ['codigo_barras'], schema='produtos')
    op.create_index('idx_produtos_sku', 'produtos', ['sku'], schema='produtos')
    op.create_index('idx_produtos_categoria_id', 'produtos', ['categoria_id'], schema='produtos')
    op.create_index('idx_produtos_marca_id', 'produtos', ['marca_id'], schema='produtos')
    op.create_index('idx_produtos_status', 'produtos', ['status'], schema='produtos')
    op.create_index('idx_categorias_nome', 'categorias', ['nome'], schema='produtos')
    op.create_index('idx_marcas_nome', 'marcas', ['nome'], schema='produtos')


def downgrade() -> None:
    """Downgrade schema."""
    # Remover índices
    op.drop_index('idx_marcas_nome', table_name='marcas', schema='produtos')
    op.drop_index('idx_categorias_nome', table_name='categorias', schema='produtos')
    op.drop_index('idx_produtos_status', table_name='produtos', schema='produtos')
    op.drop_index('idx_produtos_marca_id', table_name='produtos', schema='produtos')
    op.drop_index('idx_produtos_categoria_id', table_name='produtos', schema='produtos')
    op.drop_index('idx_produtos_sku', table_name='produtos', schema='produtos')
    op.drop_index('idx_produtos_codigo_barras', table_name='produtos', schema='produtos')
    op.drop_index('idx_produtos_nome', table_name='produtos', schema='produtos')
    
    # Remover tabelas
    op.drop_table('produtos', schema='produtos')
    op.drop_table('marcas', schema='produtos')
    op.drop_table('categorias', schema='produtos')
    
    # Remover ENUMs
    op.execute("DROP TYPE IF EXISTS produtos.statusproduto")
    op.execute("DROP TYPE IF EXISTS produtos.unidademedida")

