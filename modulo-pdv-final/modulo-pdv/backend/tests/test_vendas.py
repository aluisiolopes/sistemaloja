"""
Testes para o módulo de vendas (PDV).
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime

from app.main import app
from app.database import get_db, Base
from app.models import Venda, ItemVenda, PagamentoVenda, StatusVenda, FormaPagamento

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_pdv.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Criar as tabelas de teste
Base.metadata.create_all(bind=engine)

client = TestClient(app)

class TestVendas:
    """Classe de testes para vendas"""

    def setup_method(self):
        """Setup executado antes de cada teste"""
        # Limpar dados de teste
        db = TestingSessionLocal()
        db.query(PagamentoVenda).delete()
        db.query(ItemVenda).delete()
        db.query(Venda).delete()
        db.commit()
        db.close()

    def test_criar_venda_simples(self):
        """Testa criação de uma venda simples"""
        venda_data = {
            "itens": [
                {
                    "produto_id": str(uuid.uuid4()),
                    "quantidade": 2,
                    "preco_unitario": 1500,  # R$ 15,00
                    "desconto_item": 0
                }
            ],
            "pagamentos": [
                {
                    "forma_pagamento": "dinheiro",
                    "valor_pago": 3000,  # R$ 30,00
                    "valor_recebido": 3000
                }
            ],
            "desconto_total": 0,
            "cliente_id": None,
            "vendedor_id": None,
            "criado_por": "test_user"
        }

        response = client.post("/api/v1/vendas/", json=venda_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["subtotal"] == 3000
        assert data["total_venda"] == 3000
        assert data["status"] == "concluida"
        assert len(data["itens"]) == 1
        assert len(data["pagamentos"]) == 1

    def test_criar_venda_com_desconto(self):
        """Testa criação de venda com desconto"""
        venda_data = {
            "itens": [
                {
                    "produto_id": str(uuid.uuid4()),
                    "quantidade": 1,
                    "preco_unitario": 5000,  # R$ 50,00
                    "desconto_item": 500  # R$ 5,00 desconto no item
                }
            ],
            "pagamentos": [
                {
                    "forma_pagamento": "cartao_credito",
                    "valor_pago": 3500  # R$ 35,00 (50 - 5 - 10)
                }
            ],
            "desconto_total": 1000,  # R$ 10,00 desconto total
            "criado_por": "test_user"
        }

        response = client.post("/api/v1/vendas/", json=venda_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["subtotal"] == 4500  # 50 - 5 (desconto do item)
        assert data["desconto_total"] == 1000
        assert data["total_venda"] == 3500  # 45 - 10 (desconto total)

    def test_criar_venda_pagamento_misto(self):
        """Testa criação de venda com pagamento misto"""
        venda_data = {
            "itens": [
                {
                    "produto_id": str(uuid.uuid4()),
                    "quantidade": 1,
                    "preco_unitario": 10000,  # R$ 100,00
                    "desconto_item": 0
                }
            ],
            "pagamentos": [
                {
                    "forma_pagamento": "dinheiro",
                    "valor_pago": 5000,  # R$ 50,00
                    "valor_recebido": 5000
                },
                {
                    "forma_pagamento": "cartao_credito",
                    "valor_pago": 5000  # R$ 50,00
                }
            ],
            "desconto_total": 0,
            "criado_por": "test_user"
        }

        response = client.post("/api/v1/vendas/", json=venda_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["total_venda"] == 10000
        assert len(data["pagamentos"]) == 2

    def test_criar_venda_valor_pagamento_incorreto(self):
        """Testa erro quando valor dos pagamentos não corresponde ao total"""
        venda_data = {
            "itens": [
                {
                    "produto_id": str(uuid.uuid4()),
                    "quantidade": 1,
                    "preco_unitario": 5000,
                    "desconto_item": 0
                }
            ],
            "pagamentos": [
                {
                    "forma_pagamento": "dinheiro",
                    "valor_pago": 3000  # Valor menor que o total
                }
            ],
            "desconto_total": 0,
            "criado_por": "test_user"
        }

        response = client.post("/api/v1/vendas/", json=venda_data)
        assert response.status_code == 400
        assert "não corresponde ao total da venda" in response.json()["detail"]

    def test_listar_vendas(self):
        """Testa listagem de vendas"""
        # Primeiro criar uma venda
        venda_data = {
            "itens": [
                {
                    "produto_id": str(uuid.uuid4()),
                    "quantidade": 1,
                    "preco_unitario": 2000,
                    "desconto_item": 0
                }
            ],
            "pagamentos": [
                {
                    "forma_pagamento": "pix",
                    "valor_pago": 2000
                }
            ],
            "desconto_total": 0,
            "criado_por": "test_user"
        }

        create_response = client.post("/api/v1/vendas/", json=venda_data)
        assert create_response.status_code == 201

        # Listar vendas
        response = client.get("/api/v1/vendas/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 1
        assert len(data["vendas"]) >= 1
        assert data["pagina"] == 1
        assert data["por_pagina"] == 20

    def test_buscar_venda_por_id(self):
        """Testa busca de venda por ID"""
        # Criar venda
        venda_data = {
            "itens": [
                {
                    "produto_id": str(uuid.uuid4()),
                    "quantidade": 1,
                    "preco_unitario": 1000,
                    "desconto_item": 0
                }
            ],
            "pagamentos": [
                {
                    "forma_pagamento": "vale_presente",
                    "valor_pago": 1000
                }
            ],
            "desconto_total": 0,
            "criado_por": "test_user"
        }

        create_response = client.post("/api/v1/vendas/", json=venda_data)
        venda_id = create_response.json()["id"]

        # Buscar por ID
        response = client.get(f"/api/v1/vendas/{venda_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == venda_id
        assert data["total_venda"] == 1000

    def test_buscar_venda_inexistente(self):
        """Testa busca de venda que não existe"""
        venda_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/vendas/{venda_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Venda não encontrada"

    def test_atualizar_status_venda(self):
        """Testa atualização do status de uma venda"""
        # Criar venda
        venda_data = {
            "itens": [
                {
                    "produto_id": str(uuid.uuid4()),
                    "quantidade": 1,
                    "preco_unitario": 1500,
                    "desconto_item": 0
                }
            ],
            "pagamentos": [
                {
                    "forma_pagamento": "crediario",
                    "valor_pago": 1500
                }
            ],
            "desconto_total": 0,
            "criado_por": "test_user"
        }

        create_response = client.post("/api/v1/vendas/", json=venda_data)
        venda_id = create_response.json()["id"]

        # Atualizar status
        update_data = {
            "status": "cancelada",
            "atualizado_por": "test_admin"
        }

        response = client.put(f"/api/v1/vendas/{venda_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "cancelada"
        assert data["atualizado_por"] == "test_admin"

    def test_cancelar_venda(self):
        """Testa cancelamento de venda"""
        # Criar venda
        venda_data = {
            "itens": [
                {
                    "produto_id": str(uuid.uuid4()),
                    "quantidade": 1,
                    "preco_unitario": 2500,
                    "desconto_item": 0
                }
            ],
            "pagamentos": [
                {
                    "forma_pagamento": "dinheiro",
                    "valor_pago": 2500,
                    "valor_recebido": 3000
                }
            ],
            "desconto_total": 0,
            "criado_por": "test_user"
        }

        create_response = client.post("/api/v1/vendas/", json=venda_data)
        venda_id = create_response.json()["id"]

        # Cancelar venda
        response = client.delete(f"/api/v1/vendas/{venda_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Venda cancelada com sucesso"

        # Verificar se foi cancelada
        get_response = client.get(f"/api/v1/vendas/{venda_id}")
        assert get_response.json()["status"] == "cancelada"

    def test_resumo_vendas(self):
        """Testa geração de resumo de vendas"""
        # Criar algumas vendas
        for i in range(3):
            venda_data = {
                "itens": [
                    {
                        "produto_id": str(uuid.uuid4()),
                        "quantidade": 1,
                        "preco_unitario": 1000 * (i + 1),
                        "desconto_item": 0
                    }
                ],
                "pagamentos": [
                    {
                        "forma_pagamento": "dinheiro",
                        "valor_pago": 1000 * (i + 1)
                    }
                ],
                "desconto_total": 0,
                "criado_por": "test_user"
            }
            client.post("/api/v1/vendas/", json=venda_data)

        # Buscar resumo
        response = client.get("/api/v1/vendas/resumo/vendas")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_vendas"] == 3
        assert data["valor_total"] == 6000  # 1000 + 2000 + 3000
        assert data["ticket_medio"] == 2000.0

    def test_health_check(self):
        """Testa endpoints de health check"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Sistema de Gestão de Lojas - Módulo PDV" in response.json()["message"]

        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "pdv-api"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

