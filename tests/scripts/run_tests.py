#!/usr/bin/env python
"""
Script de execução automatizada de testes com correção de erros.
"""

import os
import sys
import subprocess
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("teste_automatizado.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class TestRunner:
    """Executor de testes automatizado com correção de erros."""

    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.test_results = {}
        self.coverage_target = 100
        self.max_retries = 3

    def setup_environment(self) -> bool:
        """Configura o ambiente de teste."""
        logger.info("Configurando ambiente de teste...")

        try:
            # Instalar dependências de teste
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"],
                check=True,
                capture_output=True,
            )

            # Configurar variáveis de ambiente
            os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings_test"
            os.environ["PYTHONPATH"] = str(self.project_root)

            logger.info("Ambiente configurado com sucesso!")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao configurar ambiente: {e}")
            return False

    def run_migrations(self) -> bool:
        """Executa migrações no banco de teste."""
        logger.info("Executando migrações...")

        try:
            subprocess.run(
                [
                    sys.executable,
                    "manage.py",
                    "migrate",
                    "--settings=tests.settings_test",
                ],
                check=True,
                capture_output=True,
            )

            logger.info("Migrações executadas com sucesso!")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao executar migrações: {e}")
            return False

    def run_tests_for_app(self, app_name: str) -> Tuple[bool, Dict]:
        """Executa testes para uma aplicação específica."""
        logger.info(f"Executando testes para {app_name}...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            f"{app_name}/",
            "--tb=short",
            "--maxfail=5",
            f"--cov={app_name}",
            "--cov-report=term-missing",
            "--cov-report=json",
            "--cov-fail-under=80",
            "-v",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Analisar resultados
            success = result.returncode == 0
            coverage_data = self._extract_coverage_data(result.stdout)

            self.test_results[app_name] = {
                "success": success,
                "coverage": coverage_data,
                "output": result.stdout,
                "errors": result.stderr,
            }

            if success:
                logger.info(f"Testes para {app_name} executados com sucesso!")
            else:
                logger.warning(f"Falhas nos testes para {app_name}")

            return success, self.test_results[app_name]

        except Exception as e:
            logger.error(f"Erro ao executar testes para {app_name}: {e}")
            return False, {}

    def run_full_test_suite(self) -> bool:
        """Executa a suíte completa de testes."""
        logger.info("Iniciando execução da suíte completa de testes...")

        critical_apps = ["cursos", "alunos", "matriculas", "turmas", "presencas"]
        all_success = True

        for app in critical_apps:
            success, results = self.run_tests_for_app(app)
            if not success:
                all_success = False
                self._attempt_auto_fix(app, results)

        # Executar testes de integração
        self._run_integration_tests()

        # Gerar relatório final
        self._generate_final_report()

        return all_success

    def _extract_coverage_data(self, output: str) -> Dict:
        """Extrai dados de cobertura do output."""
        coverage_data = {"percentage": 0, "missing_lines": []}

        # Buscar por linha de cobertura
        lines = output.split("\n")
        for line in lines:
            if "TOTAL" in line and "%" in line:
                try:
                    percentage = float(line.split("%")[0].split()[-1])
                    coverage_data["percentage"] = percentage
                except:
                    pass

        return coverage_data

    def _attempt_auto_fix(self, app_name: str, results: Dict) -> bool:
        """Tenta corrigir automaticamente erros comuns."""
        logger.info(f"Tentando corrigir erros automaticamente para {app_name}...")

        errors = results.get("errors", "")
        output = results.get("output", "")

        # Padrões comuns de erro e suas correções
        error_patterns = {
            "ImportError": self._fix_import_error,
            "ModuleNotFoundError": self._fix_module_not_found,
            "AttributeError": self._fix_attribute_error,
            "NameError": self._fix_name_error,
            "SyntaxError": self._fix_syntax_error,
        }

        for error_type, fix_function in error_patterns.items():
            if error_type in errors or error_type in output:
                try:
                    fix_function(app_name, errors + output)
                    logger.info(f"Correção aplicada para {error_type}")
                    return True
                except Exception as e:
                    logger.error(f"Falha na correção automática: {e}")

        return False

    def _fix_import_error(self, app_name: str, error_text: str) -> None:
        """Corrige erros de importação."""
        logger.info(f"Corrigindo ImportError para {app_name}")

        # Criar arquivo __init__.py se não existir
        init_file = self.project_root / app_name / "__init__.py"
        if not init_file.exists():
            init_file.touch()

        # Criar arquivo __init__.py no diretório de testes
        test_init = self.project_root / app_name / "tests" / "__init__.py"
        if not test_init.exists():
            test_init.parent.mkdir(exist_ok=True)
            test_init.touch()

    def _fix_module_not_found(self, app_name: str, error_text: str) -> None:
        """Corrige erros de módulo não encontrado."""
        logger.info(f"Corrigindo ModuleNotFoundError para {app_name}")

        # Adicionar app ao INSTALLED_APPS se necessário
        settings_test = self.project_root / "tests" / "settings_test.py"
        if settings_test.exists():
            content = settings_test.read_text()
            if app_name not in content:
                # Adicionar app à lista de INSTALLED_APPS
                content = content.replace(
                    "INSTALLED_APPS = [", f"INSTALLED_APPS = [\n    '{app_name}',"
                )
                settings_test.write_text(content)

    def _fix_attribute_error(self, app_name: str, error_text: str) -> None:
        """Corrige erros de atributo."""
        logger.info(f"Corrigindo AttributeError para {app_name}")
        # Implementar correções específicas para AttributeError
        pass

    def _fix_name_error(self, app_name: str, error_text: str) -> None:
        """Corrige erros de nome."""
        logger.info(f"Corrigindo NameError para {app_name}")
        # Implementar correções específicas para NameError
        pass

    def _fix_syntax_error(self, app_name: str, error_text: str) -> None:
        """Corrige erros de sintaxe."""
        logger.info(f"Corrigindo SyntaxError para {app_name}")
        # Implementar correções específicas para SyntaxError
        pass

    def _run_integration_tests(self) -> None:
        """Executa testes de integração."""
        logger.info("Executando testes de integração...")

        cmd = [sys.executable, "-m", "pytest", "tests/integration/", "--tb=short", "-v"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            self.test_results["integration"] = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
            }

        except Exception as e:
            logger.error(f"Erro ao executar testes de integração: {e}")

    def _generate_final_report(self) -> None:
        """Gera relatório final dos testes."""
        logger.info("Gerando relatório final...")

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_apps": len(self.test_results),
            "successful_apps": sum(
                1 for r in self.test_results.values() if r.get("success", False)
            ),
            "coverage_summary": {},
            "details": self.test_results,
        }

        # Calcular cobertura média
        total_coverage = 0
        coverage_count = 0

        for app, results in self.test_results.items():
            if "coverage" in results:
                coverage = results["coverage"].get("percentage", 0)
                total_coverage += coverage
                coverage_count += 1
                report["coverage_summary"][app] = coverage

        if coverage_count > 0:
            report["average_coverage"] = total_coverage / coverage_count

        # Salvar relatório
        report_file = self.project_root / "relatorio_testes.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # Relatório em texto
        self._generate_text_report(report)

        logger.info(f"Relatório salvo em {report_file}")

    def _generate_text_report(self, report: Dict) -> None:
        """Gera relatório em texto."""
        text_report = f"""
RELATÓRIO DE TESTES AUTOMATIZADOS
================================

Data/Hora: {report['timestamp']}
Total de aplicações testadas: {report['total_apps']}
Aplicações com sucesso: {report['successful_apps']}
Cobertura média: {report.get('average_coverage', 0):.2f}%

DETALHES POR APLICAÇÃO:
"""

        for app, results in report["details"].items():
            status = "✓ SUCESSO" if results.get("success", False) else "✗ FALHA"
            coverage = results.get("coverage", {}).get("percentage", 0)

            text_report += f"""
{app.upper()}: {status}
  Cobertura: {coverage:.2f}%
"""

        report_file = self.project_root / "relatorio_testes.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(text_report)

    def run_parallel_tests(self) -> bool:
        """Executa testes em paralelo."""
        logger.info("Executando testes em paralelo...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--tb=short",
            "--maxfail=10",
            "--cov=.",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=90",
            "-n",
            "auto",  # Execução paralela
            "-v",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            self.test_results["parallel"] = {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
            }

            logger.info("Testes paralelos executados!")
            return result.returncode == 0

        except Exception as e:
            logger.error(f"Erro ao executar testes paralelos: {e}")
            return False


def main():
    """Função principal."""
    runner = TestRunner()

    # Configurar ambiente
    if not runner.setup_environment():
        logger.error("Falha na configuração do ambiente")
        sys.exit(1)

    # Executar migrações
    if not runner.run_migrations():
        logger.error("Falha nas migrações")
        sys.exit(1)

    # Executar testes
    if len(sys.argv) > 1 and sys.argv[1] == "--parallel":
        success = runner.run_parallel_tests()
    else:
        success = runner.run_full_test_suite()

    if success:
        logger.info("Todos os testes executados com sucesso!")
        sys.exit(0)
    else:
        logger.error("Alguns testes falharam")
        sys.exit(1)


if __name__ == "__main__":
    main()
