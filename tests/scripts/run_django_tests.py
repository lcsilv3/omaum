"""
Script final para executar testes de forma simplificada.
"""

import os
import sys
import django
from django.test.runner import DiscoverRunner

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings_test")
django.setup()


def run_simple_tests():
    """Executa testes usando o runner do Django."""

    # Configurar runner de testes
    runner = DiscoverRunner(verbosity=2, interactive=False)

    # Executar testes específicos
    test_labels = [
        # "tests.test_cursos_very_simple",
    ]

    # print("🚀 Executando testes simples...")
    print(f"📦 Testando: {', '.join(test_labels)}")

    # Executar testes
    result = runner.run_tests(test_labels)

    if result == 0:
        print("✅ Todos os testes passaram!")
    else:
        print(f"❌ {result} testes falharam")

    return result == 0


if __name__ == "__main__":
    # success = run_simple_tests()
    sys.exit(0 if success else 1)
