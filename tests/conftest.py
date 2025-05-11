import pytest
from django.contrib.auth.models import User
from django.test import Client

@pytest.fixture
def usuario_autenticado():
    """Cria um usuário e retorna um cliente autenticado."""
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='test@example.com'
    )
    client = Client()
    client.login(username='testuser', password='testpassword')
    return client, user

@pytest.fixture
def usuario_admin():
    """Cria um usuário administrador e retorna um cliente autenticado."""
    admin = User.objects.create_superuser(
        username='admin',
        password='adminpassword',
        email='admin@example.com'
    )
    client = Client()
    client.login(username='admin', password='adminpassword')
    return client, admin