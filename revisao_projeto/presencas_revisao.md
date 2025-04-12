# Revisão da Funcionalidade: presencas

## Arquivos forms.py:


### Arquivo: presencas\forms.py

```python
from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from .models import PresencaAcademica

class PresencaForm(forms.ModelForm):
    class Meta:
        model = PresencaAcademica
        fields = ['aluno', 'turma', 'data', 'presente', 'justificativa']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data > date.today():
            raise ValidationError("A data da presença não pode ser no futuro.")
        return data

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        turma = cleaned_data.get('turma')
        data = cleaned_data.get('data')

        if aluno and turma and data:
            # Check if this is an update (instance exists)
            if self.instance.pk:
                # Exclude the current instance from the uniqueness check
                existing = PresencaAcademica.objects.filter(
                    aluno=aluno, 
                    turma=turma, 
                    data=data
                ).exclude(pk=self.instance.pk).exists()
            else:
                # For new instances, check if any record exists
                existing = PresencaAcademica.objects.filter(
                    aluno=aluno, 
                    turma=turma, 
                    data=data
                ).exists()

            if existing:
                raise ValidationError("Já existe um registro de presença para este aluno nesta turma e data.")
        
        return cleaned_data
```

## Arquivos views.py:


### Arquivo: presencas\views.py

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import PresencaAcademica
from .forms import PresencaForm  # Changed from PresencaAcademicaForm to PresencaForm
from alunos.models import Aluno
from turmas.models import Turma
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
import xlsxwriter

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def listar_presencas(request):
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

    return render(request, 'presencas/listar_presencas.html', {
        'presencas': presencas,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'alunos': alunos,
        'turmas': turmas
    })

@login_required
@permission_required('presencas.add_presencaacademica', raise_exception=True)
def registrar_presenca(request):
    """Registra a presença de um aluno."""
    if request.method == 'POST':
        form = PresencaForm(request.POST)
        if form.is_valid():
            presenca = form.save(commit=False)
            presenca.registrado_por = request.user
            presenca.save()
            messages.success(request, 'Presença registrada com sucesso!')
            return redirect('presencas:listar_presencas')
    else:
        form = PresencaForm()

    return render(request, 'presencas/registrar_presenca.html', {'form': form})

@login_required
@permission_required('presencas.change_presencaacademica', raise_exception=True)
def editar_presenca(request, id):
    """Edita um registro de presença."""
    presenca = get_object_or_404(PresencaAcademica, id=id)
    if request.method == 'POST':
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presença atualizada com sucesso!')
            return redirect('presencas:listar_presencas')
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
        return redirect('presencas:listar_presencas')

    return render(request, 'presencas/excluir_presenca.html', {'presenca': presenca})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def detalhar_presenca(request, id):
    """Exibe os detalhes de um registro de presença."""
    presenca = get_object_or_404(PresencaAcademica, id=id)
    return render(request, 'presencas/detalhar_presenca.html', {'presenca': presenca})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas(request):
    """Exibe um relatório de presenças com filtros."""
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

    # Calcular estatísticas
    presencas_count = {
        'presentes': presencas.filter(presente=True).count(),
        'ausentes': presencas.filter(presente=False).count()
    }
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()

    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'presencas_count': presencas_count,
    }
    return render(request, 'presencas/relatorio_presencas.html', context)

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas_pdf(request):
    """Gera um relatório de presenças em formato PDF."""
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
    data = [['Aluno', 'Turma', 'Data', 'Status', 'Justificativa']]  # Linha de cabeçalho
    for presenca in presencas:
        data.append([
            presenca.aluno.nome,
            presenca.turma.nome if hasattr(presenca, 'turma') and presenca.turma else "N/A",
            presenca.data.strftime('%d/%m/%Y'),
            "Presente" if presenca.presente else "Ausente",
            presenca.justificativa if presenca.justificativa else "-"
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
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas_excel(request):
    """Gera um relatório de presenças em formato Excel."""
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

    # Criar um buffer para receber os dados do Excel
    buffer = BytesIO()

    # Criar o objeto Excel
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet('Presenças')

    # Definir estilos
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4F81BD',
        'color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })

    cell_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })

    # Definir largura das colunas
    worksheet.set_column('A:A', 30)  # Aluno
    worksheet.set_column('B:B', 20)  # Turma
    worksheet.set_column('C:C', 15)  # Data
    worksheet.set_column('D:D', 15)  # Status
    worksheet.set_column('E:E', 40)  # Justificativa

    # Escrever cabeçalho
    headers = ['Aluno', 'Turma', 'Data', 'Status', 'Justificativa']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Escrever dados
    for row, presenca in enumerate(presencas, start=1):
        worksheet.write(row, 0, presenca.aluno.nome, cell_format)
        worksheet.write(row, 1, presenca.turma.nome if hasattr(presenca, 'turma') and presenca.turma else "N/A", cell_format)
        worksheet.write(row, 2, presenca.data.strftime('%d/%m/%Y'), cell_format)
        worksheet.write(row, 3, "Presente" if presenca.presente else "Ausente", cell_format)
        worksheet.write(row, 4, presenca.justificativa if presenca.justificativa else "-", cell_format)

    # Adicionar estatísticas
    row = len(presencas) + 3
    worksheet.write(row, 0, "Estatísticas", workbook.add_format({'bold': True, 'font_size': 14}))

    row += 1
    worksheet.write(row, 0, "Total de Registros:")
    worksheet.write(row, 1, len(presencas))

    row += 1
    presentes = sum(1 for p in presencas if p.presente)
    worksheet.write(row, 0, "Total de Presenças:")
    worksheet.write(row, 1, presentes)

    row += 1
    worksheet.write(row, 0, "Total de Ausências:")
    worksheet.write(row, 1, len(presencas) - presentes)

    # Fechar o workbook
    workbook.close()

    # Retornar resposta
    buffer.seek(0)

    # Definir nome do arquivo com data atual
    data_atual = datetime.now().strftime('%d-%m-%Y')
    filename = f"relatorio_presencas_{data_atual}.xlsx"

    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
