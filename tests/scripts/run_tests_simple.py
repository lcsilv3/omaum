"""
Script simplificado para execução de testes paralelos.
"""

import os
import sys
import subprocess
from datetime import datetime


def run_tests():
    """Executa testes em paralelo de forma simplificada."""

    # Configurar ambiente
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings_test"

    # Comando básico sem argumentos duplicados
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-n",
        "auto",
        "tests/test_cursos.py",
        "tests/test_alunos.py",
        "tests/test_matriculas.py",
        "tests/integration/",
    ]

    print("🚀 Executando testes paralelos...")
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

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
