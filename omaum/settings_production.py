"""
Configurações específicas para teste de deploy e produção.
Este arquivo pode ser usado para testar as configurações de segurança.
"""

import os
import secrets

# Importa todas as configurações do settings.py principal
from .settings import *  # noqa: F403

# Sobrescreve configurações específicas para produção/teste
DEBUG = False

# Configurações de segurança forçadas para teste
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# SECRET_KEY segura para teste
SECRET_KEY = secrets.token_urlsafe(50)

# Hosts permitidos para teste
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "testserver", "exemplo.com"]

# Configurações de logging para produção
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Criar diretório de logs se não existir
os.makedirs(BASE_DIR / "logs", exist_ok=True)
