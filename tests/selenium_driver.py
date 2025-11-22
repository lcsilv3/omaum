"""Utilitários para inicializar WebDriver de forma compatível com a versão do Chrome instalada."""

from __future__ import annotations

import os
from pathlib import Path

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def _local_driver_path() -> str | None:
    """Retorna caminho para driver local configurado via env ou pasta drivers."""

    env_path = os.environ.get("CHROMEDRIVER_PATH")
    if env_path:
        resolved = Path(env_path).expanduser().resolve()
        if resolved.is_file():
            return str(resolved)

    repo_driver = (
        Path(__file__).resolve().parent.parent / "drivers" / "chromedriver.exe"
    )
    if repo_driver.is_file():
        return str(repo_driver)

    return None


def get_chrome_service() -> Service:
    """Retorna um Service configurado com o ChromeDriver adequado."""

    local_driver = _local_driver_path()
    if local_driver:
        return Service(local_driver)

    try:
        driver_path = ChromeDriverManager().install()
    except Exception as exc:  # pragma: no cover - apenas em ambientes offline
        raise RuntimeError(
            "Falha ao baixar o ChromeDriver automaticamente. "
            "Informe CHROMEDRIVER_PATH ou coloque o binário em drivers/."
        ) from exc

    return Service(driver_path)
