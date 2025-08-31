#!/usr/bin/env python3
"""
Script para gerenciar migrações do banco de dados do módulo de produtos.
"""

import os
import sys
import subprocess
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

def run_command(command, description):
    """Executa um comando e retorna o resultado."""
    print(f"\n{description}...")
    print(f"Executando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0:
            print("✅ Sucesso!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Erro!")
            if result.stderr:
                print(f"Erro: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Exceção ao executar comando: {e}")
        return False

def show_migration_status():
    """Mostra o status atual das migrações."""
    return run_command("alembic current", "Verificando status atual das migrações")

def show_migration_history():
    """Mostra o histórico de migrações."""
    return run_command("alembic history --verbose", "Mostrando histórico de migrações")

def upgrade_to_head():
    """Executa todas as migrações pendentes."""
    return run_command("alembic upgrade head", "Executando migrações pendentes")

def downgrade_one_step():
    """Desfaz a última migração."""
    return run_command("alembic downgrade -1", "Desfazendo última migração")

def create_new_migration():
    """Cria uma nova migração baseada nas mudanças nos modelos."""
    message = input("Digite uma mensagem para a migração: ").strip()
    if not message:
        print("Mensagem é obrigatória!")
        return False
    
    return run_command(f'alembic revision --autogenerate -m "{message}"', "Criando nova migração")

def create_empty_migration():
    """Cria uma migração vazia."""
    message = input("Digite uma mensagem para a migração vazia: ").strip()
    if not message:
        print("Mensagem é obrigatória!")
        return False
    
    return run_command(f'alembic revision -m "{message}"', "Criando migração vazia")

def show_menu():
    """Mostra o menu de opções."""
    print("\n" + "="*60)
    print("🗄️  GERENCIADOR DE MIGRAÇÕES - MÓDULO DE PRODUTOS")
    print("="*60)
    print("1. 📊 Mostrar status atual das migrações")
    print("2. 📜 Mostrar histórico de migrações")
    print("3. ⬆️  Executar migrações pendentes (upgrade)")
    print("4. ⬇️  Desfazer última migração (downgrade)")
    print("5. 🆕 Criar nova migração (autogenerate)")
    print("6. 📝 Criar migração vazia")
    print("7. ❌ Sair")
    print("="*60)

def main():
    """Função principal do script."""
    print("Bem-vindo ao Gerenciador de Migrações!")
    
    # Verificar se estamos no diretório correto
    backend_dir = Path(__file__).parent.parent
    if not (backend_dir / "alembic.ini").exists():
        print("❌ Erro: Arquivo alembic.ini não encontrado!")
        print("Certifique-se de estar executando este script do diretório backend.")
        return False
    
    while True:
        show_menu()
        
        try:
            choice = input("\nEscolha uma opção (1-7): ").strip()
            
            if choice == "1":
                show_migration_status()
            elif choice == "2":
                show_migration_history()
            elif choice == "3":
                upgrade_to_head()
            elif choice == "4":
                confirm = input("⚠️  Tem certeza que deseja desfazer a última migração? (s/N): ").strip().lower()
                if confirm in ['s', 'sim', 'y', 'yes']:
                    downgrade_one_step()
                else:
                    print("Operação cancelada.")
            elif choice == "5":
                create_new_migration()
            elif choice == "6":
                create_empty_migration()
            elif choice == "7":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida! Escolha um número de 1 a 7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

