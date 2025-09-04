"""
Aplicação principal do módulo de gestão de clientes.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import os

from app.database import create_tables
from app.routers import clientes, vendas

# Configuração do lifespan da aplicação
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    """
    # Startup: Cria as tabelas do banco de dados
    print("🚀 Iniciando aplicação...")
    create_tables()
    print("✅ Tabelas do banco de dados criadas/verificadas")
    
    yield
    
    # Shutdown
    print("🛑 Encerrando aplicação...")

# Criação da aplicação FastAPI
app = FastAPI(
    title="Sistema de Gestão de Lojas - Módulo PDV",
    description="""
    API para gestão de vendas (PDV) do Sistema de Gestão de Lojas.
    
    ## Funcionalidades
    
    * **Clientes**: CRUD completo para gestão de clientes
    * **Vendas**: Sistema completo de PDV (Ponto de Venda)
    * **Itens de Venda**: Gestão de produtos vendidos
    * **Pagamentos**: Múltiplas formas de pagamento
    * **Relatórios**: Resumos e históricos de vendas
    
    ## Módulo PDV
    
    * **Registro de Vendas**: Interface completa para registro de transações
    * **Formas de Pagamento**: Dinheiro, cartão, PIX, vale-presente, crediário
    * **Pagamento Misto**: Suporte a múltiplas formas de pagamento
    * **Histórico**: Consulta e filtros avançados de vendas
    
    ## Status da Venda
    
    * **Pendente**: Venda em andamento
    * **Concluída**: Venda finalizada com sucesso
    * **Cancelada**: Venda cancelada
    * **Estornada**: Venda estornada
    """,
    version="1.0.0",
    contact={
        "name": "Sistema de Gestão de Lojas",
        "email": "suporte@gestaolojas.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para tratamento de erros globais
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """
    Middleware para tratamento global de erros.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"Erro não tratado: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Erro interno do servidor",
                "error_code": "INTERNAL_SERVER_ERROR",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        )

# Inclusão dos routers
app.include_router(clientes.router, prefix="/api/v1")
app.include_router(vendas.router)

# Endpoint de health check
@app.get("/", tags=["health"])
async def root():
    """
    Endpoint de health check da aplicação.
    """
    return {
        "message": "Sistema de Gestão de Lojas - Módulo PDV",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """
    Endpoint detalhado de health check.
    """
    return {
        "status": "healthy",
        "service": "pdv-api",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "connected"  # Aqui poderia verificar a conexão real
    }

# Configuração para execução direta
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

