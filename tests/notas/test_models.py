from django.test import TestCase
from django.utils import timezone
from notas.models import Avaliacao, Nota
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import AtividadeAcademica
import datetime

class AvaliacaoModelTestCase(TestCase):
    """Testes unitários para o modelo Avaliacao."""
    
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
        
        # Criar avaliação para os testes
        self.avaliacao = Avaliacao.objects.create(
            nome="Prova Final",
            descricao="Avaliação final do curso",
            data=timezone.now().date(),
            peso=2.0,
            turma=self.turma,
            atividade=self.atividade
        )
    
    def test_criacao_avaliacao(self):
        """Testa a criação de uma avaliação."""
        self.assertEqual(self.avaliacao.nome, "Prova Final")
        self.assertEqual(self.avaliacao.descricao, "Avaliação final do curso")
        self.assertEqual(self.avaliacao.peso, 2.0)
        self.assertEqual(self.avaliacao.turma, self.turma)
        self.assertEqual(self.avaliacao.atividade, self.atividade)
    
    def test_representacao_string(self):
        """Testa a representação em string do modelo."""
        representacao_esperada = f"Prova Final - {self.turma.nome}"
        self.assertEqual(str(self.avaliacao), representacao_esperada)

class NotaModelTestCase(TestCase):
    """Testes unitários para o modelo Nota."""
    
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
        
        # Criar um aluno para os testes
        self.aluno = Aluno.objects.create(
            cpf="12345678900",
            nome="Aluno Teste",
            email="aluno@teste.com",
            data_nascimento="1990-01-01"
        )
        
        # Criar avaliação para os testes
        self.avaliacao = Avaliacao.objects.create(
            nome="Prova Final",
            descricao="Avaliação final do curso",
            data=timezone.now().date(),
            peso=2.0,
            turma=self.turma,
            atividade=self.atividade
        )
        
        # Criar nota para os testes
        self.nota = Nota.objects.create(
            avaliacao=self.avaliacao,
            aluno=self.aluno,
            valor=8.5,
            observacao="Bom desempenho"
        )
    
    def test_criacao_nota(self):
        """Testa a criação de uma nota."""
        self.assertEqual(self.nota.avaliacao, self.avaliacao)
        self.assertEqual(self.nota.aluno, self.aluno)
        self.assertEqual(self.nota.valor, 8.5)
        self.assertEqual(self.nota.observacao, "Bom desempenho")
    
    def test_representacao_string(self):
        """Testa a representação em string do modelo."""
        representacao_esperada = f"{self.aluno.nome} - {self.avaliacao.nome}: 8.5"
        self.assertEqual(str(self.nota), representacao_esperada)
    
    def test_validacao_nota(self):
        """Testa a validação do valor da nota."""
        # Nota com valor negativo
        with self.assertRaises(Exception):
            nota_invalida = Nota.objects.create(
                avaliacao=self.avaliacao,
                aluno=self.aluno,
                valor=-1.0,
                observacao="Nota inválida"
            )
        
        # Nota com valor acima de 10
        with self.assertRaises(Exception):
            nota_invalida = Nota.objects.create(
                avaliacao=self.avaliacao,
                aluno=self.aluno,
                valor=11.0,
                observacao="Nota inválida"
            )