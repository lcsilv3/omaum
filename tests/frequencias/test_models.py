from django.test import TestCase
from django.utils import timezone
from frequencias.models import Frequencia, RegistroFrequencia
from alunos.services import criar_aluno
from turmas.models import Turma
from atividades.models import Atividade

class FrequenciaModelTestCase(TestCase):
    """Testes unitários para o modelo Frequencia."""
    
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
        
        # Criar frequência para os testes
        self.frequencia = Frequencia.objects.create(
            atividade=self.atividade,
            data=timezone.now().date(),
            observacoes="Teste de frequência"
        )
    
    def test_criacao_frequencia(self):
        """Testa a criação de uma frequência."""
        self.assertEqual(self.frequencia.atividade, self.atividade)
        self.assertEqual(self.frequencia.observacoes, "Teste de frequência")
        self.assertIsNotNone(self.frequencia.data)
    
    def test_representacao_string(self):
        """Testa a representação em string do modelo."""
        data_formatada = self.frequencia.data.strftime("%d/%m/%Y")
        representacao_esperada = f"Frequência - {self.atividade.nome} - {data_formatada}"
        self.assertEqual(str(self.frequencia), representacao_esperada)

class RegistroFrequenciaModelTestCase(TestCase):
    """Testes unitários para o modelo RegistroFrequencia."""
    
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
        
        # Criar um aluno para os testes usando o serviço
        self.aluno = criar_aluno({
            "cpf": "12345678900",
            "nome": "Aluno Teste",
            "email": "aluno@teste.com",
            "data_nascimento": "1990-01-01"
        })
        
        # Criar frequência para os testes
        self.frequencia = Frequencia.objects.create(
            atividade=self.atividade,
            data=timezone.now().date(),
            observacoes="Teste de frequência"
        )
        
        # Criar registro de frequência para os testes
        self.registro = RegistroFrequencia.objects.create(
            frequencia=self.frequencia,
            aluno=self.aluno,
            presente=True,
            justificativa=""
        )
    
    def test_criacao_registro_frequencia(self):
        """Testa a criação de um registro de frequência."""
        self.assertEqual(self.registro.frequencia, self.frequencia)
        self.assertEqual(self.registro.aluno, self.aluno)
        self.assertTrue(self.registro.presente)
        self.assertEqual(self.registro.justificativa, "")
    
    def test_representacao_string(self):
        """Testa a representação em string do modelo."""
        status = "Presente" if self.registro.presente else "Ausente"
        representacao_esperada = f"{self.aluno.nome} - {status}"
        self.assertEqual(str(self.registro), representacao_esperada)
    
    def test_registro_com_justificativa(self):
        """Testa um registro de frequência com justificativa."""
        registro = RegistroFrequencia.objects.create(
            frequencia=self.frequencia,
            aluno=self.aluno,
            presente=False,
            justificativa="Atestado médico"
        )
        self.assertFalse(registro.presente)
        self.assertEqual(registro.justificativa, "Atestado médico")
