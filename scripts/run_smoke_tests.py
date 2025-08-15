"""
Runner de testes de fumaça com marcadores de início e fim.

Imprime:
- PYTEST_START
- PYTEST_END:OK ou PYTEST_END:FAIL CODE=<n>

Usa DJANGO_SETTINGS_MODULE=tests.settings_test.
"""

from __future__ import annotations

import os
import sys
import subprocess


def main() -> int:
    # Garantir settings de teste do Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings_test")

    # Comando pytest base (sem cobertura para reduzir ruído)
    pytest_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cov",
        "-rA",
    ]

    # Filtro padrão: smoke test de edição em lote
    # Permite sobrescrever via argumentos
    if len(sys.argv) > 1:
        # Passa os argumentos como estão para o pytest após os padrões
        pytest_cmd.extend(sys.argv[1:])
    else:
        pytest_cmd.extend([
            "presencas/tests/test_edicao_lote_ajax_smoke.py",
            "-k",
            "edicao_lote_ajax_smoke",
        ])

    print("PYTEST_START", flush=True)
    code = subprocess.call(pytest_cmd)
    if code == 0:
        print("PYTEST_END:OK", flush=True)
    else:
        print(f"PYTEST_END:FAIL CODE={code}", flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
