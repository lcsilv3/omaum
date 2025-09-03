"""Watcher de testes: executa pytest quando arquivos em 'presencas/' mudam.

Requisitos: watchdog, pytest
Executar via venv do projeto para usar dependências corretas.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path
from threading import Event, Thread

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


ROOT = Path(__file__).resolve().parent.parent
WATCH_DIR = ROOT / "presencas"


class DebouncedRunner(FileSystemEventHandler):
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self._last_run = 0.0
        self._pending = Event()
        self._thread = Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        while True:
            self._pending.wait()
            # Debounce window
            time.sleep(self.delay)
            self._pending.clear()
            self.run_tests()

    def on_modified(self, event):  # type: ignore[override]
        if event.is_directory:
            return
        if not event.src_path.endswith(".py"):
            return
        if "__pycache__" in event.src_path:
            return
        self._pending.set()

    def run_tests(self):
        print("\n🧪 Executando testes rápidos de presenças...")
        try:
            # Escopo focado para ser rápido
            cmd = [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "-n",  # Desativa o pytest-xdist para evitar erros de concorrência no watcher
                "0",
                "presencas/tests",
                "-k",
                "presencas or edicao_lote or ajax",
            ]
            subprocess.run(cmd, cwd=str(ROOT), check=False)
        except Exception as e:
            print(f"❌ Falha ao executar testes: {e}")


def main():
    print(f"👀 Observando alterações em: {WATCH_DIR}")
    observer = Observer()
    handler = DebouncedRunner(delay=0.6)
    observer.schedule(handler, str(WATCH_DIR), recursive=True)
    observer.start()
    print(
        "✅ Watch de testes iniciado. Salve um arquivo em 'presencas/' para disparar."
    )
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n⏹️ Watcher encerrado")
    observer.join()


if __name__ == "__main__":
    main()
