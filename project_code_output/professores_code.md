# Código da Funcionalidade: professores
*Gerado automaticamente*



## professores\admin.py

python
from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'especialidade', 'ativo', 'data_cadastro')
    list_filter = ('ativo', 'especialidade', 'data_cadastro')
    search_fields = ('nome', 'email', 'especialidade')
    list_editable = ('ativo',)
    readonly_fields = ('data_cadastro',)
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Informações Profissionais', {
            'fields': ('especialidade', 'ativo', 'observacoes')
        }),
        ('Informações do Sistema', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',)
        }),
    )





## professores\apps.py

python
from django.apps import AppConfig

class ProfessoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'professores'
    verbose_name = 'Professores'





## professores\forms.py

python
from django import forms
from django.core.validators import RegexValidator
from .models import Professor

class ProfessorForm(forms.ModelForm):
    # Adiciona validação para o formato do telefone
    telefone = forms.CharField(
        max_length=15, 
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Formato inválido. Use (99) 99999-9999'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': '(99) 99999-9999'
            }
        )
    )
    
    class Meta:
        model = Professor
        fields = ['nome', 'email', 'telefone', 'especialidade', 'observacoes', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do professor'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Área de especialidade'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações adicionais sobre o professor'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica se o email já existe (exceto para o próprio professor em caso de edição)
        if Professor.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError('Este e-mail já está em uso por outro professor.')
        return email





## professores\models.py

python
from django.db import models
from django.utils import timezone

class Professor(models.Model):
    """Modelo para armazenar informações dos professores"""
    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    especialidade = models.CharField(max_length=100, verbose_name="Especialidade")
    data_cadastro = models.DateTimeField(default=timezone.now, verbose_name="Data de cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    def __str__(self):
        return self.nome
    
    @property
    def turmas(self):
        """Retorna as turmas associadas ao professor"""
        return self.turma_set.all()
    
    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ['nome']

class HistoricoAlteracaoProfessor(models.Model):
    """Modelo para rastrear alterações nos dados dos professores"""
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='historico')
    campo = models.CharField(max_length=50)
    valor_antigo = models.TextField(blank=True, null=True)
    valor_novo = models.TextField(blank=True, null=True)
    usuario = models.CharField(max_length=100)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Histórico de Alteração"
        verbose_name_plural = "Histórico de Alterações"
        ordering = ['-data_alteracao']





## professores\tests.py

python
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





## professores\urls.py

python
from django.urls import path
from . import views

app_name = 'professores'

urlpatterns = [
    path('', views.listar_professores, name='listar_professores'),
    path('cadastrar/', views.cadastrar_professor, name='cadastrar_professor'),
    path('<int:professor_id>/', views.detalhes_professor, name='detalhes_professor'),
    path('<int:professor_id>/editar/', views.editar_professor, name='editar_professor'),
    path('<int:professor_id>/excluir/', views.excluir_professor, name='excluir_professor'),
    path('exportar/csv/', views.exportar_professores_csv, name='exportar_professores_csv'),
    path('exportar/pdf/', views.exportar_professores_pdf, name='exportar_professores_pdf'),
]





## professores\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Professor
from .forms import ProfessorForm
from core.utils import registrar_log, adicionar_mensagem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO

@login_required
def listar_professores(request):
    """Exibe a lista de professores cadastrados com paginação e filtros"""
    professores_list = Professor.objects.all()
    
    # Lista de especialidades para o filtro
    especialidades = Professor.objects.values_list('especialidade', flat=True).distinct()
    
    # Parâmetros de busca e filtros
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    especialidade = request.GET.get('especialidade', '')
    
    # Aplicar filtros
    if query:
        professores_list = professores_list.filter(
            nome__icontains=query
        ) | professores_list.filter(
            email__icontains=query
        ) | professores_list.filter(
            especialidade__icontains=query
        )
    
    if status == 'ativo':
        professores_list = professores_list.filter(ativo=True)
    elif status == 'inativo':
        professores_list = professores_list.filter(ativo=False)
    
    if especialidade:
        professores_list = professores_list.filter(especialidade=especialidade)
    
    # Paginação
    paginator = Paginator(professores_list, 10)  # 10 professores por página
    page = request.GET.get('page')
    
    try:
        professores = paginator.page(page)
    except PageNotAnInteger:
        professores = paginator.page(1)
    except EmptyPage:
        professores = paginator.page(paginator.num_pages)
    
    return render(request, 'professores/listar_professores.html', {
        'professores': professores,
        'titulo': 'Lista de Professores',
        'query': query,
        'status': status,
        'especialidade': especialidade,
        'especialidades': especialidades
    })

@login_required
def cadastrar_professor(request):
    """Cadastra um novo professor"""
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save()
            registrar_log(request, f'Professor {professor.nome} cadastrado com sucesso')
            adicionar_mensagem(request, 'sucesso', 'Professor cadastrado com sucesso!')
            return redirect('professores:listar_professores')
    else:
        form = ProfessorForm()
    
    return render(request, 'professores/cadastrar_professor.html', {
        'form': form,
        'titulo': 'Cadastrar Professor',
        'botao': 'Cadastrar'
    })

@login_required
def detalhes_professor(request, professor_id):
    """Exibe os detalhes de um professor específico"""
    professor = get_object_or_404(Professor, pk=professor_id)
    return render(request, 'professores/detalhes_professor.html', {
        'professor': professor,
        'titulo': f'Detalhes do Professor: {professor.nome}'
    })

@login_required
def editar_professor(request, professor_id):
    """Edita as informações de um professor e registra alterações"""
    professor = get_object_or_404(Professor, pk=professor_id)
    
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            # Registrar alterações antes de salvar
            for campo in form.changed_data:
                valor_antigo = getattr(professor, campo)
                valor_novo = form.cleaned_data[campo]
                
                # Não registrar se os valores forem iguais
                if valor_antigo != valor_novo:
                    HistoricoAlteracaoProfessor.objects.create(
                        professor=professor,
                        campo=campo,
                        valor_antigo=str(valor_antigo),
                        valor_novo=str(valor_novo),
                        usuario=request.user.username
                    )
            
            form.save()
            registrar_log(request, f'Professor {professor.nome} atualizado')
            adicionar_mensagem(request, 'sucesso', 'Professor atualizado com sucesso!')
            return redirect('professores:detalhes_professor', professor_id=professor.id)
    else:
        form = ProfessorForm(instance=professor)
    
    return render(request, 'professores/cadastrar_professor.html', {
        'form': form,
        'titulo': f'Editar Professor: {professor.nome}',
        'botao': 'Atualizar',
        'professor': professor
    })

@login_required
def excluir_professor(request, professor_id):
    """Exclui um professor do sistema"""
    professor = get_object_or_404(Professor, pk=professor_id)
    
    if request.method == 'POST':
        nome_professor = professor.nome
        professor.delete()
        registrar_log(request, f'Professor {nome_professor} excluído', tipo='AVISO')
        adicionar_mensagem(request, 'aviso', f'Professor {nome_professor} excluído com sucesso!')
        return redirect('professores:listar_professores')
    
    return render(request, 'professores/confirmar_exclusao.html', {
        'professor': professor,
        'titulo': f'Confirmar Exclusão: {professor.nome}'
    })

@login_required
def exportar_professores_csv(request):
    """Exporta a lista de professores em formato CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="professores.csv"'
    
    # Aplicar filtros se existirem
    professores = Professor.objects.all()
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    especialidade = request.GET.get('especialidade', '')
    
    if query:
        professores = professores.filter(
            nome__icontains=query
        ) | professores.filter(
            email__icontains=query
        ) | professores.filter(
            especialidade__icontains=query
        )
    
    if status == 'ativo':
        professores = professores.filter(ativo=True)
    elif status == 'inativo':
        professores = professores.filter(ativo=False)
    
    if especialidade:
        professores = professores.filter(especialidade=especialidade)
    
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Email', 'Telefone', 'Especialidade', 'Status', 'Data de Cadastro'])
    
    for professor in professores:
        writer.writerow([
            professor.nome,
            professor.email,
            professor.telefone or 'Não informado',
            professor.especialidade,
            'Ativo' if professor.ativo else 'Inativo',
            professor.data_cadastro.strftime('%d/%m/%Y %H:%M')
        ])
    
    registrar_log(request, f'Exportou lista de professores em CSV')
    return response

@login_required
def exportar_professores_pdf(request):
    """Exporta a lista de professores em formato PDF"""
    # Aplicar filtros se existirem
    professores = Professor.objects.all()
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    especialidade = request.GET.get('especialidade', '')
    
    if query:
        professores = professores.filter(
            nome__icontains=query
        ) | professores.filter(
            email__icontains=query
        ) | professores.filter(
            especialidade__icontains=query
        )
    
    if status == 'ativo':
        professores = professores.filter(ativo=True)
    elif status == 'inativo':
        professores = professores.filter(ativo=False)
    
    if especialidade:
        professores = professores.filter(especialidade=especialidade)
    
    # Criar PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Dados da tabela
    data = [['Nome', 'Email', 'Especialidade', 'Status']]
    for professor in professores:
        data.append([
            professor.nome,
            professor.email,
            professor.especialidade,
            'Ativo' if professor.ativo else 'Inativo'
        ])
    
    # Criar tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    # Retornar o PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="professores.pdf"'
    
    registrar_log(request, f'Exportou lista de professores em PDF')
    return response

@login_required
def estatisticas_professores(request):
    """Exibe estatísticas sobre os professores cadastrados"""
    total_professores = Professor.objects.count()
    professores_ativos = Professor.objects.filter(ativo=True).count()
    professores_inativos = Professor.objects.filter(ativo=False).count()
    
    # Contagem por especialidade
    especialidades = Professor.objects.values('especialidade').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Professores mais recentes
    professores_recentes = Professor.objects.order_by('-data_cadastro')[:5]
    
    return render(request, 'professores/estatisticas_professores.html', {
        'total_professores': total_professores,
        'professores_ativos': professores_ativos,
        'professores_inativos': professores_inativos,
        'especialidades': especialidades,
        'professores_recentes': professores_recentes,
        'titulo': 'Estatísticas de Professores'
    })





## professores\templates\professores\cadastrar_professor.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ titulo }}</h1>
    
    <div class="card">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="{{ form.nome.id_for_label }}" class="form-label">Nome completo</label>
                        {{ form.nome }}
                        {% if form.nome.errors %}
                            <div class="text-danger">{{ form.nome.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6 mb-3">
                        <label for="{{ form.email.id_for_label }}" class="form-label">E-mail</label>
                        {{ form.email }}
                        {% if form.email.errors %}
                            <div class="text-danger">{{ form.email.errors }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="{{ form.telefone.id_for_label }}" class="form-label">Telefone</label>
                        {{ form.telefone }}
                        {% if form.telefone.errors %}
                            <div class="text-danger">{{ form.telefone.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6 mb-3">
                        <label for="{{ form.especialidade.id_for_label }}" class="form-label">Especialidade</label>
                        {{ form.especialidade }}
                        {% if form.especialidade.errors %}
                            <div class="text-danger">{{ form.especialidade.errors }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.observacoes.id_for_label }}" class="form-label">Observações</label>
                    {{ form.observacoes }}
                    {% if form.observacoes.errors %}
                        <div class="text-danger">{{ form.observacoes.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="mb-3 form-check">
                    {{ form.ativo }}
                    <label class="form-check-label" for="{{ form.ativo.id_for_label }}">Professor ativo</label>
                    {% if form.ativo.errors %}
                        <div class="text-danger">{{ form.ativo.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'professores:listar_professores' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">{{ botao }}</button>
                </div>
            </form>
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}





## professores\templates\professores\confirmar_exclusao.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-danger text-white">
            <h4>Confirmar Exclusão</h4>
        </div>
        <div class="card-body">
            <p class="lead">Você tem certeza que deseja excluir o professor <strong>{{ professor.nome }}</strong>?</p>
            <p>Esta ação não poderá ser desfeita.</p>
            
            <div class="mt-4">
                <form method="post">
                    {% csrf_token %}
                    <div class="d-flex justify-content-between">
                        <a href="{% url 'professores:detalhes_professor' professor.id %}" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}





## professores\templates\professores\detalhes_professor.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ titulo }}</h1>
    
    <div class="card">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Informações do Professor</h5>
                <div>
                    <a href="{% url 'professores:editar_professor' professor.id %}" class="btn btn-warning btn-sm">
                        <i class="fas fa-edit"></i> Editar
                    </a>
                    <a href="{% url 'professores:excluir_professor' professor.id %}" class="btn btn-danger btn-sm">
                        <i class="fas fa-trash"></i> Excluir
                    </a>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nome:</strong> {{ professor.nome }}</p>
                    <p><strong>E-mail:</strong> {{ professor.email }}</p>
                    <p><strong>Telefone:</strong> {{ professor.telefone|default:"Não informado" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Especialidade:</strong> {{ professor.especialidade }}</p>
                    <p>
                        <strong>Status:</strong> 
                        {% if professor.ativo %}
                            <span class="badge bg-success">Ativo</span>
                        {% else %}
                            <span class="badge bg-danger">Inativo</span>
                        {% endif %}
                    </p>
                    <p><strong>Data de Cadastro:</strong> {{ professor.data_cadastro|date:"d/m/Y H:i" }}</p>
                </div>
            </div>
            
            {% if professor.observacoes %}
            <div class="mt-3">
                <h6>Observações:</h6>
                <p>{{ professor.observacoes|linebreaks }}</p>
            </div>
            {% endif %}
        </div>
    </div>
    
    <div class="card mt-4">
        <div class="card-header">
            <h5 class="mb-0">Turmas Associadas</h5>
        </div>
        <div class="card-body">
            {% if professor.turmas %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Nome</th>
                                <th>Curso</th>
                                <th>Período</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for turma in professor.turmas %}
                                <tr>
                                    <td>{{ turma.nome }}</td>
                                    <td>{{ turma.curso.nome }}</td>
                                    <td>{{ turma.periodo }}</td>
                                    <td>
                                        <a href="{% url 'turmas:detalhes_turma' turma.id %}" class="btn btn-info btn-sm">
                                            <i class="fas fa-eye"></i> Detalhes
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p>Nenhuma turma associada.</p>
            {% endif %}
        </div>
    </div>
    
    <div class="card mt-4">
        <div class="card-header">
            <h5 class="mb-0">Histórico de Alterações</h5>
        </div>
        <div class="card-body">
            {% if professor.historico.all %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Campo</th>
                                <th>Valor Antigo</th>
                                <th>Valor Novo</th>
                                <th>Usuário</th>
                                <th>Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for alteracao in professor.historico.all %}
                                <tr>
                                    <td>{{ alteracao.campo }}</td>
                                    <td>{{ alteracao.valor_antigo }}</td>
                                    <td>{{ alteracao.valor_novo }}</td>
                                    <td>{{ alteracao.usuario }}</td>
                                    <td>{{ alteracao.data_alteracao|date:"d/m/Y H:i" }}</td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p>Nenhuma alteração registrada.</p>
            {% endif %}
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}





## professores\templates\professores\listar_professores.html

html
{% extends 'core/base.html' %}

{% block title %}Lista de Professores{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Professores</h1>
        <a href="{% url 'professores:cadastrar_professor' %}" class="btn btn-primary">
            <i class="fas fa-plus"></i> Novo Professor
        </a>
        <!-- Adicionar após o botão "Novo Professor" -->
        <div class="dropdown ms-2">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="exportarDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fas fa-download"></i> Exportar
            </button>
            <ul class="dropdown-menu" aria-labelledby="exportarDropdown">
                <li>
                    <a class="dropdown-item" href="{% url 'professores:exportar_professores_csv' %}{% if query %}?q={{ query }}{% endif %}{% if status %}&status={{ status }}{% endif %}{% if especialidade %}&especialidade={{ especialidade }}{% endif %}">
                        <i class="fas fa-file-csv"></i> CSV
                    </a>
                </li>
                <li>
                    <a class="dropdown-item" href="{% url 'professores:exportar_professores_pdf' %}{% if query %}?q={{ query }}{% endif %}{% if status %}&status={{ status }}{% endif %}{% if especialidade %}&especialidade={{ especialidade }}{% endif %}">
                        <i class="fas fa-file-pdf"></i> PDF
                    </a>
                </li>
            </ul>
        </div>
    </div>

    <!-- Adicionar após o título e antes da tabela -->
    <div class="card mb-4">
        <div class="card-body">
            <form method="get" class="mb-0">
                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="input-group">
                            <input type="text" name="q" class="form-control" placeholder="Buscar por nome, email ou especialidade" value="{{ query }}">
                            <button class="btn btn-outline-secondary" type="submit">Buscar</button>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <select name="status" class="form-select" onchange="this.form.submit()">
                            <option value="">Status</option>
                            <option value="ativo" {% if request.GET.status == 'ativo' %}selected{% endif %}>Ativos</option>
                            <option value="inativo" {% if request.GET.status == 'inativo' %}selected{% endif %}>Inativos</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <select name="especialidade" class="form-select" onchange="this.form.submit()">
                            <option value="">Todas as especialidades</option>
                            {% for esp in especialidades %}
                                <option value="{{ esp }}" {% if request.GET.especialidade == esp %}selected{% endif %}>{{ esp }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="col-md-2">
                        <a href="{% url 'professores:listar_professores' %}" class="btn btn-outline-secondary w-100">Limpar</a>
                    </div>
                </div>
            </form>
        </div>
    </div>

    {% if professores %}
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>E-mail</th>
                        <th>Especialidade</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for professor in professores %}
                        <tr>
                            <td>{{ professor.nome }}</td>
                            <td>{{ professor.email }}</td>
                            <td>{{ professor.especialidade }}</td>
                            <td>
                                {% if professor.ativo %}
                                    <span class="badge bg-success">Ativo</span>
                                {% else %}
                                    <span class="badge bg-danger">Inativo</span>
                                {% endif %}
                            </td>
                            <td>
                                <a href="{% url 'professores:detalhes_professor' professor.id %}" class="btn btn-sm btn-info">
                                    <i class="fas fa-eye"></i>
                                </a>
                                <a href="{% url 'professores:editar_professor' professor.id %}" class="btn btn-sm btn-warning">
                                    <i class="fas fa-edit"></i>
                                </a>
                                <a href="{% url 'professores:excluir_professor' professor.id %}" class="btn btn-sm btn-danger">
                                    <i class="fas fa-trash"></i>
                                </a>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% else %}
        <div class="alert alert-info">
            Nenhum professor cadastrado. <a href="{% url 'professores:cadastrar_professor' %}">Cadastrar um professor</a>.
        </div>
    {% endif %}

    {% if professores.has_other_pages %}
    <nav aria-label="Navegação de páginas">
        <ul class="pagination justify-content-center">
            {% if professores.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ professores.previous_page_number }}{% if query %}&q={{ query }}{% endif %}" aria-label="Anterior">
                        <span aria-hidden="true">«</span>
                    </a>
                </li>
            {% else %}
                <li class="page-item disabled">
                    <span class="page-link" aria-hidden="true">«</span>
                </li>
            {% endif %}
            
            {% for i in professores.paginator.page_range %}
                {% if professores.number == i %}
                    <li class="page-item active"><span class="page-link">{{ i }}</span></li>
                {% else %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ i }}{% if query %}&q={{ query }}{% endif %}">{{ i }}</a>
                    </li>
                {% endif %}
            {% endfor %}
            
            {% if professores.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ professores.next_page_number }}{% if query %}&q={{ query }}{% endif %}" aria-label="Próximo">
                        <span aria-hidden="true">»</span>
                    </a>
                </li>
            {% else %}
                <li class="page-item disabled">
                    <span class="page-link" aria-hidden="true">»</span>
                </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}

    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}



