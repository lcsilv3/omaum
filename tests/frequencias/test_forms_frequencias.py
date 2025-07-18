from django.test import TestCase
from django.utils import timezone
from frequencias.forms import FrequenciaMensalForm
from turmas.models import Turma
from atividades.models import Atividade

class FrequenciaFormTestCase(TestCase):
    """Testes unitários para o formulário de frequência."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar uma atividade para os testes
        self.atividade = Atividade.objects.create(
            nome="Atividade de Teste",
            descricao="Descrição da atividade",
            data_inicio=timezone.now(),
            responsavel="Professor Teste",
            tipo_atividade="aula",
            status="agendada"
        )
        self.atividade.turmas.add(self.turma)
    
    def test_frequencia_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            'atividade': self.atividade.id,
            'data': timezone.now().date(),
            'observacoes': 'Teste de formulário'
        }
        form = FrequenciaMensalForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_frequencia_form_invalido(self):
        """Testa se o formulário é inválido com dados incorretos."""
        # Formulário sem atividade
        form_data = {
            'data': timezone.now().date(),
            'observacoes': 'Teste de formulário'
        }
        form = FrequenciaMensalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('atividade', form.errors)
        
        # Formulário sem data
        form_data = {
            'atividade': self.atividade.id,
            'observacoes': 'Teste de formulário'
        }
        form = FrequenciaMensalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('data', form.errors)

