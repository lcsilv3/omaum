# Código da Funcionalidade: punicoes
*Gerado automaticamente*



## punicoes\admin.py

python
from django.contrib import admin
from .models import Punicao

@admin.register(Punicao)
class PunicaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_punicao', 'data')
    list_filter = ('tipo_punicao', 'data')
    search_fields = ('aluno__nome', 'descricao')



## punicoes\forms.py

python
from django import forms
from .models import Punicao
from django.core.exceptions import ValidationError
import datetime

class PunicaoForm(forms.ModelForm):
    class Meta:
        model = Punicao
        fields = ['aluno', 'descricao', 'data', 'tipo_punicao', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao')
        if len(descricao) < 10:
            raise ValidationError("A descrição da punição deve ter pelo menos 10 caracteres.")
        return descricao

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data > datetime.date.today():
            raise ValidationError("A data da punição não pode ser no futuro.")
        return data



## punicoes\models.py

python
from django.db import models
from django.contrib.auth.models import User
from alunos.models import Aluno

class Punicao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='punicoes')
    descricao = models.TextField()
    data = models.DateField()
    tipo_punicao = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True, null=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Punição - {self.aluno.nome} - {self.data}"

    class Meta:
        ordering = ['-data']
        permissions = [
            ("gerar_relatorio_punicao", "Pode gerar relatório de punições"),
        ]




## punicoes\urls.py

python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_punicoes, name='listar_punicoes'),
    path('criar/', views.criar_punicao, name='criar_punicao'),
    path('<int:id>/', views.detalhe_punicao, name='detalhe_punicao'),
    path('<int:id>/editar/', views.editar_punicao, name='editar_punicao'),
    path('<int:id>/excluir/', views.excluir_punicao, name='excluir_punicao'),
]




## punicoes\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Punicao
from .forms import PunicaoForm
from alunos.models import Aluno

@login_required
@permission_required('punicoes.add_punicao', raise_exception=True)
def criar_punicao(request):
    if request.method == 'POST':
        form = PunicaoForm(request.POST)
        if form.is_valid():
            punicao = form.save(commit=False)
            punicao.registrado_por = request.user
            punicao.save()
            messages.success(request, 'Punição criada com sucesso!')
            return redirect('listar_punicoes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PunicaoForm()
    return render(request, 'punicoes/criar_punicao.html', {'form': form})

@login_required
@permission_required('punicoes.change_punicao', raise_exception=True)
def editar_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    if request.method == 'POST':
        form = PunicaoForm(request.POST, instance=punicao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punição atualizada com sucesso!')
            return redirect('listar_punicoes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PunicaoForm(instance=punicao)
    return render(request, 'punicoes/editar_punicao.html', {'form': form, 'punicao': punicao})

@login_required
@permission_required('punicoes.view_punicao', raise_exception=True)
def listar_punicoes(request):
    punicoes_list = Punicao.objects.all().select_related('aluno')
    
    # Filtros
    aluno_id = request.GET.get('aluno')
    tipo_punicao = request.GET.get('tipo_punicao')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if aluno_id:
        punicoes_list = punicoes_list.filter(aluno_id=aluno_id)
    if tipo_punicao:
        punicoes_list = punicoes_list.filter(tipo_punicao=tipo_punicao)
    if data_inicio:
        punicoes_list = punicoes_list.filter(data__gte=data_inicio)
    if data_fim:
        punicoes_list = punicoes_list.filter(data__lte=data_fim)
    
    # Paginação
    paginator = Paginator(punicoes_list, 10)  # 10 itens por página
    page = request.GET.get('page')
    
    try:
        punicoes = paginator.page(page)
    except PageNotAnInteger:
        punicoes = paginator.page(1)
    except EmptyPage:
        punicoes = paginator.page(paginator.num_pages)
    
    # Obter tipos de punição únicos para o filtro
    tipos_punicao = Punicao.objects.values_list('tipo_punicao', flat=True).distinct()
    alunos = Aluno.objects.all()
    
    return render(request, 'punicoes/listar_punicoes.html', {
        'punicoes': punicoes,
        'aluno_id': aluno_id,
        'tipo_punicao': tipo_punicao,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'tipos_punicao': tipos_punicao,
        'alunos': alunos
    })

@login_required
@permission_required('punicoes.view_punicao', raise_exception=True)
def detalhe_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    return render(request, 'punicoes/detalhe_punicao.html', {'punicao': punicao})

@login_required
@permission_required('punicoes.delete_punicao', raise_exception=True)
def excluir_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    if request.method == 'POST':
        punicao.delete()
        messages.success(request, 'Punição excluída com sucesso.')
        return redirect('listar_punicoes')
    return render(request, 'punicoes/excluir_punicao.html', {'punicao': punicao})



## punicoes\templates\punicoes\criar_punicao.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Nova Punição</h1>
    <form method="post">
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
        <button type="submit" class="btn btn-primary">Criar Punição</button>
    </form>
</div>
{% endblock %}




## punicoes\templates\punicoes\detalhe_punicao.html

html
{% extends 'core/base.html' %}

{% block content %}
<h1>Detalhes da Punição</h1>
<dl>
    <dt>Aluno:</dt>
    <dd>{{ punicao.aluno.nome }}</dd>
    <dt>Tipo:</dt>
    <dd>{{ punicao.tipo_punicao }}</dd>
    <dt>Data:</dt>
    <dd>{{ punicao.data }}</dd>
    <dt>Descrição:</dt>
    <dd>{{ punicao.descricao }}</dd>
    <dt>Observações:</dt>
    <dd>{{ punicao.observacoes|default:"Nenhuma observação" }}</dd>
</dl>
<a href="{% url 'editar_punicao' punicao.id %}" class="btn btn-warning">Editar</a>
<a href="{% url 'listar_punicoes' %}" class="btn btn-secondary">Voltar</a>
{% endblock %}



## punicoes\templates\punicoes\editar_punicao.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Punição</h1>
    <form method="post">
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
        <button type="submit" class="btn btn-primary">Atualizar Punição</button>
        <a href="{% url 'listar_punicoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## punicoes\templates\punicoes\excluir_punicao.html

html
{% extends 'core/base.html' %}

{% block content %}
<h1>Excluir Punição</h1>
<p>Tem certeza que deseja excluir a punição de {{ punicao.aluno.nome }} do tipo {{ punicao.tipo_punicao }}?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
    <a href="{% url 'listar_punicoes' %}" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}



## punicoes\templates\punicoes\listar_punicoes.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Lista de Punições</h1>
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
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
                    <label for="tipo_punicao" class="form-label">Tipo de Punição</label>
                    <select name="tipo_punicao" id="tipo_punicao" class="form-select">
                        <option value="">Todos</option>
                        {% for tipo in tipos_punicao %}
                            <option value="{{ tipo }}" {% if tipo_punicao == tipo %}selected{% endif %}>{{ tipo }}</option>
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
                    <a href="{% url 'listar_punicoes' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>
    <table class="table">
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Descrição</th>
                <th>Data</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for punicao in punicoes %}
            <tr>
                <td>{{ punicao.aluno }}</td>
                <td>{{ punicao.descricao|truncatewords:10 }}</td>
                <td>{{ punicao.data }}</td>
                <td>
                    <a href="{% url 'detalhe_punicao' punicao.id %}" class="btn btn-sm btn-info">Detalhes</a>
                    <a href="{% url 'editar_punicao' punicao.id %}" class="btn btn-sm btn-warning">Editar</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4">Nenhuma punição registrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <a href="{% url 'criar_punicao' %}" class="btn btn-primary">Nova Punição</a>
</div>
{% endblock %}


