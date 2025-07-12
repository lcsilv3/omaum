#!/usr/bin/env python
"""
Script para executar todos os testes de integração do sistema de presenças.
Permite execução seletiva e relatórios detalhados.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
import argparse


class IntegrationTestRunner:
    """Runner para testes de integração com relatórios e métricas."""
    
    def __init__(self):
        self.test_modules = {
            'integration': 'presencas.tests.test_integration',
            'user_stories': 'presencas.tests.test_user_stories', 
            'performance': 'presencas.tests.test_performance',
            'browser': 'presencas.tests.test_browser',
            'compatibility': 'presencas.tests.test_compatibility'
        }
        
        self.results = {}
        self.total_start_time = None
    
    def setup_environment(self):
        """Configura ambiente para testes."""
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
        
        # Configurações específicas para testes
        os.environ['TESTING'] = 'true'
        os.environ['SELENIUM_HEADLESS'] = 'true'
        
        # Verificar dependências
        self.check_dependencies()
    
    def check_dependencies(self):
        """Verifica se dependências estão disponíveis."""
        try:
            import django
            print("✓ Django disponível")
        except ImportError:
            print("✗ Django não encontrado")
            sys.exit(1)
        
        try:
            import selenium
            print("✓ Selenium disponível")
        except ImportError:
            print("⚠ Selenium não disponível - testes de browser serão pulados")
        
        try:
            import coverage
            print("✓ Coverage disponível")
        except ImportError:
            print("⚠ Coverage não disponível - sem relatórios de cobertura")
    
    def run_test_module(self, module_name, module_path, verbose=False):
        """Executa um módulo de teste específico."""
        print(f"\n{'='*60}")
        print(f"Executando: {module_name.upper()}")
        print(f"Módulo: {module_path}")
        print('='*60)
        
        start_time = time.time()
        
        # Comando do Django test
        cmd = ['python', 'manage.py', 'test', module_path]
        if verbose:
            cmd.append('--verbosity=2')
        else:
            cmd.append('--verbosity=1')
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            execution_time = time.time() - start_time
            
            self.results[module_name] = {
                'success': result.returncode == 0,
                'execution_time': execution_time,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
            
            if result.returncode == 0:
                print(f"✓ {module_name} - SUCESSO ({execution_time:.2f}s)")
            else:
                print(f"✗ {module_name} - FALHOU ({execution_time:.2f}s)")
                if verbose:
                    print("STDERR:", result.stderr)
                    print("STDOUT:", result.stdout)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"✗ {module_name} - TIMEOUT (>300s)")
            self.results[module_name] = {
                'success': False,
                'execution_time': 300,
                'error': 'Timeout'
            }
            return False
        
        except Exception as e:
            print(f"✗ {module_name} - ERRO: {e}")
            self.results[module_name] = {
                'success': False,
                'execution_time': 0,
                'error': str(e)
            }
            return False
    
    def run_with_coverage(self, modules_to_run, verbose=False):
        """Executa testes com coverage."""
        print("\n" + "="*60)
        print("EXECUTANDO COM COVERAGE")
        print("="*60)
        
        # Preparar comando coverage
        test_modules = []
        for module in modules_to_run:
            if module in self.test_modules:
                test_modules.append(self.test_modules[module])
        
        if not test_modules:
            print("Nenhum módulo válido especificado")
            return False
        
        cmd = [
            'coverage', 'run', 
            '--source=presencas',
            '--omit=*/migrations/*,*/tests/*',
            'manage.py', 'test'
        ] + test_modules
        
        if verbose:
            cmd.append('--verbosity=2')
        
        start_time = time.time()
        
        try:
            result = subprocess.run(cmd, timeout=600)  # 10 minutos
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✓ Testes com coverage - SUCESSO ({execution_time:.2f}s)")
                
                # Gerar relatório de coverage
                print("\nGerando relatório de coverage...")
                subprocess.run(['coverage', 'report'])
                subprocess.run(['coverage', 'html'])
                print("Relatório HTML gerado em htmlcov/")
                
                return True
            else:
                print(f"✗ Testes com coverage - FALHOU ({execution_time:.2f}s)")
                return False
                
        except subprocess.TimeoutExpired:
            print("✗ Testes com coverage - TIMEOUT")
            return False
    
    def run_specific_tests(self, test_pattern, verbose=False):
        """Executa testes específicos por padrão."""
        print(f"\n{'='*60}")
        print(f"Executando testes com padrão: {test_pattern}")
        print('='*60)
        
        cmd = [
            'python', 'manage.py', 'test',
            '--pattern', test_pattern
        ]
        
        if verbose:
            cmd.append('--verbosity=2')
        
        try:
            result = subprocess.run(cmd, timeout=300)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print("✗ Timeout executando testes específicos")
            return False
    
    def print_summary(self):
        """Imprime resumo dos resultados."""
        print("\n" + "="*60)
        print("RESUMO DOS TESTES")
        print("="*60)
        
        total_time = time.time() - self.total_start_time if self.total_start_time else 0
        
        success_count = sum(1 for r in self.results.values() if r.get('success', False))
        total_count = len(self.results)
        
        print(f"Total de módulos: {total_count}")
        print(f"Sucessos: {success_count}")
        print(f"Falhas: {total_count - success_count}")
        print(f"Tempo total: {total_time:.2f}s")
        
        print(f"\nDetalhes por módulo:")
        for module, result in self.results.items():
            status = "✓" if result.get('success', False) else "✗"
            time_str = f"{result.get('execution_time', 0):.2f}s"
            print(f"  {status} {module:15} - {time_str}")
            
            if not result.get('success', False) and 'error' in result:
                print(f"    Erro: {result['error']}")
        
        # Taxa de sucesso
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        print(f"\nTaxa de sucesso: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("🎉 Todos os testes passaram!")
        elif success_rate >= 80:
            print("⚠ Maioria dos testes passou - verificar falhas")
        else:
            print("❌ Muitos testes falharam - investigar problemas")
    
    def run_all(self, verbose=False, with_coverage=False):
        """Executa todos os testes de integração."""
        self.total_start_time = time.time()
        
        print("🚀 Iniciando Suite de Testes de Integração")
        print(f"Módulos a executar: {list(self.test_modules.keys())}")
        
        if with_coverage:
            return self.run_with_coverage(list(self.test_modules.keys()), verbose)
        
        all_success = True
        
        for module_name, module_path in self.test_modules.items():
            success = self.run_test_module(module_name, module_path, verbose)
            if not success:
                all_success = False
        
        self.print_summary()
        return all_success
    
    def run_selected(self, modules, verbose=False, with_coverage=False):
        """Executa módulos selecionados."""
        self.total_start_time = time.time()
        
        selected_modules = {}
        for module in modules:
            if module in self.test_modules:
                selected_modules[module] = self.test_modules[module]
            else:
                print(f"⚠ Módulo '{module}' não encontrado")
        
        if not selected_modules:
            print("❌ Nenhum módulo válido selecionado")
            return False
        
        print(f"🚀 Executando módulos selecionados: {list(selected_modules.keys())}")
        
        if with_coverage:
            return self.run_with_coverage(modules, verbose)
        
        all_success = True
        
        for module_name, module_path in selected_modules.items():
            success = self.run_test_module(module_name, module_path, verbose)
            if not success:
                all_success = False
        
        self.print_summary()
        return all_success


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description='Execute testes de integração do sistema de presenças'
    )
    
    parser.add_argument(
        '--modules', '-m',
        nargs='*',
        choices=['integration', 'user_stories', 'performance', 'browser', 'compatibility'],
        help='Módulos específicos para executar'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Executar com saída detalhada'
    )
    
    parser.add_argument(
        '--coverage', '-c',
        action='store_true',
        help='Executar com coverage'
    )
    
    parser.add_argument(
        '--pattern', '-p',
        type=str,
        help='Padrão para executar testes específicos (ex: *UserStory*)'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Listar módulos disponíveis'
    )
    
    args = parser.parse_args()
    
    runner = IntegrationTestRunner()
    runner.setup_environment()
    
    if args.list:
        print("Módulos de teste disponíveis:")
        for name, path in runner.test_modules.items():
            print(f"  {name:15} - {path}")
        return
    
    if args.pattern:
        success = runner.run_specific_tests(args.pattern, args.verbose)
        sys.exit(0 if success else 1)
    
    if args.modules:
        success = runner.run_selected(args.modules, args.verbose, args.coverage)
    else:
        success = runner.run_all(args.verbose, args.coverage)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
