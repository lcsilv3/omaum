# Código da Funcionalidade: alunos - Parte 1/3
*Gerado automaticamente*



## alunos\admin.py

python
from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'numero_iniciatico', 'email', 'cpf', 'sexo']
    search_fields = ['nome', 'numero_iniciatico', 'email', 'cpf']
    list_filter = ['sexo', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Dados Pessoais', {
            'fields': ['cpf', 'nome', 'data_nascimento', 'hora_nascimento', 'email', 'foto', 'sexo']
        }),
        ('Dados Iniciáticos', {
            'fields': ['numero_iniciatico', 'nome_iniciatico']
        }),
        ('Nacionalidade e Naturalidade', {
            'fields': ['nacionalidade', 'naturalidade']
        }),
        ('Endereço', {
            'fields': ['rua', 'numero_imovel', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
        }),
        ('Contatos de Emergência', {
            'fields': [
                'nome_primeiro_contato', 'celular_primeiro_contato', 'tipo_relacionamento_primeiro_contato',
                'nome_segundo_contato', 'celular_segundo_contato', 'tipo_relacionamento_segundo_contato'
            ]
        }),
        ('Informações Médicas', {
            'fields': [
                'tipo_sanguineo', 'fator_rh', 'alergias', 'condicoes_medicas_gerais', 
                'convenio_medico', 'hospital'
            ]
        }),
        ('Metadados', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]





## alunos\apps.py

python
from django.apps import AppConfig

class AlunosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alunos'





## alunos\forms.py

python
from django import forms
from django.core.validators import RegexValidator
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

class AlunoForm(forms.ModelForm):
    """
    Formulário para criação e edição de alunos.
    """
    # Validadores personalizados
    cpf_validator = RegexValidator(
        r'^\d{11}$',
        'O CPF deve conter exatamente 11 dígitos numéricos.'
    )
    
    # Campos com validação adicional
    cpf = forms.CharField(
        validators=[cpf_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Somente números'})
    )
    
    class Meta:
        model = get_aluno_model()
        fields = [
            'cpf', 'nome', 'data_nascimento', 'hora_nascimento', 'email', 'foto', 'sexo',
            'numero_iniciatico', 'nome_iniciatico',
            'nacionalidade', 'naturalidade',
            'rua', 'numero_imovel', 'complemento', 'bairro', 'cidade', 'estado', 'cep',
            'nome_primeiro_contato', 'celular_primeiro_contato', 'tipo_relacionamento_primeiro_contato',
            'nome_segundo_contato', 'celular_segundo_contato', 'tipo_relacionamento_segundo_contato',
            'tipo_sanguineo', 'fator_rh', 'alergias', 'condicoes_medicas_gerais', 'convenio_medico', 'hospital'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_nascimento': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'numero_iniciatico': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_iniciatico': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control', 'value': 'Brasileira'}),
            'naturalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_imovel': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Somente números'}),
            'nome_primeiro_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'celular_primeiro_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_relacionamento_primeiro_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_segundo_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'celular_segundo_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_relacionamento_segundo_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_sanguineo': forms.TextInput(attrs={'class': 'form-control'}),
            'fator_rh': forms.Select(attrs={'class': 'form-control'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'condicoes_medicas_gerais': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'convenio_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cpf': 'CPF',
            'nome': 'Nome Completo',
            'data_nascimento': 'Data de Nascimento',
            'hora_nascimento': 'Hora de Nascimento',
            'email': 'E-mail',
            'foto': 'Foto',
            'sexo': 'Sexo',
            'numero_iniciatico': 'Número Iniciático',
            'nome_iniciatico': 'Nome Iniciático',
            'nacionalidade': 'Nacionalidade',
            'naturalidade': 'Naturalidade',
            'rua': 'Rua',
            'numero_imovel': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'cep': 'CEP',
            'nome_primeiro_contato': 'Nome do Primeiro Contato',
            'celular_primeiro_contato': 'Celular do Primeiro Contato',
            'tipo_relacionamento_primeiro_contato': 'Relacionamento',
            'nome_segundo_contato': 'Nome do Segundo Contato',
            'celular_segundo_contato': 'Celular do Segundo Contato',
            'tipo_relacionamento_segundo_contato': 'Relacionamento',
            'tipo_sanguineo': 'Tipo Sanguíneo',
            'fator_rh': 'Fator RH',
            'alergias': 'Alergias',
            'condicoes_medicas_gerais': 'Condições Médicas',
            'convenio_medico': 'Convênio Médico',
            'hospital': 'Hospital de Preferência',
        }
        help_texts = {
            'cpf': 'Digite apenas os 11 números do CPF, sem pontos ou traços.',
            'data_nascimento': 'Formato: DD/MM/AAAA',
            'hora_nascimento': 'Formato: HH:MM',
            'numero_iniciatico': 'Número único de identificação do iniciado.',
            'cep': 'Digite apenas os 8 números do CEP, sem hífen.',
            'tipo_sanguineo': 'Ex: A, B, AB, O',
            'fator_rh': 'Positivo (+) ou Negativo (-)',
            'alergias': 'Liste todas as alergias conhecidas. Deixe em branco se não houver.',
            'condicoes_medicas_gerais': 'Descreva condições médicas relevantes. Deixe em branco se não houver.',
        }
    
    def clean_cpf(self):
        """Validação personalizada para o campo CPF."""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf = ''.join(filter(str.isdigit, cpf))
            
            # Verifica se tem 11 dígitos
            if len(cpf) != 11:
                raise forms.ValidationError('O CPF deve conter exatamente 11 dígitos.')
            
            # Aqui você poderia adicionar uma validação mais complexa do CPF
            # como verificar os dígitos verificadores
            
        return cpf
    
    def clean_nome(self):
        """Validação personalizada para o campo nome."""
        nome = self.cleaned_data.get('nome')
        if nome:
            # Capitaliza a primeira letra de cada palavra
            nome = ' '.join(word.capitalize() for word in nome.split())
        return nome
    
    def clean_email(self):
        """Validação personalizada para o campo email."""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()  # Converte para minúsculas
            
            # Verifica se o email já existe (exceto para o próprio registro em caso de edição)
            Aluno = get_aluno_model()
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                if Aluno.objects.filter(email=email).exclude(pk=instance.pk).exists():
                    raise forms.ValidationError('Este e-mail já está em uso por outro aluno.')
            else:
                if Aluno.objects.filter(email=email).exists():
                    raise forms.ValidationError('Este e-mail já está em uso.')
        return email
    
    def clean_cep(self):
        """Validação personalizada para o campo CEP."""
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remove caracteres não numéricos
            cep = ''.join(filter(str.isdigit, cep))
            
            # Verifica se tem 8 dígitos
            if len(cep) != 8:
                raise forms.ValidationError('O CEP deve conter exatamente 8 dígitos.')
        return cep
    
    def clean(self):
        """Validação global do formulário."""
        cleaned_data = super().clean()
        
        # Verifica se pelo menos um contato de emergência foi fornecido
        nome_primeiro_contato = cleaned_data.get('nome_primeiro_contato')
        celular_primeiro_contato = cleaned_data.get('celular_primeiro_contato')
        
        if not nome_primeiro_contato or not celular_primeiro_contato:
            self.add_error('nome_primeiro_contato', 'É necessário fornecer pelo menos um contato de emergência.')
            self.add_error('celular_primeiro_contato', 'É necessário fornecer pelo menos um contato de emergência.')
        
        return cleaned_data





## alunos\models.py

python
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

class Aluno(models.Model):
    # Opções para o campo sexo
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    # Opções para o campo fator_rh
    FATOR_RH_CHOICES = [
        ('+', 'Positivo'),
        ('-', 'Negativo'),
    ]
    
    # Validadores
    cpf_validator = RegexValidator(
        regex=r'^\d{11}$',
        message=_('CPF deve conter 11 dígitos numéricos')
    )
    
    celular_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message=_('Número de celular inválido')
    )
    
    # Campos do modelo
    cpf = models.CharField(
        max_length=11,
        primary_key=True,
        validators=[cpf_validator],
        verbose_name=_('CPF')
    )
    nome = models.CharField(max_length=100, verbose_name=_('Nome Completo'))
    data_nascimento = models.DateField(verbose_name=_('Data de Nascimento'))
    hora_nascimento = models.TimeField(
        null=True, 
        blank=True, 
        verbose_name=_('Hora de Nascimento')
    )
    email = models.EmailField(unique=True, verbose_name=_('E-mail'))
    foto = models.ImageField(
        upload_to='alunos/fotos/', 
        null=True, 
        blank=True, 
        verbose_name=_('Foto')
    )
    sexo = models.CharField(
        max_length=1, 
        choices=SEXO_CHOICES, 
        default='M', 
        verbose_name=_('Sexo')
    )
    
    # Dados iniciáticos - Tornando estes campos nullable
    numero_iniciatico = models.CharField(
        max_length=10, 
        unique=True, 
        null=True,  # Permitir nulo
        blank=True,  # Permitir em branco
        verbose_name=_('Número Iniciático')
    )
    nome_iniciatico = models.CharField(
        max_length=100, 
        null=True,  # Permitir nulo
        blank=True,  # Permitir em branco
        verbose_name=_('Nome Iniciático')
    )
    
    # Nacionalidade e naturalidade
    nacionalidade = models.CharField(
        max_length=50, 
        default='Brasileira', 
        verbose_name=_('Nacionalidade')
    )
    naturalidade = models.CharField(
        max_length=50, 
        verbose_name=_('Naturalidade')
    )
    
    # Endereço
    rua = models.CharField(max_length=100, verbose_name=_('Rua'))
    numero_imovel = models.CharField(max_length=10, verbose_name=_('Número'))
    complemento = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Complemento')
    )
    bairro = models.CharField(max_length=50, verbose_name=_('Bairro'))
    cidade = models.CharField(max_length=50, verbose_name=_('Cidade'))
    estado = models.CharField(max_length=2, verbose_name=_('Estado'))
    cep = models.CharField(max_length=8, verbose_name=_('CEP'))
    
    # Contatos de emergência
    nome_primeiro_contato = models.CharField(
        max_length=100, 
        verbose_name=_('Nome do Primeiro Contato')
    )
    celular_primeiro_contato = models.CharField(
        max_length=11, 
        validators=[celular_validator], 
        verbose_name=_('Celular do Primeiro Contato')
    )
    tipo_relacionamento_primeiro_contato = models.CharField(
        max_length=50, 
        verbose_name=_('Tipo de Relacionamento do Primeiro Contato')
    )
    
    nome_segundo_contato = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Nome do Segundo Contato')
    )
    celular_segundo_contato = models.CharField(
        max_length=11, 
        blank=True, 
        null=True, 
        validators=[celular_validator], 
        verbose_name=_('Celular do Segundo Contato')
    )
    tipo_relacionamento_segundo_contato = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_('Tipo de Relacionamento do Segundo Contato')
    )
    
    # Informações médicas
    tipo_sanguineo = models.CharField(
        max_length=3, 
        verbose_name=_('Tipo Sanguíneo')
    )
    fator_rh = models.CharField(
        max_length=1, 
        choices=FATOR_RH_CHOICES, 
        verbose_name=_('Fator RH')
    )
    alergias = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('Alergias')
    )
    condicoes_medicas_gerais = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('Condições Médicas Gerais')
    )
    convenio_medico = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Convênio Médico')
    )
    hospital = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Hospital de Preferência')
    )
    
    # Metadados - Definindo um valor padrão para created_at
    created_at = models.DateTimeField(
        default=timezone.now,  # Valor padrão
        verbose_name=_('Criado em')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Atualizado em')
    )
    
    def __str__(self):
        return self.nome
    
    def clean(self):
        """Validação personalizada para o modelo."""
        super().clean()
    
    class Meta:
        verbose_name = _('Aluno')
        verbose_name_plural = _('Alunos')
        ordering = ['nome']





