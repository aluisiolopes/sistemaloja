from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import produtos
from app.database import create_tables

app = FastAPI(
    title="API de Gestão de Produtos",
    description="API para gerenciar produtos, categorias e marcas no sistema de gestão de lojas.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:3000", # Para o frontend React
    "http://localhost:8001", # Para testes locais
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"]
)

# Incluir os routers
app.include_router(produtos.router, prefix="/api/v1", tags=["Produtos"])

@app.on_event("startup")
def on_startup():
    create_tables() # Cria as tabelas no banco de dados ao iniciar a aplicação

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API de Gestão de Produtos!"}


