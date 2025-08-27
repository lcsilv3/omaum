import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_pagina_criar_aluno(client, django_user_model):
    django_user_model.objects.create_user(username="u1", password="pw")
    client.login(username="u1", password="pw")
    resp = client.get(reverse("alunos:criar_aluno"))
    if resp.status_code != 200:
        # Ajuda diagnóstica temporária: mostra primeiro trecho do HTML
        inicio = resp.content[:500].decode("utf-8", errors="ignore")
        assert False, f"Status inesperado {resp.status_code}. Trecho resposta: {inicio}"
    content = resp.content.decode("utf-8")
    assert "<form" in content
    assert ("Cadastrar" in content) or ("Atualizar" in content)
    assert "Selecione" in content
