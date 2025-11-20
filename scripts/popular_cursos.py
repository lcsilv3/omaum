#!/usr/bin/env python
"""Sincroniza cursos utilizando a planilha oficial do projeto."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional, Union

import django


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.development")

django.setup()

from scripts.manutencao.sincronizar_cursos import (  # noqa: E402  # pylint: disable=wrong-import-position
    executar_sincronizacao,
)


def popular_cursos(
    arquivo: Optional[Union[str, Path]] = None,
    manter_existentes: bool = True,
) -> None:
    """Executa a sincronização de cursos a partir da planilha informada."""

    caminho = Path(arquivo) if arquivo else None
    executar_sincronizacao(caminho, manter_existentes)


if __name__ == "__main__":
    print("Iniciando sincronização de cursos...")
    popular_cursos(manter_existentes=True)
    print("Sincronização concluída.")
