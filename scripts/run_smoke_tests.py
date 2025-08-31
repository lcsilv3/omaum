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

# Garante que o diretório do projeto está no sys.path
import pathlib

project_root = pathlib.Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def main() -> int:
    # Forçar settings de teste do Django e limpar variáveis conflitantes
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.configs.settings_test"
    os.environ.pop("PYTHONPATH", None)

    # Comando pytest base (sem cobertura para reduzir ruído)
    pytest_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-rA",
    ]

    # Debug: mostrar variáveis de ambiente e sys.path
    print(
        f"[DEBUG] DJANGO_SETTINGS_MODULE={os.environ.get('DJANGO_SETTINGS_MODULE')}",
        flush=True,
    )
    print(f"[DEBUG] sys.path={sys.path}", flush=True)

    # Filtro padrão: smoke test de edição em lote
    # Permite sobrescrever via argumentos
    if len(sys.argv) > 1:
        # Passa os argumentos como estão para o pytest após os padrões
        pytest_cmd.extend(sys.argv[1:])
    else:
        pytest_cmd.extend(
            [
                "presencas/tests/test_edicao_lote_ajax_smoke.py",
                "-k",
                "edicao_lote_ajax_smoke",
            ]
        )

    print("PYTEST_START", flush=True)
    code = subprocess.call(pytest_cmd)
    if code == 0:
        print("PYTEST_END:OK", flush=True)
    else:
        print(f"PYTEST_END:FAIL CODE={code}", flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
