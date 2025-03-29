# Código da Funcionalidade: alunos
*Gerado automaticamente*



## alunos\admin.py

python
from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cpf']
    search_fields = ['nome', 'email', 'cpf']
    list_filter = ['sexo', 'status']





## alunos\apps.py

python
from django.apps import AppConfig

class AlunosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alunos'





## alunos\forms.py

python
from django import forms
from alunos.models import Aluno  # Corrigido: importar do módulo alunos
from django.core.exceptions import ValidationError


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'cpf', 'nome', 'data_nascimento', 'hora_nascimento', 'email', 
            'sexo', 'nacionalidade', 'naturalidade', 'rua', 'numero_imovel', 
            'cidade', 'estado', 'bairro', 'cep', 'nome_primeiro_contato', 
            'celular_primeiro_contato', 'tipo_relacionamento_primeiro_contato', 
            'nome_segundo_contato', 'celular_segundo_contato', 
            'tipo_relacionamento_segundo_contato', 'tipo_sanguineo', 'fator_rh',
            'curso'
        ]
        # Você pode adicionar widgets personalizados aqui se necessário

    def clean(self):
        cleaned_data = super().clean()
        # Adicionar validações cruzadas aqui se necessário
        return cleaned_data


class ImportForm(forms.Form):
    file = forms.FileField()





## alunos\models.py

python
from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.utils import timezone

