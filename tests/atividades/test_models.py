import pytest
from django.utils import timezone
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestAtividadeAcademicaModel:
    """Testes para o modelo AtividadeAcademica."""
    
    def test_criar_atividade_academica(self):
        """Testa a criação de uma atividade acadêmica."""
        atividade = AtividadeAcademica.objects.create(
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
    
    def test_atividade_academica_str(self):
        """Testa a representação string da atividade acadêmica."""
        atividade = AtividadeAcademica.objects.create(
            nome="Aula de Filosofia",
            data_inicio=timezone.now(),
            tipo_atividade="aula",
            status="agendada"
        )
        assert str(atividade) == "Aula de Filosofia"
    
    def test_atividade_academica_com_turmas(self):
        """Testa a associação de turmas a uma atividade acadêmica."""
        turma1 = Turma.objects.create(nome="Turma A", codigo="TA-001")
        turma2 = Turma.objects.create(nome="Turma B", codigo="TB-001")
        
        atividade = AtividadeAcademica.objects.create(
            nome="Aula de Filosofia",
            data_inicio=timezone.now(),
            tipo_atividade="aula",
            status="agendada"
        )
        
        atividade.turmas.add(turma1, turma2)
        
        assert atividade.turmas.count() == 2
        assert turma1 in atividade.turmas.all()
        assert turma2 in atividade.turmas.all()

@pytest.mark.django_db
class TestAtividadeRitualisticaModel:
    """Testes para o modelo AtividadeRitualistica."""
    
    def test_criar_atividade_ritualistica(self):
        """Testa a criação de uma atividade ritualística."""
        turma = Turma.objects.create(nome="Turma A", codigo="TA-001")
        
        atividade = AtividadeRitualistica.objects.create(
            nome="Ritual de Iniciação",
            descricao="Ritual para novos membros",
            data=timezone.now().date(),
            hora_inicio="19:00",
            hora_fim="21:00",
            local="Templo Principal",
            turma=turma
        )
        
        assert atividade.pk is not None
        assert atividade.nome == "Ritual de Iniciação"
        assert atividade.turma == turma
    
    def test_atividade_ritualistica_str(self):
        """Testa a representação string da atividade ritualística."""
        turma = Turma.objects.create(nome="Turma A", codigo="TA-001")
        data = timezone.now().date()
        
        atividade = AtividadeRitualistica.objects.create(
            nome="Ritual de Iniciação",
            data=data,
            hora_inicio="19:00",
            hora_fim="21:00",
            local="Templo Principal",
            turma=turma
        )
        
        assert str(atividade) == f"Ritual de Iniciação - {data}"
    
    def test_validacao_horarios(self):
        """Testa se a hora de início é anterior à hora de fim."""
        turma = Turma.objects.create(nome="Turma A", codigo="TA-001")
        
        atividade = AtividadeRitualistica(
            nome="Ritual de Iniciação",
            data=timezone.now().date(),
            hora_inicio="21:00",  # Hora de início posterior à hora de fim
            hora_fim="19:00",
            local="Templo Principal",
            turma=turma
        )
        
        with pytest.raises(ValidationError):
            atividade.full_clean()