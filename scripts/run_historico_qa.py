"""Execução rápida do checklist de QA do histórico.

Passos executados:
1. ``python manage.py migrate --noinput``
2. ``pytest alunos/tests -k historico --no-cov --cov-fail-under=0``

Saída amigável para acompanhar o status de cada etapa.
"""

from __future__ import annotations

import os
import subprocess
import sys
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = PROJECT_ROOT / "logs" / "historico_suite.log"


def _ensure_log_dir() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def log(message: str) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(formatted + "\n")


def run_step(command: list[str], label: str, env: dict[str, str] | None = None) -> None:
    """Executa um comando exibindo rótulo e status."""
    log(f"\n==> {label}")
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    if completed.stdout:
        for line in completed.stdout.splitlines():
            log(f"{label}: {line}")

    if completed.stderr:
        for line in completed.stderr.splitlines():
            log(f"{label} [stderr]: {line}")

    if completed.returncode == 0:
        log(f"✔ {label} concluído com sucesso.")
    else:
        log(f"✖ {label} falhou (código {completed.returncode}).")
        raise SystemExit(completed.returncode)


def _ensure_testing_dependencies() -> None:
    """Garante que pytest e pytest-django estejam disponíveis."""
    log("\n==> Verificando dependências de teste")
    missing_modules: list[str] = []

    for module_name in ("pytest", "pytest_django"):
        if importlib.util.find_spec(module_name) is None:
            missing_modules.append(module_name)

    if missing_modules:
        log("✖ Dependências de teste ausentes: " + ", ".join(sorted(missing_modules)))
        log("Instale-as com: pip install pytest pytest-django")
        raise SystemExit(1)

    log("✔ Dependências de teste disponíveis.")


def main() -> int:
    _ensure_log_dir()
    log("Iniciando checklist de histórico")
    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")

    run_step(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        "Aplicando migrações",
        env=env,
    )

    pytest_env = env.copy()
    pytest_env.setdefault("DJANGO_SETTINGS_MODULE", "tests.configs.settings_test")

    _ensure_testing_dependencies()

    run_step(
        [
            sys.executable,
            "-m",
            "pytest",
            "alunos/tests",
            "-k",
            "historico",
            "--no-cov",
            "--cov-fail-under=0",
        ],
        "Executando testes de histórico",
        env=pytest_env,
    )

    log("Checklist do histórico finalizado com sucesso!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
