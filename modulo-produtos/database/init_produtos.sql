CREATE SCHEMA IF NOT EXISTS produtos;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criação do ENUM para unidade de medida
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'unidademedida') THEN
        CREATE TYPE produtos.unidademedida AS ENUM (
            'unidade', 'kg', 'g', 'm', 'cm', 'mm', 'l', 'ml', 'caixa', 'pacote'
        );
    END IF;
END
$$;

-- Criação do ENUM para status do produto
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statusproduto') THEN
        CREATE TYPE produtos.statusproduto AS ENUM (
            'ativo', 'inativo', 'esgotado', 'promocao'
        );
    END IF;
END
$$;

-- Criação da tabela de categorias
CREATE TABLE IF NOT EXISTS produtos.categorias (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE
);

-- Criação da tabela de marcas
CREATE TABLE IF NOT EXISTS produtos.marcas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE
);

-- Criação da tabela de produtos
CREATE TABLE IF NOT EXISTS produtos.produtos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    codigo_barras VARCHAR(255) UNIQUE,
    sku VARCHAR(255) UNIQUE,
    preco_venda INTEGER NOT NULL DEFAULT 0,
    preco_custo INTEGER NOT NULL DEFAULT 0,
    unidade_medida produtos.unidademedida NOT NULL DEFAULT 'unidade',
    categoria_id UUID REFERENCES produtos.categorias(id) ON DELETE SET NULL,
    marca_id UUID REFERENCES produtos.marcas(id) ON DELETE SET NULL,
    status produtos.statusproduto NOT NULL DEFAULT 'ativo',
    imagem_url VARCHAR(255),
    observacoes TEXT,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_atualizacao TIMESTAMP WITH TIME ZONE,
    criado_por VARCHAR(100),
    atualizado_por VARCHAR(100)
);

-- Índices para a tabela de produtos
CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos.produtos (nome);
CREATE INDEX IF NOT EXISTS idx_produtos_codigo_barras ON produtos.produtos (codigo_barras);
CREATE INDEX IF NOT EXISTS idx_produtos_sku ON produtos.produtos (sku);
CREATE INDEX IF NOT EXISTS idx_produtos_categoria_id ON produtos.produtos (categoria_id);
CREATE INDEX IF NOT EXISTS idx_produtos_marca_id ON produtos.produtos (marca_id);
CREATE INDEX IF NOT EXISTS idx_produtos_status ON produtos.produtos (status);

-- Índices para as tabelas de categorias e marcas
CREATE INDEX IF NOT EXISTS idx_categorias_nome ON produtos.categorias (nome);
CREATE INDEX IF NOT EXISTS idx_marcas_nome ON produtos.marcas (nome);

-- Inserir dados de exemplo (opcional)
INSERT INTO produtos.categorias (nome) VALUES
    ('Eletrônicos'),
    ('Roupas'),
    ('Alimentos'),
    ('Livros')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO produtos.marcas (nome) VALUES
    ('Samsung'),
    ('Apple'),
    ('Nike'),
    ('Nestle'),
    ('Editora XYZ')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO produtos.produtos (nome, descricao, codigo_barras, sku, preco_venda, preco_custo, unidade_medida, categoria_id, marca_id, status, imagem_url, criado_por)
SELECT
    'Smartphone Galaxy S23',
    'Celular de última geração com câmera de alta resolução.',
    '7891234567890',
    'SMART-S23',
    500000,
    350000,
    'unidade',
    (SELECT id FROM produtos.categorias WHERE nome = 'Eletrônicos'),
    (SELECT id FROM produtos.marcas WHERE nome = 'Samsung'),
    'ativo',
    'https://example.com/galaxy-s23.jpg',
    'sistema'
WHERE NOT EXISTS (SELECT 1 FROM produtos.produtos WHERE sku = 'SMART-S23');

INSERT INTO produtos.produtos (nome, descricao, codigo_barras, sku, preco_venda, preco_custo, unidade_medida, categoria_id, marca_id, status, imagem_url, criado_por)
SELECT
    'Camiseta Esportiva Dry-Fit',
    'Camiseta leve e respirável para atividades físicas.',
    '7890987654321',
    'CAMI-DRYFIT-M',
    12000,
    6000,
    'unidade',
    (SELECT id FROM produtos.categorias WHERE nome = 'Roupas'),
    (SELECT id FROM produtos.marcas WHERE nome = 'Nike'),
    'ativo',
    'https://example.com/camiseta-nike.jpg',
    'sistema'
WHERE NOT EXISTS (SELECT 1 FROM produtos.produtos WHERE sku = 'CAMI-DRYFIT-M');

INSERT INTO produtos.produtos (nome, descricao, codigo_barras, sku, preco_venda, preco_custo, unidade_medida, categoria_id, marca_id, status, imagem_url, criado_por)
SELECT
    'Chocolate ao Leite 100g',
    'Delicioso chocolate ao leite, ideal para sobremesas.',
    '7894561237890',
    'CHOC-LEITE-100G',
    800,
    400,
    'unidade',
    (SELECT id FROM produtos.categorias WHERE nome = 'Alimentos'),
    (SELECT id FROM produtos.marcas WHERE nome = 'Nestle'),
    'ativo',
    'https://example.com/chocolate-nestle.jpg',
    'sistema'
WHERE NOT EXISTS (SELECT 1 FROM produtos.produtos WHERE sku = 'CHOC-LEITE-100G');


