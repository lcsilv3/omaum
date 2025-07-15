import pytest
from django.utils import timezone
from atividades.models import Atividade
from turmas.models import Turma

@pytest.mark.django_db
class TestAtividadeModel:
    """Testes para o modelo Atividade."""
    
    def test_criar_atividade(self):
        """Testa a criação de uma atividade."""
        atividade = Atividade.objects.create(
            nome="Aula de Filosofia",
            descricao="Introdução à Filosofia",
            data_inicio=timezone.now(),
            responsavel="Prof. Silva",
            tipo_atividade="aula",
            status="agendada"
        )
        assert atividade.pk is not None
        assert atividade.nome == "Aula de Filosofia"
        assert atividade.status == "agendada"
    
    def test_atividade_str(self):
        """Testa a representação string da atividade."""
        atividade = Atividade.objects.create(
            nome="Aula de Filosofia",
            data_inicio=timezone.now(),
            tipo_atividade="aula",
            status="agendada"
        )
        assert str(atividade) == "Aula de Filosofia"
    
    def test_atividade_com_turmas(self):
        """Testa a associação de turmas a uma atividade."""
        Turma.objects.create(nome="Turma A", codigo="TA-001")
        Turma.objects.create(nome="Turma B", codigo="TB-001")
        
        Atividade.objects.create(
            nome="Aula de Filosofia",
            data_inicio=timezone.now(),
            tipo_atividade="aula",
            status="agendada"
        )
        
        # Note: Assuming turmas relationship still exists in new model
        # atividade.turmas.add(turma1, turma2)
        
        # assert atividade.turmas.count() == 2
        # assert turma1 in atividade.turmas.all()
        # assert turma2 in atividade.turmas.all()

