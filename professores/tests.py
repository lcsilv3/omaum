from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Professor
from .forms import ProfessorForm

class ProfessorModelTest(TestCase):
    """Testes para o modelo Professor"""
    
    def setUp(self):
        self.professor = Professor.objects.create(
            nome="João Silva",
            email="joao@exemplo.com",
            telefone="(11) 99999-9999",
            especialidade="Matemática"
        )
    
    def test_professor_creation(self):
        """Testa a criação de um professor"""
        self.assertEqual(self.professor.nome, "João Silva")
        self.assertEqual(self.professor.email, "joao@exemplo.com")
        self.assertEqual(self.professor.telefone, "(11) 99999-9999")
        self.assertEqual(self.professor.especialidade, "Matemática")
        self.assertTrue(self.professor.ativo)
    
    def test_professor_str(self):
        """Testa a representação string do modelo"""
        self.assertEqual(str(self.professor), "João Silva")
    
    def test_professor_ordering(self):
        """Testa a ordenação dos professores"""
        Professor.objects.create(
            nome="Ana Souza",
            email="ana@exemplo.com",
            especialidade="Português"
        )
        professores = Professor.objects.all()
        self.assertEqual(professores[0].nome, "Ana Souza")
        self.assertEqual(professores[1].nome, "João Silva")


class ProfessorFormTest(TestCase):
    """Testes para o formulário de Professor"""
    
    def setUp(self):
        self.professor = Professor.objects.create(
            nome="João Silva",
            email="joao@exemplo.com",
            telefone="(11) 99999-9999",
            especialidade="Matemática"
        )
    
    def test_valid_form(self):
        """Testa formulário com dados válidos"""
        data = {
            'nome': 'Maria Santos',
            'email': 'maria@exemplo.com',
            'telefone': '(11) 99999-9999',
            'especialidade': 'História',
            'ativo': True
        }
        form = ProfessorForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email_format(self):
        """Testa formulário com formato de email inválido"""
        data = {
            'nome': 'Maria Santos',
            'email': 'email-invalido',
            'especialidade': 'História',
            'ativo': True
        }
        form = ProfessorForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_duplicate_email(self):
        """Testa formulário com email duplicado"""
        data = {
            'nome': 'Maria Santos',
            'email': 'joao@exemplo.com',  # Email já existente
            'especialidade': 'História',
            'ativo': True
        }
        form = ProfessorForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_invalid_phone_format(self):
        """Testa formulário com formato de telefone inválido"""
        data = {
            'nome': 'Maria Santos',
            'email': 'maria@exemplo.com',
            'telefone': '999999999',  # Formato inválido
            'especialidade': 'História',
            'ativo': True
        }
        form = ProfessorForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('telefone', form.errors)


class ProfessorViewsTest(TestCase):
    """Testes para as views de Professor"""
    
    def setUp(self):
        # Cria um usuário para testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Cria um cliente e faz login
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Cria um professor para testes
        self.professor = Professor.objects.create(
            nome="João Silva",
            email="joao@exemplo.com",
            telefone="(11) 99999-9999",
            especialidade="Matemática"
        )
    
    def test_listar_professores_view(self):
        """Testa a view de listagem de professores"""
        response = self.client.get(reverse('professores:listar_professores'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'professores/listar_professores.html')
        self.assertContains(response, "João Silva")
        self.assertContains(response, "joao@exemplo.com")
    
    def test_cadastrar_professor_view_get(self):
        """Testa a view de cadastro de professor (GET)"""
        response = self.client.get(reverse('professores:cadastrar_professor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'professores/cadastrar_professor.html')
        self.assertIsInstance(response.context['form'], ProfessorForm)
    
    def test_cadastrar_professor_view_post(self):
        """Testa a view de cadastro de professor (POST)"""
        data = {
            'nome': 'Maria Santos',
            'email': 'maria@exemplo.com',
            'telefone': '(11) 99999-9999',
            'especialidade': 'História',
            'ativo': True
        }
        response = self.client.post(reverse('professores:cadastrar_professor'), data)
        self.assertRedirects(response, reverse('professores:listar_professores'))
        self.assertTrue(Professor.objects.filter(email='maria@exemplo.com').exists())
    
    def test_detalhes_professor_view(self):
        """Testa a view de detalhes de professor"""
        response = self.client.get(
            reverse('professores:detalhes_professor', args=[self.professor.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'professores/detalhes_professor.html')
        self.assertEqual(response.context['professor'], self.professor)
    
    def test_editar_professor_view_get(self):
        """Testa a view de edição de professor (GET)"""
        response = self.client.get(
            reverse('professores:editar_professor', args=[self.professor.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'professores/cadastrar_professor.html')
        self.assertIsInstance(response.context['form'], ProfessorForm)
    
    def test_editar_professor_view_post(self):
        """Testa a view de edição de professor (POST)"""
        data = {
            'nome': 'João Silva Atualizado',
            'email': 'joao@exemplo.com',
            'telefone': '(11) 99999-9999',
            'especialidade': 'Física',
            'ativo': True
        }
        response = self.client.post(
            reverse('professores:editar_professor', args=[self.professor.id]),
            data
        )
        self.assertRedirects(
            response, 
            reverse('professores:detalhes_professor', args=[self.professor.id])
        )
        
        # Recarrega o professor do banco de dados
        self.professor.refresh_from_db()
        self.assertEqual(self.professor.nome, 'João Silva Atualizado')
        self.assertEqual(self.professor.especialidade, 'Física')
    
    def test_excluir_professor_view_get(self):
        """Testa a view de exclusão de professor (GET)"""
        response = self.client.get(
            reverse('professores:excluir_professor', args=[self.professor.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'professores/confirmar_exclusao.html')
    
    def test_exclu
