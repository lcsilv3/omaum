import pytest
from alunos.forms import AlunoForm
from datetime import date

class TestAlunoForm:
    """Testes para o formulário de Aluno."""
    
    def test_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            'cpf': '12345678900',
            'nome': 'João da Silva',
            'email': 'joao@exemplo.com',
            'data_nascimento': '1990-01-01',
            'sexo': 'M',
            'situacao': 'ativo',
        }
        form = AlunoForm(data=form_data)
        assert form.is_valid(), f"Formulário inválido: {form.errors}"
    
    def test_form_invalido_campos_obrigatorios(self):
        """Testa se o formulário é inválido quando campos obrigatórios estão ausentes."""
        form_data = {
            'email': 'joao@exemplo.com',
        }
        form = AlunoForm(data=form_data)
        assert not form.is_valid()
        assert 'cpf' in form.errors
        assert 'nome' in form.errors
        assert 'data_nascimento' in form.errors
    
    def test_form_invalido_email(self):
        """Testa se o formulário é inválido com email incorreto."""
        form_data = {
            'cpf': '12345678900',
            'nome': 'João da Silva',
            'email': 'email_invalido',
            'data_nascimento': '1990-01-01',
            'sexo': 'M',
        }
        form = AlunoForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors
    
    def test_form_data_nascimento_futura(self):
        """Testa se o formulário rejeita datas de nascimento futuras."""
        future_date = date.today().replace(year=date.today().year + 1).strftime('%Y-%m-%d')
        form_data = {
            'cpf': '12345678900',
            'nome': 'João da Silva',
            'email': 'joao@exemplo.com',
            'data_nascimento': future_date,
            'sexo': 'M',
        }
        form = AlunoForm(data=form_data)
        assert not form.is_valid()
        assert 'data_nascimento' in form.errors