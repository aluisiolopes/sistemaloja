-- Script de inicialização do banco de dados para o módulo de clientes
-- Este script será executado automaticamente quando o container PostgreSQL for iniciado

-- Criação da extensão UUID para gerar IDs únicos
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criação do schema para o módulo de clientes
CREATE SCHEMA IF NOT EXISTS clientes;

-- Comentário sobre o schema
COMMENT ON SCHEMA clientes IS 'Schema para o módulo de gestão de clientes do sistema de gestão de lojas';

