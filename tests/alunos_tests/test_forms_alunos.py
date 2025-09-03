from alunos.forms import AlunoForm


class TestAlunoForm:
    def test_form_valido(self):
        form = AlunoForm(
            data={
                "cpf": "12345678900",
                "nome": "João da Silva",
                "email": "joao@exemplo.com",
                "data_nascimento": "1990-01-01",
                "sexo": "M",
                "situacao": "ATIVO",
            }
        )
        assert form.is_valid()

    def test_form_invalido_campos_obrigatorios(self):
        form = AlunoForm(data={"email": "joao@exemplo.com"})
        assert not form.is_valid()
        assert "cpf" in form.errors
        assert "nome" in form.errors
        assert "data_nascimento" in form.errors

    def test_form_invalido_email(self):
        form = AlunoForm(
            data={
                "cpf": "12345678900",
                "nome": "João da Silva",
                "email": "email_invalido",
                "data_nascimento": "1990-01-01",
                "sexo": "M",
            }
        )
        assert not form.is_valid()
        assert "email" in form.errors


class TestAlunoForm:
    def test_form_valido(self):
        form = AlunoForm(
            data={
                "cpf": "12345678900",
                "nome": "João da Silva",
                "email": "joao@exemplo.com",
                "data_nascimento": "1990-01-01",
                "sexo": "M",
                "situacao": "ATIVO",
            }
        )
        assert form.is_valid()

    def test_form_invalido_campos_obrigatorios(self):
        form = AlunoForm(data={"email": "joao@exemplo.com"})
        assert not form.is_valid()
        assert "cpf" in form.errors
        assert "nome" in form.errors
        assert "data_nascimento" in form.errors

    def test_form_invalido_email(self):
        form = AlunoForm(
            data={
                "cpf": "12345678900",
                "nome": "João da Silva",
                "email": "email_invalido",
                "data_nascimento": "1990-01-01",
                "sexo": "M",
            }
        )
        assert not form.is_valid()
        assert "email" in form.errors
