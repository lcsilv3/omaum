import pytest
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
def test_minimal_get_criar_aluno():
    client = Client()
    url = reverse("alunos:criar_aluno")
    response = client.get(url)
    html = response.content.decode()
    with open("html_dump_minimal_get.html", "w", encoding="utf-8") as f:
        f.write(html)
    assert response.status_code == 200, f"Status code: {response.status_code}"
    assert html.strip() != "", "HTML vazio na resposta do GET minimal"
