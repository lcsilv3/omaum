# Código da Funcionalidade: relatorios - Parte 1/2
*Gerado automaticamente*



## relatorios\admin.py

python
from django.contrib import admin
from django.contrib.auth.models import Permission

# Registrar permissões no admin para facilitar a atribuição
admin.site.register(Permission)





## relatorios\apps.py

python
from django.apps import AppConfig


class RelatoriosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relatorios'





## relatorios\models.py

python
from django.db import models

# Create your models here.





## relatorios\tests.py

python
from django.test import TestCase

# Create your tests here.





## relatorios\urls.py

python
from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.index, name='index'),
    path('alunos/', views.relatorio_alunos, name='relatorio_alunos'),
    path('alunos/pdf/', views.relatorio_alunos_pdf, name='relatorio_alunos_pdf'),
    path('presencas/', views.relatorio_presencas, name='relatorio_presencas'),
    path('presencas/pdf/', views.relatorio_presencas_pdf, name='relatorio_presencas_pdf'),
    path('punicoes/', views.relatorio_punicoes, name='relatorio_punicoes'),
    path('punicoes/pdf/', views.relatorio_punicoes_pdf, name='relatorio_punicoes_pdf'),
]





## relatorios\views.py

python
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from alunos.models import Aluno
from presencas.models import PresencaAcademica
from punicoes.models import Punicao
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

@login_required
def index(request):
    """
    Página inicial do módulo de relatórios.
    """
    return render(request, 'relatorios/index.html')

