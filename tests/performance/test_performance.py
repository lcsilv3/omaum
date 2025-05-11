from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from frequencias.models import Frequencia, RegistroFrequencia
from notas.models import Avaliacao, Nota
from pagamentos.models import Pagamento, TipoPagamento
from matriculas.models import Matricula
import time
import datetime
import random
import string

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
            atividade = AtividadeAcademica.objects.create(
                nome=f"Atividade de Teste {i+1}",
                descricao=f"Descrição da atividade {i+1}",
                data_inicio=timezone.now() + datetime.timedelta(days=i),
                responsavel="Professor Teste",
                tipo_atividade=random.choice(["aula", "palestra", "workshop", "seminario", "outro"]),
                status=random.choice(["agendada", "em_andamento", "concluida", "cancelada"])
            )
            # Associar a atividade a turmas aleatórias
            for turma in random.sample(self.turmas, random.randint(1, 3)):
                atividade.turmas.add(turma)
            self.atividades.append(atividade)
        
        # Criar frequências e registros
        self.frequencias = []
        for atividade in self.atividades[:10]:  # Usar apenas as 10 primeiras atividades
            frequencia = Frequencia.objects.create(
                atividade=atividade,
                data=timezone.now().date(),
                observacoes=f"Frequência para {atividade.nome}"
            )
            self.frequencias.append(frequencia)
            
            # Criar registros de frequência para alunos das turmas da atividade
            alunos_turmas = []
            for turma in atividade.turmas.all():
                matriculas = Matricula.objects.filter(turma=turma, status="A")
                alunos_turmas.extend([m.aluno for m in matriculas])
            
            for aluno in alunos_turmas:
                RegistroFrequencia.objects.create(
                    frequencia=frequencia,
                    aluno=aluno,
                    presente=random.choice([True, False]),
                    justificativa="" if random.random() > 0.2 else "Justificativa de teste"
                )                    presente