```

## Arquivos urls.py:


### Arquivo: presencas\urls.py

```python
from django.urls import path
from . import views

app_name = 'presencas'

urlpatterns = [
    path('lista/', views.listar_presencas, name='listar_presencas'),  # Alterado para usar a função existente
    path('registrar/', views.registrar_presenca, name='registrar_presenca'),
    path('editar/<int:id>/', views.editar_presenca, name='editar_presenca'),
    path('excluir/<int:id>/', views.excluir_presenca, name='excluir_presenca'),
    path('detalhar/<int:id>/', views.detalhar_presenca, name='detalhar_presenca'),
    path('relatorio/', views.relatorio_presencas, name='relatorio_presencas'),
    path('relatorio/pdf/', views.relatorio_presencas_pdf, name='relatorio_presencas_pdf'),
    path('relatorio/excel/', views.relatorio_presencas_excel, name='relatorio_presencas_excel'),
]

```

## Arquivos models.py:


### Arquivo: presencas\models.py

```python
from django.db import models
from django.contrib.auth.models import User
from alunos.models import Aluno
from turmas.models import Turma

class PresencaAcademica(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE, 
        verbose_name='Aluno',
        to_field='cpf'  # Especificar que estamos referenciando o campo cpf
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE, 
        verbose_name='Turma'
    )
    data = models.DateField(verbose_name='Data')
    presente = models.BooleanField(default=True, verbose_name='Presente')
    justificativa = models.TextField(blank=True, null=True, verbose_name='Justificativa')
    registrado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Registrado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome} - {self.data}"

    class Meta:
        verbose_name = 'Presença Acadêmica'
        verbose_name_plural = 'Presenças Acadêmicas'
        ordering = ['-data', 'aluno__nome']
        unique_together = ['aluno', 'turma', 'data']
```

## Arquivos de Template:


### Arquivo: presencas\templates\presencas\detalhar_presenca.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Presença</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações do Registro</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ presenca.aluno.nome }}</p>
                    <p><strong>Turma:</strong> {{ presenca.turma.nome }}</p>
                    <p><strong>Data:</strong> {{ presenca.data|date:"d/m/Y" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Status:</strong> {% if presenca.presente %}Presente{% else %}Ausente{% endif %}</p>
                    <p><strong>Registrado por:</strong> {{ presenca.registrado_por.username }}</p>
                    <p><strong>Data de Registro:</strong> {{ presenca.data_registro|date:"d/m/Y H:i" }}</p>
                </div>
            </div>

            {% if presenca.justificativa %}
            <div class="mt-3">
                <h6>Justificativa:</h6>
                <div class="p-3 bg-light rounded">
                    {{ presenca.justificativa }}
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <div class="mt-3">
        <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-warning">Editar</a>
        <a href="{% url 'presencas:excluir_presenca' presenca.id %}" class="btn btn-danger">Excluir</a>
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
</div>
{% endblock %}
```


