from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from atividades.models import Atividade
from turmas.models import Turma
from django.utils import timezone

class AtividadesAcademicasViewsTestCase(TestCase):
    """Testes de integração para as views de atividades acadêmicas."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Criar uma turma para associar às atividades
        self.turma = Turma.objects.create(
            nome="Turma A",
            codigo="TA-001",
            status="A"
        )
        
        # Criar algumas atividades para testes
        self.atividade = Atividade.objects.create(
            nome="Aula de Filosofia",
            descricao="Introdução à Filosofia",
            data_inicio=timezone.now(),
            responsavel="Prof. Silva",
            tipo_atividade="aula",
            status="agendada"
        )
        self.atividade.turmas.add(self.turma)
        
        # Cliente para fazer requisições
        self.client = Client()
    
    def test_listar_atividades_academicas_view(self):
        """Testa se a view de listagem de atividades acadêmicas funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de listagem de atividades acadêmicas
        response = self.client.get(reverse('atividades:listar_atividades_academicas'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se as atividades estão no contexto
        self.assertIn('atividades', response.context)
        self.assertEqual(len(response.context['atividades']), 1)
        
        # Verificar se o nome da atividade está na página
        self.assertContains(response, "Aula de Filosofia")
    
    def test_detalhar_atividade_academica_view(self):
        """Testa se a view de detalhes da atividade acadêmica funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de detalhes da atividade acadêmica
        response = self.client.get(
            reverse('atividades:detalhar_atividade_academica', args=[self.atividade.pk])
        )
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a atividade está no contexto
        self.assertIn('atividade', response.context)
        self.assertEqual(response.context['atividade'].pk, self.atividade.pk)
        
        # Verificar se os dados da atividade estão na página
        self.assertContains(response, self.atividade.nome)
        self.assertContains(response, self.atividade.descricao)
    
    def test_criar_atividade_academica_view(self):
        """Testa se a view de criação de atividade acadêmica funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de criação de atividade acadêmica
        response = self.client.get(reverse('atividades:criar_atividade_academica'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formulário está no contexto
        self.assertIn('form', response.context)
        
        # Dados para a nova atividade
        nova_atividade_data = {
            'nome': 'Nova Aula de História',
            'descricao': 'História do Brasil',
            'data_inicio': timezone.now().strftime('%Y-%m-%d'),
            'responsavel': 'Prof. Santos',
            'local': 'Sala 102',
            'tipo_atividade': 'aula',
            'status': 'agendada',
            'turmas': [self.turma.id],
        }
        
        # Enviar o formulário para criar uma nova atividade
        response = self.client.post(
            reverse('atividades:criar_atividade_academica'),
            data=nova_atividade_data,
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a atividade foi criada no banco de dados
        self.assertTrue(Atividade.objects.filter(nome='Nova Aula de História').exists())
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Atividade acadêmica criada com sucesso")

class AtividadesRitualisticasViewsTestCase(TestCase):
    """Testes de integração para as views de atividades ritualísticas."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Criar uma turma para associar às atividades
        self.turma = Turma.objects.create(
            nome="Turma A",
            codigo="TA-001",
            status="A"
        )
        
        # Criar algumas atividades para testes
        self.atividade = Atividade.objects.create(
            nome="Ritual de Iniciação",
            descricao="Ritual para novos membros",
            data_inicio=timezone.now().date(),
            data_fim=timezone.now().date(),
            responsavel="Teste",
            local="Templo Principal"
        )
        
        # Cliente para fazer requisições
        self.client = Client()
    
    def test_listar_atividades_ritualisticas_view(self):
        """Testa se a view de listagem de atividades ritualísticas funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de listagem de atividades ritualísticas
        response = self.client.get(reverse('atividades:listar_atividades_ritualisticas'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se as atividades estão no contexto
        self.assertIn('atividades', response.context)
        self.assertEqual(len(response.context['atividades']), 1)
        
        # Verificar se o nome da atividade está na página
        self.assertContains(response, "Ritual de Iniciação")
