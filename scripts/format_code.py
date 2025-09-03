"""Script para formatar automaticamente o código Python.

Este script monitora alterações nos arquivos Python e aplica formatação automática
usando black, isort e flake8.
"""

import time
import sys
from pathlib import Path
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class CodeFormatter(FileSystemEventHandler):
    """Manipulador de eventos para formatar código automaticamente."""

    def __init__(self):
        self.last_modified = {}

    def on_modified(self, event):
        if event.is_directory:
            return

        # Evita processar o mesmo arquivo múltiplas vezes em um curto período
        if event.src_path in self.last_modified:
            if time.time() - self.last_modified[event.src_path] < 1:
                return

        if event.src_path.endswith(".py"):
            self.format_file(event.src_path)
            self.last_modified[event.src_path] = time.time()

    def format_file(self, file_path):
        """Aplica formatação e lint usando Ruff em um arquivo Python."""
        print(f"\n🔄 Formatando e verificando {file_path} com Ruff...")
        try:
            # Formata o arquivo com Ruff
            subprocess.run(
                [sys.executable, "-m", "ruff", "format", file_path],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            print("✅ Ruff: Formatação aplicada")
            # Verifica problemas de lint com Ruff
            result = subprocess.run(
                [sys.executable, "-m", "ruff", "check", file_path],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if result.returncode == 0:
                print("✅ Ruff: Nenhum problema de lint encontrado")
            else:
                print("⚠️ Ruff encontrou problemas:")
                if result.stdout:
                    for line in result.stdout.splitlines():
                        print(f"  {line}")
                else:
                    print(
                        "⚠️ Ruff não retornou saída padrão (stdout). Verifique possíveis problemas de encoding ou execução."
                    )
            print("✨ Verificação concluída!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao rodar Ruff: {e}")
            if e.stdout:
                print(f"Saída: {e.stdout}")
            if e.stderr:
                print(f"Erro: {e.stderr}")


def watch_directory(path):
    """Inicia o monitoramento do diretório."""
    print(f"🔍 Monitorando alterações em: {path}")
    event_handler = CodeFormatter()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n⏹️ Monitoramento interrompido")

    observer.join()


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    watch_directory(project_root)
