#!/usr/bin/env python3
"""
Script para executar testes do módulo de produtos.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Executa um comando e retorna o resultado."""
    print(f"\n{description}...")
    print(f"Executando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, cwd=Path(__file__).parent.parent)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exceção ao executar comando: {e}")
        return False

def run_all_tests():
    """Executa todos os testes."""
    return run_command("python -m pytest tests/ -v", "Executando todos os testes")

def run_model_tests():
    """Executa apenas os testes de modelos."""
    return run_command("python -m pytest tests/test_models.py -v", "Executando testes de modelos")

def run_crud_tests():
    """Executa apenas os testes de CRUD."""
    return run_command("python -m pytest tests/test_crud.py -v", "Executando testes de CRUD")

def run_api_tests():
    """Executa apenas os testes de API."""
    return run_command("python -m pytest tests/test_api.py -v", "Executando testes de API")

def run_tests_with_coverage():
    """Executa testes com cobertura de código."""
    # Instalar coverage se não estiver instalado
    subprocess.run("pip install coverage", shell=True, capture_output=True)
    
    success = run_command("coverage run -m pytest tests/", "Executando testes com cobertura")
    if success:
        run_command("coverage report", "Gerando relatório de cobertura")
        run_command("coverage html", "Gerando relatório HTML de cobertura")
        print("\n📊 Relatório HTML de cobertura gerado em: htmlcov/index.html")
    
    return success

def show_menu():
    """Mostra o menu de opções."""
    print("\n" + "="*60)
    print("🧪 EXECUTOR DE TESTES - MÓDULO DE PRODUTOS")
    print("="*60)
    print("1. 🚀 Executar todos os testes")
    print("2. 🏗️  Executar testes de modelos")
    print("3. 📊 Executar testes de CRUD")
    print("4. 🌐 Executar testes de API")
    print("5. 📈 Executar testes com cobertura de código")
    print("6. ❌ Sair")
    print("="*60)

def main():
    """Função principal do script."""
    print("Bem-vindo ao Executor de Testes!")
    
    # Verificar se estamos no diretório correto
    backend_dir = Path(__file__).parent.parent
    if not (backend_dir / "app").exists():
        print("❌ Erro: Diretório 'app' não encontrado!")
        print("Certifique-se de estar executando este script do diretório backend.")
        return False
    
    while True:
        show_menu()
        
        try:
            choice = input("\nEscolha uma opção (1-6): ").strip()
            
            if choice == "1":
                success = run_all_tests()
                print("✅ Todos os testes executados com sucesso!" if success else "❌ Alguns testes falharam.")
            elif choice == "2":
                success = run_model_tests()
                print("✅ Testes de modelos executados com sucesso!" if success else "❌ Testes de modelos falharam.")
            elif choice == "3":
                success = run_crud_tests()
                print("✅ Testes de CRUD executados com sucesso!" if success else "❌ Testes de CRUD falharam.")
            elif choice == "4":
                success = run_api_tests()
                print("✅ Testes de API executados com sucesso!" if success else "❌ Testes de API falharam.")
            elif choice == "5":
                success = run_tests_with_coverage()
                print("✅ Testes com cobertura executados com sucesso!" if success else "❌ Testes com cobertura falharam.")
            elif choice == "6":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida! Escolha um número de 1 a 6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

