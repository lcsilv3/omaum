#!/usr/bin/env python
"""
Script de automação completa para testes.
Instala dependências, configura ambiente e executa testes com correção automática.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime


class TestAutomationManager:
    """Gerenciador de automação de testes completo."""

    def __init__(self, project_root=None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.venv_path = self.project_root / "venv"
        self.python_exe = (
            self.venv_path / "Scripts" / "python.exe"
            if os.name == "nt"
            else self.venv_path / "bin" / "python"
        )
        self.pip_exe = (
            self.venv_path / "Scripts" / "pip.exe"
            if os.name == "nt"
            else self.venv_path / "bin" / "pip"
        )

    def setup_virtual_environment(self):
        """Configura ambiente virtual se não existir."""
        if not self.venv_path.exists():
            print("🔧 Criando ambiente virtual...")
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_path)], check=True
            )
            print("✅ Ambiente virtual criado!")
        else:
            print("✅ Ambiente virtual já existe")

    def install_dependencies(self):
        """Instala todas as dependências necessárias."""
        print("📦 Instalando dependências...")

        # Instalar dependências principais
        if (self.project_root / "requirements.txt").exists():
            subprocess.run(
                [str(self.pip_exe), "install", "-r", "requirements.txt"], check=True
            )

        # Instalar dependências de desenvolvimento
        if (self.project_root / "requirements-dev.txt").exists():
            subprocess.run(
                [str(self.pip_exe), "install", "-r", "requirements-dev.txt"], check=True
            )

        # Instalar dependências de teste
        if (self.project_root / "requirements-test.txt").exists():
            subprocess.run(
                [str(self.pip_exe), "install", "-r", "requirements-test.txt"],
                check=True,
            )

        print("✅ Dependências instaladas!")

    def setup_django_environment(self):
        """Configura ambiente Django."""
        print("🔧 Configurando ambiente Django...")

        # Configurar variáveis de ambiente
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings_test"
        os.environ["PYTHONPATH"] = str(self.project_root)

        # Executar migrações se necessário
        try:
            subprocess.run(
                [
                    str(self.python_exe),
                    "manage.py",
                    "migrate",
                    "--settings=tests.settings_test",
                ],
                check=True,
                capture_output=True,
            )
            print("✅ Migrações executadas!")
        except subprocess.CalledProcessError:
            print("⚠️  Migrações não executadas (banco em memória)")

    def run_automated_tests(self):
        """Executa testes automatizados com correção de erros."""
        print("🚀 Iniciando execução automatizada de testes...")

        # Executar testes com script personalizado
        test_script = self.project_root / "tests" / "run_tests.py"

        if test_script.exists():
            result = subprocess.run(
                [str(self.python_exe), str(test_script)], capture_output=True, text=True
            )

            print(
                f"📊 Resultado dos testes: {'✅ SUCESSO' if result.returncode == 0 else '❌ FALHA'}"
            )

            if result.stdout:
                print("📄 Saída:")
                print(result.stdout)

            if result.stderr:
                print("🔴 Erros:")
                print(result.stderr)

            return result.returncode == 0
        else:
            print("❌ Script de testes não encontrado")
            return False

    def run_parallel_tests(self):
        """Executa testes em paralelo."""
        print("⚡ Executando testes em paralelo...")

        parallel_script = self.project_root / "tests" / "run_parallel_tests.py"

        if parallel_script.exists():
            result = subprocess.run(
                [str(self.python_exe), str(parallel_script)],
                capture_output=True,
                text=True,
            )

            print(
                f"📊 Resultado dos testes paralelos: {'✅ SUCESSO' if result.returncode == 0 else '❌ FALHA'}"
            )

            if result.stdout:
                print("📄 Saída:")
                print(result.stdout)

            return result.returncode == 0
        else:
            print("❌ Script de testes paralelos não encontrado")
            return False

    def run_coverage_analysis(self):
        """Executa análise de cobertura."""
        print("📊 Executando análise de cobertura...")

        cmd = [
            str(self.python_exe),
            "-m",
            "pytest",
            "--cov=.",
            "--cov-report=html:htmlcov",
            "--cov-report=term-missing",
            "--cov-report=json:coverage.json",
            "--cov-fail-under=90",
            "tests/",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Análise de cobertura concluída!")
                self.generate_coverage_summary()
            else:
                print("❌ Análise de cobertura falhou")
                print(result.stdout)
                print(result.stderr)

            return result.returncode == 0

        except Exception as e:
            print(f"❌ Erro na análise de cobertura: {e}")
            return False

    def generate_coverage_summary(self):
        """Gera resumo da cobertura."""
        coverage_file = self.project_root / "coverage.json"

        if coverage_file.exists():
            try:
                with open(coverage_file, "r") as f:
                    coverage_data = json.load(f)

                total_coverage = coverage_data.get("totals", {}).get(
                    "percent_covered", 0
                )

                print("\n📊 RESUMO DE COBERTURA")
                print(f"{'='*50}")
                print(f"Cobertura total: {total_coverage:.2f}%")

                if total_coverage >= 90:
                    print("✅ Meta de cobertura atingida!")
                else:
                    print("⚠️  Meta de cobertura não atingida")

            except Exception as e:
                print(f"❌ Erro ao gerar resumo de cobertura: {e}")

    def generate_test_report(self):
        """Gera relatório final dos testes."""
        print("📋 Gerando relatório final...")

        report = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "python_version": sys.version,
            "status": "completed",
        }

        # Salvar relatório
        report_file = self.project_root / "test_automation_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📋 Relatório salvo em: {report_file}")

    def run_complete_automation(self):
        """Executa automação completa."""
        print("🤖 INICIANDO AUTOMAÇÃO COMPLETA DE TESTES")
        print("=" * 60)

        start_time = time.time()

        try:
            # 1. Configurar ambiente virtual
            self.setup_virtual_environment()

            # 2. Instalar dependências
            self.install_dependencies()

            # 3. Configurar Django
            self.setup_django_environment()

            # 4. Executar testes automatizados
            tests_passed = self.run_automated_tests()

            # 5. Executar testes paralelos
            if tests_passed:
                self.run_parallel_tests()

            # 6. Executar análise de cobertura
            self.run_coverage_analysis()

            # 7. Gerar relatório final
            self.generate_test_report()

            end_time = time.time()
            duration = end_time - start_time

            print(f"\n⏱️  Tempo total: {duration:.2f} segundos")
            print("🎉 AUTOMAÇÃO COMPLETA FINALIZADA!")

            return tests_passed

        except Exception as e:
            print(f"❌ Erro na automação: {e}")
            return False


def main():
    """Função principal."""
    import argparse

    parser = argparse.ArgumentParser(description="Automação completa de testes")
    parser.add_argument("--project-root", help="Diretório raiz do projeto")
    parser.add_argument(
        "--setup-only", action="store_true", help="Apenas configurar ambiente"
    )
    parser.add_argument(
        "--tests-only", action="store_true", help="Apenas executar testes"
    )
    parser.add_argument(
        "--coverage-only", action="store_true", help="Apenas análise de cobertura"
    )

    args = parser.parse_args()

    # Criar gerenciador
    manager = TestAutomationManager(args.project_root)

    # Executar ação solicitada
    if args.setup_only:
        manager.setup_virtual_environment()
        manager.install_dependencies()
        manager.setup_django_environment()
    elif args.tests_only:
        success = manager.run_automated_tests()
        sys.exit(0 if success else 1)
    elif args.coverage_only:
        success = manager.run_coverage_analysis()
        sys.exit(0 if success else 1)
    else:
        success = manager.run_complete_automation()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
