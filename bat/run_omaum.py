"""Utilitário para inicializar o servidor de desenvolvimento do Omaum no Windows."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SERVER_URL = "http://127.0.0.1:8000/"


def resolver_python() -> str:
    """Retorna o executável Python preferencial, usando a virtualenv local quando disponível."""

    venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable or "python"


def iniciar_servidor(python_cmd: str) -> subprocess.Popen[str]:
    """Inicia o servidor Django e devolve o processo ativo."""

    manage_py = PROJECT_ROOT / "manage.py"
    comando = [python_cmd, str(manage_py), "runserver"]
    return subprocess.Popen(
        comando,
        cwd=PROJECT_ROOT,
        stdout=None,
        stderr=None,
        text=True,
        creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        if sys.platform == "win32"
        else 0,
    )


def encerrar_servidor(process: subprocess.Popen[str]) -> None:
    """Finaliza o processo do servidor de forma graciosa."""

    if process.poll() is not None:
        return
    if sys.platform == "win32":
        process.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


def main() -> None:
    """Executa o fluxo completo: seleciona Python, inicia server e abre o navegador."""

    os.chdir(PROJECT_ROOT)
    python_cmd = resolver_python()

    servidor = iniciar_servidor(python_cmd)
    time.sleep(2)

    if servidor.poll() is not None:
        print("Falha ao iniciar o servidor Django. Verifique os logs no terminal.")
        return

    webbrowser.open(SERVER_URL)
    print("Servidor em execução. Pressione Ctrl+C para encerrar.")

    try:
        servidor.wait()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
        encerrar_servidor(servidor)


if __name__ == "__main__":
    main()
