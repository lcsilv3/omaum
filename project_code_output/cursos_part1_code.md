# Código da Funcionalidade: cursos - Parte 1/2
*Gerado automaticamente*



## cursos\admin.py

python
from django.contrib import admin
from .models import Curso

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    # Adjust list_display to use fields that actually exist in the Curso model
    list_display = ['codigo_curso', 'duracao']  # Remove 'nome' if it doesn't exist
    search_fields = ['codigo_curso']
    list_filter = ['duracao']





## cursos\apps.py

python
from django.apps import AppConfig


class CursosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cursos'





## cursos\forms.py

python
from django import forms
from importlib import import_module

def get_curso_model():
    cursos_module = import_module('cursos.models')
    return getattr(cursos_module, 'Curso')

class CursoForm(forms.ModelForm):
    class Meta:
        model = get_curso_model()
        fields = ['codigo_curso', 'nome', 'descricao', 'duracao']
        widgets = {
            'codigo_curso': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
        }
        
    def clean_codigo_curso(self):
        codigo = self.cleaned_data.get('codigo_curso')
        if codigo <= 0:
            raise forms.ValidationError('O código do curso deve ser um número inteiro positivo.')
        return codigo

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise ValidationError("O nome do curso deve ter pelo menos 3 caracteres.")
        return nome




## cursos\models.py

python
from django.db import models
from django.core.validators import MinValueValidator

class Curso(models.Model):
    codigo_curso = models.IntegerField(
        'Código do Curso', 
        primary_key=True,
        validators=[MinValueValidator(1)],
        help_text='Digite um número inteiro positivo'
    )
    nome = models.CharField('Nome do Curso', max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    duracao = models.PositiveIntegerField('Duração (meses)', default=6)

    def __str__(self):
        return f"{self.codigo_curso} - {self.nome}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['codigo_curso']





## cursos\tests.py

python
# Este arquivo está vazio intencionalmente
# Os testes estão nos arquivos test_*.py





## cursos\test_forms.py

python
from django.test import TestCase
from cursos.forms import CursoForm

class CursoFormTest(TestCase):
    """Testes para o formulário CursoForm"""
    
    def test_form_valid(self):
        """Teste com dados válidos no formulário"""
        form_data = {
            'codigo_curso': 201,
            'nome': 'Curso de Teste',
            'descricao': 'Descrição do curso de teste',
            'duracao': 6
        }
        form = CursoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_codigo_negativo(self):
        """Teste com código de curso negativo (inválido)"""
        form_data = {
            'codigo_curso': -1,
            'nome': 'Curso de Teste',
            'descricao': 'Descrição do curso de teste',
            'duracao': 6
        }
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('codigo_curso', form.errors)
    
    def test_form_campos_obrigatorios(self):
        """Teste para verificar campos obrigatórios"""
        form_data = {}  # Formulário vazio
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('codigo_curso', form.errors)
        self.assertIn('nome', form.errors)
        self.assertIn('duracao', form.errors)





## cursos\test_integration.py

python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from cursos.models import Curso

class CursoIntegrationTest(TestCase):
    """Testes de integração para o aplicativo cursos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        # Criar um usuário para testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Fazer login com o usuário de teste
        self.client.login(username='testuser', password='testpassword')
    
    def test_fluxo_completo_curso(self):
        """Teste do fluxo completo: criar, visualizar, editar e excluir um curso"""
        
        # 1. Criar um novo curso
        response_criar = self.client.post(
            reverse('cursos:criar_curso'),
            {
                'codigo_curso': 401,
                'nome': 'Curso de Integração',
                'descricao': 'Descrição do curso de integração',
                'duracao': 8
            }
        )
        self.assertEqual(response_criar.status_code, 302)  # Redirecionamento após sucesso
        self.assertTrue(Curso.objects.filter(codigo_curso=401).exists())





## cursos\test_models.py

python
from django.test import TestCase
from django.core.exceptions import ValidationError
from cursos.models import Curso

class CursoModelTest(TestCase):
    """Testes para o modelo Curso"""
    
    def test_criar_curso_com_dados_validos(self):
        """Teste de criação de curso com dados válidos"""
        curso = Curso.objects.create(
            codigo_curso=101,
            nome="Curso de Teste",
            descricao="Descrição do curso de teste",
            duracao=6
        )
        self.assertEqual(curso.nome, "Curso de Teste")
        self.assertEqual(curso.codigo_curso, 101)
        self.assertEqual(curso.duracao, 6)
        self.assertEqual(curso.descricao, "Descrição do curso de teste")
    
    def test_str_representation(self):
        """Teste da representação string do modelo"""
        curso = Curso.objects.create(
            codigo_curso=102,
            nome="Curso de Python",
            descricao="Aprenda Python do zero",
            duracao=3
        )
        self.assertEqual(str(curso), "102 - Curso de Python")
    
    def test_ordering(self):
        """Teste para verificar a ordenação dos cursos"""
        Curso.objects.create(codigo_curso=105, nome="Curso Z", duracao=6)
        Curso.objects.create(codigo_curso=103, nome="Curso A", duracao=6)
        Curso.objects.create(codigo_curso=104, nome="Curso M", duracao=6)
        
        cursos = Curso.objects.all()
        self.assertEqual(cursos[0].codigo_curso, 103)  # Primeiro curso (ordenado por codigo_curso)
        self.assertEqual(cursos[1].codigo_curso, 104)  # Segundo curso
        self.assertEqual(cursos[2].codigo_curso, 105)  # Terceiro curso





## cursos\test_urls.py

python
from django.test import TestCase
from django.urls import reverse, resolve
from cursos.views import listar_cursos, criar_curso, detalhar_curso, editar_curso, excluir_curso

class CursoUrlsTest(TestCase):
    """Testes para as URLs do aplicativo cursos"""
    
    def test_listar_cursos_url(self):
        """Teste da URL de listagem de cursos"""
        url = reverse('cursos:listar_cursos')
        self.assertEqual(url, '/cursos/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, listar_cursos)
    
    def test_criar_curso_url(self):
        """Teste da URL de criação de curso"""
        url = reverse('cursos:criar_curso')
        self.assertEqual(url, '/cursos/criar/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, criar_curso)





## cursos\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from cursos.models import Curso

class CursoViewTest(TestCase):
    """Testes para as views do aplicativo cursos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        # Criar um usuário para testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Fazer login com o usuário de teste
        self.client.login(username='testuser', password='testpassword')
        # Criar um curso para testes
        self.curso = Curso.objects.create(
            codigo_curso=301,
            nome="Curso de Teste",
            descricao="Descrição do curso de teste",
            duracao=6
        )
    
    def test_listar_cursos_view(self):
        """Teste da view de listagem de cursos"""
        response = self.client.get(reverse('cursos:listar_cursos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/listar_cursos.html')
        self.assertContains(response, "Curso de Teste")
        self.assertContains(response, "301")
    
    def test_criar_curso_view_get(self):
        """Teste da view de criação de curso (GET)"""
        response = self.client.get(reverse('cursos:criar_curso'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/criar_curso.html')
    
    def test_detalhar_curso_view(self):
        """Teste da view de detalhes de curso"""
        response = self.client.get(
            reverse('cursos:detalhar_curso', args=[self.curso.codigo_curso])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/detalhar_curso.html')
        self.assertContains(response, "Curso de Teste")



