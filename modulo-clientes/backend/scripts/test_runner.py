#!/usr/bin/env python3
"""
Script para executar testes do módulo de clientes.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_tests_with_sqlite():
    """Executa os testes usando SQLite em memória."""
    print("🧪 Executando testes com SQLite em memória...")
    
    # Define variável de ambiente para usar SQLite nos testes
    env = os.environ.copy()
    env['TESTING'] = 'true'
    env['DATABASE_URL'] = 'sqlite:///./test.db'
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=short'],
            env=env,
            check=True,
            capture_output=False
        )
        print("✅ Todos os testes passaram!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Alguns testes falharam. Código de saída: {e.returncode}")
        return False

def run_specific_test(test_file):
    """Executa um arquivo de teste específico."""
    print(f"🧪 Executando testes do arquivo: {test_file}")
    
    env = os.environ.copy()
    env['TESTING'] = 'true'
    env['DATABASE_URL'] = 'sqlite:///./test.db'
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', f'tests/{test_file}', '-v'],
            env=env,
            check=True,
            capture_output=False
        )
        print(f"✅ Testes do arquivo {test_file} passaram!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Testes do arquivo {test_file} falharam. Código de saída: {e.returncode}")
        return False

def run_coverage():
    """Executa testes com cobertura de código."""
    print("📊 Executando testes com análise de cobertura...")
    
    # Instala coverage se não estiver instalado
    try:
        import coverage
    except ImportError:
        print("📦 Instalando coverage...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'coverage'], check=True)
    
    env = os.environ.copy()
    env['TESTING'] = 'true'
    env['DATABASE_URL'] = 'sqlite:///./test.db'
    
    try:
        # Executa testes com coverage
        subprocess.run([
            sys.executable, '-m', 'coverage', 'run', 
            '-m', 'pytest', 'tests/', '-v'
        ], env=env, check=True)
        
        # Gera relatório
        subprocess.run([sys.executable, '-m', 'coverage', 'report'], check=True)
        
        # Gera relatório HTML
        subprocess.run([sys.executable, '-m', 'coverage', 'html'], check=True)
        print("📊 Relatório de cobertura gerado em htmlcov/index.html")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar análise de cobertura: {e.returncode}")
        return False

def validate_code_quality():
    """Valida a qualidade do código."""
    print("🔍 Validando qualidade do código...")
    
    # Lista de verificações
    checks = [
        {
            'name': 'Verificação de sintaxe Python',
            'command': [sys.executable, '-m', 'py_compile'] + 
                      [str(f) for f in Path('app').rglob('*.py')],
            'required': True
        }
    ]
    
    # Verifica se flake8 está disponível
    try:
        subprocess.run([sys.executable, '-m', 'flake8', '--version'], 
                      capture_output=True, check=True)
        checks.append({
            'name': 'Análise de estilo (flake8)',
            'command': [sys.executable, '-m', 'flake8', 'app/', '--max-line-length=100'],
            'required': False
        })
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ℹ️  flake8 não encontrado, pulando análise de estilo")
    
    all_passed = True
    for check in checks:
        print(f"🔧 {check['name']}...")
        try:
            result = subprocess.run(
                check['command'], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print(f"✅ {check['name']} passou!")
        except subprocess.CalledProcessError as e:
            print(f"❌ {check['name']} falhou!")
            if e.stdout:
                print(f"Output: {e.stdout}")
            if e.stderr:
                print(f"Error: {e.stderr}")
            
            if check['required']:
                all_passed = False
    
    return all_passed

def main():
    """Função principal."""
    print("🚀 Script de Testes do Módulo de Clientes")
    print("=" * 50)
    
    while True:
        print("\n📋 Opções disponíveis:")
        print("1. Executar todos os testes")
        print("2. Executar teste específico")
        print("3. Executar testes com cobertura")
        print("4. Validar qualidade do código")
        print("5. Executar validação completa")
        print("6. Sair")
        
        escolha = input("\n🔍 Escolha uma opção (1-6): ").strip()
        
        if escolha == "1":
            run_tests_with_sqlite()
        
        elif escolha == "2":
            print("\nArquivos de teste disponíveis:")
            test_files = list(Path('tests').glob('test_*.py'))
            for i, test_file in enumerate(test_files, 1):
                print(f"{i}. {test_file.name}")
            
            try:
                file_choice = int(input("Escolha o número do arquivo: ")) - 1
                if 0 <= file_choice < len(test_files):
                    run_specific_test(test_files[file_choice].name)
                else:
                    print("❌ Opção inválida!")
            except ValueError:
                print("❌ Por favor, digite um número válido!")
        
        elif escolha == "3":
            run_coverage()
        
        elif escolha == "4":
            validate_code_quality()
        
        elif escolha == "5":
            print("🔄 Executando validação completa...")
            
            success = True
            success &= validate_code_quality()
            success &= run_tests_with_sqlite()
            
            if success:
                print("🎉 Validação completa passou!")
            else:
                print("💥 Validação completa falhou!")
        
        elif escolha == "6":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()

