"""
Script para execução de testes paralelos otimizados.
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
from datetime import datetime


def run_parallel_tests(apps=None, workers=None, coverage=True):
    """
    Executa testes em paralelo com configurações otimizadas.

    Args:
        apps: Lista de apps para testar (default: apps críticos)
        workers: Número de workers (default: auto)
        coverage: Se deve gerar relatório de cobertura (default: True)
    """

    # Apps críticos por padrão
    critical_apps = ["cursos", "alunos", "matriculas", "turmas", "presencas"]
    test_apps = apps or critical_apps

    # Configurar comando base
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--tb=short",
        "--maxfail=10",
        "-v",
        "--strict-markers",
        "--strict-config",
    ]

    # Adicionar execução paralela
    if workers:
        cmd.extend(["-n", str(workers)])
    else:
        cmd.extend(["-n", "auto"])

    # Adicionar cobertura JSON adicional se solicitado
    if coverage:
        cmd.extend(["--cov-report=json:coverage.json"])

    # Adicionar apps específicos
    for app in test_apps:
        cmd.append(f"tests/test_{app}.py")

    # Adicionar testes de integração
    cmd.append("tests/integration/")

    print(f"🚀 Executando testes paralelos para: {', '.join(test_apps)}")
    print(f"📦 Comando: {' '.join(cmd)}")

    # Executar testes
    start_time = datetime.now()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        end_time = datetime.now()
        duration = end_time - start_time

        print(f"\n⏱️  Tempo de execução: {duration}")
        print(f"📊 Código de saída: {result.returncode}")

        if result.returncode == 0:
            print("✅ Todos os testes passaram!")
        else:
            print("❌ Alguns testes falharam")

        print("\n📄 Saída dos testes:")
        print(result.stdout)

        if result.stderr:
            print("\n🔴 Erros:")
            print(result.stderr)

        # Gerar relatório de cobertura se disponível
        if coverage and Path("coverage.json").exists():
            generate_coverage_report()

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False


def generate_coverage_report():
    """Gera relatório de cobertura formatado."""
    try:
        with open("coverage.json", "r") as f:
            coverage_data = json.load(f)

        total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)

        print(f"\n📊 RELATÓRIO DE COBERTURA")
        print(f"{'='*50}")
        print(f"Cobertura total: {total_coverage:.2f}%")

        files_data = coverage_data.get("files", {})

        print(f"\n📁 Cobertura por arquivo:")
        for file_path, file_data in files_data.items():
            if any(
                app in file_path
                for app in ["cursos", "alunos", "matriculas", "turmas", "presencas"]
            ):
                coverage_percent = file_data.get("summary", {}).get(
                    "percent_covered", 0
                )
                print(f"  {file_path}: {coverage_percent:.1f}%")

        # Verificar se atingiu meta
        if total_coverage >= 90:
            print(f"\n✅ Meta de cobertura atingida! ({total_coverage:.2f}% >= 90%)")
        else:
            print(f"\n⚠️  Meta de cobertura não atingida ({total_coverage:.2f}% < 90%)")

    except Exception as e:
        print(f"❌ Erro ao gerar relatório de cobertura: {e}")


def run_specific_tests(test_pattern, verbose=True):
    """Executa testes específicos baseados em padrão."""

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        test_pattern,
        "--tb=short",
        "-v" if verbose else "-q",
    ]

    print(f"🎯 Executando testes específicos: {test_pattern}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        print(f"📊 Código de saída: {result.returncode}")
        print(result.stdout)

        if result.stderr:
            print("🔴 Erros:")
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False


def run_smoke_tests():
    """Executa testes de fumaça (smoke tests) rápidos."""

    smoke_tests = [
        "tests/test_cursos.py::CursoModelTest::test_curso_creation",
        "tests/test_alunos.py::AlunoModelTest::test_aluno_creation",
        "tests/test_matriculas.py::MatriculaModelTest::test_matricula_creation",
        "tests/integration/test_sistema_completo.py::FluxoCompletoSistemaTest::test_fluxo_completo_aluno_matricula_turma_presenca",
    ]

    cmd = [sys.executable, "-m", "pytest", "--tb=short", "-v"] + smoke_tests

    print("🚨 Executando testes de fumaça...")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Testes de fumaça passaram!")
        else:
            print("❌ Testes de fumaça falharam")
            print(result.stdout)
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erro ao executar testes de fumaça: {e}")
        return False


def run_performance_tests():
    """Executa testes de performance."""

    performance_tests = [
        "tests/test_cursos.py::CursoIntegrationTest::test_performance_listagem_cursos",
        "tests/test_alunos.py::AlunoIntegrationTest::test_performance_listagem_alunos",
        "tests/test_matriculas.py::MatriculaIntegrationTest::test_performance_listagem_matriculas",
        "tests/integration/test_sistema_completo.py::FluxoCompletoSistemaTest::test_performance_sistema_completo",
    ]

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--tb=short",
        "-v",
        "--durations=10",  # Mostrar 10 testes mais lentos
    ] + performance_tests

    print("⚡ Executando testes de performance...")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Testes de performance passaram!")
        else:
            print("❌ Testes de performance falharam")

        print(result.stdout)
        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erro ao executar testes de performance: {e}")
        return False


def main():
    """Função principal do script."""

    parser = argparse.ArgumentParser(
        description="Execução de testes paralelos otimizados"
    )
    parser.add_argument("--apps", nargs="+", help="Apps específicos para testar")
    parser.add_argument("--workers", type=int, help="Número de workers paralelos")
    parser.add_argument(
        "--no-coverage", action="store_true", help="Não gerar relatório de cobertura"
    )
    parser.add_argument(
        "--smoke", action="store_true", help="Executar apenas testes de fumaça"
    )
    parser.add_argument(
        "--performance", action="store_true", help="Executar testes de performance"
    )
    parser.add_argument("--pattern", help="Padrão de testes específicos")

    args = parser.parse_args()

    # Configurar ambiente
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings_test"

    # Executar tipo de teste solicitado
    if args.smoke:
        success = run_smoke_tests()
    elif args.performance:
        success = run_performance_tests()
    elif args.pattern:
        success = run_specific_tests(args.pattern)
    else:
        success = run_parallel_tests(
            apps=args.apps, workers=args.workers, coverage=not args.no_coverage
        )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
