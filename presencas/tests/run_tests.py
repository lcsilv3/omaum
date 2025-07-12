#!/usr/bin/env python
"""
Script para executar a suite completa de testes do aplicativo presencas.
Inclui geração de relatórios de cobertura e métricas de performance.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Configurar environment para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')

import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import execute_from_command_line


class TestRunner:
    """Runner personalizado para testes do aplicativo presencas."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.results = {}
        
    def setup(self):
        """Configuração inicial."""
        django.setup()
        
        # Verificar se coverage está disponível
        try:
            import coverage
            self.has_coverage = True
        except ImportError:
            self.has_coverage = False
            print("Warning: coverage not available. Install with: pip install coverage")
    
    def run_all_tests(self, verbosity=2, with_coverage=True):
        """Executa todos os testes do aplicativo presencas."""
        print("=" * 70)
        print("EXECUTANDO SUITE COMPLETA DE TESTES - PRESENCAS")
        print("=" * 70)
        
        self.start_time = time.time()
        
        if with_coverage and self.has_coverage:
            return self._run_with_coverage(verbosity)
        else:
            return self._run_without_coverage(verbosity)
    
    def _run_with_coverage(self, verbosity):
        """Executa testes com cobertura."""
        import coverage
        
        # Configurar coverage
        cov = coverage.Coverage(
            source=['presencas'],
            omit=[
                '*/tests/*',
                '*/migrations/*',
                '*/venv/*',
                '*/env/*',
                '*/__pycache__/*',
                '*/site-packages/*'
            ]
        )
        
        cov.start()
        
        try:
            # Executar testes
            result = self._execute_tests(verbosity)
            
            cov.stop()
            cov.save()
            
            # Gerar relatórios
            self._generate_coverage_reports(cov)
            
            return result
            
        except Exception as e:
            cov.stop()
            print(f"Erro durante execução dos testes: {e}")
            return False
    
    def _run_without_coverage(self, verbosity):
        """Executa testes sem cobertura."""
        return self._execute_tests(verbosity)
    
    def _execute_tests(self, verbosity):
        """Executa os testes usando o runner do Django."""
        # Configurar runner
        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=verbosity, interactive=False)
        
        # Lista de módulos de teste
        test_modules = [
            'presencas.tests.test_models',
            'presencas.tests.test_services', 
            'presencas.tests.test_calculadora_estatisticas',
            'presencas.tests.test_views',
            'presencas.tests.test_apis',
            'presencas.tests.test_forms'
        ]
        
        print(f"\nExecutando {len(test_modules)} módulos de teste...")
        print("-" * 50)
        
        failures = 0
        
        for module in test_modules:
            print(f"\n► Executando: {module}")
            
            try:
                result = test_runner.run_tests([module])
                
                if result:
                    failures += result
                    print(f"  ✗ Falhou com {result} erro(s)")
                else:
                    print(f"  ✓ Passou")
                    
            except Exception as e:
                print(f"  ✗ Erro: {e}")
                failures += 1
        
        self.end_time = time.time()
        
        # Relatório final
        self._print_summary(failures, len(test_modules))
        
        return failures == 0
    
    def _generate_coverage_reports(self, cov):
        """Gera relatórios de cobertura."""
        print("\n" + "=" * 50)
        print("RELATÓRIO DE COBERTURA")
        print("=" * 50)
        
        # Relatório no terminal
        print("\nCobertura por arquivo:")
        cov.report(show_missing=True)
        
        # Relatório HTML
        html_dir = Path(__file__).parent / 'coverage_html'
        html_dir.mkdir(exist_ok=True)
        
        try:
            cov.html_report(directory=str(html_dir))
            print(f"\n✓ Relatório HTML gerado em: {html_dir}/index.html")
        except Exception as e:
            print(f"✗ Erro ao gerar relatório HTML: {e}")
        
        # Relatório XML (para CI/CD)
        xml_file = Path(__file__).parent / 'coverage.xml'
        try:
            cov.xml_report(outfile=str(xml_file))
            print(f"✓ Relatório XML gerado em: {xml_file}")
        except Exception as e:
            print(f"✗ Erro ao gerar relatório XML: {e}")
        
        # Verificar cobertura mínima
        total_coverage = cov.report(show_missing=False, skip_covered=False)
        print(f"\n📊 Cobertura total: {total_coverage:.1f}%")
        
        if total_coverage < 90:
            print("⚠️  ATENÇÃO: Cobertura abaixo de 90%!")
        else:
            print("✅ Meta de cobertura atingida (≥90%)")
    
    def _print_summary(self, failures, total_modules):
        """Imprime resumo da execução."""
        duration = self.end_time - self.start_time
        
        print("\n" + "=" * 70)
        print("RESUMO DA EXECUÇÃO")
        print("=" * 70)
        
        print(f"Módulos executados: {total_modules}")
        print(f"Falhas: {failures}")
        print(f"Tempo total: {duration:.2f}s")
        
        if failures == 0:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
        else:
            print(f"\n❌ {failures} MÓDULO(S) COM FALHAS")
        
        print("=" * 70)
    
    def run_specific_tests(self, test_pattern, verbosity=2):
        """Executa testes específicos baseado em padrão."""
        print(f"Executando testes que combinam com: {test_pattern}")
        
        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=verbosity, interactive=False)
        
        return test_runner.run_tests([test_pattern])
    
    def run_performance_tests(self):
        """Executa apenas testes de performance."""
        print("Executando testes de performance...")
        
        performance_tests = [
            'presencas.tests.test_calculadora_estatisticas.TestCalculadoraEstatisticas.test_performance_com_dataset_grande',
            'presencas.tests.test_apis.APIPerformanceTest',
            'presencas.tests.test_services.PresencaServicesTest.test_registrar_presencas_multiplas'
        ]
        
        for test in performance_tests:
            print(f"\n► {test}")
            result = self.run_specific_tests(test, verbosity=1)
            
            if result:
                print(f"  ✗ Falhou")
            else:
                print(f"  ✓ Passou")


def main():
    """Função principal do script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Executar testes do aplicativo presencas')
    parser.add_argument(
        '--no-coverage', 
        action='store_true', 
        help='Executar sem cobertura'
    )
    parser.add_argument(
        '--verbosity', 
        type=int, 
        default=2, 
        choices=[0, 1, 2, 3],
        help='Nível de verbosidade (0-3)'
    )
    parser.add_argument(
        '--pattern', 
        type=str, 
        help='Padrão para executar testes específicos'
    )
    parser.add_argument(
        '--performance', 
        action='store_true', 
        help='Executar apenas testes de performance'
    )
    parser.add_argument(
        '--check-migrations', 
        action='store_true', 
        help='Verificar se há migrações pendentes'
    )
    
    args = parser.parse_args()
    
    runner = TestRunner()
    runner.setup()
    
    # Verificar migrações pendentes
    if args.check_migrations:
        print("Verificando migrações pendentes...")
        try:
            execute_from_command_line(['manage.py', 'makemigrations', '--check', '--dry-run'])
            print("✓ Nenhuma migração pendente")
        except SystemExit:
            print("⚠️  Há migrações pendentes!")
            return 1
    
    # Executar testes específicos
    if args.pattern:
        success = runner.run_specific_tests(args.pattern, args.verbosity)
        return 0 if success == 0 else 1
    
    # Executar testes de performance
    if args.performance:
        runner.run_performance_tests()
        return 0
    
    # Executar todos os testes
    success = runner.run_all_tests(
        verbosity=args.verbosity,
        with_coverage=not args.no_coverage
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
