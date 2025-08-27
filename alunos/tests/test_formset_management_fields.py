import pytest
from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
def test_formset_management_fields_present():
    """
    Testa se os campos de controle do formset de histórico SEMPRE aparecem no HTML,
    tanto em GET quanto em POST com erro de validação.
    """
    client = Client()
    # Cria usuário se não existir
    from django.contrib.auth.models import User

    username = "lcsilv3"
    password = "iG356900"
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    # 1. GET: Novo aluno autenticado
    url = reverse("alunos:criar_aluno")
    response = client.get(url)
    html = response.content.decode()
    with open("html_dump_formset_get.html", "w", encoding="utf-8") as f:
        f.write(html)
    assert 'name="historico-TOTAL_FORMS"' in html, "Campo TOTAL_FORMS ausente no GET"
    assert (
        'name="historico-INITIAL_FORMS"' in html
    ), "Campo INITIAL_FORMS ausente no GET"
    assert (
        'name="historico-MIN_NUM_FORMS"' in html
    ), "Campo MIN_NUM_FORMS ausente no GET"
    assert (
        'name="historico-MAX_NUM_FORMS"' in html
    ), "Campo MAX_NUM_FORMS ausente no GET"

    # 2. POST: Envia dados inválidos para forçar erro de validação
    post_data = {
        "cpf": "",  # campo obrigatório vazio
        "nome": "",
        "data_nascimento": "",
        "historico-TOTAL_FORMS": "1",
        "historico-INITIAL_FORMS": "0",
        "historico-MIN_NUM_FORMS": "0",
        "historico-MAX_NUM_FORMS": "20",
        "historico-0-codigo": "",
        "historico-0-ordem_servico": "",
        "historico-0-data_os": "",
        "historico-0-numero_iniciatico": "",
        "historico-0-nome_iniciatico": "",
        "historico-0-observacoes": "",
    }
    response = client.post(url, post_data)
    html = response.content.decode()
    assert 'name="historico-TOTAL_FORMS"' in html, "Campo TOTAL_FORMS ausente no POST"
    assert (
        'name="historico-INITIAL_FORMS"' in html
    ), "Campo INITIAL_FORMS ausente no POST"
    assert (
        'name="historico-MIN_NUM_FORMS"' in html
    ), "Campo MIN_NUM_FORMS ausente no POST"
    assert (
        'name="historico-MAX_NUM_FORMS"' in html
    ), "Campo MAX_NUM_FORMS ausente no POST"
