import pytest
from django.contrib.auth.models import User
from alunos.models import Pais, Estado, Cidade, Bairro


@pytest.fixture(autouse=True)
def ensure_localidades_db(db):
    """Cria localidades mínimas para todos os testes (idempotente)."""
    Pais.objects.get_or_create(
        codigo="BRA",
        defaults={"nome": "Brasil", "nacionalidade": "Brasileira", "ativo": True},
    )
    estado, _ = Estado.objects.get_or_create(
        codigo="SP", defaults={"nome": "São Paulo", "regiao": "Sudeste"}
    )
    cidade, _ = Cidade.objects.get_or_create(nome="São Paulo", estado=estado)
    Bairro.objects.get_or_create(nome="Centro", cidade=cidade)


@pytest.fixture
def user(client, db):
    u = User.objects.create_user(username="tester", password="pass123")
    client.login(username="tester", password="pass123")
    return u


@pytest.fixture
def localidades(db):
    estado = Estado.objects.get(codigo="SP")
    cidade = Cidade.objects.get(nome="São Paulo", estado=estado)
    bairro = Bairro.objects.get(nome="Centro", cidade=cidade)
    pais = Pais.objects.get(codigo="BRA")
    return {"pais": pais, "estado": estado, "cidade": cidade, "bairro": bairro}
