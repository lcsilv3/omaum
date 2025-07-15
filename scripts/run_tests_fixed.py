#!/usr/bin/env python
"""
Script para executar testes do sistema OMAUM
"""

import os
import sys
import time
import subprocess
import argparse
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurar variáveis de ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')

def run_tests(test_type=None, coverage=False, verbose=False):
    """
    Executa testes do sistema OMAUM
    
    Args:
        test_type: Tipo de teste ('unit', 'integration', 'e2e', 'performance', 'security')
        coverage: Se deve executar com cobertura de código
        verbose: Se deve mostrar saída detalhada
    """
    
    # Comando base
    command = ['python', '-m', 'pytest']
    
    # Adicionar diretório específico baseado no tipo de teste
    if test_type == 'unit':
        command.append('tests/*/test_*.py')
    elif test_type == 'integration':
        command.append('tests/integration/')
    elif test_type == 'e2e':
        command.append('tests/e2e/')
    elif test_type == 'performance':
        command.append('tests/performance/')
    elif test_type == 'security':
        command.append('tests/security/')
    else:
        # Se não especificado, executa todos os testes
        command.append('tests/')
    
    if coverage:
        # Usar coverage
        command = ['coverage', 'run', '--source=.', '-m', 'pytest'] + command[2:]
    
    if verbose:
        command.append('-v')
    
    # Adicionar configurações específicas do pytest
    command.extend([
        '--tb=short',
        '--strict-markers',
        '--maxfail=5'
    ])
    
    print(f"Executando comando: {' '.join(command)}")
    start_time = time.time()
    
    try:
        result = subprocess.run(command, capture_output=not verbose, text=True)
        end_time = time.time()
        
        print(f"\nTempo de execução: {end_time - start_time:.2f} segundos")
        
        if result.returncode == 0:
            print("✅ Todos os testes passaram!")
            
            if coverage:
                print("\n📊 Gerando relatório de cobertura...")
                subprocess.run(['coverage', 'report'])
                subprocess.run(['coverage', 'html'])
                print("Relatório HTML gerado em htmlcov/index.html")
        else:
            print(f"❌ Alguns testes falharam (código de saída: {result.returncode})")
            if not verbose and result.stdout:
                print("\nSaída dos testes:")
                print(result.stdout)
            if result.stderr:
                print("\nErros:")
                print(result.stderr)
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Execução interrompida pelo usuário")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Executar testes do sistema OMAUM')
    parser.add_argument(
        '--type', '-t',
        choices=['unit', 'integration', 'e2e', 'performance', 'security'],
        help='Tipo de teste a executar'
    )
    parser.add_argument(
        '--coverage', '-c',
        action='store_true',
        help='Executar com cobertura de código'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Saída detalhada'
    )
    
    args = parser.parse_args()
    
    success = run_tests(
        test_type=args.type,
        coverage=args.coverage,
        verbose=args.verbose
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
