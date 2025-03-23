# Código da Funcionalidade: presencas
*Gerado automaticamente*



## presencas\admin.py

python
from django.contrib import admin

# Register your models here.




## presencas\apps.py

python
from django.apps import AppConfig


class PresencasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'presencas'




## presencas\forms.py

python
from django import forms
from .models import PresencaAcademica
import datetime
from django.core.exceptions import ValidationError

class PresencaForm(forms.ModelForm):
    class Meta:
        model = PresencaAcademica
        fields = ['aluno', 'turma', 'data', 'presente']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data > datetime.date.today():
            raise ValidationError("A data da presença não pode ser no futuro.")
        return data
        
    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        turma = cleaned_data.get('turma')
        data = cleaned_data.get('data')
        
        if aluno and turma and data:
            if PresencaAcademica.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                raise ValidationError("Já existe um registro de presença para este aluno nesta turma e data.")
        
        return cleaned_data



## presencas\models.py

python
from django.db import models
from django.contrib.auth.models import User
from turmas.models import Turma
from alunos.models import Aluno

class PresencaAcademica(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField(default=False)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno} - {self.turma} - {self.data}"

    class Meta:
        verbose_name = "Presença Acadêmica"
        verbose_name_plural = "Presenças Acadêmicas"
        permissions = [
            ("gerar_relatorio_presenca", "Pode gerar relatório de presenças"),
        ]



## presencas\tests.py

python
from django.test import TestCase

# Create your tests here.




## presencas\urls.py

python
from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_presenca, name='registrar_presenca'),
    path('lista/', views.lista_presencas, name='lista_presencas'),
    path('editar/<int:id>/', views.editar_presenca, name='editar_presenca'),
    path('excluir/<int:id>/', views.excluir_presenca, name='excluir_presenca'),
]




## presencas\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import PresencaAcademica
from .forms import PresencaForm
from alunos.models import Aluno
from turmas.models import Turma

@login_required
@permission_required('presencas.add_presencaacademica', raise_exception=True)
def registrar_presenca(request):
    if request.method == 'POST':
        form = PresencaForm(request.POST)
        if form.is_valid():
            presenca = form.save(commit=False)
            presenca.registrado_por = request.user
            presenca.save()
            messages.success(request, 'Presença registrada com sucesso!')
            return redirect('lista_presencas')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = PresencaForm()
    
    return render(request, 'presencas/registrar_presenca.html', {'form': form})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def lista_presencas(request):
    presencas_list = PresencaAcademica.objects.all().select_related('aluno', 'turma')
    
    # Filtros
    aluno_id = request.GET.get('aluno')
    turma_id = request.GET.get('turma')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if aluno_id:
        presencas_list = presencas_list.filter(aluno_id=aluno_id)
    if turma_id:
        presencas_list = presencas_list.filter(turma_id=turma_id)
    if data_inicio:
        presencas_list = presencas_list.filter(data__gte=data_inicio)
    if data_fim:
        presencas_list = presencas_list.filter(data__lte=data_fim)
    
    # Paginação
    paginator = Paginator(presencas_list, 10)  # 10 itens por página
    page = request.GET.get('page')
    
    try:
        presencas = paginator.page(page)
    except PageNotAnInteger:
        presencas = paginator.page(1)
    except EmptyPage:
        presencas = paginator.page(paginator.num_pages)
    
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    
    return render(request, 'presencas/lista_presencas.html', {
        'presencas': presencas,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'alunos': alunos,
        'turmas': turmas
    })

@login_required
@permission_required('presencas.change_presencaacademica', raise_exception=True)
def editar_presenca(request, id):
    presenca = get_object_or_404(PresencaAcademica, id=id)
    
    if request.method == 'POST':
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presença atualizada com sucesso!')
            return redirect('lista_presencas')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = PresencaForm(instance=presenca)
    
    return render(request, 'presencas/editar_presenca.html', {'form': form, 'presenca': presenca})

@login_required
@permission_required('presencas.delete_presencaacademica', raise_exception=True)
def excluir_presenca(request, id):
    presenca = get_object_or_404(PresencaAcademica, id=id)
    
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença excluída com sucesso!')
        return redirect('lista_presencas')
    
    return render(request, 'presencas/excluir_presenca.html', {'presenca': presenca})




## presencas\management\commands\setup_presencas_permissions.py

python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from presencas.models import PresencaAcademica

class Command(BaseCommand):
    help = 'Set up permissions for the presencas app'

    def handle(self, *args, **options):
        # Create a group for teachers if it doesn't exist
        teachers_group, created = Group.objects.get_or_create(name='Professores')
        
        # Get content type for the PresencaAcademica model
        content_type = ContentType.objects.get_for_model(PresencaAcademica)
        
        # Get all permissions for the PresencaAcademica model
        permissions = Permission.objects.filter(content_type=content_type)
        
        # Add all permissions to the teachers group
        for permission in permissions:
            teachers_group.permissions.add(permission)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully set up permissions for the presencas app'))




