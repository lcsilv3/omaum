import pytest
from alunos.models import Aluno
from django.core.exceptions import ValidationError
from django.db import IntegrityError

@pytest.mark.django_db
class TestAlunoModel:
    """Testes para o modelo Aluno."""
    
    def test_criar_aluno_valido(self):
        """Testa a criação de um aluno com dados válidos."""
        aluno = Aluno.objects.create(
            cpf="12345678900",
            nome="João da Silva",
            email="joao@exemplo.com",
            data_nascimento="1990-01-01",
            sexo="M",
            situacao="ativo"
        )
        assert aluno.pk is not None
        assert aluno.nome == "João da Silva"
        assert aluno.cpf == "12345678900"
    
    def test_cpf_unico(self):
        """Testa se o CPF é único."""
        Aluno.objects.create(
            cpf="12345678900",
            nome="João da Silva",
            email="joao@exemplo.com",
            data_nascimento="1990-01-01"
        )
        
        with pytest.raises(IntegrityError):
            Aluno.objects.create(
                cpf="12345678900",  # CPF duplicado
                nome="Maria Souza",
                email="maria@exemplo.com",
                data_nascimento="1992-05-15"
            )
    
    def test_aluno_str(self):
        """Testa a representação string do aluno."""
        aluno = Aluno.objects.create(
            cpf="12345678900",
            nome="João da Silva",
            email="joao@exemplo.com",
            data_nascimento="1990-01-01"
        )
        assert str(aluno) == "João da Silva"