"""
Configurações de teste otimizadas para máxima velocidade.
"""

import sys
from pathlib import Path

# Adicionar o diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importar configurações base
try:
    from omaum.settings import *
except ImportError:
    # Configurações básicas se não conseguir importar
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = 'test-secret-key'
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'alunos',
        'cursos',
        'matriculas',
        'turmas',
        'presencas',
    ]

# Banco de dados em memória para velocidade máxima
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Desabilitar migrações desnecessárias


class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Configurações para testes rápidos
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Desabilitar cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Configurações de email para testes
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Desabilitar logs desnecessários
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}

# Configurações de media para testes
MEDIA_ROOT = '/tmp/omaum_test_media'

# Desabilitar collectstatic
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configurações de teste específicas
TESTING = True
DEBUG = False
