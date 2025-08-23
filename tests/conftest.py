"""
Configurações globais para testes otimizados.
"""

import pytest
import django
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client
from django.core.management import call_command
from django.db import connection
import tempfile
import shutil
from unittest.mock import patch

django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """Configuração do banco de dados para a sessão (já em settings_test)."""
    # Nada extra: settings_test já define DB em memória.
    return
 

@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """Configuração global do ambiente de teste."""
    # Criar diretório temporário para media
    temp_media = tempfile.mkdtemp()
    settings.MEDIA_ROOT = temp_media
    
    yield
    
    # Cleanup
    shutil.rmtree(temp_media, ignore_errors=True)
 

@pytest.fixture(scope='session', autouse=True)
def ensure_migrations_applied(django_db_setup, django_db_blocker):
    """Garante que migrações essenciais (alunos) foram aplicadas no DB em memória."""
    with django_db_blocker.unblock():
        existing = set(connection.introspection.table_names())
        if 'alunos_aluno' not in existing:
            call_command('migrate', 'alunos', interactive=False, verbosity=0)
        # Garantir tabelas iniciaticos (não críticas se unmanaged) somente se faltar
        if 'alunos_tipocodigo' not in existing:
            # Rodar migrações globais se necessário
            call_command('migrate', interactive=False, verbosity=0)


@pytest.fixture
def usuario_autenticado(db):
    """Cria um usuário e retorna um cliente autenticado."""
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    client = Client()
    client.login(username='testuser', password='testpassword')
    return client, user
 

@pytest.fixture
def usuario_admin(db):
    """Cria um usuário administrador e retorna um cliente autenticado."""
    admin = User.objects.create_superuser(username='admin', password='adminpassword', email='admin@example.com')
    client = Client()
    client.login(username='admin', password='adminpassword')
    return client, admin
 

@pytest.fixture
def usuario_sem_permissoes(db):
    """Cria um usuário sem permissões especiais."""
    user = User.objects.create_user(username='noperms', password='noperms', email='noperms@example.com')
    client = Client()
    client.login(username='noperms', password='noperms')
    return client, user
 

@pytest.fixture
def client_nao_autenticado():
    """Cliente não autenticado."""
    return Client()
 

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Habilita acesso ao banco de dados para todos os testes."""
    return None
 

@pytest.fixture
def fast_password_hasher():
    """Usa hasher rápido para testes."""
    with patch('django.contrib.auth.hashers.make_password') as mock_hash:
        mock_hash.return_value = 'hashed_password'
        yield mock_hash
 

@pytest.fixture
def mock_send_email():
    """Mock para envio de emails."""
    with patch('django.core.mail.send_mail') as mock_mail:
        yield mock_mail



