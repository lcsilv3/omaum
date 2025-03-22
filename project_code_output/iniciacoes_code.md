# Código da Funcionalidade: iniciacoes
*Gerado automaticamente*



## iniciacoes\admin.py

python
from django.contrib import admin
from .models import Iniciacao

@admin.register(Iniciacao)
class IniciacaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'nome_curso', 'data_iniciacao')
    list_filter = ('nome_curso', 'data_iniciacao')
    search_fields = ('aluno__nome', 'nome_curso')




## iniciacoes\apps.py

python
from django.apps import AppConfig


class IniciacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iniciacoes'




## iniciacoes\forms.py

python
from django import forms
from .models import Iniciacao

class IniciacaoForm(forms.ModelForm):
    class Meta:
        model = Iniciacao
        fields = ['aluno', 'nome_curso', 'data_iniciacao', 'observacoes']
        widgets = {
            'data_iniciacao': forms.DateInput(attrs={'type': 'date'}),
        }



## iniciacoes\models.py

python
from django.db import models
from alunos.models import Aluno

class Iniciacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='iniciacoes')
    nome_curso = models.CharField(max_length=100)
    data_iniciacao = models.DateField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Iniciação - {self.aluno.nome} - {self.nome_curso}"

    class Meta:
        ordering = ['-data_iniciacao']




## iniciacoes\tests.py

python
from django.test import TestCase

# Create your tests here.




## iniciacoes\urls.py

python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_iniciacoes, name='listar_iniciacoes'),
    path('criar/', views.criar_iniciacao, name='criar_iniciacao'),
    path('<int:id>/', views.detalhe_iniciacao, name='detalhe_iniciacao'),
    path('<int:id>/editar/', views.editar_iniciacao, name='editar_iniciacao'),
    path('<int:id>/excluir/', views.excluir_iniciacao, name='excluir_iniciacao'),
]




## iniciacoes\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Iniciacao
from .forms import IniciacaoForm

def listar_iniciacoes(request):
    iniciacoes = Iniciacao.objects.all()
    return render(request, 'iniciacoes/listar_iniciacoes.html', {'iniciacoes': iniciacoes})

def criar_iniciacao(request):
    if request.method == 'POST':
        form = IniciacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação criada com sucesso.')
            return redirect('listar_iniciacoes')
    else:
        form = IniciacaoForm()
    return render(request, 'iniciacoes/criar_iniciacao.html', {'form': form})

def detalhe_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    return render(request, 'iniciacoes/detalhe_iniciacao.html', {'iniciacao': iniciacao})

def editar_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == 'POST':
        form = IniciacaoForm(request.POST, instance=iniciacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação atualizada com sucesso.')
            return redirect('listar_iniciacoes')
    else:
        form = IniciacaoForm(instance=iniciacao)
    return render(request, 'iniciacoes/editar_iniciacao.html', {'form': form, 'iniciacao': iniciacao})

def excluir_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == 'POST':
        iniciacao.delete()
        messages.success(request, 'Iniciação excluída com sucesso.')
        return redirect('listar_iniciacoes')
    return render(request, 'iniciacoes/excluir_iniciacao.html', {'iniciacao': iniciacao})




## iniciacoes\templates\iniciacoes\detalhe_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Detalhes da Iniciação</h1>
<dl>
    <dt>Aluno:</dt>
    <dd>{{ iniciacao.aluno.nome }}</dd>
    <dt>Curso:</dt>
    <dd>{{ iniciacao.nome_curso }}</dd>
    <dt>Data:</dt>
    <dd>{{ iniciacao.data_iniciacao }}</dd>
    <dt>Observações:</dt>
    <dd>{{ iniciacao.observacoes|default:"Nenhuma observação" }}</dd>
</dl>
<a href="{% url 'editar_iniciacao' iniciacao.id %}" class="btn btn-warning">Editar</a>
<a href="{% url 'listar_iniciacoes' %}" class="btn btn-secondary">Voltar</a>
{% endblock %}



## iniciacoes\templates\iniciacoes\editar_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Editar Iniciação</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{% url 'listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}



## iniciacoes\templates\iniciacoes\excluir_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Excluir Iniciação</h1>
<p>Tem certeza que deseja excluir a iniciação de {{ iniciacao.aluno.nome }} no curso {{ iniciacao.nome_curso }}?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
    <a href="{% url 'listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}



## iniciacoes\templates\iniciacoes\listar_iniciacoes.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Lista de Iniciações</h1>
<a href="{% url 'criar_iniciacao' %}" class="btn btn-primary">Nova Iniciação</a>
<table class="table mt-3">
    <thead>
        <tr>
            <th>Aluno</th>
            <th>Curso</th>
            <th>Data</th>
            <th>Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for iniciacao in iniciacoes %}
        <tr>
            <td>{{ iniciacao.aluno.nome }}</td>
            <td>{{ iniciacao.nome_curso }}</td>
            <td>{{ iniciacao.data_iniciacao }}</td>
            <td>
                <a href="{% url 'detalhe_iniciacao' iniciacao.id %}" class="btn btn-sm btn-info">Detalhes</a>
                <a href="{% url 'editar_iniciacao' iniciacao.id %}" class="btn btn-sm btn-warning">Editar</a>
                <a href="{% url 'excluir_iniciacao' iniciacao.id %}" class="btn btn-sm btn-danger">Excluir</a>
            </td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="4">Nenhuma iniciação encontrada.</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}



## iniciacoes\tests\test_models.py

python
from django.test import TestCase
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoModelTest(TestCase):
    def setUp(self):
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

    def test_criar_iniciacao(self):
        iniciacao = Iniciacao.objects.create(
            cpf_aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )
        self.assertEqual(iniciacao.nome_curso, 'Curso de Iniciação')
        self.assertEqual(iniciacao.cpf_aluno, self.aluno)




## iniciacoes\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.iniciacao = Iniciacao.objects.create(
            cpf_aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )

    def test_listar_iniciacoes(self):
        response = self.client.get(reverse('listar_iniciacoes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')
        self.assertContains(response, 'Curso de Iniciação')


