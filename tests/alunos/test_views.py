from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from alunos.services import criar_aluno, buscar_aluno_por_cpf

class AlunosViewsTestCase(TestCase):
    """Testes de integração para as views do módulo de alunos."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Criar alguns alunos para testes usando o serviço
        self.aluno1 = criar_aluno({
            "cpf": "12345678900",
            "nome": "João da Silva",
            "email": "joao@exemplo.com",
            "data_nascimento": "1990-01-01"
        })
        
        self.aluno2 = criar_aluno({
            "cpf": "98765432100",
            "nome": "Maria Souza",
            "email": "maria@exemplo.com",
            "data_nascimento": "1992-05-15"
        })
        
        # Cliente para fazer requisições
        self.client = Client()
    
    def test_listar_alunos_view_nao_autenticado(self):
        """Testa se a view de listagem de alunos redireciona para login quando não autenticado."""
        response = self.client.get(reverse('alunos:listar_alunos'))
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        self.assertIn('/login/', response.url)  # Redirecionamento para a página de login
    
    def test_listar_alunos_view_autenticado(self):
        """Testa se a view de listagem de alunos funciona quando autenticado."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de listagem de alunos
        response = self.client.get(reverse('alunos:listar_alunos'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se os alunos estão no contexto
        self.assertIn('alunos', response.context)
        self.assertEqual(len(response.context['alunos']), 2)
        
        # Verificar se os nomes dos alunos estão na página
        self.assertContains(response, "João da Silva")
        self.assertContains(response, "Maria Souza")
    
    def test_detalhar_aluno_view(self):
        """Testa se a view de detalhes do aluno funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de detalhes do aluno
        response = self.client.get(
            reverse('alunos:detalhar_aluno', args=[self.aluno1.cpf])
        )
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o aluno está no contexto
        self.assertIn('aluno', response.context)
        self.assertEqual(response.context['aluno'].cpf, self.aluno1.cpf)
        
        # Verificar se os dados do aluno estão na página
        self.assertContains(response, self.aluno1.nome)
        self.assertContains(response, self.aluno1.email)
    
    def test_criar_aluno_view_get(self):
        """Testa se a view de criação de aluno exibe o formulário corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de criação de aluno
        response = self.client.get(reverse('alunos:criar_aluno'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formulário está no contexto
        self.assertIn('form', response.context)
    
    def test_editar_aluno_view(self):
        """Testa se a view de edição de aluno funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de edição do aluno
        response = self.client.get(
            reverse('alunos:editar_aluno', args=[self.aluno1.cpf])
        )
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formulário está no contexto
        self.assertIn('form', response.context)
        
        # Verificar se os dados do aluno estão preenchidos no formulário
        self.assertEqual(response.context['form'].instance.cpf, self.aluno1.cpf)
        
        # Dados atualizados para o aluno
        dados_atualizados = {
            'cpf': self.aluno1.cpf,  # CPF não deve mudar
            'nome': 'João Silva Atualizado',
            'email': 'joao.atualizado@exemplo.com',
            'data_nascimento': '1990-01-01',
            'sexo': 'M',
        }
        
        # Enviar o formulário para atualizar o aluno
        response = self.client.post(
            reverse('alunos:editar_aluno', args=[self.aluno1.cpf]),
            data=dados_atualizados,
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o aluno foi atualizado no banco de dados
        aluno_atualizado = buscar_aluno_por_cpf(self.aluno1.cpf)
        self.assertEqual(aluno_atualizado.nome, 'João Silva Atualizado')
        self.assertEqual(aluno_atualizado.email, 'joao.atualizado@exemplo.com')
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Aluno atualizado com sucesso")
    
    def test_excluir_aluno_view(self):
        """Testa se a view de exclusão de aluno funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de confirmação de exclusão
        response = self.client.get(
            reverse('alunos:excluir_aluno', args=[self.aluno1.cpf])
        )
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o aluno está no contexto
        self.assertIn('aluno', response.context)
        
        # Enviar a confirmação de exclusão
        response = self.client.post(
            reverse('alunos:excluir_aluno', args=[self.aluno1.cpf]),
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o aluno foi excluído do banco de dados
        self.assertIsNone(buscar_aluno_por_cpf(self.aluno1.cpf))
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Aluno excluído com sucesso")
    
    def test_criar_aluno_view_post(self):
        """Testa se a view de criação de aluno cria um novo aluno corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Dados para o novo aluno
        novo_aluno_data = {
            'cpf': '11122233344',
            'nome': 'Pedro Oliveira',
            'email': 'pedro@exemplo.com',
            'data_nascimento': '1995-10-20',
            'sexo': 'M',
        }
        
        # Enviar o formulário para criar um novo aluno
        response = self.client.post(
            reverse('alunos:criar_aluno'),
            data=novo_aluno_data,
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o aluno foi criado no banco de dados
        self.assertIsNotNone(buscar_aluno_por_cpf('11122233344'))
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Aluno cadastrado com sucesso")