class Aluno(models.Model):
    SEXO_CHOICES = [
        ('M', _('Masculino')),
        ('F', _('Feminino')),
        ('O', _('Outro')),
    ]

    TIPO_SANGUINEO_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    FATOR_RH_CHOICES = [
        ('+', 'Positivo'),
        ('-', 'Negativo'),
    ]

    ESTADO_CIVIL_CHOICES = [
        ('S', _('Solteiro(a)')),
        ('C', _('Casado(a)')),
        ('D', _('Divorciado(a)')),
        ('V', _('Viúvo(a)')),
        ('U', _('União Estável')),
    ]

    ESCOLARIDADE_CHOICES = [
        ('EF', _('Ensino Fundamental')),
        ('EM', _('Ensino Médio')),
        ('ES', _('Ensino Superior')),
        ('PG', _('Pós-Graduação')),
        ('ME', _('Mestrado')),
        ('DO', _('Doutorado')),
    ]

    STATUS_CHOICES = [
        ('A', _('Ativo')),
        ('I', _('Inativo')),
        ('S', _('Suspenso')),
    ]
    cpf_validator = RegexValidator(
        regex=r'^\d{11}$',
        message=_('CPF deve conter 11 dígitos numéricos')
    )

    celular_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message=_('Número de celular inválido')
    )

    cep_validator = RegexValidator(
        regex=r'^\d{8}$',
        message=_('CEP deve conter 8 dígitos numéricos')
    )

    telefone_fixo_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message=_('Número de telefone fixo inválido')
    )
    cpf = models.CharField(
        _('CPF'),
        max_length=11,
        primary_key=True,
        validators=[cpf_validator],
        help_text=_('Digite apenas números')
    )
    foto = models.ImageField(
        _('Foto'),
        upload_to='alunos/',
        null=True,
        blank=True
    )
    nome = models.CharField(
        _('Nome completo'),
        max_length=100
    )
    data_nascimento = models.DateField(_('Data de nascimento'))
    hora_nascimento = models.TimeField(_('Hora de nascimento'))
    numero_iniciatico = models.CharField(
        _('Número iniciático'),
        max_length=20,
        blank=True,
        null=True
    )
    nome_iniciatico = models.CharField(
        _('Nome iniciático'),
        max_length=100,
        blank=True,
        null=True
    )
    data_iniciacao = models.DateField(_('Data de iniciação'), null=True, blank=True)

    sexo = models.CharField(
        _('Sexo'),
        max_length=1,
        choices=SEXO_CHOICES
    )
    estado_civil = models.CharField(
        _('Estado Civil'),
        max_length=1,
        choices=ESTADO_CIVIL_CHOICES,
        null=True,  # Adicione esta linha
        blank=True,  # Adicione esta linha
        default='S'  # Adicione esta linha (S para Solteiro como padrão)
    )

    profissao = models.CharField(
        _('Profissão'), 
        max_length=100,
        null=True,  # Adicione esta linha
        blank=True  # Adicione esta linha
    )
    escolaridade = models.CharField(
        _('Escolaridade'),
        max_length=2,
        choices=ESCOLARIDADE_CHOICES,
        null=True,  # Adicione esta linha
        blank=True  # Adicione esta linha
    )

    email = models.EmailField(
        _('E-mail'),
        validators=[EmailValidator()]
    )
    telefone_fixo = models.CharField(
        _('Telefone Fixo'),
        max_length=11,
        validators=[telefone_fixo_validator],
        blank=True,
        null=True
    )
    nacionalidade = models.CharField(_('Nacionalidade'), max_length=50)
    naturalidade = models.CharField(_('Naturalidade'), max_length=50)
    cep = models.CharField(
        _('CEP'),
        max_length=8,
        validators=[cep_validator]
    )
    rua = models.CharField(_('Rua'), max_length=100)
    numero_imovel = models.CharField(_('Número'), max_length=10)
    complemento = models.CharField(
        _('Complemento'),
        max_length=50,
        blank=True,
        null=True
    )
    bairro = models.CharField(_('Bairro'), max_length=50)
    cidade = models.CharField(_('Cidade'), max_length=50)
    estado = models.CharField(_('Estado'), max_length=2)
    nome_primeiro_contato = models.CharField(
        _('Nome do primeiro contato'),
        max_length=100
    )
    celular_primeiro_contato = models.CharField(
        _('Celular do primeiro contato'),
        max_length=11,
        validators=[celular_validator]
    )
    tipo_relacionamento_primeiro_contato = models.CharField(
        _('Relacionamento do primeiro contato'),
        max_length=50
    )
    nome_segundo_contato = models.CharField(
        _('Nome do segundo contato'),
        max_length=100
    )
    celular_segundo_contato = models.CharField(
        _('Celular do segundo contato'),
        max_length=11,
        validators=[celular_validator]
    )
    tipo_relacionamento_segundo_contato = models.CharField(
        _('Relacionamento do segundo contato'),
        max_length=50
    )
    tipo_sanguineo = models.CharField(
        _('Tipo sanguíneo'),
        max_length=2,
        choices=TIPO_SANGUINEO_CHOICES
    )
    fator_rh = models.CharField(
        _('Fator RH'),
        max_length=1,
        choices=FATOR_RH_CHOICES
    )
    alergias = models.TextField(
        _('Alergias'),
        blank=True,
        null=True
    )
    condicoes_medicas_gerais = models.TextField(
        _('Condições médicas'),
        blank=True,
        null=True
    )
    convenio_medico = models.CharField(
        _('Convênio médico'),
        max_length=100,
        blank=True,
        null=True
    )
    hospital = models.CharField(
        _('Hospital de preferência'),
        max_length=100,
        blank=True,
        null=True
    )
    status = models.CharField(
        _('Status'),
        max_length=1,
        choices=STATUS_CHOICES,
        default='A'
    )

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(
        _('Atualizado em'),
        auto_now=True
    )

    curso = models.ForeignKey(
        'cursos.Curso',  # Use string reference to avoid circular imports
        on_delete=models.SET_NULL,  # Prevent deletion of Curso if students are enrolled
        verbose_name=_('Curso'),
        related_name='alunos',  # This allows curso.alunos.all() to get all students in a course
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Aluno')
        verbose_name_plural = _('Alunos')
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('aluno-detail', args=[str(self.cpf)])

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not self.curso_id:
            raise ValidationError({'curso': _('Todo aluno deve estar associado a um curso.')})

    @property
    def idade(self):
        today = date.today()
        return today.year - self.data_nascimento.year - (
            (today.month, today.day) <
            (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def tempo_desde_iniciacao(self):
        if self.data_iniciacao:
            today = date.today()
            delta = today - self.data_iniciacao
            return delta.days
        return None





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
    path('', views.listar_alunos, name='listar'),
    path('buscar/', views.buscar_alunos, name='buscar'),
    path('cadastrar/', views.cadastrar_aluno, name='cadastrar'),
    path('editar/<str:cpf>/', views.editar_aluno, name='editar'),
    path('excluir/<str:cpf>/', views.excluir_aluno, name='excluir'),
    path('detalhes/<str:cpf>/', views.detalhes_aluno, name='detalhes'),
    path('exportar/', views.exportar_alunos, name='exportar'),
    path('importar/', views.importar_alunos, name='importar'),
    path('relatorio/', views.relatorio_alunos, name='relatorio'),
    path('dashboard/', views.dashboard, name='dashboard'),
]





## alunos\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import HttpResponse
import csv
from io import StringIO
from importlib import import_module

# Importar modelos e formulários
Aluno = import_module('alunos.models').Aluno
AlunoForm = import_module('alunos.forms').AlunoForm
ImportForm = import_module('alunos.forms').ImportForm
# Obter o modelo Curso de onde estiver definido
Curso = import_module('cursos.models').Curso

@login_required
def listar_alunos(request):
    query = request.GET.get('q')
    curso_id = request.GET.get('curso')

    queryset = Aluno.objects.all()

    if query:
        queryset = queryset.filter(
            Q(nome__icontains=query) | 
            Q(cpf__icontains=query) | 
            Q(email__icontains=query)
        )

    if curso_id:
        queryset = queryset.filter(curso_id=curso_id)

    queryset = queryset.select_related('curso')

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cursos = Curso.objects.all()

    return render(request, 'alunos/listar_alunos.html', {
        'page_obj': page_obj,
        'alunos': page_obj,
        'query': query,
        'cursos': cursos,
        'curso_selecionado': curso_id
    })

@login_required
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Aluno cadastrado com sucesso!'))
            return redirect('alunos:listar')
        else:
            messages.error(request, _('Erro ao cadastrar aluno. Verifique os dados.'))
    else:
        form = AlunoForm()
    return render(request, 'alunos/aluno_form.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Aluno
from .forms import AlunoForm
@login_required
def editar_aluno(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, _('Dados do aluno atualizados com sucesso!'))
            return redirect('alunos:detalhes', cpf=aluno.cpf)
        else:
            messages.error(request, _('Erro ao atualizar dados do aluno. Por favor, verifique os dados.'))
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'alunos/editar_aluno.html', {'form': form, 'aluno': aluno})

@login_required
def detalhes_aluno(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    return render(request, 'alunos/detalhes_aluno.html', {'aluno': aluno})

@login_required
def excluir_aluno(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == 'POST':
        if request.POST.get('confirmar') == 'sim':
            aluno.delete()
            messages.success(request, _('Aluno excluído com sucesso!'))
            return redirect('alunos:listar')
        else:
            messages.info(request, _('Exclusão cancelada.'))
            return redirect('alunos:detalhes', cpf=cpf)
    return render(request, 'alunos/excluir_aluno.html', {'aluno': aluno})

@login_required
def buscar_alunos(request):
    query = request.GET.get('q', '')
    alunos = Aluno.objects.filter(
        Q(nome__icontains=query) |
        Q(cpf__icontains=query) |
        Q(email__icontains=query)
    ) if query else Aluno.objects.none()
    return render(request, 'alunos/buscar.html', {'alunos': alunos, 'query': query})

@login_required
def exportar_alunos(request):
    alunos = Aluno.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alunos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'CPF', 'Email', 'Data de Nascimento'])

    for aluno in alunos:
        writer.writerow([aluno.nome, aluno.cpf, aluno.email, aluno.data_nascimento])
    return response

@login_required
def importar_alunos(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = StringIO(decoded_file)
            next(io_string)  # Pular o cabeçalho
            for row in csv.reader(io_string, delimiter=','):
                _, created = Aluno.objects.update_or_create(
                    cpf=row[1],
                    defaults={
                        'nome': row[0],
                        'email': row[2],
                        'data_nascimento': row[3],
                    }
                )
            messages.success(request, _('Alunos importados com sucesso!'))
            return redirect('alunos:listar')
    else:
        form = ImportForm()
    return render(request, 'alunos/importar.html', {'form': form})

@login_required
def relatorio_alunos(request):
    alunos = Aluno.objects.all()
    total_alunos = alunos.count()
    # Remover referência a curso se não existir no modelo
    context = {
        'alunos': alunos,
        'total_alunos': total_alunos,
    }
    return render(request, 'alunos/relatorio.html', context)

@login_required
def dashboard(request):
    context = {
        'total_alunos': Aluno.objects.count(),
        'alunos_ativos': Aluno.objects.filter(status='A').count(),
        'alunos_recentes': Aluno.objects.order_by('-created_at')[:5],
    }
    
    try:
        Curso = apps.get_model('core', 'Curso')
        context['total_cursos'] = Curso.objects.count()
        
        # Dados para o gráfico
        cursos = Curso.objects.all()
        context['cursos_labels'] = [curso.nome for curso in cursos]
        context['alunos_por_curso_data'] = [0] * len(cursos)  # Placeholder
    except:
        context['total_cursos'] = 0
        context['cursos_labels'] = []
        context['alunos_por_curso_data'] = []

    return render(request, 'alunos/dashboard.html', context)




## alunos\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-03-26 11:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('cpf', models.CharField(help_text='Digite apenas números', max_length=11, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='CPF deve conter 11 dígitos numéricos', regex='^\\d{11}$')], verbose_name='CPF')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='alunos/', verbose_name='Foto')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome completo')),
                ('data_nascimento', models.DateField(verbose_name='Data de nascimento')),
                ('hora_nascimento', models.TimeField(verbose_name='Hora de nascimento')),
                ('numero_iniciatico', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número iniciático')),
                ('nome_iniciatico', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome iniciático')),
                ('data_iniciacao', models.DateField(blank=True, null=True, verbose_name='Data de iniciação')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=1, verbose_name='Sexo')),
                ('estado_civil', models.CharField(blank=True, choices=[('S', 'Solteiro(a)'), ('C', 'Casado(a)'), ('D', 'Divorciado(a)'), ('V', 'Viúvo(a)'), ('U', 'União Estável')], default='S', max_length=1, null=True, verbose_name='Estado Civil')),
                ('profissao', models.CharField(blank=True, max_length=100, null=True, verbose_name='Profissão')),
                ('escolaridade', models.CharField(blank=True, choices=[('EF', 'Ensino Fundamental'), ('EM', 'Ensino Médio'), ('ES', 'Ensino Superior'), ('PG', 'Pós-Graduação'), ('ME', 'Mestrado'), ('DO', 'Doutorado')], max_length=2, null=True, verbose_name='Escolaridade')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='E-mail')),
                ('telefone_fixo', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='Número de telefone fixo inválido', regex='^\\d{10,11}$')], verbose_name='Telefone Fixo')),
                ('nacionalidade', models.CharField(max_length=50, verbose_name='Nacionalidade')),
                ('naturalidade', models.CharField(max_length=50, verbose_name='Naturalidade')),
                ('cep', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='CEP deve conter 8 dígitos numéricos', regex='^\\d{8}$')], verbose_name='CEP')),
                ('rua', models.CharField(max_length=100, verbose_name='Rua')),
                ('numero_imovel', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('cidade', models.CharField(max_length=50, verbose_name='Cidade')),
                ('estado', models.CharField(max_length=2, verbose_name='Estado')),
                ('nome_primeiro_contato', models.CharField(max_length=100, verbose_name='Nome do primeiro contato')),
                ('celular_primeiro_contato', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Número de celular inválido', regex='^\\d{10,11}$')], verbose_name='Celular do primeiro contato')),
                ('tipo_relacionamento_primeiro_contato', models.CharField(max_length=50, verbose_name='Relacionamento do primeiro contato')),
                ('nome_segundo_contato', models.CharField(max_length=100, verbose_name='Nome do segundo contato')),
                ('celular_segundo_contato', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Número de celular inválido', regex='^\\d{10,11}$')], verbose_name='Celular do segundo contato')),
                ('tipo_relacionamento_segundo_contato', models.CharField(max_length=50, verbose_name='Relacionamento do segundo contato')),
                ('tipo_sanguineo', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], max_length=2, verbose_name='Tipo sanguíneo')),
                ('fator_rh', models.CharField(choices=[('+', 'Positivo'), ('-', 'Negativo')], max_length=1, verbose_name='Fator RH')),
                ('alergias', models.TextField(blank=True, null=True, verbose_name='Alergias')),
                ('condicoes_medicas_gerais', models.TextField(blank=True, null=True, verbose_name='Condições médicas')),
                ('convenio_medico', models.CharField(blank=True, max_length=100, null=True, verbose_name='Convênio médico')),
                ('hospital', models.CharField(blank=True, max_length=100, null=True, verbose_name='Hospital de preferência')),
                ('status', models.CharField(choices=[('A', 'Ativo'), ('I', 'Inativo'), ('S', 'Suspenso')], default='A', max_length=1, verbose_name='Status')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('curso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alunos', to='cursos.curso', verbose_name='Curso')),
            ],
            options={
                'verbose_name': 'Aluno',
                'verbose_name_plural': 'Alunos',
                'ordering': ['nome'],
            },
        ),
    ]





