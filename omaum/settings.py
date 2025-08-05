"""
Configurações do projeto OMAUM.
Este arquivo contém as configurações principais do Django, incluindo:
- Configurações de segurança
- Aplicativos instalados
- Configurações de middleware
- Configurações de banco de dados
- Configurações de internacionalização
- Configurações de arquivos estáticos e mídia
"""

# Importações e configurações existentes
import os
from pathlib import Path
import secrets

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY será definido na seção de segurança abaixo

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "testserver"]

# ===== CONFIGURAÇÕES DE SEGURANÇA =====

# Configurações de segurança para produção
# Estas configurações devem ser ajustadas conforme o ambiente

# HSTS (HTTP Strict Transport Security)
# Define por quanto tempo o navegador deve lembrar que o site deve usar HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 ano em segundos
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL/HTTPS
# Redireciona automaticamente HTTP para HTTPS
SECURE_SSL_REDIRECT = not DEBUG  # Apenas em produção

# Cookies seguros
# Garante que os cookies só sejam enviados via HTTPS
SESSION_COOKIE_SECURE = not DEBUG  # Apenas em produção
CSRF_COOKIE_SECURE = not DEBUG     # Apenas em produção

# Configurações adicionais de segurança
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuração da SECRET_KEY mais segura
# IMPORTANTE: Em produção, use uma variável de ambiente
if DEBUG:
    # Para desenvolvimento, mantém uma chave consistente
    SECRET_KEY = "django-insecure-dev-key-change-in-production-" + "x" * 20
else:
    # Para produção, use uma variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_urlsafe(50))

# Configuração de hosts permitidos mais restritiva
if not DEBUG:
    ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "testserver"]

# ===== FIM DAS CONFIGURAÇÕES DE SEGURANÇA =====

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Aplicações do projeto
    "core",
    "alunos",
    "atividades",
    "cursos",
    "frequencias",
    "matriculas",
    "notas",
    "pagamentos",
    "presencas",
    "relatorios",
    "turmas",
    # Third party apps
    "rest_framework",
    "widget_tweaks",
    "django_select2",
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # Verifique por middlewares personalizados aqui
]

ROOT_URLCONF = "omaum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "omaum", "templates"),
            os.path.join(BASE_DIR, "matriculas", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "omaum.context_processors.pagamentos_context",
                # Novo context processor
            ],
        },
    },
]  # Este colchete estava na linha errada

# Correção de linha longa em WSGI_APPLICATION
WSGI_APPLICATION = "omaum.wsgi.application"  # Esta linha deve começar sem o colchete

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]

# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# Configurações de autenticação
LOGIN_URL = "/entrar/"
# Adicionar estas linhas para resolver o problema de redirecionamento
LOGIN_REDIRECT_URL = "/"  # Redireciona para a página inicial após o login
LOGOUT_REDIRECT_URL = "/"  # Redireciona para a página inicial após o logout

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": ("{levelname} {asctime} {module} {message}"),
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/django.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "presencas.views_ext.registro_presenca": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "alunos.services": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "presencas.api": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Configurações do Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "presencas_api": "100/hour",
    },
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# Remover Debug Toolbar temporariamente
if "debug_toolbar" in INSTALLED_APPS:
    INSTALLED_APPS.remove("debug_toolbar")

if "debug_toolbar.middleware.DebugToolbarMiddleware" in MIDDLEWARE:
    MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

# Configuração para evitar interferência do Debug Toolbar em requisições AJAX
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": (lambda request: False if request.is_ajax() else True),
}
