import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade
# from frequencias.models import Frequencia, RegistroFrequencia  # Removido: símbolo(s) inexistente(s)
from matriculas.models import Matricula
import datetime
import random

@pytest.mark.django_db
class PerformanceTestCase(TestCase):
    """Testes de desempenho para os módulos adicionais."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Cliente para fazer requisições
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Criar dados de teste em massa
        self.criar_dados_teste()
    
    def criar_dados_teste(self):
        """Cria dados de teste em massa para os testes de desempenho."""
        # Criar turmas
        self.turmas = []
        for i in range(5):
            turma = Turma.objects.create(
                nome=f"Turma de Teste {i+1}",
                codigo=f"TT-{i+1:03d}",
                data_inicio=timezone.now().date(),
                status="A"
            )
            self.turmas.append(turma)
        
        # Criar alunos e matrículas
        self.alunos = []
        for i in range(100):
            aluno = Aluno.objects.create(
                cpf=f"{i+1:011d}",
                nome=f"Aluno Teste {i+1}",
                email=f"aluno{i+1}@teste.com",
                data_nascimento="1990-01-01"
            )
            self.alunos.append(aluno)
            
            # Matricular aluno em uma turma aleatória
            turma = random.choice(self.turmas)
            Matricula.objects.create(
                aluno=aluno,
                turma=turma,
                data_matricula=timezone.now().date(),
                status="A"
            )
        
        # Criar atividades
        self.atividades = []
        for i in range(20):
            atividade = Atividade.objects.create(
                nome=f"Atividade de Teste {i+1}",
                descricao=f"Descrição da atividade {i+1}",
                data_inicio=timezone.now().date() + datetime.timedelta(days=i),
                hora_inicio=timezone.now().time(),
                responsavel="Professor Teste",
                tipo_atividade=random.choice(["AULA", "PALESTRA", "WORKSHOP", "SEMINARIO", "OUTRO"]),
                status=random.choice(["PENDENTE", "CONFIRMADA", "REALIZADA", "CANCELADA"])
            )
            # Associar a atividade a turmas aleatórias
            for turma in random.sample(self.turmas, random.randint(1, 3)):
                atividade.turmas.add(turma)
            self.atividades.append(atividade)
        
## Blocos de código soltos removidos após limpeza estrutural