## alunos\tests.py

python
from django.test import TestCase
from alunos.models import Aluno
from datetime import date, time
from django.core.exceptions import ValidationError  # Adicionada importação faltante


class AlunoTest(TestCase):
    def test_criar_aluno(self):
        aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Test',
            data_nascimento=date(1995, 5, 15),
            hora_nascimento=time(14, 30),
            email='joao@test.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Test',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Test',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        self.assertEqual(aluno.nome, 'João Test')

class AlunoValidationTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'cpf': '12345678901',
            'nome': 'Carlos Souza',
            'data_nascimento': date(1975, 12, 25),
            'hora_nascimento': time(8, 30),
            'email': 'carlos@example.com',
            'sexo': 'M',
            'nacionalidade': 'Brasileira',
            'naturalidade': 'São Paulo',
            'rua': 'Rua Augusta',
            'numero_imovel': '789',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'bairro': 'Consolação',
            'cep': '01234567',
            'nome_primeiro_contato': 'Pedro Souza',
            'celular_primeiro_contato': '11999999999',
            'tipo_relacionamento_primeiro_contato': 'Pai',
            'nome_segundo_contato': 'Julia Souza',
            'celular_segundo_contato': '11988888888',
            'tipo_relacionamento_segundo_contato': 'Mãe',
            'tipo_sanguineo': 'B',
            'fator_rh': '+'
        }

    def test_cpf_invalido(self):
        self.valid_data['cpf'] = '123'
        aluno = Aluno(**self.valid_data)
        with self.assertRaises(ValidationError):
            aluno.full_clean()

    def test_email_invalido(self):
        self.valid_data['email'] = 'email_invalido'
        aluno = Aluno(**self.valid_data)
        with self.assertRaises(ValidationError):
            aluno.full_clean()

    def test_sexo_invalido(self):
        self.valid_data['sexo'] = 'X'
        aluno = Aluno(**self.valid_data)
        with self.assertRaises(ValidationError):
            aluno.full_clean()

    def test_data_futura_invalida(self):
        self.valid_data['data_nascimento'] = date(2025, 1, 1)
        aluno = Aluno(**self.valid_data)
        with self.assertRaises(ValidationError):
            aluno.full_clean()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class SeleniumTestCase(TestCase):
    def setUp(self):
        service = Service('chromedriver.exe')  # Path to your chromedriver
        self.driver = webdriver.Chrome(service=service)
        
    def tearDown(self):
        self.driver.quit()




