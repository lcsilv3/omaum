from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "omaum_prod"),
        "USER": os.environ.get("POSTGRES_USER", "omaum_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": "omaum-db",
        "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://omaum-redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.environ.get("REDIS_PASSWORD", ""),
        },
    }
}

SECRET_KEY = os.environ.get("SECRET_KEY")

# Em produção, não usamos STATICFILES_DIRS - todos estáticos vêm dos apps
STATICFILES_DIRS = []

STATIC_ROOT = "/app/static"
STATIC_URL = "/static/"

MEDIA_ROOT = "/app/media"
MEDIA_URL = "/media/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

ENVIRONMENT_LABEL = "Ambiente de Produção"
ENVIRONMENT_BADGE_CLASSES = "bg-danger text-white"
ENVIRONMENT_HINT = "Use credenciais oficiais."
ENVIRONMENT_SHOW_BANNER = True
