import pytest
from django.urls import reverse
from alunos.models import Aluno
from alunos.utils import get_codigo_model, get_tipo_codigo_model
from django.contrib.auth.models import User, Permission


@pytest.mark.django_db
def test_adicionar_registro_historico(client):
    # Cria usuário e autentica
    user = User.objects.create_user(
        username="testuser", password="testpass", is_staff=True, is_active=True
    )
    perms = Permission.objects.filter(
        codename__in=["change_aluno", "view_aluno", "add_aluno"]
    )
    user.user_permissions.set(perms)
    client.login(username="testuser", password="testpass")

    # Cria um TipoCodigo válido e associa ao Codigo
    TipoCodigo = get_tipo_codigo_model()
    Codigo = get_codigo_model()
    assert TipoCodigo and Codigo, "Modelos iniciáticos indisponíveis"
    tipo_codigo = TipoCodigo.objects.create(nome="TESTE", descricao="Tipo de teste")
    codigo = Codigo.objects.create(tipo_codigo=tipo_codigo, nome="Código Teste")

    # Cria um aluno de teste
    aluno = Aluno.objects.create(
        cpf="12345678901",
        nome="Teste",
        email="teste@exemplo.com",
        data_nascimento="2000-01-01",
        sexo="M",
        situacao="ATIVO",
    )
    url = reverse("alunos:editar_aluno", args=[aluno.cpf])
    response = client.get(url)
    if response.status_code == 302:
        destino = response.get("Location", None)
        pytest.fail(f"Redirecionado para: {destino}")
    assert response.status_code == 200
    # Simula adição de registro histórico via POST
    data = {
        "cpf": aluno.cpf,
        "nome": aluno.nome,
        "email": aluno.email,
        "data_nascimento": aluno.data_nascimento,
        "sexo": aluno.sexo,
        "situacao": aluno.situacao,
        "nacionalidade": "Brasileiro",
        "naturalidade": "São Paulo",
        "historico-TOTAL_FORMS": "1",
        "historico-INITIAL_FORMS": "0",
        "historico-MIN_NUM_FORMS": "0",
        "historico-MAX_NUM_FORMS": "20",
        "historico-0-id": "",
        "historico-0-codigo": str(codigo.pk),
        "historico-0-ordem_servico": "OS123",
        "historico-0-data_os": "2025-07-12",
        "historico-0-numero_iniciatico": "001",
        "historico-0-nome_iniciatico": "Primeiro",
        "historico-0-observacoes": "Teste automático",
        "historico-0-ativo": "True",
    }
    response = client.post(url, data)
    if response.status_code != 302:
        # Tenta extrair erros do form e do formset do contexto
        try:
            form = response.context.get("form")
            historico_formset = response.context.get("historico_formset")
            form_errors = getattr(form, "errors", None)
            formset_errors = getattr(historico_formset, "errors", None)
            print("Form errors:", form_errors)
            print("Formset errors:", formset_errors)
        except Exception as e:
            print("Erro ao extrair erros do contexto:", e)
        # Exibe o HTML completo para depuração
        pytest.fail(
            f"Status code: {response.status_code}. HTML:\n{response.content.decode(errors='ignore')}"
        )
    assert response.status_code == 302  # Redireciona após salvar
