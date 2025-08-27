import pytest
from turmas.models import Turma
from django.utils import timezone
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestTurmaModel:
    """Testes para o modelo Turma."""

    def test_criar_turma(self):
        """Testa a criação de uma turma."""
        from cursos.models import Curso

        curso = Curso.objects.create(nome="Curso Teste")
        turma = Turma.objects.create(
            nome="Turma de Filosofia 2023", curso=curso, status="A"
        )
        assert turma.pk is not None
        assert turma.nome == "Turma de Filosofia 2023"
        assert turma.curso == curso
        assert turma.status == "A"

    def test_turma_str(self):
        """Testa a representação string da turma."""
        from cursos.models import Curso

        curso = Curso.objects.create(nome="Curso Teste")
        turma = Turma.objects.create(nome="Turma de Filosofia 2023", curso=curso)
        assert str(turma) == f"Turma de Filosofia 2023 - {curso.nome}"

    # Removido teste de código único pois campo 'codigo' não existe mais

    # Removido teste de datas inválidas pois campos 'data_inicio' e 'data_fim' não existem mais
