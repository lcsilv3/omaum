import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_search_estados(user, localidades, client):
    # usa minusculo sem acento para validar fallback acento-insensível
    url = reverse("alunos:api_search_estados") + "?q=paulo"
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data and any("São Paulo" == e["nome"] for e in data)


def test_search_cidades(user, localidades, client):
    url = (
        reverse("alunos:api_search_cidades")
        + "?q=paulo&estado_id="
        + str(localidades["estado"].id)
    )
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data and any(c["nome"] == "São Paulo" for c in data)


def test_get_cidades_por_estado(user, localidades, client):
    url = reverse("alunos:api_cidades_por_estado", args=[localidades["estado"].id])
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert any("São Paulo" in c["nome"] for c in data)


def test_search_bairros(user, localidades, client):
    url = (
        reverse("alunos:api_search_bairros")
        + "?q=cent&cidade_id="
        + str(localidades["cidade"].id)
    )
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data and any(b["nome"] == "Centro" for b in data)


def test_get_bairros_por_cidade(user, localidades, client):
    url = reverse("alunos:api_bairros_por_cidade", args=[localidades["cidade"].id])
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert any("Centro" in b["nome"] for b in data)
