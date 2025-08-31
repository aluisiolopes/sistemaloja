-- Script de inicialização do banco de dados para o módulo de clientes
-- Este script será executado automaticamente quando o container PostgreSQL for iniciado

-- Criação da extensão UUID para gerar IDs únicos
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criação do schema para o módulo de clientes
CREATE SCHEMA IF NOT EXISTS clientes;

-- Cria os tipos ENUM manualmente e de forma segura (apenas se não existirem)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipocliente') THEN
        CREATE TYPE clientes.tipocliente AS ENUM ('pessoa_fisica', 'pessoa_juridica');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statuscliente') THEN
        CREATE TYPE clientes.statuscliente AS ENUM ('ativo', 'inativo', 'bloqueado');
    END IF;
END$$;

-- Comentário sobre o schema
COMMENT ON SCHEMA clientes IS 'Schema para o módulo de gestão de clientes do sistema de gestão de lojas';