## presencas\templates\presencas\editar_presenca.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Presença</h1>
    
    <div class="card mb-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                    <div class="text-danger">
                        {% for error in field.errors %}
                        <small>{{ error }}</small>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
                
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Salvar Alterações</button>
                    <a href="{% url 'lista_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




## presencas\templates\presencas\excluir_presenca.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Registro de Presença</h1>
    
    <div class="card mb-4">
        <div class="card-body">
            <div class="alert alert-danger">
                <h5>Confirmação de Exclusão</h5>
                <p>Você está prestes a excluir o seguinte registro de presença:</p>
                <ul>
                    <li><strong>Aluno:</strong> {{ presenca.aluno }}</li>
                    <li><strong>Turma:</strong> {{ presenca.turma }}</li>
                    <li><strong>Data:</strong> {{ presenca.data }}</li>
                    <li><strong>Presente:</strong> {% if presenca.presente %}Sim{% else %}Não{% endif %}</li>
                </ul>
                <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
            </div>
            
            <form method="post">
                {% csrf_token %}
                <div class="mt-3">
                    <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
                    <a href="{% url 'lista_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




## presencas\templates\presencas\lista_presencas.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Lista de Presenças</h1>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if turma_id == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.codigo_turma }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ data_fim }}">
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                    <a href="{% url 'lista_presencas' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>
    
    <table class="table">
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Turma</th>
                <th>Data</th>
                <th>Presente</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for presenca in presencas %}
            <tr>
                <td>{{ presenca.aluno }}</td>
                <td>{{ presenca.turma }}</td>
                <td>{{ presenca.data }}</td>
                <td>{% if presenca.presente %}Sim{% else %}Não{% endif %}</td>
                <td>
                    <a href="{% url 'editar_presenca' presenca.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'excluir_presenca' presenca.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5">Nenhuma presença registrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <!-- Paginação -->
    {% if presencas.paginator.num_pages > 1 %}
    <nav aria-label="Navegação de página">
        <ul class="pagination justify-content-center">
            {% if presencas.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Primeira">
                        <span aria-hidden="true">««</span>
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.previous_page_number }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Anterior">
                        <span aria-hidden="true">«</span>
                    </a>
                </li>
            {% else %}
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Primeira">
                        <span aria-hidden="true">««</span>
                    </a>
                </li>
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Anterior">
                        <span aria-hidden="true">«</span>
                    </a>
                </li>
            {% endif %}
            
            {% for i in presencas.paginator.page_range %}
                {% if presencas.number == i %}
                    <li class="page-item active"><a class="page-link" href="#">{{ i }}</a></li>
                {% elif i > presencas.number|add:'-3' and i < presencas.number|add:'3' %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ i }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}">{{ i }}</a>
                    </li>
                {% endif %}
            {% endfor %}
            
            {% if presencas.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.next_page_number }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Próxima">
                        <span aria-hidden="true">»</span>
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.paginator.num_pages }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Última">
                        <span aria-hidden="true">»»</span>
                    </a>
                </li>
            {% else %}
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Próxima">
                        <span aria-hidden="true">»</span>
                    </a>
                </li>
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Última">
                        <span aria-hidden="true">»»</span>
                    </a>
                </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
    
    <a href="{% url 'registrar_presenca' %}" class="btn btn-primary">Nova Presença</a>
</div>
{% endblock %}




## presencas\templates\presencas\registrar_presenca.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Presença</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Registrar</button>
    </form>
    <a href="{% url 'lista_presencas' %}" class="btn btn-secondary mt-2">Voltar</a>
</div>
{% endblock %}




## presencas\tests\test_forms.py

python
from django.test import TestCase
from presencas.forms import PresencaForm
from alunos.models import Aluno
from turmas.models import Turma
from datetime import date, time, timedelta

class PresencaFormTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_form_valido(self):
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today(),
            'presente': True
        }
        form = PresencaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_data_futura(self):
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today() + timedelta(days=1),
            'presente': True
        }
        form = PresencaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('data', form.errors)

    def test_form_duplicado(self):
        # Criar uma presença inicial
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today(),
            'presente': True
        }
        form = PresencaForm(data=data)
        form.is_valid()




## presencas\tests\test_models.py

python
from django.test import TestCase
from presencas.models import PresencaAcademica
from turmas.models import Turma
from alunos.models import Aluno
from datetime import date, time

class PresencaAcademicaModelTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_criar_presenca(self):
        presenca = PresencaAcademica.objects.create(
            turma=self.turma,
            aluno=self.aluno,
            data=date(2023, 10, 1),
            presente=True
        )
        self.assertEqual(presenca.presente, True)
        self.assertEqual(presenca.aluno, self.aluno)




## presencas\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from presencas.models import PresencaAcademica
from turmas.models import Turma
from alunos.models import Aluno
from datetime import date, time

class PresencaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        self.presenca = PresencaAcademica.objects.create(
            turma=self.turma,
            aluno=self.aluno,
            data=date(2023, 10, 1),
            presente=True
        )

    def test_listar_presencas(self):
        response = self.client.get(reverse('lista_presencas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')


