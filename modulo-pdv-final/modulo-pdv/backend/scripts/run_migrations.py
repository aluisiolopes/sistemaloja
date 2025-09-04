#!/usr/bin/env python3
"""
Script para executar migrações do banco de dados.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Executa um comando e trata erros."""
    print(f"🔧 {description}...")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {description} concluído com sucesso!")
        if result.stdout:
            print(f"📄 Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}: {e}")
        if e.stdout:
            print(f"📄 Output: {e.stdout}")
        if e.stderr:
            print(f"🚨 Error: {e.stderr}")
        return False

def check_alembic_setup():
    """Verifica se o Alembic está configurado."""
    alembic_ini = Path("alembic.ini")
    alembic_dir = Path("alembic")
    
    if not alembic_ini.exists():
        print("❌ Arquivo alembic.ini não encontrado!")
        return False
    
    if not alembic_dir.exists():
        print("❌ Diretório alembic não encontrado!")
        return False
    
    print("✅ Configuração do Alembic encontrada!")
    return True

def show_migration_status():
    """Mostra o status atual das migrações."""
    print("📊 Verificando status das migrações...")
    run_command("alembic current", "Verificação do status atual")
    run_command("alembic history --verbose", "Histórico de migrações")

def upgrade_database():
    """Executa upgrade do banco de dados."""
    return run_command("alembic upgrade head", "Upgrade do banco de dados")

def downgrade_database(revision="base"):
    """Executa downgrade do banco de dados."""
    return run_command(f"alembic downgrade {revision}", f"Downgrade para {revision}")

def create_migration(message):
    """Cria uma nova migração."""
    return run_command(f'alembic revision --autogenerate -m "{message}"', f"Criação de migração: {message}")

def main():
    """Função principal."""
    print("🚀 Script de Migrações do Banco de Dados")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not check_alembic_setup():
        print("💡 Certifique-se de estar no diretório backend do projeto!")
        sys.exit(1)
    
    while True:
        print("\n📋 Opções disponíveis:")
        print("1. Mostrar status das migrações")
        print("2. Executar upgrade (aplicar migrações)")
        print("3. Executar downgrade")
        print("4. Criar nova migração")
        print("5. Sair")
        
        escolha = input("\n🔍 Escolha uma opção (1-5): ").strip()
        
        if escolha == "1":
            show_migration_status()
        
        elif escolha == "2":
            if upgrade_database():
                print("🎉 Banco de dados atualizado com sucesso!")
            else:
                print("💥 Falha ao atualizar banco de dados!")
        
        elif escolha == "3":
            revision = input("📝 Digite a revisão de destino (ou 'base' para reverter tudo): ").strip()
            if not revision:
                revision = "base"
            
            confirmacao = input(f"⚠️  Tem certeza que deseja fazer downgrade para '{revision}'? (s/N): ").lower()
            if confirmacao in ['s', 'sim', 'y', 'yes']:
                if downgrade_database(revision):
                    print("🎉 Downgrade executado com sucesso!")
                else:
                    print("💥 Falha ao executar downgrade!")
            else:
                print("❌ Downgrade cancelado.")
        
        elif escolha == "4":
            message = input("📝 Digite a mensagem da migração: ").strip()
            if message:
                if create_migration(message):
                    print("🎉 Migração criada com sucesso!")
                    print("💡 Lembre-se de revisar o arquivo gerado antes de aplicar!")
                else:
                    print("💥 Falha ao criar migração!")
            else:
                print("❌ Mensagem não pode estar vazia!")
        
        elif escolha == "5":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()

