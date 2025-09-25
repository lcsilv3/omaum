"""
Script final para executar testes de forma simplificada.
"""

import os
import sys
import subprocess
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_simple_tests():
    """Executa testes usando manage.py."""

    # Configurar ambiente
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings_test"

    # Comando para executar testes
    cmd = [
        sys.executable,
        "manage.py",
        "test",
        # "tests.test_cursos_very_simple",
        "--verbosity=2",
        "--keepdb",
    ]

    # print("🚀 Executando testes simples...")
    print(f"📦 Comando: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)

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
    # success = run_simple_tests()
    sys.exit(0 if success else 1)
