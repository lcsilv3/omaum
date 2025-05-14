# Revisão da Funcionalidade: relatorios

## Arquivos forms.py:


### Arquivo: relatorios\forms.py

python
from django import forms
from .models import Relatorio


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ["titulo", "conteudo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "conteudo": forms.Textarea(attrs={"class": "form-control"}),
        }



## Arquivos views.py:


### Arquivo: relatorios\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Relatorio
from .forms import RelatorioForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from importlib import import_module
from django.utils import timezone
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_presenca_model():
    """Obtém o modelo Presenca dinamicamente."""
    try:
        presencas_module = import_module("presencas.models")
        return getattr(presencas_module, "Presenca")
    except (ImportError, AttributeError):
        return None


def get_punicao_model():
    """Obtém o modelo Punicao dinamicamente."""
    try:
        punicoes_module = import_module("punicoes.models")
        return getattr(punicoes_module, "Punicao")
    except (ImportError, AttributeError):
        return None


@login_required
def listar_relatorios(request):
    """Lista todos os relatórios disponíveis."""
    relatorios = Relatorio.objects.all().order_by('-data_criacao')
    return render(
        request,
        "relatorios/listar_relatorios.html",
        {"relatorios": relatorios},
    )


@login_required
def detalhar_relatorio(request, relatorio_id):
    """Exibe os detalhes de um relatório específico."""
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    return render(
        request, "relatorios/detalhar_relatorio.html", {"relatorio": relatorio}
    )


@login_required
def criar_relatorio(request):
    """Cria um novo relatório."""
    if request.method == "POST":
        form = RelatorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("relatorios:listar_relatorios")
    else:
        form = RelatorioForm()
    return render(request, "relatorios/form_relatorio.html", {"form": form})


@login_required
def editar_relatorio(request, relatorio_id):
    """Edita um relatório existente."""
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    if request.method == "POST":
        form = RelatorioForm(request.POST, instance=relatorio)
        if form.is_valid():
            form.save()
            return redirect("relatorios:listar_relatorios")
    else:
        form = RelatorioForm(instance=relatorio)
    return render(request, "relatorios/form_relatorio.html", {"form": form})


@login_required
def excluir_relatorio(request, relatorio_id):
    """Exclui um relatório."""
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    if request.method == "POST":
        relatorio.delete()
        return redirect("relatorios:listar_relatorios")
    return render(
        request, "relatorios/confirmar_exclusao.html", {"relatorio": relatorio}
    )


