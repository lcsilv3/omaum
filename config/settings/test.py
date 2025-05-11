"""
Configurações de teste para o projeto OMAUM.
"""

from .base import *  # Importe as configurações base

# Sobrescreva as configurações necessárias para testes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
}

# Desabilitar cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Configurar o backend de e-mail para testes
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Configurações de mídia para testes
MEDIA_ROOT = BASE_DIR / 'media_test'

# Configurações de arquivos estáticos para testes
STATIC_ROOT = BASE_DIR / 'static_test'

# Configurações adicionais para testes
DEBUG = False
TEMPLATE_DEBUG = False
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())