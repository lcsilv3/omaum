import pytest
from turmas.models import Turma
from django.utils import timezone
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestTurmaModel:
    """Testes para o modelo Turma."""
    
    def test_criar_turma(self):
        """Testa a criação de uma turma."""
        turma = Turma.objects.create(
            nome="Turma de Filosofia 2023",
            codigo="FIL-2023",
            data_inicio=timezone.now().date(),
            status="A"
        )
        assert turma.pk is not None
        assert turma.nome == "Turma de Filosofia 2023"
        assert turma.codigo == "FIL-2023"
        assert turma.status == "A"
    
    def test_turma_str(self):
        """Testa a representação string da turma."""
        turma = Turma.objects.create(
            nome="Turma de Filosofia 2023",
            codigo="FIL-2023"
        )
        assert str(turma) == "Turma de Filosofia 2023"
    
    def test_codigo_turma_unico(self):
        """Testa se o código da turma é único."""
        Turma.objects.create(
            nome="Turma A",
            codigo="TURMA-001"
        )
        
        with pytest.raises(Exception):  # Pode ser IntegrityError ou ValidationError
            Turma.objects.create(
                nome="Turma B",
                codigo="TURMA-001"  # Código duplicado
            )
    
    def test_data_fim_posterior_data_inicio(self):
        """Testa se a data de fim é posterior à data de início."""
        data_inicio = timezone.now().date()
        data_fim = data_inicio - timezone.timedelta(days=1)  # Data de fim anterior à data de início
        
        turma = Turma(
            nome="Turma de Filosofia 2023",
            codigo="FIL-2023",
            data_inicio=data_inicio,
            data_fim=data_fim,
            status="A"
        )
        
        with pytest.raises(ValidationError):
            turma.full_clean()