### Arquivo: presencas\templates\presencas\editar_presenca.html

```html
{% extends 'base.html' %}

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
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: presencas\templates\presencas\excluir_presenca.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Registro de Presença</h1>
    
    <div class="card mb-4">
        <div class="card-body">
            <div class="alert alert-danger">
                <h5>Confirmação de Exclusão</h5>
                <p>Você está prestes a excluir o seguinte registro de presença:</p>
                <ul>
                    <li><strong>Aluno:</strong> {{ presenca.aluno.nome }}</li>
                    <li><strong>Turma:</strong> {{ presenca.turma.nome }}</li>
                    <li><strong>Data:</strong> {{ presenca.data|date:"d/m/Y" }}</li>
                    <li><strong>Status:</strong> {% if presenca.presente %}Presente{% else %}Ausente{% endif %}</li>
                </ul>
                <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
            </div>
            
            <form method="post">
                {% csrf_token %}
                <div class="mt-3">
                    <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: presencas\templates\presencas\listar_presencas.html

```html
{% extends 'base.html' %}

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
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Limpar Filtros</a>
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
                <td>{{ presenca.aluno.nome }}</td>
                <td>{{ presenca.turma.nome }}</td>
                <td>{{ presenca.data|date:"d/m/Y" }}</td>
                <td>{% if presenca.presente %}Sim{% else %}Não{% endif %}</td>
                <td>
                    <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'presencas:excluir_presenca' presenca.id %}" class="btn btn-sm btn-danger">Excluir</a>
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

    <div class="mt-3">
        <a href="{% url 'presencas:registrar_presenca' %}" class="btn btn-primary">Registrar Nova Presença</a>
        <a href="{% url 'presencas:relatorio_presencas' %}" class="btn btn-info">Gerar Relatório</a>
    </div>
</div>
{% endblock %}

```


### Arquivo: presencas\templates\presencas\registrar_presenca.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Presen√ßa</h1>

    <div class="card mb-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}

                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                        <div class="invalid-feedback">
                            {{ field.errors }}
                        </div>
                    {% endif %}
                </div>
                {% endfor %}
                <button type="submit" class="btn btn-primary">Registrar</button>
            </form>
        </div>
    </div>
    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary mt-2">Voltar</a>
</div>
{% endblock %}

```


### Arquivo: presencas\templates\presencas\relatorio_presencas.html

```html
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
                    <label for="turma" class="form-label">Turma:</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if turma_id == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <label for="data_inicio" class="form-label">Data Início:</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ data_inicio }}">
                </div>
                <div class="col-md-2">
                    <label for="data_fim" class="form-label">Data Fim:</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ data_fim }}">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Botões de ação -->
    <div class="mb-3">
        <a href="{% url 'presencas:relatorio_presencas_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i> Baixar PDF
        </a>
        <a href="{% url 'presencas:relatorio_presencas_excel' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-success">
            <i class="fas fa-file-excel"></i> Baixar Excel
        </a>
    </div>

    <!-- Estatísticas -->
    <div class="mt-4 mb-4">
        <h5>Estatísticas</h5>
        <div class="row">
            <div class="col-md-4">
                <div class="card bg-light">
                    <div class="card-body">
                        <h6 class="card-title">Total de Registros</h6>
                        <p class="card-text display-6">{{ presencas.count }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-success text-white">
                    <div class="card-body">
                        <h6 class="card-title">Presenças</h6>
                        <p class="card-text display-6">{{ presencas_count.presentes }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-danger text-white">
                    <div class="card-body">
                        <h6 class="card-title">Ausências</h6>
                        <p class="card-text display-6">{{ presencas_count.ausentes }}</p>
                    </div>
                </div>
            </div>
        </div>
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
                        <th>Justificativa</th>
                    </tr>
                </thead>
                <tbody>
                    {% for presenca in presencas %}
                    <tr>
                        <td>{{ presenca.aluno.nome }}</td>
                        <td>{{ presenca.turma.nome|default:"N/A" }}</td>
                        <td>{{ presenca.data|date:"d/m/Y" }}</td>
                        <td>
                            {% if presenca.presente %}
                                <span class="badge bg-success">Presente</span>
                            {% else %}
                                <span class="badge bg-danger">Ausente</span>
                            {% endif %}
                        </td>
                        <td>{{ presenca.justificativa|default:"-"|truncatechars:50 }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center">Nenhuma presença encontrada com os filtros selecionados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```
