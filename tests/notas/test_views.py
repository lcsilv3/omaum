from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from notas.models import Avaliacao, Nota
from alunos.services import criar_aluno
from turmas.models import Turma
from atividades.models import Atividade
from matriculas.models import Matricula

@pytest.mark.django_db
class NotasViewsTestCase(TestCase):
    """Testes de integração para as views do módulo de notas."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
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
        
        # Criar uma avaliação para os testes
        self.avaliacao = Avaliacao.objects.create(
            nome="Prova Final",
            descricao="Avaliação final do curso",
            data=timezone.now().date(),
            peso=2.0,
            turma=self.turma,
            atividade=self.atividade
        )
        
        # Criar notas para os testes
        Nota.objects.create(
            avaliacao=self.avaliacao,
            aluno=self.aluno1,
            valor=8.5,
            observacao="Bom desempenho"
        )
        
        Nota.objects.create(
            avaliacao=self.avaliacao,
            aluno=self.aluno2,
            valor=7.0,
            observacao="Desempenho regular"
        )
        
        # Cliente para fazer requisições
        self.client = Client()
    
    def test_listar_avaliacoes_view(self):
        """Testa se a view de listagem de avaliações funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de listagem de avaliações
        response = self.client.get(reverse('notas:listar_avaliacoes'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se as avaliações estão no contexto
        self.assertIn('avaliacoes', response.context)
        self.assertEqual(len(response.context['avaliacoes']), 1)
        
        # Verificar se a avaliação está na página
        self.assertContains(response, "Prova Final")
        self.assertContains(response, self.turma.nome)
    
    def test_criar_avaliacao_view(self):
        """Testa se a view de criação de avaliação funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de criação de avaliação
        response = self.client.get(reverse('notas:criar_avaliacao'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formulário está no contexto
        self.assertIn('form', response.context)
        
        # Dados para a nova avaliação
        nova_avaliacao_data = {
            'nome': 'Prova Parcial',
            'descricao': 'Avaliação parcial do curso',
            'data': timezone.now().date().strftime('%Y-%m-%d'),
            'peso': 1.0,
            'turma': self.turma.id,
            'atividade': self.atividade.id
        }
        
        # Enviar o formulário para criar uma nova avaliação
        response = self.client.post(
            reverse('notas:criar_avaliacao'),
            data=nova_avaliacao_data,
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a avaliação foi criada no banco de dados
        self.assertTrue(Avaliacao.objects.filter(nome='Prova Parcial').exists())
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Avaliação criada com sucesso")
    
    def test_lancar_notas_view(self):
        """Testa se a view de lançamento de notas funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de lançamento de notas
        response = self.client.get(
            reverse('notas:lancar_notas', args=[self.avaliacao.id])
        )
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formset está no contexto
        self.assertIn('formset', response.context)
        
        # Dados para o lançamento de notas
        notas_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '2',
            'form-MAX_NUM_FORMS': '',
            'form-0-id': Nota.objects.get(aluno=self.aluno1).id,
            'form-0-aluno': self.aluno1.cpf,
            'form-0-valor': '9.0',
            'form-0-observacao': 'Excelente desempenho',
            'form-1-id': Nota.objects.get(aluno=self.aluno2).id,
            'form-1-aluno': self.aluno2.cpf,
            'form-1-valor': '6.5',
            'form-1-observacao': 'Desempenho abaixo do esperado'
        }
        
        # Enviar o formulário para atualizar as notas
        response = self.client.post(
            reverse('notas:lancar_notas', args=[self.avaliacao.id]),
            data=notas_data,
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se as notas foram atualizadas no banco de dados
        nota1 = Nota.objects.get(aluno=self.aluno1)
        self.assertEqual(nota1.valor, 9.0)
        self.assertEqual(nota1.observacao, 'Excelente desempenho')
        
        nota2 = Nota.objects.get(aluno=self.aluno2)
        self.assertEqual(nota2.valor, 6.5)
        self.assertEqual(nota2.observacao, 'Desempenho abaixo do esperado')
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Notas lançadas com sucesso")