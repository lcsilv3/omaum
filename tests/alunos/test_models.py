import pytest
from alunos.services import criar_aluno
from django.db import IntegrityError

@pytest.mark.django_db
class TestAlunoModel:
    """Testes para o modelo Aluno, utilizando a camada de serviço."""

    def test_criar_aluno_valido(self):
        """Testa a criação de um aluno com dados válidos através do serviço."""
        aluno_data = {
            "cpf": "12345678900",
            "nome": "João da Silva",
            "email": "joao@exemplo.com",
            "data_nascimento": "1990-01-01",
            "sexo": "M",
            "situacao": "ATIVO"
        }
        aluno = criar_aluno(aluno_data)
        assert aluno is not None
        assert aluno.pk is not None
        assert aluno.nome == "João da Silva"
        assert aluno.cpf == "12345678900"

    def test_cpf_unico(self):
        """Testa se o serviço impede a criação de um aluno com CPF duplicado."""
        aluno_data_1 = {
            "cpf": "12345678900",
            "nome": "João da Silva",
            "email": "joao@exemplo.com",
            "data_nascimento": "1990-01-01"
        }
        criar_aluno(aluno_data_1)

        aluno_data_2 = {
            "cpf": "12345678900",  # CPF duplicado
            "nome": "Maria Souza",
            "email": "maria@exemplo.com",
            "data_nascimento": "1992-05-15"
        }
        # O serviço deve retornar None ao falhar por violação de unicidade
        aluno_duplicado = criar_aluno(aluno_data_2)
        assert aluno_duplicado is None

    def test_aluno_str(self):
        """Testa a representação string do aluno criado via serviço."""
        aluno_data = {
            "cpf": "12345678900",
            "nome": "João da Silva",
            "email": "joao@exemplo.com",
            "data_nascimento": "1990-01-01"
        }
        aluno = criar_aluno(aluno_data)
        assert str(aluno) == "João da Silva"