import traceback
from app.database import SessionLocal
from app.crud import ClienteCRUD
from app.schemas import ClienteCreate

def test_create_cliente():
    print("--- Iniciando teste de criação de cliente ---")
    db = None
    try:
        # Pega uma sessão do banco de dados
        db = SessionLocal()
        print("Sessão do banco obtida com sucesso.")

        # Cria um objeto com os dados do cliente
        cliente_data = ClienteCreate(
            nome="Cliente de Teste Debug",
            tipo_cliente="pessoa_fisica",
            cpf_cnpj="11122233344",
            email="debug@teste.com",
            status="ativo"
        )
        print("Dados do cliente para criação:", cliente_data.model_dump())

        # Instancia o CRUD
        crud = ClienteCRUD(db)
        print("Instância do CRUD criada.")

        # Tenta criar o cliente
        print("Tentando executar crud.create(cliente_data)...")
        novo_cliente = crud.create(cliente_data)

        print("\n--- SUCESSO! ---")
        print("Cliente criado com sucesso:", novo_cliente.to_dict())

    except Exception as e:
        print("\n--- FALHA! OCORREU UM ERRO: ---")
        traceback.print_exc() # Imprime o erro detalhado

    finally:
        if db:
            db.close()
            print("Sessão do banco fechada.")

if __name__ == "__main__":
    test_create_cliente()