## alunos\test_models.py

python
from django.test import TestCase
from alunos.models import Aluno
from datetime import date, time

class AlunoModelTest(TestCase):
    def test_criar_aluno(self):
        aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Test',
            data_nascimento=date(1995, 5, 15),
            hora_nascimento=time(14, 30),
            email='joao@test.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Test',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Test',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        self.assertEqual(aluno.nome, 'João Test')





## alunos\test_ui.py

python
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from alunos.models import Aluno
from datetime import date, time

class AlunoUITest(LiveServerTestCase):
    def setUp(self):
        service = Service('chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        
        # Create a test student
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='Maria Test',
            data_nascimento=date(1995, 5, 15),
            hora_nascimento=time(14, 30),
            email='maria@test.com',
            sexo='F',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='João Test',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Pai',
            nome_segundo_contato='Ana Test',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Mãe',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def tearDown(self):
        self.browser.quit()

    def test_listar_alunos(self):
        # Access the student listing page
        self.browser.get(f'{self.live_server_url}/alunos/')
        
        # Check page title
        self.assertIn('Lista de Alunos', self.browser.title)
        
        # Check header
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(header.text, 'Lista de Alunos')
        
        # Check if test student is listed
        student_element = self.browser.find_element(By.CLASS_NAME, 'aluno-nome')
        self.assertEqual(student_element.text, 'Maria Test')





## alunos\urls.py

python
from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('', views.listar_alunos, name='listar_alunos'),
    path('criar/', views.criar_aluno, name='criar_aluno'),
    path('cadastrar/', views.criar_aluno, name='cadastrar_aluno'),  # Alias para compatibilidade
    path('<str:cpf>/detalhes/', views.detalhar_aluno, name='detalhar_aluno'),
    path('<str:cpf>/editar/', views.editar_aluno, name='editar_aluno'),
    path('<str:cpf>/excluir/', views.excluir_aluno, name='excluir_aluno'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exportar/', views.exportar_alunos, name='exportar_alunos'),
    path('importar/', views.importar_alunos, name='importar_alunos'),
    path('relatorio/', views.relatorio_alunos, name='relatorio_alunos'),
]





## alunos\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from importlib import import_module
from django.core.exceptions import ValidationError

def get_models():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_forms():
    """Obtém o formulário AlunoForm dinamicamente."""
    alunos_forms = import_module('alunos.forms')
    return getattr(alunos_forms, 'AlunoForm')

@login_required
def listar_alunos(request):
    """Lista todos os alunos cadastrados."""
    try:
        Aluno = get_models()
        
        # Obter parâmetros de busca e filtro
        query = request.GET.get('q', '')
        
        # Filtrar alunos
        alunos = Aluno.objects.all()
        
        if query:
            alunos = alunos.filter(
                Q(nome__icontains=query) | 
                Q(cpf__icontains=query) | 
                Q(email__icontains=query) |
                Q(numero_iniciatico__icontains=query)
            )
        
        # Paginação
        paginator = Paginator(alunos, 10)  # 10 alunos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Obter cursos para o filtro
        try:
            Curso = import_module('cursos.models').Curso
            cursos = Curso.objects.all()
        except:
            cursos = []
        
        context = {
            'alunos': page_obj,
            'page_obj': page_obj,
            'query': query,
            'cursos': cursos,
            'curso_selecionado': request.GET.get('curso', ''),
        }
        
        return render(request, 'alunos/listar_alunos.html', context)
    except Exception as e:
        # Em vez de mostrar a mensagem de erro, apenas retornamos uma lista vazia
        return render(request, 'alunos/listar_alunos.html', {
            'alunos': [],
            'page_obj': None,
            'query': '',
            'cursos': [],
            'curso_selecionado': '',
        })

@login_required
def criar_aluno(request):
    """Cria um novo aluno."""
    AlunoForm = get_forms()
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                aluno = form.save()
                messages.success(request, 'Aluno cadastrado com sucesso!')
                return redirect('alunos:detalhar_aluno', cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar aluno: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AlunoForm()
    
    return render(request, 'alunos/formulario_aluno.html', {'form': form, 'aluno': None})

@login_required
def detalhar_aluno(request, cpf):
    """Exibe os detalhes de um aluno."""
    Aluno = get_models()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    return render(request, 'alunos/detalhar_aluno.html', {'aluno': aluno})

@login_required
def editar_aluno(request, cpf):
    """Edita um aluno existente."""
    Aluno = get_models()
    AlunoForm = get_forms()
    
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Aluno atualizado com sucesso!')
                return redirect('alunos:detalhar_aluno', cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                messages.error(request, f'Erro ao atualizar aluno: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AlunoForm(instance=aluno)
    
    return render(request, 'alunos/formulario_aluno.html', {'form': form, 'aluno': aluno})

@login_required
def excluir_aluno(request, cpf):
    """Exclui um aluno."""
    Aluno = get_models()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    if request.method == 'POST':
        try:
            aluno.delete()
            messages.success(request, 'Aluno excluído com sucesso!')
            return redirect('alunos:listar_alunos')
        except Exception as e:
            messages.error(request, f'Erro ao excluir aluno: {str(e)}')
            return redirect('alunos:detalhar_aluno', cpf=aluno.cpf)
    
    return render(request, 'alunos/excluir_aluno.html', {'aluno': aluno})

@login_required
def dashboard(request):
    """Exibe o dashboard de alunos com estatísticas."""
    try:
        Aluno = get_models()
        total_alunos = Aluno.objects.count()
        
        # Contagem por sexo
        total_masculino = Aluno.objects.filter(sexo='M').count()
        total_feminino = Aluno.objects.filter(sexo='F').count()
        total_outros = Aluno.objects.filter(sexo='O').count()
        
        # Alunos recentes
        alunos_recentes = Aluno.objects.order_by('-created_at')[:5]
        
        context = {
            'total_alunos': total_alunos,
            'total_masculino': total_masculino,
            'total_feminino': total_feminino,
            'total_outros': total_outros,
            'alunos_recentes': alunos_recentes,
        }
        
        return render(request, 'alunos/dashboard.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao carregar dashboard: {str(e)}")
        return redirect('alunos:listar_alunos')

@login_required
def exportar_alunos(request):
    """Exporta os dados dos alunos para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        
        Aluno = get_models()
        alunos = Aluno.objects.all()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="alunos.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['CPF', 'Nome', 'Email', 'Data de Nascimento', 'Sexo', 'Número Iniciático'])
        
        for aluno in alunos:
            writer.writerow([
                aluno.cpf,
                aluno.nome,
                aluno.email,
                aluno.data_nascimento,
                aluno.get_sexo_display(),
                aluno.numero_iniciatico
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar alunos: {str(e)}")
        return redirect('alunos:listar_alunos')

@login_required
def importar_alunos(request):
    """Importa alunos de um arquivo CSV."""
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            import csv
            from io import TextIOWrapper
            
            Aluno = get_models()
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Processar cada linha do CSV
                    Aluno.objects.create(
                        cpf=row.get('CPF', '').strip(),
                        nome=row.get('Nome', '').strip(),
                        email=row.get('Email', '').strip(),
                        data_nascimento=row.get('Data de Nascimento', '').strip(),
                        sexo=row.get('Sexo', 'M')[0].upper(),  # Pega a primeira letra e converte para maiúscula
                        numero_iniciatico=row.get('Número Iniciático', '').strip(),
                        nome_iniciatico=row.get('Nome Iniciático', row.get('Nome', '')).strip(),
                        nacionalidade=row.get('Nacionalidade', 'Brasileira').strip(),
                        naturalidade=row.get('Naturalidade', '').strip(),
                        rua=row.get('Rua', '').strip(),
                        numero_imovel=row.get('Número', '').strip(),
                        complemento=row.get('Complemento', '').strip(),
                        bairro=row.get('Bairro', '').strip(),
                        cidade=row.get('Cidade', '').strip(),
                        estado=row.get('Estado', '').strip(),
                        cep=row.get('CEP', '').strip(),
                        nome_primeiro_contato=row.get('Nome do Primeiro Contato', '').strip(),
                        celular_primeiro_contato=row.get('Celular do Primeiro Contato', '').strip(),
                        tipo_relacionamento_primeiro_contato=row.get('Tipo de Relacionamento do Primeiro Contato', '').strip(),
                        tipo_sanguineo=row.get('Tipo Sanguíneo', '').strip(),
                        fator_rh=row.get('Fator RH', '+').strip(),
                    )
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(request, f"{count} alunos importados com {len(errors)} erros.")
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(request, f"... e mais {len(errors) - 5} erros.")
            else:
                messages.success(request, f"{count} alunos importados com sucesso!")
            
            return redirect('alunos:listar_alunos')
        except Exception as e:
            messages.error(request, f"Erro ao importar alunos: {str(e)}")
    
    return render(request, 'alunos/importar_alunos.html')

@login_required
def relatorio_alunos(request):
    """Exibe um relatório com estatísticas sobre os alunos."""
    try:
        Aluno = get_models()
        total_alunos = Aluno.objects.count()
        total_masculino = Aluno.objects.filter(sexo='M').count()
        total_feminino = Aluno.objects.filter(sexo='F').count()
        total_outros = Aluno.objects.filter(sexo='O').count()
        
        # Calcular idade média
        from django.db.models import Avg, F
        from django.db.models.functions import ExtractYear
        from django.utils import timezone
        
        current_year = timezone.now().year
        idade_media = Aluno.objects.annotate(
            idade=current_year - ExtractYear('data_nascimento')
        ).aggregate(Avg('idade'))['idade__avg'] or 0
        
        context = {
            'total_alunos': total_alunos,
            'total_masculino': total_masculino,
            'total_feminino': total_feminino,
            'total_outros': total_outros,
            'idade_media': round(idade_media, 1),
        }
        
        return render(request, 'alunos/relatorio_alunos.html', context)
    except Exception as e:
        messages.error(request, f"Erro ao gerar relatório: {str(e)}")
        return redirect('alunos:listar_alunos')




## alunos\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-04-03 17:19

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('cpf', models.CharField(max_length=11, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='CPF deve conter 11 dígitos numéricos', regex='^\\d{11}$')], verbose_name='CPF')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('hora_nascimento', models.TimeField(blank=True, null=True, verbose_name='Hora de Nascimento')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='alunos/fotos/', verbose_name='Foto')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], default='M', max_length=1, verbose_name='Sexo')),
                ('numero_iniciatico', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Número Iniciático')),
                ('nome_iniciatico', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome Iniciático')),
                ('nacionalidade', models.CharField(default='Brasileira', max_length=50, verbose_name='Nacionalidade')),
                ('naturalidade', models.CharField(max_length=50, verbose_name='Naturalidade')),
                ('rua', models.CharField(max_length=100, verbose_name='Rua')),
                ('numero_imovel', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('cidade', models.CharField(max_length=50, verbose_name='Cidade')),
                ('estado', models.CharField(max_length=2, verbose_name='Estado')),
                ('cep', models.CharField(max_length=8, verbose_name='CEP')),
                ('nome_primeiro_contato', models.CharField(max_length=100, verbose_name='Nome do Primeiro Contato')),
                ('celular_primeiro_contato', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Número de celular inválido', regex='^\\d{10,11}$')], verbose_name='Celular do Primeiro Contato')),
                ('tipo_relacionamento_primeiro_contato', models.CharField(max_length=50, verbose_name='Tipo de Relacionamento do Primeiro Contato')),
                ('nome_segundo_contato', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome do Segundo Contato')),
                ('celular_segundo_contato', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='Número de celular inválido', regex='^\\d{10,11}$')], verbose_name='Celular do Segundo Contato')),
                ('tipo_relacionamento_segundo_contato', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo de Relacionamento do Segundo Contato')),
                ('tipo_sanguineo', models.CharField(max_length=3, verbose_name='Tipo Sanguíneo')),
                ('fator_rh', models.CharField(choices=[('+', 'Positivo'), ('-', 'Negativo')], max_length=1, verbose_name='Fator RH')),
                ('alergias', models.TextField(blank=True, null=True, verbose_name='Alergias')),
                ('condicoes_medicas_gerais', models.TextField(blank=True, null=True, verbose_name='Condições Médicas Gerais')),
                ('convenio_medico', models.CharField(blank=True, max_length=100, null=True, verbose_name='Convênio Médico')),
                ('hospital', models.CharField(blank=True, max_length=100, null=True, verbose_name='Hospital de Preferência')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Aluno',
                'verbose_name_plural': 'Alunos',
                'ordering': ['nome'],
            },
        ),
    ]



