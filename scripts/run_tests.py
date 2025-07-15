#!/usr/bin/env python
"""
Script para executar testes no projeto OMAUM com diferentes configurações.
"""

import argparse
import subprocess
import sys
import time
import os

def run_tests(test_type=None, coverage=False, verbose=False):
    """
    Executa os testes com as configurações especificadas.
    
    Args:
        test_type: Tipo de teste a executar (unit, integration, e2e, performance, security)
        coverage: Se deve executar com cobertura de código
        verbose: Se deve mostrar saída detalhada
    """
    # Comando base
    command = ['python', 'manage.py', 'test']
    
    # Adicionar tipo de teste específico
    if test_type:
        if test_type == 'unit':
            command.append('tests.unit')
        elif test_type == 'integration':
            command.append('tests.integration')
        elif test_type == 'e2e':
            command.append('tests.e2e')
        elif test_type == 'performance':
            command.append('tests.performance')
        elif test_type == 'security':
            command.append('tests.security')
        else:
            print(f"Tipo de teste desconhecido: {test_type}")
            return False
    
    # Configurar cobertura de código
    if coverage:
        # Substituir o comando para usar o coverage
        command = ['coverage', 'run', '--source=.'] + command[1:]
    
    # Configurar verbosidade
    if verbose:
        command.append('-v')
    
    # Executar o comando
    print(f"Executando comando: {' '.join(command)}")
    start_time = time.time()
    result = subprocess.run(command, capture_output=not verbose)
    end_time = time.time()
    
    # Mostrar resultados
    if result.returncode == 0:
        print(f"✓ Testes executados com sucesso em {end_time - start_time:.2f}s")
        
        # Mostrar relatório de cobertura se solicitado
        if coverage:
            print("\nRelatório de cobertura:")
            subprocess.run(['coverage', 'report'])
    else:
        print(f"✗ Testes falharam (código de saída: {result.returncode})")
        if not verbose:
            print(f"Saída de erro: {result.stderr.decode()}")
    
    return result.returncode == 0

def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(description='Executar testes do projeto OMAUM')
    parser.add_argument('--type', choices=['unit', 'integration', 'e2e', 'performance', 'security'],
                        help='Tipo de teste a executar')
    parser.add_argument('--coverage', action='store_true',
                        help='Executar com cobertura de código')
    parser.add_argument('--verbose', action='store_true',
                        help='Mostrar saída detalhada')
    
    args = parser.parse_args()
    
    # Configurar ambiente Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
    
    # Executar testes
    success = run_tests(
        test_type=args.type,
        coverage=args.coverage,
        verbose=args.verbose
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
