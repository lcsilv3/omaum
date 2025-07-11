from django.test import TestCase
from django.utils import timezone
from frequencias.forms import FrequenciaForm, RegistroFrequenciaFormSet
from alunos.services import criar_aluno
from turmas.models import Turma
from atividades.models import Atividade
from matriculas.models import Matricula

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
        form = FrequenciaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_frequencia_form_invalido(self):
        """Testa se o formulário é inválido com dados incorretos."""
        # Formulário sem atividade
        form_data = {
            'data': timezone.now().date(),
            'observacoes': 'Teste de formulário'
        }
        form = FrequenciaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('atividade', form.errors)
        
        # Formulário sem data
        form_data = {
            'atividade': self.atividade.id,
            'observacoes': 'Teste de formulário'
        }
        form = FrequenciaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('data', form.errors)

class RegistroFrequenciaFormSetTestCase(TestCase):
    """Testes unitários para o formset de registro de frequência."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar alunos para os testes usando o serviço
        self.aluno1 = criar_aluno({
            "cpf": "12345678900",
            "nome": "Aluno Teste 1",
            "email": "aluno1@teste.com",
            "data_nascimento": "1990-01-01"
        })
        
        self.aluno2 = criar_aluno({
            "cpf": "98765432100",
            "nome": "Aluno Teste 2",
            "email": "aluno2@teste.com",
            "data_nascimento": "1992-05-15"
        })
        
        # Matricular alunos na turma
        Matricula.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A"
        )
        
        Matricula.objects.create(
            aluno=self.aluno2,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A"
        )
    
    def test_registro_frequencia_formset(self):
        """Testa o formset de registro de frequência."""
        # Dados para o formset
        formset_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-aluno': self.aluno1.cpf,
            'form-0-presente': 'True',
            'form-0-justificativa': '',
            'form-1-aluno': self.aluno2.cpf,
            'form-1-presente': 'False',
            'form-1-justificativa': 'Atestado médico'
        }
        
        formset = RegistroFrequenciaFormSet(data=formset_data)
        self.assertTrue(formset.is_valid())
        
        # Verificar os dados do formset
        self.assertEqual(len(formset.forms), 2)
        self.assertEqual(formset.forms[0].cleaned_data['aluno'], self.aluno1.cpf)
        self.assertTrue(formset.forms[0].cleaned_data['presente'])
        self.assertEqual(formset.forms[1].cleaned_data['aluno'], self.aluno2.cpf)
        self.assertFalse(formset.forms[1].cleaned_data['presente'])
        self.assertEqual(formset.forms[1].cleaned_data['justificativa'], 'Atestado médico')