## alunos\templates\alunos\aluno_form.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container">
  <h1>Cadastrar Novo Aluno</h1>
  <form method="post" class="aluno-form">
    {% csrf_token %}
    {% if form.non_field_errors %}
      <div class="alert alert-danger">
        {% for error in form.non_field_errors %}
          {{ error }}
        {% endfor %}
      </div>
    {% endif %}
    {% for field in form %}
      <div class="form-group">
        {{ field.label_tag }}
        {{ field }}
        {% if field.errors %}
          <div class="alert alert-danger">
            {% for error in field.errors %}
              {{ error }}
            {% endfor %}
          </div>
        {% endif %}
        {% if field.help_text %}
          <small class="form-text text-muted">{{ field.help_text }}</small>
        {% endif %}
      </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary">Cadastrar Aluno</button>
  </form>
</div>
{% endblock %}






## alunos\templates\alunos\dashboard.html

html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">Dashboard de Alunos</h1>

    <div class="row">
        <!-- Cartão de Total de Alunos -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-primary">
                <div class="card-body">
                    <h5 class="card-title">Total de Alunos</h5>
                    <p class="card-text display-4">{{ total_alunos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Alunos Ativos -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-success">
                <div class="card-body">
                    <h5 class="card-title">Alunos Ativos</h5>
                    <p class="card-text display-4">{{ alunos_ativos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Alunos por Curso -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-info">
                <div class="card-body">
                    <h5 class="card-title">Cursos</h5>
                    <p class="card-text display-4">{{ total_cursos }}</p>
                </div>
            </div>
        </div>

        <!-- Cartão de Atividades Recentes -->
        <div class="col-md-3 mb-4">
            <div class="card text-white bg-warning">
                <div class="card-body">
                    <h5 class="card-title">Atividades Recentes</h5>
                    <p class="card-text display-4">{{ atividades_recentes }}</p>
                </div>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <!-- Gráfico de Alunos por Curso -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Alunos por Curso</h5>
                    <canvas id="alunosPorCursoChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Lista de Alunos Recentes -->
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Alunos Recentemente Adicionados</h5>
                    <ul class="list-group">
                        {% for aluno in alunos_recentes %}
                            <li class="list-group-item">
                                {{ aluno.nome }}
                                <a href="{% url 'alunos:detalhes' aluno.cpf %}" class="btn btn-sm btn-info float-right">Detalhes</a>
                            </li>
                        {% empty %}
                            <li class="list-group-item">Nenhum aluno recente.</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <!-- Ações Rápidas -->
        <div class="col-md-12">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Ações Rápidas</h5>
                    <a href="{% url 'alunos:cadastrar' %}" class="btn btn-primary mr-2">Cadastrar Novo Aluno</a>
                    <a href="{% url 'alunos:listar' %}" class="btn btn-secondary mr-2">Listar Todos os Alunos</a>
                    <a href="{% url 'alunos:exportar' %}" class="btn btn-success mr-2">Exportar Dados</a>
                    <a href="{% url 'alunos:importar' %}" class="btn btn-info">Importar Dados</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('alunosPorCursoChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: JSON.parse('{{ cursos_labels|safe }}'),
            datasets: [{
                label: 'Número de Alunos',
                data: JSON.parse('{{ alunos_por_curso_data|safe }}'),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
</script>
{% endblock %}





## alunos\templates\alunos\detalhes_aluno.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Aluno - {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h2>Detalhes do Aluno</h2>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    {% if aluno.foto %}
                        <img src="{{ aluno.foto.url }}" alt="Foto de {{ aluno.nome }}" class="img-fluid rounded">
                    {% else %}
                        <div class="text-center p-5 bg-light rounded">
                            <i class="fas fa-user fa-5x text-secondary"></i>
                            <p class="mt-2">Sem foto</p>
                        </div>
                    {% endif %}
                </div>
                <div class="col-md-8">
                    <h3>{{ aluno.nome }}</h3>
                    <p><strong>CPF:</strong> {{ aluno.cpf }}</p>
                    <p><strong>Data de Nascimento:</strong> {{ aluno.data_nascimento }}</p>
                    <p><strong>Idade:</strong> {{ aluno.idade }} anos</p>
                    <p><strong>Email:</strong> {{ aluno.email }}</p>
                    <p><strong>Sexo:</strong> {{ aluno.get_sexo_display }}</p>
                    <p><strong>Status:</strong> {{ aluno.get_status_display }}</p>
                </div>
            </div>

            <div class="mt-4">
                <h4>Informações Pessoais</h4>
                <hr>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Nacionalidade:</strong> {{ aluno.nacionalidade }}</p>
                        <p><strong>Naturalidade:</strong> {{ aluno.naturalidade }}</p>
                        <p><strong>Estado Civil:</strong> {{ aluno.get_estado_civil_display }}</p>
                        <p><strong>Profissão:</strong> {{ aluno.profissao|default:"Não informado" }}</p>
                        <p><strong>Escolaridade:</strong> {{ aluno.get_escolaridade_display|default:"Não informado" }}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Tipo Sanguíneo:</strong> {{ aluno.tipo_sanguineo }} {{ aluno.fator_rh }}</p>
                        <p><strong>Alergias:</strong> {{ aluno.alergias|default:"Nenhuma informada" }}</p>
                        <p><strong>Condições Médicas:</strong> {{ aluno.condicoes_medicas_gerais|default:"Nenhuma informada" }}</p>
                        <p><strong>Convênio Médico:</strong> {{ aluno.convenio_medico|default:"Não informado" }}</p>
                        <p><strong>Hospital de Preferência:</strong> {{ aluno.hospital|default:"Não informado" }}</p>
                    </div>
                </div>
            </div>

            <div class="mt-4">
                <h4>Endereço</h4>
                <hr>
                <p>{{ aluno.rua }}, {{ aluno.numero_imovel }}{% if aluno.complemento %}, {{ aluno.complemento }}{% endif %}</p>
                <p>{{ aluno.bairro }}, {{ aluno.cidade }} - {{ aluno.estado }}</p>
                <p>CEP: {{ aluno.cep }}</p>
            </div>

            <div class="mt-4">
                <h4>Contatos de Emergência</h4>
                <hr>
                <div class="row">
                    <div class="col-md-6">
                        <h5>Contato Principal</h5>
                        <p><strong>Nome:</strong> {{ aluno.nome_primeiro_contato }}</p>
                        <p><strong>Telefone:</strong> {{ aluno.celular_primeiro_contato }}</p>
                        <p><strong>Relação:</strong> {{ aluno.tipo_relacionamento_primeiro_contato }}</p>
                    </div>
                    <div class="col-md-6">
                        <h5>Contato Secundário</h5>
                        <p><strong>Nome:</strong> {{ aluno.nome_segundo_contato }}</p>
                        <p><strong>Telefone:</strong> {{ aluno.celular_segundo_contato }}</p>
                        <p><strong>Relação:</strong> {{ aluno.tipo_relacionamento_segundo_contato }}</p>
                    </div>
                </div>
            </div>

            {% if aluno.data_iniciacao %}
            <div class="mt-4">
                <h4>Informações Iniciáticas</h4>
                <hr>
                <p><strong>Data de Iniciação:</strong> {{ aluno.data_iniciacao }}</p>
                <p><strong>Tempo desde a Iniciação:</strong> {{ aluno.tempo_desde_iniciacao }} dias</p>
                {% if aluno.numero_iniciatico %}
                    <p><strong>Número Iniciático:</strong> {{ aluno.numero_iniciatico }}</p>
                {% endif %}
                {% if aluno.nome_iniciatico %}
                    <p><strong>Nome Iniciático:</strong> {{ aluno.nome_iniciatico }}</p>
                {% endif %}
            </div>
            {% endif %}
        </div>
        <div class="card-footer">
            <div class="btn-group">
                <a href="{% url 'alunos:editar' aluno.cpf %}" class="btn btn-primary">Editar</a>
                <a href="{% url 'alunos:excluir' aluno.cpf %}" class="btn btn-danger">Excluir</a>
                <a href="{% url 'alunos:listar' %}" class="btn btn-secondary">Voltar</a>
            </div>
            <small class="text-muted float-right">
                Cadastrado em: {{ aluno.created_at|date:"d/m/Y H:i" }} | 
                Última atualização: {{ aluno.updated_at|date:"d/m/Y H:i" }}
            </small>
        </div>
    </div>
</div>
{% endblock %}





## alunos\templates\alunos\editar_aluno.html

html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Editar Aluno - {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Aluno</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        
        <div class="row">
            <div class="col-md-6">
                <h3>Informações Pessoais</h3>
                {{ form.nome|crispy }}
                {{ form.cpf|crispy }}
                {{ form.data_nascimento|crispy }}
                {{ form.sexo|crispy }}
                {{ form.email|crispy }}
                {{ form.telefone_fixo|crispy }}
            </div>
            <div class="col-md-6">
                <h3>Endereço</h3>
                {{ form.cep|crispy }}
                {{ form.rua|crispy }}
                {{ form.numero_imovel|crispy }}
                {{ form.complemento|crispy }}
                {{ form.bairro|crispy }}
                {{ form.cidade|crispy }}
                {{ form.estado|crispy }}
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <h3>Informações Acadêmicas</h3>
                {{ form.curso|crispy }}
                {{ form.numero_iniciatico|crispy }}
                {{ form.nome_iniciatico|crispy }}
                {{ form.data_iniciacao|crispy }}
            </div>
            <div class="col-md-6">
                <h3>Informações Médicas</h3>
                {{ form.tipo_sanguineo|crispy }}
                {{ form.fator_rh|crispy }}
                {{ form.alergias|crispy }}
                {{ form.condicoes_medicas_gerais|crispy }}
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <h3>Contato de Emergência 1</h3>
                {{ form.nome_primeiro_contato|crispy }}
                {{ form.celular_primeiro_contato|crispy }}
                {{ form.tipo_relacionamento_primeiro_contato|crispy }}
            </div>
            <div class="col-md-6">
                <h3>Contato de Emergência 2</h3>
                {{ form.nome_segundo_contato|crispy }}
                {{ form.celular_segundo_contato|crispy }}
                {{ form.tipo_relacionamento_segundo_contato|crispy }}
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-12">
                <h3>Foto</h3>
                {{ form.foto|crispy }}
            </div>
        </div>
        
        <div class="mt-4">
            <button type="submit" class="btn btn-primary">Salvar Alterações</button>
            <a href="{% url 'alunos:detalhes' aluno.cpf %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}




## alunos\templates\alunos\excluir_aluno.html

html
{% extends 'base.html' %}

{% block title %}Excluir Aluno - {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-danger text-white">
            <h2>Confirmar Exclusão</h2>
        </div>
        <div class="card-body">
            <div class="alert alert-warning">
                <h4 class="alert-heading">Atenção!</h4>
                <p>Você está prestes a excluir o aluno <strong>{{ aluno.nome }}</strong> (CPF: {{ aluno.cpf }}).</p>
                <p>Esta ação não pode ser desfeita. Todos os dados deste aluno serão permanentemente removidos do sistema.</p>
            </div>
            
            <form method="post">
                {% csrf_token %}
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="confirmar" value="sim" required> 
                        Eu confirmo que desejo excluir este aluno
                    </label>
                </div>
                <div class="btn-group">
                    <button type="submit" class="btn btn-danger">Excluir Aluno</button>
                    <a href="{% url 'alunos:detalhes' aluno.cpf %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}





## alunos\templates\alunos\listar_alunos.html

html
{% extends 'base.html' %}
{% load i18n %}

{% block content %}
<div class="container mt-4">
    <h1>{% trans "Lista de Alunos" %}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="row mb-3">
        <div class="col-md-8">
            <form method="get" class="form-inline">
                <div class="input-group">
                    <input type="text" name="q" class="form-control" placeholder="{% trans 'Buscar por nome, CPF ou email' %}" value="{{ request.GET.q }}">
                    <div class="input-group-append">
                        <button class="btn btn-outline-secondary" type="submit">{% trans "Buscar" %}</button>
                    </div>
                </div>
            </form>
        </div>
        <div class="col-md-4">
            <a href="{% url 'alunos:cadastrar' %}" class="btn btn-primary mb-3">
                <i class="fas fa-plus"></i> {% trans "Novo Aluno" %}
            </a>
        </div>
    </div>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Nome</th>
                <th>CPF</th>
                <th>Email</th>
                <th>Curso</th>
                <th>Status</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for aluno in page_obj %}
            <tr>
                <td class="aluno-nome">{{ aluno.nome }}</td>
                <td>{{ aluno.cpf }}</td>
                <td>{{ aluno.email }}</td>
                <td>{{ aluno.curso.nome }}</td>
                <td>
                    {% if aluno.status == 'A' %}
                        <span class="badge badge-success">Ativo</span>
                    {% elif aluno.status == 'I' %}
                        <span class="badge badge-secondary">Inativo</span>
                    {% elif aluno.status == 'S' %}
                        <span class="badge badge-warning">Suspenso</span>
                    {% endif %}
                </td>
                <td>
                    <div class="btn-group">
                        <a href="{% url 'alunos:detalhes' aluno.cpf %}" class="btn btn-sm btn-info">Detalhes</a>
                        <a href="{% url 'alunos:editar' aluno.cpf %}" class="btn btn-sm btn-primary">Editar</a>
                        <a href="{% url 'alunos:excluir' aluno.cpf %}" class="btn btn-sm btn-danger">Excluir</a>
                    </div>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6" class="text-center">Nenhum aluno encontrado.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    {% if page_obj.has_other_pages %}
    <nav aria-label="Paginação">
        <ul class="pagination">
            {% if page_obj.has_previous %}
                <li class="page-item"><a class="page-link" href="?page=1">« Primeira</a></li>
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}">Anterior</a></li>
            {% endif %}

            {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                    <li class="page-item active"><span class="page-link">{{ num }}</span></li>
                {% else %}
                    <li class="page-item"><a class="page-link" href="?page={{ num }}">{{ num }}</a></li>
                {% endif %}
            {% endfor %}

            {% if page_obj.has_next %}
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}">Próxima</a></li>
                <li class="page-item"><a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Última »</a></li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
{% endblock %}





## alunos\templates\alunos\registro.html

html
{% extends 'base.html' %}

{% block content %}
<h2>Registro</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Registrar</button>
</form>

<a href="javascript:history.back()" class="back-button">Voltar</a>

<style>
    .back-button {
        margin-top: 20px;
        display: inline-block;
        padding: 10px 20px;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        text-decoration: none;
        color: #333;
        border-radius: 5px;
    }
</style>
{% endblock %}





## alunos\tests\test_ui.py

python
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class AlunoUITest(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')  # Run in headless mode for CI environments
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try:
            self.browser = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
        except Exception as e:
            print(f"Could not initialize Chrome driver: {e}")
            self.skipTest("Webdriver not available")
            
    def tearDown(self):
        if hasattr(self, 'browser'):
            self.browser.quit()

    def test_listar_alunos(self):
        self.browser.get(self.live_server_url + reverse('alunos:listar'))
        self.assertIn('Lista de Alunos', self.browser.title)

    def test_criar_aluno(self):
        self.browser.get(self.live_server_url + reverse('alunos:cadastrar'))
        self.assertIn('Cadastrar Novo Aluno', self.browser.page_source)
        
        # Fill form and submit
        self.browser.find_element(By.NAME, 'nome').send_keys('João Test')
        self.browser.find_element(By.NAME, 'cpf').send_keys('98765432100')
        # Add other form fields...
        
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Verify success        self.assertIn('Aluno criado com sucesso', self.browser.page_source)        self.assertIn('Lista de Alunos', self.browser.title)


