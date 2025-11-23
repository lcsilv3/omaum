#!/usr/bin/env python
"""Wrapper para executar scripts do projeto localmente com PYTHONPATH configurado.

Uso:
  python scripts/run_local.py scripts/popular_codigos_por_tipo.py

O wrapper procura em ordem:
 - venv\Scripts\python.exe (na raiz do repositório)
 - py -3 (launcher do Windows)
 - python (PATH)

Ele configura PYTHONPATH para a raiz do repositório e então executa o script alvo.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VENV_PY = REPO_ROOT / "venv" / "Scripts" / "python.exe"


def find_python():
    candidates = [str(VENV_PY), "py -3", "python"]

    def candidate_exec(cmd):
        """Retorna uma lista de tokens para executar o candidato."""
        if cmd == "py -3":
            return ["py", "-3"]
        parts = cmd.split()
        return parts

    def is_working(cmd):
        parts = candidate_exec(cmd)
        try:
            # testa import básico
            proc = subprocess.run(parts + ["-c", "import sys; print(sys.executable)"],
                                  cwd=REPO_ROOT,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=5)
            return proc.returncode == 0
        except Exception:
            return False

    for c in candidates:
        # se for caminho absoluto
        if os.path.isabs(c) and Path(c).exists():
            if is_working(c):
                return c
            continue
        # senão tente localizar no PATH
        which = shutil.which(c.split()[0])
        if which:
            # se for o launcher `py`, retorne exatamente 'py -3' se funcional
            if c.startswith("py"):
                if is_working("py -3"):
                    return "py -3"
                continue
            if is_working(which):
                return which
    return None


def run_script(python_exec, script_path, args):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    cmd = []
    if python_exec == "py -3":
        cmd = ["py", "-3", str(script_path)] + args
    else:
        cmd = [python_exec, str(script_path)] + args
    print(f"Executando: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, cwd=REPO_ROOT, env=env)
    proc.communicate()
    return proc.returncode


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/run_local.py <script_relativo>")
        sys.exit(2)
    script_rel = sys.argv[1]
    script_path = (REPO_ROOT / script_rel).resolve()
    if not script_path.exists():
        print(f"Script não encontrado: {script_path}")
        sys.exit(1)

    python_exec = find_python()
    if not python_exec:
        print("Nenhum interpretador Python encontrado. Instale Python 3.8+ e/ou crie o venv.")
        sys.exit(3)

    rc = run_script(python_exec, script_path, sys.argv[2:])
    if rc != 0:
        print(f"Script retornou código {rc}")
    sys.exit(rc)


if __name__ == '__main__':
    main()
