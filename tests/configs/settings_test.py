"""
Configurações de teste otimizadas para máxima velocidade.
"""

import sys
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

# Settings de teste mínimos (evita wildcard import para lint limpo)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(f"[DEBUG] BASE_DIR usado nos testes: {BASE_DIR}")
SECRET_KEY = "test-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = True
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "atividades",
    "frequencias",
    "notas",
    "pagamentos",
    "relatorios",
    "alunos",
    "cursos",
    "matriculas",
    "turmas",
    "presencas",
    "rest_framework",
    "widget_tweaks",
    "django_select2",
    "django_extensions",
]

# Banco de dados em memória para velocidade máxima
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "omaum.urls"

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "omaum" / "templates"),
            str(BASE_DIR / "omaum" / "templates" / "registration"),
            str(BASE_DIR / "matriculas" / "templates"),
            str(BASE_DIR / "tests" / "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "string_if_invalid": "",
            "builtins": [],
            "loaders": [
                (
                    "django.template.loaders.filesystem.Loader",
                    [
                        str(BASE_DIR / "omaum" / "templates"),
                        str(BASE_DIR / "omaum" / "templates" / "base copy.html"),
                    ],
                ),
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Desabilitar migrações desnecessárias


# Ativamos migrações reais para apps críticos usados nos testes (alunos, iniciaticos)
# e desabilitamos para o restante para manter velocidade.
class PartialDisableMigrations(dict):
    def __contains__(self, item):  # noqa: D401
        return True


MIGRATION_MODULES = {
    # Mantemos migrações reais para 'alunos'. Desativamos outros grandes temporariamente.
    "cursos": None,
    "matriculas": None,
    "turmas": None,
    "presencas": None,
    "core": None,
    "atividades": None,
    "frequencias": None,
    "notas": None,
    "pagamentos": None,
    "relatorios": None,
}

# TODO: Avaliar remoção deste bloqueio parcial de migrações após estabilização
# do desempenho dos testes de alunos (benchmark alvo < Xs). Manter apenas se
# ganho for significativo; caso contrário usar migrações reais para detectar
# alterações de schema inadvertidas.

# Configurações para testes rápidos
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Desabilitar cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Configurações de email para testes
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Desabilitar logs desnecessários
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
        },
    },
}

# Configurações de media para testes
MEDIA_ROOT = "/tmp/omaum_test_media"


# Configuração de arquivos estáticos para testes
STATIC_URL = "/static/"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Configurações de teste específicas
TESTING = True
DEBUG = False