@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
def relatorio_alunos(request):
    # Obter parâmetros de filtro
    nome = request.GET.get('nome', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todos os alunos
    alunos = Aluno.objects.all()
    
    # Aplicar filtros
    if nome:
        alunos = alunos.filter(nome__icontains=nome)
    if data_inicio:
        alunos = alunos.filter(data_nascimento__gte=data_inicio)
    if data_fim:
        alunos = alunos.filter(data_nascimento__lte=data_fim)
    
    context = {
        'alunos': alunos,
        'nome': nome,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'relatorios/relatorio_alunos.html', context)

@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
def relatorio_alunos_pdf(request):
    # Obter parâmetros de filtro
    nome = request.GET.get('nome', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todos os alunos
    alunos = Aluno.objects.all()
    
    # Aplicar filtros
    if nome:
        alunos = alunos.filter(nome__icontains=nome)
    if data_inicio:
        alunos = alunos.filter(data_nascimento__gte=data_inicio)
    if data_fim:
        alunos = alunos.filter(data_nascimento__lte=data_fim)
    
    # Criar um buffer para receber os dados do PDF
    buffer = BytesIO()
    
    # Criar o objeto PDF
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    
    # Container para os objetos 'Flowable'
    elementos = []
    
    # Definir estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']
    
    # Adicionar título
    elementos.append(Paragraph("Relatório de Alunos", estilo_titulo))
    
    # Criar dados da tabela
    data = [['Nome', 'CPF', 'Email', 'Data de Nascimento']]  # Linha de cabeçalho
    for aluno in alunos:
        data.append([
            aluno.nome,
            aluno.cpf,
            aluno.email,
            aluno.data_nascimento.strftime('%d/%m/%Y')
        ])
    
    # Criar tabela
    tabela = Table(data)
    
    # Adicionar estilo à tabela
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabela.setStyle(estilo)
    
    # Adicionar tabela aos elementos
    elementos.append(tabela)
    
    # Construir PDF
    doc.build(elementos)
    
    # Retornar resposta
    buffer.seek(0)
    
    # Definir nome do arquivo com data atual
    data_atual = datetime.now().strftime('%d-%m-%Y')
    filename = f"relatorio_alunos_{data_atual}.pdf"
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas(request):
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todas as presenças
    presencas = PresencaAcademica.objects.all().select_related('aluno', 'turma')
    
    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno_id=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma_id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    
    context = {
        'presencas': presencas,
        'alunos': alunos,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'relatorios/relatorio_presencas.html', context)

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas_pdf(request):
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todas as presenças
    presencas = PresencaAcademica.objects.all().select_related('aluno', 'turma')
    
    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno_id=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma_id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    # Criar um buffer para receber os dados do PDF
    buffer = BytesIO()
    
    # Criar o objeto PDF
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    
    # Container para os objetos 'Flowable'
    elementos = []
    
    # Definir estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']
    
    # Adicionar título
    elementos.append(Paragraph("Relatório de Presenças", estilo_titulo))
    
    # Criar dados da tabela
    data = [['Aluno', 'Turma', 'Data', 'Status']]  # Linha de cabeçalho
    for presenca in presencas:
        data.append([
            presenca.aluno.nome,
            presenca.turma.nome if hasattr(presenca, 'turma') and presenca.turma else "N/A",
            presenca.data.strftime('%d/%m/%Y'),
            "Presente" if presenca.presente else "Ausente"
        ])
    
    # Criar tabela
    tabela = Table(data)
    
    # Adicionar estilo à tabela
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabela.setStyle(estilo)
    
    # Adicionar tabela aos elementos
    elementos.append(tabela)
    
    # Construir PDF
    doc.build(elementos)
    
    # Retornar resposta
    buffer.seek(0)
    
    # Definir nome do arquivo com data atual
    data_atual = datetime.now().strftime('%d-%m-%Y')
    filename = f"relatorio_presencas_{data_atual}.pdf"
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@permission_required('punicoes.view_punicao', raise_exception=True)
def relatorio_punicoes(request):
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    tipo_punicao = request.GET.get('tipo_punicao', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todas as punições
    punicoes = Punicao.objects.all().select_related('aluno')
    
    # Aplicar filtros
    if aluno_id:
        punicoes = punicoes.filter(aluno_id=aluno_id)
    if tipo_punicao:
        punicoes = punicoes.filter(tipo_punicao=tipo_punicao)
    if data_inicio:
        punicoes = punicoes.filter(data__gte=data_inicio)
    if data_fim:
        punicoes = punicoes.filter(data__lte=data_fim)
    
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    tipos_punicao = Punicao.objects.values_list('tipo_punicao', flat=True).distinct()
    
    context = {
        'punicoes': punicoes,
        'alunos': alunos,
        'tipos_punicao': tipos_punicao,
        'aluno_id': aluno_id,
        'tipo_punicao': tipo_punicao,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'relatorios/relatorio_punicoes.html', context)

@login_required
@permission_required('punicoes.view_punicao', raise_exception=True)
def relatorio_punicoes_pdf(request):
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    tipo_punicao = request.GET.get('tipo_punicao', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todas as punições
    punicoes = Punicao.objects.all().select_related('aluno')
    
    # Aplicar filtros
    if aluno_id:
        punicoes = punicoes.filter(aluno_id=aluno_id)
    if tipo_punicao:
        punicoes = punicoes.filter(tipo_punicao=tipo_punicao)
    if data_inicio:
        punicoes = punicoes.filter(data__gte=data_inicio)
    if data_fim:
        punicoes = punicoes.filter(data__lte=data_fim)
    
    # Criar um buffer para receber os dados do PDF
    buffer = BytesIO()
    
    # Criar o objeto PDF
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    
    # Container para os objetos 'Flowable'
    elementos = []
    
    # Definir estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']
    
    # Adicionar título
    elementos.append(Paragraph("Relatório de Punições", estilo_titulo))
    
    # Criar dados da tabela
    data = [['Aluno', 'Tipo de Punição', 'Data', 'Descrição']]  # Linha de cabeçalho
    for punicao in punicoes:
        data.append([
            punicao.aluno.nome,
            punicao.tipo_punicao,
            punicao.data.strftime('%d/%m/%Y'),
            punicao.descricao[:100] + '...' if len(punicao.descricao) > 100 else punicao.descricao
        ])
    
    # Criar tabela
    tabela = Table(data)
    
    # Adicionar estilo à tabela
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabela.setStyle(estilo)
    
    # Adicionar tabela aos elementos
    elementos.append(tabela)
    
    # Construir PDF
    doc.build(elementos)
    
    # Retornar resposta
    buffer.seek(0)
    
    # Definir nome do arquivo com data atual
    data_atual = datetime.now().strftime('%d-%m-%Y')
    filename = f"relatorio_punicoes_{data_atual}.pdf"
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response





## relatorios\templates\relatorios\gerar_relatorio.html

html
{% extends 'core/base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}





## relatorios\templates\relatorios\index.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Relatórios do Sistema</h1>
    
    <div class="row mt-4">
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Relatório de Alunos</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">Gere relatórios completos dos alunos cadastrados no sistema, com opções de filtros por nome e data de nascimento.</p>
                </div>
                <div class="card-footer">
                    <a href="{% url 'relatorio_alunos' %}" class="btn btn-primary">Acessar</a>
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
                    <a href="{% url 'relatorio_presencas' %}" class="btn btn-success">Acessar</a>
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
                    <a href="{% url 'relatorio_punicoes' %}" class="btn btn-danger">Acessar</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}





## relatorios\templates\relatorios\relatorio_alunos.html

html
{% extends 'core/base.html' %}

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
        <a href="{% url 'relatorio_alunos_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
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





## relatorios\templates\relatorios\relatorio_presencas.html

html
{% extends 'core/base.html' %}

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
        <a href="{% url 'relatorio_presencas_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
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