@login_required
def relatorio_alunos(request):
    """Gera um relatório de alunos com filtros."""
    try:
        Aluno = get_aluno_model()
        
        # Obter parâmetros de filtro
        nome = request.GET.get('nome', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Filtrar alunos
        alunos = Aluno.objects.all()
        
        if nome:
            alunos = alunos.filter(nome__icontains=nome)
        
        if data_inicio and data_fim:
            alunos = alunos.filter(data_nascimento__range=[data_inicio, data_fim])
        elif data_inicio:
            alunos = alunos.filter(data_nascimento__gte=data_inicio)
        elif data_fim:
            alunos = alunos.filter(data_nascimento__lte=data_fim)
        
        return render(
            request, 
            "relatorios/relatorio_alunos.html", 
            {
                "alunos": alunos,
                "nome": nome,
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        )
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de alunos: {str(e)}")
        return render(
            request, 
            "relatorios/relatorio_alunos.html", 
            {"erro": f"Erro ao gerar relatório: {str(e)}"}
        )


@login_required
def relatorio_presencas(request):
    """Gera um relatório de presenças com filtros."""
    try:
        Presenca = get_presenca_model()
        Aluno = get_aluno_model()
        
        if not Presenca:
            return render(
                request, 
                "relatorios/relatorio_presencas.html", 
                {"erro": "Módulo de presenças não disponível"}
            )
        
        # Obter parâmetros de filtro
        aluno_id = request.GET.get('aluno', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Obter todos os alunos para o filtro
        alunos = Aluno.objects.all().order_by('nome')
        
        # Filtrar presenças
        presencas = Presenca.objects.all().order_by('-data')
        
        if aluno_id:
            presencas = presencas.filter(aluno_id=aluno_id)
        
        if data_inicio and data_fim:
            presencas = presencas.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)
        elif data_fim:
            presencas = presencas.filter(data__lte=data_fim)
        
        return render(
            request, 
            "relatorios/relatorio_presencas.html", 
            {
                "presencas": presencas,
                "alunos": alunos,
                "aluno_id": aluno_id,
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        )
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de presenças: {str(e)}")
        return render(
            request, 
            "relatorios/relatorio_presencas.html", 
            {"erro": f"Erro ao gerar relatório: {str(e)}"}
        )


@login_required
def relatorio_punicoes(request):
    """Gera um relatório de punições com filtros."""
    try:
        Punicao = get_punicao_model()
        Aluno = get_aluno_model()
        
        if not Punicao:
            return render(
                request, 
                "relatorios/relatorio_punicoes.html", 
                {"erro": "Módulo de punições não disponível"}
            )
        
        # Obter parâmetros de filtro
        aluno_id = request.GET.get('aluno', '')
        tipo_punicao = request.GET.get('tipo_punicao', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Obter todos os alunos para o filtro
        alunos = Aluno.objects.all().order_by('nome')
        
        # Obter todos os tipos de punição para o filtro
        tipos_punicao = Punicao.objects.values_list('tipo_punicao', flat=True).distinct()
        
        # Filtrar punições
        punicoes = Punicao.objects.all().order_by('-data')
        
        if aluno_id:
            punicoes = punicoes.filter(aluno_id=aluno_id)
        
        if tipo_punicao:
            punicoes = punicoes.filter(tipo_punicao=tipo_punicao)
        
        if data_inicio and data_fim:
            punicoes = punicoes.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            punicoes = punicoes.filter(data__gte=data_inicio)
        elif data_fim:
            punicoes = punicoes.filter(data__lte=data_fim)
        
        return render(
            request, 
            "relatorios/relatorio_punicoes.html", 
            {
                "punicoes": punicoes,
                "alunos": alunos,
                "tipos_punicao": tipos_punicao,
                "aluno_id": aluno_id,
                "tipo_punicao": tipo_punicao,
                "data_inicio": data_inicio,
                "data_fim": data_fim
            }
        )
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de punições: {str(e)}")
        return render(
            request, 
            "relatorios/relatorio_punicoes.html", 
            {"erro": f"Erro ao gerar relatório: {str(e)}"}
        )


@login_required
def relatorio_alunos_pdf(request):
    """Gera um relatório de alunos em PDF."""
    try:
        # Importar biblioteca para geração de PDF
        from django.template.loader import get_template
        from xhtml2pdf import pisa
        from io import BytesIO
        
        # Obter os mesmos parâmetros de filtro que na view relatorio_alunos
        nome = request.GET.get('nome', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Filtrar alunos (mesmo código da view relatorio_alunos)
        Aluno = get_aluno_model()
        alunos = Aluno.objects.all()
        
        if nome:
            alunos = alunos.filter(nome__icontains=nome)
        
        if data_inicio and data_fim:
            alunos = alunos.filter(data_nascimento__range=[data_inicio, data_fim])
        elif data_inicio:
            alunos = alunos.filter(data_nascimento__gte=data_inicio)
        elif data_fim:
            alunos = alunos.filter(data_nascimento__lte=data_fim)
        
        # Renderizar o template para HTML
        template = get_template('relatorios/relatorio_alunos_pdf.html')
        html = template.render({
            'alunos': alunos,
            'nome': nome,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'data_geracao': timezone.now(),
        })
        
        # Criar resposta HTTP com PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_alunos.pdf"'
        
        # Gerar PDF
        pdf_status = pisa.CreatePDF(
            html, dest=response)
        
        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de alunos: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)
@login_required
def relatorio_presencas_pdf(request):
    """Gera um relatório de presenças em PDF."""
    try:
        # Importar biblioteca para geração de PDF
        from django.template.loader import get_template
        from xhtml2pdf import pisa
        from io import BytesIO
        
        # Obter os mesmos parâmetros de filtro que na view relatorio_presencas
        aluno_id = request.GET.get('aluno', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Filtrar presenças (mesmo código da view relatorio_presencas)
        Presenca = get_presenca_model()
        Aluno = get_aluno_model()
        
        if not Presenca:
            return HttpResponse('Módulo de presenças não disponível', status=404)
        
        presencas = Presenca.objects.all().order_by('-data')
        
        if aluno_id:
            presencas = presencas.filter(aluno_id=aluno_id)
        
        if data_inicio and data_fim:
            presencas = presencas.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)
        elif data_fim:
            presencas = presencas.filter(data__lte=data_fim)
        
        # Renderizar o template para HTML
        template = get_template('relatorios/relatorio_presencas_pdf.html')
        html = template.render({
            'presencas': presencas,
            'aluno': Aluno.objects.get(id=aluno_id) if aluno_id else None,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'data_geracao': timezone.now(),
        })
        
        # Criar resposta HTTP com PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_presencas.pdf"'
        
        # Gerar PDF
        pdf_status = pisa.CreatePDF(
            html, dest=response)
        
        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de presenças: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)

@login_required
def relatorio_punicoes_pdf(request):
    """Gera um relatório de punições em PDF."""
    try:
        # Importar biblioteca para geração de PDF
        from django.template.loader import get_template
        from xhtml2pdf import pisa
        from io import BytesIO
        
        # Obter os mesmos parâmetros de filtro que na view relatorio_punicoes
        aluno_id = request.GET.get('aluno', '')
        tipo_punicao = request.GET.get('tipo_punicao', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        
        # Filtrar punições (mesmo código da view relatorio_punicoes)
        Punicao = get_punicao_model()
        Aluno = get_aluno_model()
        
        if not Punicao:
            return HttpResponse('Módulo de punições não disponível', status=404)
        
        punicoes = Punicao.objects.all().order_by('-data')
        
        if aluno_id:
            punicoes = punicoes.filter(aluno_id=aluno_id)
        
        if tipo_punicao:
            punicoes = punicoes.filter(tipo_punicao=tipo_punicao)
        
        if data_inicio and data_fim:
            punicoes = punicoes.filter(data__range=[data_inicio, data_fim])
        elif data_inicio:
            punicoes = punicoes.filter(data__gte=data_inicio)
        elif data_fim:
            punicoes = punicoes.filter(data__lte=data_fim)
        
        # Renderizar o template para HTML
        template = get_template('relatorios/relatorio_punicoes_pdf.html')
        html = template.render({
            'punicoes': punicoes,
            'aluno': Aluno.objects.get(id=aluno_id) if aluno_id else None,
            'tipo_punicao': tipo_punicao,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'data_geracao': timezone.now(),
        })
        
        # Criar resposta HTTP com PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_punicoes.pdf"'
        
        # Gerar PDF
        pdf_status = pisa.CreatePDF(
            html, dest=response)
        
        if pdf_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF de punições: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)


## Arquivos urls.py:


### Arquivo: relatorios\urls.py

python
from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    path("", views.listar_relatorios, name="listar_relatorios"),
    path("<int:relatorio_id>/", views.detalhar_relatorio, name="detalhar_relatorio"),
    path("criar/", views.criar_relatorio, name="criar_relatorio"),
    path("<int:relatorio_id>/editar/", views.editar_relatorio, name="editar_relatorio"),
    path("<int:relatorio_id>/excluir/", views.excluir_relatorio, name="excluir_relatorio"),
    path("alunos/", views.relatorio_alunos, name="relatorio_alunos"),
    path("alunos/pdf/", views.relatorio_alunos_pdf, name="relatorio_alunos_pdf"),
    path("presencas/", views.relatorio_presencas, name="relatorio_presencas"),
    path("presencas/pdf/", views.relatorio_presencas_pdf, name="relatorio_presencas_pdf"),
    path("punicoes/", views.relatorio_punicoes, name="relatorio_punicoes"),
    path("punicoes/pdf/", views.relatorio_punicoes_pdf, name="relatorio_punicoes_pdf"),
]


## Arquivos models.py:


### Arquivo: relatorios\models.py

python
from django.db import models


class Relatorio(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo



## Arquivos de Template:


### Arquivo: relatorios\templates\relatorios\confirmar_exclusao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="card border-danger">
        <div class="card-header bg-danger text-white">
            <h4 class="mb-0">Confirmar Exclusão</h4>
        </div>
        <div class="card-body">
            <p class="lead">Tem certeza que deseja excluir o relatório "{{ relatorio.titulo }}"?</p>
            <p class="text-danger"><strong>Atenção:</strong> Esta ação não pode ser desfeita!</p>
            
            <form method="post">
                {% csrf_token %}
                <div class="d-flex justify-content-between mt-4">
                    <a href="{% url 'relatorios:detalhar_relatorio' relatorio.id %}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-danger">
                        <i class="fas fa-trash"></i> Confirmar Exclusão
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: relatorios\templates\relatorios\detalhar_relatorio.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{{ relatorio.titulo }}</h1>
        <div>
            <a href="{% url 'relatorios:listar_relatorios' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'relatorios:editar_relatorio' relatorio.id %}" class="btn btn-warning">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'relatorios:excluir_relatorio' relatorio.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Conteúdo do Relatório</h5>
                <small class="text-muted">Criado em: {{ relatorio.data_criacao|date:"d/m/Y H:i" }}</small>
            </div>
        </div>
        <div class="card-body">
            <div class="relatorio-conteudo">
                {{ relatorio.conteudo|linebreaks }}
            </div>
        </div>
    </div>
</div>
{% endblock %}            <a href="{% url 'relatorios:            <a href="{% url 'relatorios:



### Arquivo: relatorios\templates\relatorios\form_relatorio.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if form.instance.id %}Editar{% else %}Novo{% endif %} Relat√≥rio</h1>
        <a href="{% url 'relatorios:listar_relatorios' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <div class="card">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="{{ form.titulo.id_for_label }}" class="form-label">{{ form.titulo.label }}</label>
                    {{ form.titulo }}
                    {% if form.titulo.errors %}
                        <div class="alert alert-danger mt-2">
                            {{ form.titulo.errors }}
                        </div>
                    {% endif %}
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.conteudo.id_for_label }}" class="form-label">{{ form.conteudo.label }}</label>
                    {{ form.conteudo }}
                    {% if form.conteudo.errors %}
                        <div class="alert alert-danger mt-2">
                            {{ form.conteudo.errors }}
                        </div>
                    {% endif %}
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'relatorios:listar_relatorios' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">
                        {% if form.instance.id %}Atualizar{% else %}Salvar{% endif %}
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: relatorios\templates\relatorios\gerar_relatorio.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}




### Arquivo: relatorios\templates\relatorios\listar_relatorios.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatórios do Sistema</h1>
        <a href="{% url 'relatorios:criar_relatorio' %}" class="btn btn-primary">
            <i class="fas fa-plus"></i> Novo Relatório
        </a>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Relatório de Alunos</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">Gere relatórios completos dos alunos cadastrados no sistema, com opções de filtros por nome e data de nascimento.</p>
                </div>
                <div class="card-footer">
                    <a href="{% url 'relatorios:relatorio_alunos' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>

        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Relatório de Presenças</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">Acompanhe o registro de presenças dos alunos, com filtros por aluno, turma e período.</p>
                </div>
                <div class="card-footer">
                    <a href="{% url 'relatorios:relatorio_presencas' %}" class="btn btn-success">Acessar</a>
                </div>
            </div>
        </div>

        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">Relatório de Punições</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">Visualize as punições registradas no sistema, com filtros por aluno, tipo de punição e período.</p>
                </div>
                <div class="card-footer">
                    <a href="{% url 'relatorios:relatorio_punicoes' %}" class="btn btn-danger">Acessar</a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Relatórios Personalizados</h5>
        </div>
        <div class="card-body">
            {% if relatorios %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Título</th>
                                <th>Data de Criação</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for relatorio in relatorios %}
                                <tr>
                                    <td>{{ relatorio.titulo }}</td>
                                    <td>{{ relatorio.data_criacao|date:"d/m/Y H:i" }}</td>
                                    <td>
                                        <a href="{% url 'relatorios:detalhar_relatorio' relatorio.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i> Ver
                                        </a>
                                        <a href="{% url 'relatorios:editar_relatorio' relatorio.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i> Editar
                                        </a>
                                        <a href="{% url 'relatorios:excluir_relatorio' relatorio.id %}" class="btn btn-sm btn-danger">
                                            <i class="fas fa-trash"></i> Excluir
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <p class="mb-0">Nenhum relatório personalizado cadastrado. Clique em "Novo Relatório" para criar um.</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: relatorios\templates\relatorios\relatorio_alunos.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Alunos</h1>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="nome" class="form-label">Nome:</label>
                    <input type="text" id="nome" name="nome" class="form-control" value="{{ nome }}">
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data de Nascimento (Início):</label>
                    <input type="date" id="data_inicio" name="data_inicio" class="form-control" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data de Nascimento (Fim):</label>
                    <input type="date" id="data_fim" name="data_fim" class="form-control" value="{{ data_fim }}">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Botões de ação -->
    <div class="mb-3">
        <a href="{% url 'relatorios:relatorio_alunos_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i> Baixar PDF
        </a>
    </div>
    
    <!-- Tabela de resultados -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Resultados</h5>
        </div>
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>CPF</th>
                        <th>Email</th>
                        <th>Data de Nascimento</th>
                        <!-- Adicione mais colunas conforme necessário -->
                    </tr>
                </thead>
                <tbody>
                    {% for aluno in alunos %}
                    <tr>
                        <td>{{ aluno.nome }}</td>
                        <td>{{ aluno.cpf }}</td>
                        <td>{{ aluno.email }}</td>
                        <td>{{ aluno.data_nascimento|date:"d/m/Y" }}</td>
                        <!-- Adicione mais campos conforme necessário -->
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" class="text-center">Nenhum aluno encontrado com os filtros selecionados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: relatorios\templates\relatorios\relatorio_alunos_pdf.html

html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Alunos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .header {
            margin-bottom: 20px;
            text-align: center;
        }
        .filters {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }
        .text-center {
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Alunos</h1>
        <p>Data de geração: {{ data_geracao|date:"d/m/Y H:i" }}</p>
    </div>
    
    <div class="filters">
        <h3>Filtros aplicados:</h3>
        <p>
            {% if nome %}<strong>Nome:</strong> {{ nome }}{% endif %}
            {% if data_inicio %}<strong>Data de Nascimento (Início):</strong> {{ data_inicio }}{% endif %}
            {% if data_fim %}<strong>Data de Nascimento (Fim):</strong> {{ data_fim }}{% endif %}
            {% if not nome and not data_inicio and not data_fim %}Nenhum filtro aplicado{% endif %}
        </p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Nome</th>
                <th>CPF</th>
                <th>Email</th>
                <th>Data de Nascimento</th>
            </tr>
        </thead>
        <tbody>
            {% for aluno in alunos %}
            <tr>
                <td>{{ aluno.nome }}</td>
                <td>{{ aluno.cpf }}</td>
                <td>{{ aluno.email }}</td>
                <td>{{ aluno.data_nascimento|date:"d/m/Y" }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="text-center">Nenhum aluno encontrado com os filtros selecionados.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="footer">
        <p>Total de alunos: {{ alunos|length }}</p>
        <p>Relatório gerado pelo sistema OMAUM</p>
    </div>
</body>
</html>



### Arquivo: relatorios\templates\relatorios\relatorio_presencas.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Presenças</h1>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno:</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início:</label>
                    <input type="date" id="data_inicio" name="data_inicio" class="form-control" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim:</label>
                    <input type="date" id="data_fim" name="data_fim" class="form-control" value="{{ data_fim }}">
                </div>
                <div class="col-md-3 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Botões de ação -->
    <div class="mb-3">
        <a href="{% url 'relatorios:relatorio_presencas_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i> Baixar PDF
        </a>
    </div>
    
    <!-- Tabela de resultados -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Resultados</h5>
        </div>
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Aluno</th>
                        <th>Turma</th>
                        <th>Data</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for presenca in presencas %}
                    <tr>
                        <td>{{ presenca.aluno.nome }}</td>
                        <td>{{ presenca.turma.nome }}</td>
                        <td>{{ presenca.data|date:"d/m/Y" }}</td>
                        <td>
                            {% if presenca.presente %}
                                <span class="badge bg-success">Presente</span>
                            {% else %}
                                <span class="badge bg-danger">Ausente</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" class="text-center">Nenhuma presença encontrada com os filtros selecionados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: relatorios\templates\relatorios\relatorio_presencas_pdf.html

html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Presenças</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .header {
            margin-bottom: 20px;
            text-align: center;
        }
        .filters {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }
        .presente {
            color: green;
            font-weight: bold;
        }
        .ausente {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Presenças</h1>
        <p>Data de geração: {{ data_geracao|date:"d/m/Y H:i" }}</p>
    </div>
    
    <div class="filters">
        <h3>Filtros aplicados:</h3>
        <p>
            {% if aluno %}<strong>Aluno:</strong> {{ aluno.nome }}{% endif %}
            {% if data_inicio %}<strong>Data Início:</strong> {{ data_inicio }}{% endif %}
            {% if data_fim %}<strong>Data Fim:</strong> {{ data_fim }}{% endif %}
            {% if not aluno and not data_inicio and not data_fim %}Nenhum filtro aplicado{% endif %}
        </p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Turma</th>
                <th>Data</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for presenca in presencas %}
            <tr>
                <td>{{ presenca.aluno.nome }}</td>
                <td>{{ presenca.turma.nome }}</td>
                <td>{{ presenca.data|date:"d/m/Y" }}</td>
                <td>
                    {% if presenca.presente %}
                        <span class="presente">Presente</span>
                    {% else %}
                        <span class="ausente">Ausente</span>
                    {% endif %}
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="text-center">Nenhuma presença encontrada com os filtros selecionados.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="footer">
        <p>Total de registros: {{ presencas|length }}</p>
        <p>Relatório gerado pelo sistema OMAUM</p>
    </div>
</body>
</html>
</html>



### Arquivo: relatorios\templates\relatorios\relatorio_punicoes.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Punições</h1>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno:</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="tipo_punicao" class="form-label">Tipo de Punição:</label>
                    <select name="tipo_punicao" id="tipo_punicao" class="form-select">
                        <option value="">Todos</option>
                        {% for tipo in tipos_punicao %}
                            <option value="{{ tipo }}" {% if tipo_punicao == tipo %}selected{% endif %}>{{ tipo }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <label for="data_inicio" class="form-label">Data Início:</label>
                    <input type="date" id="data_inicio" name="data_inicio" class="form-control" value="{{ data_inicio }}">
                </div>
                <div class="col-md-2">
                    <label for="data_fim" class="form-label">Data Fim:</label>
                    <input type="date" id="data_fim" name="data_fim" class="form-control" value="{{ data_fim }}">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Botões de ação -->
    <div class="mb-3">
        <a href="{% url 'relatorios:relatorio_punicoes_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i> Baixar PDF
        </a>
    </div>
    
    <!-- Tabela de resultados -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Resultados</h5>
        </div>
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Aluno</th>
                        <th>Tipo de Punição</th>
                        <th>Data</th>
                        <th>Descrição</th>
                    </tr>
                </thead>
                <tbody>
                    {% for punicao in punicoes %}
                    <tr>
                        <td>{{ punicao.aluno.nome }}</td>
                        <td>{{ punicao.tipo_punicao }}</td>
                        <td>{{ punicao.data|date:"d/m/Y" }}</td>
                        <td>{{ punicao.descricao|truncatechars:50 }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" class="text-center">Nenhuma punição encontrada com os filtros selecionados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: relatorios\templates\relatorios\relatorio_punicoes_pdf.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Punições</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .header {
            margin-bottom: 20px;
            text-align: center;
        }
        .filters {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }
        .text-center {
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Punições</h1>
        <p>Data de geração: {{ data_geracao|date:"d/m/Y H:i" }}</p>
    </div>
    
    <div class="filters">
        <h3>Filtros aplicados:</h3>
        <p>
            {% if aluno %}<strong>Aluno:</strong> {{ aluno.nome }}{% endif %}
            {% if tipo_punicao %}<strong>Tipo de Punição:</strong> {{ tipo_punicao }}{% endif %}
            {% if data_inicio %}<strong>Data Início:</strong> {{ data_inicio }}{% endif %}
            {% if data_fim %}<strong>Data Fim:</strong> {{ data_fim }}{% endif %}
            {% if not aluno and not tipo_punicao and not data_inicio and not data_fim %}Nenhum filtro aplicado{% endif %}
        </p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Tipo de Punição</th>
                <th>Data</th>
                <th>Descrição</th>
            </tr>
        </thead>
        <tbody>
            {% for punicao in punicoes %}
            <tr>
                <td>{{ punicao.aluno.nome }}</td>
                <td>{{ punicao.tipo_punicao }}</td>
                <td>{{ punicao.data|date:"d/m/Y" }}</td>
                <td>{{ punicao.descricao|truncatechars:50 }}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="text-center">Nenhuma punição encontrada com os filtros selecionados.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="footer">
        <p>Total de registros: {{ punicoes|length }}</p>
        <p>Relatório gerado pelo sistema OMAUM</p>
    </div>
</body>
</html>

