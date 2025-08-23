import pytest
from django.test import RequestFactory
from alunos.forms import AlunoForm

@pytest.mark.django_db
def test_aluno_form_render_basic():
    form = AlunoForm()
    html = form.as_p()
    # Campos essenciais devem existir no HTML
    for name in [
        'nome','cpf','email','data_nascimento','sexo','situacao','estado','cidade','cep'
    ]:
        assert f'id_{name}' in html, f'Campo {name} não renderizado'
    # Placeholder 'Selecione' deve aparecer pelo menos uma vez
    assert 'Selecione' in html
