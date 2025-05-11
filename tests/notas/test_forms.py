from django.test import TestCase
from django.utils import timezone
from notas.forms import AvaliacaoForm, NotaFormSet
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from matriculas.models import Matricula

class AvaliacaoFormTestCase(TestCase):
    """Testes unitários para o formulário de avaliação."""
    
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
        self.atividade = AtividadeAcademica.objects.create(
            nome="Atividade de Teste",
            descricao="Descrição da atividade",
            data_inicio=timezone.now(),
            responsavel="Professor Teste",
            tipo_atividade="aula",
            status="agendada"
        )
        self.atividade.turmas.add(self.turma)
    
    def test_avaliacao_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            'nome': 'Prova Final',
            'descricao': 'Avaliação final do curso',
            'data': timezone.now().date(),
            'peso': 2.0,
            'turma': self.turma.id,
            'atividade': self.atividade.id
        }
        form = AvaliacaoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_avaliacao_form_invalido(self):
        """Testa se o formulário é inválido com dados incorretos."""
        # Formulário sem nome
        form_data = {
            'descricao': 'Avaliação final do curso',
            'data': timezone.now().date(),
            'peso': 2.0,
            'turma': self.turma.id,
            'atividade': self.atividade.id
        }
        form = AvaliacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        
        # Formulário com peso negativo
        form_data = {
            'nome': 'Prova Final',
            'descricao': 'Avaliação final do curso',
            'data': timezone.now().date(),
            'peso': -1.0,
            'turma': self.turma.id,
            'atividade': self.atividade.id
        }
        form = AvaliacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('peso', form.errors)

class NotaFormSetTestCase(TestCase):
    """Testes unitários para o formset de notas."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar alunos para os testes
        self.aluno1 = Aluno.objects.create(
            cpf="12345678900",
            nome="Aluno Teste 1",
            email="aluno1@teste.com",
            data_nascimento="1990-01-01"
        )
        
        self.aluno2 = Aluno.objects.create(
            cpf="98765432100",
            nome="Aluno Teste 2",
            email="aluno2@teste.com",
            data_nascimento="1992-05-15"
        )
        
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
        
        # Criar uma atividade para os testes
        self.atividade = AtividadeAcademica.objects.create(
            nome="Atividade de Teste",
            descricao="Descrição da atividade",
            data_inicio=timezone.now(),
            responsavel="Professor Teste",
            tipo_atividade="aula",
            status="agendada"
        )
        self.atividade.turmas.add(self.turma)
        
        # Criar avaliação para os testes
        self.avaliacao = Avaliacao.objects.create(
            nome="Prova Final",
            descricao="Avaliação final do curso",
            data=timezone.now().date(),
            peso=2.0,
            turma=self.turma,
            atividade=self.atividade
        )
    
    def test_nota_formset(self):
        """Testa o formset de notas."""
        # Dados para o formset
        formset_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-aluno': self.aluno1.cpf,
            'form-0-valor': '8.5',
            'form-0-observacao': 'Bom desempenho',
            'form-1-aluno': self.aluno2.cpf,
            'form-1-valor': '7.0',
            'form-1-observacao': 'Desempenho regular'
        }
        
        formset = NotaFormSet(data=formset_data, avaliacao=self.avaliacao)
        self.assertTrue(formset.is_valid())
        
        # Verificar os dados do formset
        self.assertEqual(len(formset.forms), 2)
        self.assertEqual(formset.forms[0].cleaned_data['aluno'], self.aluno1.cpf)
        self.assertEqual(formset.forms[0].cleaned_data['valor'], 8.5)
        self.assertEqual(formset.forms[0].cleaned_data['observacao'], 'Bom desempenho')
        self.assertEqual(formset.forms[1].cleaned_data['aluno'], self.aluno2.cpf)
        self.assertEqual(formset.forms[1].cleaned_data['valor'], 7.0)
        self.assertEqual(formset.forms[1].cleaned_data['observacao'], 'Desempenho regular')
    
    def test_nota_formset_invalido(self):
        """Testa se o formset é inválido com dados incorretos."""
        # Dados para o formset com nota inválida
        formset_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-aluno': self.aluno1.cpf,
            'form-0-valor': '11.0',  # Valor acima de 10
            'form-0-observacao': 'Bom desempenho',
            'form-1-aluno': self.aluno2.cpf,
            'form-1-valor': '7.0',
            'form-1-observacao': 'Desempenho regular'
        }
        
        formset = NotaFormSet(data=formset_data, avaliacao=self.avaliacao)
        self.assertFalse(formset.is_valid())
        self.assertIn('valor', formset.forms[0].errors)            aluno=self