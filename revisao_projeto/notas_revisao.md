# Revisão da Funcionalidade: notas

## Arquivos forms.py:


### Arquivo: notas\forms.py

python
from django import forms
from .models import Nota
from alunos.models import Aluno
from cursos.models import Curso

class NotaForm(forms.ModelForm):
    """
    Formulário para criação e edição de notas.
    """
    
    class Meta:
        model = Nota
        fields = ['aluno', 'curso', 'valor', 'data', 'tipo_avaliacao', 'peso', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '10'
            }),
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tipo_avaliacao': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1',
                'max': '5'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        labels = {
            'aluno': 'Aluno',
            'curso': 'Curso',
            'valor': 'Nota',
            'data': 'Data da Avaliação',
            'tipo_avaliacao': 'Tipo de Avaliação',
            'peso': 'Peso da Avaliação',
            'observacoes': 'Observações'
        }
        help_texts = {
            'valor': 'Valor entre 0 e 10',
            'peso': 'Peso da avaliação (padrão: 1.0)',
            'tipo_avaliacao': 'Selecione o tipo de avaliação'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir valor padrão para o peso
        self.fields['peso'].initial = 1.0
        
        # Filtrar apenas alunos ativos
        self.fields['aluno'].queryset = Aluno.objects.filter(situacao='ATIVO')
        
        # Filtrar apenas cursos ativos
        self.fields['curso'].queryset = Curso.objects.filter(ativo=True)
        
        # Adicionar classes CSS para estilização
        for field_name, field in self.fields.items():
            if field_name not in ['aluno', 'curso', 'tipo_avaliacao']:
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_valor(self):
        """Validação personalizada para o campo valor."""
        valor = self.cleaned_data.get('valor')
        if valor is not None:
            if valor < 0:
                raise forms.ValidationError("A nota não pode ser negativa.")
            if valor > 10:
                raise forms.ValidationError("A nota não pode ser maior que 10.")
        return valor
    
    def clean_peso(self):
        """Validação personalizada para o campo peso."""
        peso = self.cleaned_data.get('peso')
        if peso is not None:
            if peso <= 0:
                raise forms.ValidationError("O peso deve ser maior que zero.")
            if peso > 5:
                raise forms.ValidationError("O peso não pode ser maior que 5.")
        return peso



## Arquivos views.py:


### Arquivo: notas\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg, Max, Min
from .models import Nota
from alunos.models import Aluno
from cursos.models import Curso
from .forms import NotaForm
import csv
import datetime


@login_required
def listar_notas(request):
    """Lista todas as notas cadastradas."""
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    curso_id = request.GET.get('curso', '')
    periodo = request.GET.get('periodo', '')
    
    # Iniciar queryset
    notas = Nota.objects.all().select_related('aluno', 'curso')
    
    # Aplicar filtros
    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)
    
    if curso_id:
        notas = notas.filter(curso__id=curso_id)
    
    if periodo:
        hoje = datetime.datetime.now().date()
        
        if periodo == 'atual':
            # Mês atual
            notas = notas.filter(data__month=hoje.month, data__year=hoje.year)
        elif periodo == 'ultimo_mes':
            # Último mês
            um_mes_atras = hoje - datetime.timedelta(days=30)
            notas = notas.filter(data__gte=um_mes_atras)
        elif periodo == 'ultimo_trimestre':
            # Último trimestre
            tres_meses_atras = hoje - datetime.timedelta(days=90)
            notas = notas.filter(data__gte=tres_meses_atras)
        elif periodo == 'ultimo_semestre':
            # Último semestre
            seis_meses_atras = hoje - datetime.timedelta(days=180)
            notas = notas.filter(data__gte=seis_meses_atras)
    
    # Calcular estatísticas
    estatisticas = {
        'media_geral': notas.aggregate(Avg('valor'))['valor__avg'] or 0,
        'nota_maxima': notas.aggregate(Max('valor'))['valor__max'] or 0,
        'nota_minima': notas.aggregate(Min('valor'))['valor__min'] or 0,
        'total_notas': notas.count(),
    }
    
    # Obter alunos e cursos para os filtros
    alunos = Aluno.objects.filter(situacao='ATIVO')
    cursos = Curso.objects.filter(ativo=True)
    
    context = {
        'notas': notas,
        'estatisticas': estatisticas,
        'alunos': alunos,
        'cursos': cursos,
        'filtros': {
            'aluno': aluno_id,
            'curso': curso_id,
            'periodo': periodo
        }
    }
    
    return render(request, "notas/listar_notas.html", context)


@login_required
def detalhar_nota(request, nota_id):
    """Exibe os detalhes de uma nota."""
    nota = get_object_or_404(Nota, id=nota_id)
    return render(request, "notas/detalhar_nota.html", {"nota": nota})


@login_required
def criar_nota(request):
    """Cria uma nova nota."""
    if request.method == "POST":
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save()
            messages.success(request, "Nota cadastrada com sucesso!")
            return redirect("notas:detalhar_nota", nota_id=nota.id)
    else:
        form = NotaForm()
    
    return render(request, "notas/formulario_nota.html", {"form": form})


@login_required
def editar_nota(request, nota_id):
    """Edita uma nota existente."""
    nota = get_object_or_404(Nota, id=nota_id)
    
    if request.method == "POST":
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            nota = form.save()
            messages.success(request, "Nota atualizada com sucesso!")
            return redirect("notas:detalhar_nota", nota_id=nota.id)
    else:
        form = NotaForm(instance=nota)
    
    return render(request, "notas/formulario_nota.html", {"form": form, "nota": nota})


@login_required
def excluir_nota(request, nota_id):
    """Exclui uma nota."""
    nota = get_object_or_404(Nota, id=nota_id)
    
    if request.method == "POST":
        nota.delete()
        messages.success(request, "Nota excluída com sucesso!")
        return redirect("notas:listar_notas")
    
    return render(request, "notas/excluir_nota.html", {"nota": nota})


def obter_notas_filtradas(request):
    """Obtém as notas com base nos filtros aplicados."""
    aluno_id = request.GET.get('aluno', '')
    curso_id = request.GET.get('curso', '')
    periodo = request.GET.get('periodo', '')
    
    notas = Nota.objects.all().select_related('aluno', 'curso')
    
    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)
    
    if curso_id:
        notas = notas.filter(curso__id=curso_id)
    
    if periodo:
        hoje = datetime.datetime.now().date()
        
        if periodo == 'atual':
            # Mês atual
            notas = notas.filter(data__month=hoje.month, data__year=hoje.year)
        elif periodo == 'ultimo_mes':
            # Último mês
            um_mes_atras = hoje - datetime.timedelta(days=30)
            notas = notas.filter(data__gte=um_mes_atras)
        elif periodo == 'ultimo_trimestre':
            # Último trimestre
            tres_meses_atras = hoje - datetime.timedelta(days=90)
            notas = notas.filter(data__gte=tres_meses_atras)
        elif periodo == 'ultimo_semestre':
            # Último semestre
            seis_meses_atras = hoje - datetime.timedelta(days=180)
            notas = notas.filter(data__gte=seis_meses_atras)
    
    return notas


@login_required
def exportar_notas_csv(request):
    """Exporta os dados das notas para um arquivo CSV."""
    try:
        # Obter notas com os mesmos filtros da listagem
        notas = obter_notas_filtradas(request)
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="notas.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Aluno",
            "Curso",
            "Nota",
            "Data",
            "Tipo de Avaliação",
            "Observações"
        ])
        
        for nota in notas:
            writer.writerow([
                nota.aluno.nome,
                nota.curso.nome,
                nota.valor,
                nota.data.strftime("%d/%m/%Y"),
                nota.get_tipo_avaliacao_display() if hasattr(nota, "get_tipo_avaliacao_display") else "Regular",
                nota.observacoes or ""
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar notas: {str(e)}")
        return redirect("notas:listar_notas")


@login_required
def exportar_notas_excel(request):
    """Exporta os dados das notas para um arquivo Excel."""
    try:
        import xlwt
        
        # Obter notas com os mesmos filtros da listagem
        notas = obter_notas_filtradas(request)
        
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="notas.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Notas')
        
        # Estilos
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        # Cabeçalhos
        colunas = ['Aluno', 'Curso', 'Nota', 'Data', 'Tipo de Avaliação', 'Observações']
        for col_num, coluna in enumerate(colunas):
            ws.write(0, col_num, coluna, font_style)
        
        # Dados
        font_style = xlwt.XFStyle()
        for row_num, nota in enumerate(notas, 1):
            ws.write(row_num, 0, nota.aluno.nome, font_style)
            ws.write(row_num, 1, nota.curso.nome, font_style)
            ws.write(row_num, 2, float(nota.valor), font_style)
            ws.write(row_num, 3, nota.data.strftime("%d/%m/%Y"), font_style)
            ws.write(row_num, 4, nota.get_tipo_avaliacao_display() if hasattr(nota, "get_tipo_avaliacao_display") else "Regular", font_style)
            ws.write(row_num, 5, nota.observacoes or "", font_style)
        
        wb.save(response)
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar notas para Excel: {str(e)}")
        return redirect("notas:listar_notas")


@login_required
def dashboard_notas(request):
    """Exibe o dashboard de notas com estatísticas."""
    # Estatísticas gerais
    total_notas = Nota.objects.count()
    media_geral = Nota.objects.aggregate(Avg('valor'))['valor__avg'] or 0
    
    # Notas por curso
    cursos = Curso.objects.filter(ativo=True)
    notas_por_curso = []
    
    for curso in cursos:
        notas_curso = Nota.objects.filter(curso=curso)
        if notas_curso.exists():
            media_curso = notas_curso.aggregate(Avg('valor'))['valor__avg'] or 0
            notas_por_curso.append({
                'curso': curso.nome,
                'media': media_curso,
                'total': notas_curso.count()
            })
    
    # Melhores alunos
    alunos = Aluno.objects.filter(situacao='ATIVO')
    melhores_alunos = []
    
    for aluno in alunos[:10]:  # Limitar a 10 alunos para performance
        notas_aluno = Nota.objects.filter(aluno=aluno)
        if notas_aluno.exists():
            media_aluno = notas_aluno.aggregate(Avg('valor'))['valor__avg'] or 0
            melhores_alunos.append({
                'aluno': aluno,
                'media': media_aluno,
                'total_notas': notas_aluno.count()
            })
    
    # Ordenar por média decrescente
    melhores_alunos.sort(key=lambda x: x['media'], reverse=True)
    melhores_alunos = melhores_alunos[:5]  # Top 5
    
    context = {
        'total_notas': total_notas,
        'media_geral': media_geral,
        'notas_por_curso': notas_por_curso,
        'melhores_alunos': melhores_alunos
    }
    
    return render(request, "notas/dashboard_notas.html", context)


@login_required
def registrar_nota_aluno(request, aluno_cpf):
    """Registra uma nota para um aluno específico."""
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save()
            messages.success(request, 'Nota registrada com sucesso!')
            return redirect('notas:detalhar_nota', nota_id=nota.id)
    else:
        # Pré-preencher o formulário com o aluno selecionado
        form = NotaForm(initial={'aluno': aluno})
    
    return render(request, 'notas/formulario_nota.html', {
        'form': form,
        'aluno': aluno,
        'registro_direto': True
    })


@login_required
def relatorio_notas_aluno(request, aluno_cpf):
    """Exibe um relatório de notas de um aluno específico."""
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    
    # Obter todas as notas do aluno
    notas = Nota.objects.filter(aluno=aluno).select_related('curso', 'turma')
    
    # Agrupar notas por curso
    cursos_info = []
    cursos_ids = notas.values_list('curso', flat=True).distinct()
    
    for curso_id in cursos_ids:
        curso = Curso.objects.get(id=curso_id)
        notas_curso = notas.filter(curso=curso)
        
        # Calcular média ponderada
        total_pesos = sum(nota.peso for nota in notas_curso)
        if total_pesos > 0:
            media = sum(nota.valor * nota.peso for nota in notas_curso) / total_pesos
        else:
            media = 0
        
        # Determinar situação
        if media >= 7:
            situacao = 'Aprovado'
        elif media >= 5:
            situacao = 'Em Recuperação'
        else:
            situacao = 'Reprovado'
        
        cursos_info.append({
            'id': curso.id,
            'nome': curso.nome,
            'notas': notas_curso,
            'media': round(media, 1),
            'situacao': situacao
        })
    
    context = {
        'aluno': aluno,
        'cursos': cursos_info,
        'total_cursos': len(cursos_info),
    }
    
    return render(request, 'notas/relatorio_notas_aluno.html', context)


@login_required
def relatorio_notas_turma(request, turma_id):
    """Exibe um relatório de notas de uma turma específica."""
    turma = get_object_or_404(Turma, id=turma_id)
    
    # Obter todas as notas da turma
    notas = Nota.objects.filter(turma=turma).select_related('aluno')
    
    # Agrupar notas por aluno
    alunos_info = []
    alunos_ids = notas.values_list('aluno', flat=True).distinct()
    
    for aluno_id in alunos_ids:
        aluno = Aluno.objects.get(cpf=aluno_id)
        notas_aluno = notas.filter(aluno=aluno)
        
        # Calcular média ponderada
        total_pesos = sum(nota.peso for nota in notas_aluno)
        if total_pesos > 0:
            media = sum(nota.valor * nota.peso for nota in notas_aluno) / total_pesos
        else:
            media = 0
        
        # Determinar situação
        if media >= 7:
            situacao = 'Aprovado'
        elif media >= 5:
            situacao = 'Em Recuperação'
        else:
            situacao = 'Reprovado'
        
        alunos_info.append({
            'aluno': aluno,
            'notas': notas_aluno,
            'media': round(media, 1),
            'situacao': situacao
        })
    
    # Ordenar por nome do aluno
    alunos_info.sort(key=lambda x: x['aluno'].nome)
    
    context = {
        'turma': turma,
        'alunos': alunos_info,
        'total_alunos': len(alunos_info),
    }
    
    return render(request, 'notas/relatorio_notas_turma.html', context)
from django.http import HttpResponse
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
from django.utils import timezone
import pandas as pd
from io import BytesIO

def exportar_notas_pdf(request):
    """Exporta a lista de notas para PDF."""
    # Obter filtros
    aluno_id = request.GET.get('aluno', '')
    curso_id = request.GET.get('curso', '')
    
    # Filtrar notas
    notas = Nota.objects.all()
    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)
    if curso_id:
        notas = notas.filter(curso__id=curso_id)
    
    # Calcular médias
    alunos_medias = {}
    for nota in notas:
        if nota.aluno.cpf not in alunos_medias:
            alunos_medias[nota.aluno.cpf] = {
                'aluno': nota.aluno,
                'notas': [],
                'soma': 0,
                'count': 0
            }
        alunos_medias[nota.aluno.cpf]['notas'].append(nota)
        alunos_medias[nota.aluno.cpf]['soma'] += nota.valor
        alunos_medias[nota.aluno.cpf]['count'] += 1
    
    for cpf in alunos_medias:
        if alunos_medias[cpf]['count'] > 0:
            alunos_medias[cpf]['media'] = alunos_medias[cpf]['soma'] / alunos_medias[cpf]['count']
        else:
            alunos_medias[cpf]['media'] = 0
    
    # Renderizar o template HTML
    html_string = render_to_string(
        'notas/pdf/notas_pdf.html',
        {
            'notas': notas,
            'alunos_medias': alunos_medias.values(),
            'data_geracao': timezone.now(),
            'filtros': {
                'aluno': aluno_id,
                'curso': curso_id,
            }
        }
    )
    
    # Criar arquivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="notas.pdf"'
    
    # Gerar PDF a partir do HTML
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()
    
    # Retornar o PDF como resposta
    response.write(result)
    return response

def exportar_notas_excel(request):
    """Exporta a lista de notas para Excel."""
    # Obter filtros
    aluno_id = request.GET.get('aluno', '')
    curso_id = request.GET.get('curso', '')
    
    # Filtrar notas
    notas = Nota.objects.all()
    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)
    if curso_id:
        notas = notas.filter(curso__id=curso_id)
    
    # Preparar dados para o Excel
    data = []
    for nota in notas:
        data.append({
            'ID': nota.id,
            'Aluno': nota.aluno.nome,
            'CPF': nota.aluno.cpf,
            'Curso': nota.curso.nome,
            'Turma': nota.turma.nome if hasattr(nota, 'turma') and nota.turma else '',
            'Tipo de Avaliação': nota.get_tipo_avaliacao_display() if hasattr(nota, 'get_tipo_avaliacao_display') else '',
            'Nota': nota.valor,
            'Data': nota.data,
            'Observações': nota.observacoes if hasattr(nota, 'observacoes') else '',
        })
    
    # Criar DataFrame
    df = pd.DataFrame(data)
    
    # Criar arquivo Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Notas', index=False)
    
    # Ajustar largura das colunas
    worksheet = writer.sheets['Notas']
    for i, col in enumerate(df.columns):
        column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, column_width)
    
    # Adicionar formatação condicional para as notas
    formato_nota_alta = writer.book.add_format({'bold': True, 'font_color': 'green'})
    formato_nota_media = writer.book.add_format({'bold': True, 'font_color': 'orange'})
    formato_nota_baixa = writer.book.add_format({'bold': True, 'font_color': 'red'})
    
    # Coluna da nota (índice 6)
    worksheet.conditional_format(1, 6, len(data), 6, {'type': 'cell',
                                                      'criteria': '>=',
                                                      'value': 7,
                                                      'format': formato_nota_alta})
    worksheet.conditional_format(1, 6, len(data), 6, {'type': 'cell',
                                                      'criteria': 'between',
                                                      'minimum': 5,
                                                      'maximum': 6.9,
                                                      'format': formato_nota_media})
    worksheet.conditional_format(1, 6, len(data), 6, {'type': 'cell',
                                                      'criteria': '<',
                                                      'value': 5,
                                                      'format': formato_nota_baixa})
    
    writer.save()
    output.seek(0)
    
    # Retornar o arquivo Excel
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="notas.xlsx"'
    return response


## Arquivos urls.py:


### Arquivo: notas\urls.py

python
from django.urls import path
from . import views

app_name = "notas"

urlpatterns = [
    path("", views.listar_notas, name="listar_notas"),
    path("<int:nota_id>/", views.detalhar_nota, name="detalhar_nota"),
    path("criar/", views.criar_nota, name="criar_nota"),
    path("<int:nota_id>/editar/", views.editar_nota, name="editar_nota"),
    path("<int:nota_id>/excluir/", views.excluir_nota, name="excluir_nota"),
    path("exportar/csv/", views.exportar_notas_csv, name="exportar_notas_csv"),
    path("exportar/excel/", views.exportar_notas_excel, name="exportar_notas_excel"),
    path("dashboard/", views.dashboard_notas, name="dashboard_notas"),
]


## Arquivos models.py:


### Arquivo: notas\models.py

python
from django.db import models
from django.utils import timezone
from alunos.models import Aluno
from cursos.models import Curso
from turmas.models import Turma

class Nota(models.Model):
    TIPO_AVALIACAO_CHOICES = [
        ('prova', 'Prova'),
        ('trabalho', 'Trabalho'),
        ('apresentacao', 'Apresentação'),
        ('participacao', 'Participação'),
        ('atividade', 'Atividade'),
        ('exame', 'Exame Final'),
        ('outro', 'Outro'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='notas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='notas')
    tipo_avaliacao = models.CharField(max_length=20, choices=TIPO_AVALIACAO_CHOICES)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    peso = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    data = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-data', 'aluno__nome']
        # Garantir que não haja notas duplicadas para o mesmo aluno/curso/turma/tipo
        unique_together = ['aluno', 'curso', 'turma', 'tipo_avaliacao', 'data']
    
    def __str__(self):
        return f"Nota de {self.aluno} em {self.curso} ({self.get_tipo_avaliacao_display()}): {self.valor}"
    
    @property
    def valor_ponderado(self):
        """Retorna o valor da nota ponderado pelo peso."""
        return self.valor * self.peso
    
    @property
    def situacao(self):
        """Retorna a situação do aluno com base na nota."""
        if self.valor >= 7:
            return 'Aprovado'
        elif self.valor >= 5:
            return 'Em Recuperação'
        else:
            return 'Reprovado'



## Arquivos de Template:


### Arquivo: notas\templates\notas\dashboard.html

html
{% extends 'base.html' %}

{% block title %}Dashboard Acadêmico{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard Acadêmico</h1>
        <a href="{% url 'notas:listar_notas' %}" class="btn btn-secondary">
            <i class="fas fa-list"></i> Listar Notas
        </a>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Avaliações</h5>
                    <p class="card-text display-6">{{ total_avaliacoes }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Média Geral</h5>
                    <p class="card-text display-6">{{ media_geral|floatformat:1 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-info text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Aprovações</h5>
                    <p class="card-text display-6">{{ percentual_aprovacao }}%</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Distribuição de Notas</h5>
                </div>
                <div class="card-body">
                    <canvas id="distribuicaoNotas" height="250"></canvas>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Média por Curso</h5>
                </div>
                <div class="card-body">
                    <canvas id="mediaPorCurso" height="250"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Melhores Alunos</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Média Geral</th>
                            <th>Cursos</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in melhores_alunos %}
                            <tr>
                                <td>{{ aluno.nome }}</td>
                                <td>
                                    <span class="badge bg-success">{{ aluno.media|floatformat:1 }}</span>
                                </td>
                                <td>{{ aluno.cursos|join:", " }}</td>
                                <td>
                                    <a href="{% url 'notas:relatorio_notas_aluno' aluno.cpf %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-chart-line"></i> Relatório
                                    </a>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de distribuição de notas
        const ctxDistribuicao = document.getElementById('distribuicaoNotas').getContext('2d');
        new Chart(ctxDistribuicao, {
            type: 'bar',
            data: {
                labels: ['0-2', '2-4', '4-6', '6-8', '8-10'],
                datasets: [{
                    label: 'Quantidade de Notas',
                    data: [
                        {{ faixas_notas.0 }},
                        {{ faixas_notas.1 }},
                        {{ faixas_notas.2 }},
                        {{ faixas_notas.3 }},
                        {{ faixas_notas.4 }}
                    ],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(255, 159, 64, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(54, 162, 235, 0.6)'
                    ],
                    borderColor: [
                        'rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)'
                    ],
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
        
        // Gráfico de média por curso
        const ctxMedia = document.getElementById('mediaPorCurso').getContext('2d');
        new Chart(ctxMedia, {
            type: 'bar',
            data: {
                labels: [{% for curso in cursos_medias %}'{{ curso.nome }}',{% endfor %}],
                datasets: [{
                    label: 'Média',
                    data: [{% for curso in cursos_medias %}{{ curso.media }},{% endfor %}],
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: notas\templates\notas\dashboard_notas.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Notas{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Notas</h1>
        <a href="{% url 'notas:listar_notas' %}" class="btn btn-secondary">
            <i class="fas fa-list"></i> Listar Notas
        </a>
    </div>
    
    <!-- Resumo estatístico -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Notas</h5>
                    <p class="card-text display-6">{{ total_notas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Média Geral</h5>
                    <p class="card-text display-6">{{ media_geral|floatformat:1 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Notas por curso -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Médias por Curso</h5>
        </div>
        <div class="card-body">
            {% if notas_por_curso %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Curso</th>
                                <th>Média</th>
                                <th>Total de Notas</th>
                                <th>Desempenho</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for curso in notas_por_curso %}
                                <tr>
                                    <td>{{ curso.curso }}</td>
                                    <td>{{ curso.media|floatformat:1 }}</td>
                                    <td>{{ curso.total }}</td>
                                    <td>
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar {% if curso.media >= 7 %}bg-success{% elif curso.media >= 5 %}bg-warning{% else %}bg-danger{% endif %}" 
                                                 role="progressbar" 
                                                 style="width: {{ curso.media|floatformat:0 }}0%;" 
                                                 aria-valuenow="{{ curso.media|floatformat:0 }}" 
                                                 aria-valuemin="0" 
                                                 aria-valuemax="10">
                                                {{ curso.media|floatformat:1 }}
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhuma nota encontrada.
                </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Melhores alunos -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Melhores Alunos</h5>
        </div>
        <div class="card-body">
            {% if melhores_alunos %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Média</th>
                                <th>Total de Notas</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in melhores_alunos %}
                                <tr>
                                    <td>{{ item.aluno.nome }}</td>
                                    <td>
                                        <span class="badge {% if item.media >= 7 %}bg-success{% elif item.media >= 5 %}bg-warning{% else %}bg-danger{% endif %}">
                                            {{ item.media|floatformat:1 }}
                                        </span>
                                    </td>
                                    <td>{{ item.total_notas }}</td>
                                    <td>
                                        <a href="{% url 'notas:listar_notas' %}?aluno={{ item.aluno.cpf }}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i> Ver Notas
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhum aluno com notas encontrado.
                </div>
            {% endif %}
        </div>
    </div>
    
    <div class="mt-4">
        <a href="javascript:history.back()" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
</div>
{% endblock %}                            {% for item in melhores_alunos %}



### Arquivo: notas\templates\notas\detalhar_nota.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Nota{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes da Nota</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'notas:editar_nota' nota.id %}" class="btn btn-warning me-2">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'notas:excluir_nota' nota.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações da Nota</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> 
                        <a href="{% url 'alunos:detalhar_aluno' nota.aluno.cpf %}">
                            {{ nota.aluno.nome }}
                        </a>
                    </p>
                    <p><strong>Curso:</strong> {{ nota.curso.nome }}</p>
                    <p><strong>Turma:</strong> {{ nota.turma.nome }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Tipo de Avaliação:</strong> {{ nota.get_tipo_avaliacao_display }}</p>
                    <p><strong>Nota:</strong> 
                        <span class="badge {% if nota.valor >= 7 %}bg-success{% elif nota.valor >= 5 %}bg-warning text-dark{% else %}bg-danger{% endif %}">
                            {{ nota.valor|floatformat:1 }}
                        </span>
                    </p>
                    <p><strong>Peso:</strong> {{ nota.peso|floatformat:1 }}</p>
                    <p><strong>Data:</strong> {{ nota.data|date:"d/m/Y" }}</p>
                </div>
            </div>
            
            {% if nota.observacoes %}
                <hr>
                <div class="row">
                    <div class="col-12">
                        <h6>Observações:</h6>
                        <div class="p-3 bg-light rounded">
                            {{ nota.observacoes|linebreaks }}
                        </div>
                    </div>
                </div>
            {% endif %}
        </div>
        <div class="card-footer text-muted">
            <small>Registrada em: {{ nota.created_at|date:"d/m/Y H:i" }} | Última atualização: {{ nota.updated_at|date:"d/m/Y H:i" }}</small>
        </div>
    </div>
    
    <div class="d-flex justify-content-between mb-5">
        <a href="{% url 'notas:listar_notas' %}" class="btn btn-secondary">
            <i class="fas fa-list"></i> Voltar para a lista
        </a>
        <div>
            <a href="{% url 'notas:editar_nota' nota.id %}" class="btn btn-warning me-2">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'notas:excluir_nota' nota.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
        </div>
    </div>
</div>
{% endblock %}{% endblock %}



### Arquivo: notas\templates\notas\excluir_nota.html

html
{% extends 'base.html' %}

{% block title %}Excluir Nota{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card border-danger">
        <div class="card-header bg-danger text-white">
            <h4 class="mb-0">Confirmar Exclusão</h4>
        </div>
        <div class="card-body">
            <h5 class="card-title">Você tem certeza que deseja excluir esta nota?</h5>
            
            <div class="alert alert-warning">
                <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
            </div>
            
            <div class="card mb-4">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Detalhes da Nota</h5>
                </div>
                <div class="card-body">
                    <p><strong>Aluno:</strong> {{ nota.aluno.nome }}</p>
                    <p><strong>Curso:</strong> {{ nota.curso.nome }}</p>
                    <p><strong>Turma:</strong> {{ nota.turma.nome }}</p>
                    <p><strong>Tipo de Avaliação:</strong> {{ nota.get_tipo_avaliacao_display }}</p>
                    <p><strong>Nota:</strong> {{ nota.valor|floatformat:1 }}</p>
                    <p><strong>Data:</strong> {{ nota.data|date:"d/m/Y" }}</p>
                </div>
            </div>
            
            <form method="post">
                {% csrf_token %}
                <div class="d-flex justify-content-between">
                    <a href="{% url 'notas:detalhar_nota' nota.id %}" class="btn btn-secondary">
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
{% endblock %}{% endblock %}{% endblock %}        <div



### Arquivo: notas\templates\notas\formulario_nota.html

html
{% extends 'base.html' %}

{% block title %}{% if nota %}Editar{% else %}Nova{% endif %} Nota{% endblock %}

{% block extra_css %}
<style>
    .required-field label:after {
        content: " *";
        color: red;
    }
</style>
{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if nota %}Editar{% else %}Nova{% endif %} Nota</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Formulário de Nota</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.aluno.id_for_label }}" class="form-label">{{ form.aluno.label }}</label>
                            {{ form.aluno }}
                            {% if form.aluno.help_text %}
                                <div class="form-text">{{ form.aluno.help_text }}</div>
                            {% endif %}
                            {% if form.aluno.errors %}
                                <div class="alert alert-danger mt-1">
                                    {{ form.aluno.errors }}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.curso.id_for_label }}" class="form-label">{{ form.curso.label }}</label>
                            {{ form.curso }}
                            {% if form.curso.help_text %}
                                <div class="form-text">{{ form.curso.help_text }}</div>
                            {% endif %}
                            {% if form.curso.errors %}
                                <div class="alert alert-danger mt-1">
                                    {{ form.curso.errors }}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.turma.id_for_label }}" class="form-label">{{ form.turma.label }}</label>
                            {{ form.turma }}
                            {% if form.turma.help_text %}
                                <div class="form-text">{{ form.turma.help_text }}</div>
                            {% endif %}
                            {% if form.turma.errors %}
                                <div class="alert alert-danger mt-1">
                                    {{ form.turma.errors }}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.tipo_avaliacao.id_for_label }}" class="form-label">{{ form.tipo_avaliacao.label }}</label>
                            {{ form.tipo_avaliacao }}
                            {% if form.tipo_avaliacao.help_text %}
                                <div class="form-text">{{ form.tipo_avaliacao.help_text }}</div>
                            {% endif %}
                            {% if form.tipo_avaliacao.errors %}
                                <div class="alert alert-danger mt-1">
                                    {{ form.tipo_avaliacao.errors }}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="{{ form.valor.id_for_label }}" class="form-label">{{ form.valor.label }}</label>
                            {{ form.valor }}
                            {% if form.valor.help_text %}
                                <div class="form-text">{{ form.valor.help_text }}</div>
                            {% endif %}
                            {% if form.valor.errors %}
                                <div class="alert alert-danger mt-1">
                                    {{ form.valor.errors }}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="{{ form.peso.id_for_label }}" class="form-label">{{ form.peso.label }}</label>
                            {{ form.peso }}
                            {% if form.peso.help_text %}
                                <div class="form-text">{{ form.peso.help_text }}</div>
                            {% endif %}
                            {% if form.peso.errors %}
                                <div class="alert alert-danger mt-1">
                                    {{ form.peso.errors }}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="{{ form.data.id_for_label }}" class="form-label">{{ form.data.label }}</label>
                            {{ form.data }}
                            {% if form.data.help_text %}
                                <div class="form-text">{{ form.data.help_text }}</div>
                            {% endif %}
                            {% if form.data.errors %}
                                <div class="alert alert-danger mt-1">
                                    {{ form.data.errors }}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.observacoes.id_for_label }}" class="form-label">{{ form.observacoes.label }}</label>
                    {{ form.observacoes }}
                    {% if form.observacoes.help_text %}
                        <div class="form-text">{{ form.observacoes.help_text }}</div>
                    {% endif %}
                    {% if form.observacoes.errors %}
                        <div class="alert alert-danger mt-1">
                            {{ form.observacoes.errors }}
                        </div>
                    {% endif %}
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="javascript:history.back()" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Salvar
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const alunoSelect = document.getElementById('id_aluno');
        const cursoSelect = document.getElementById('id_curso');
        const turmaSelect = document.getElementById('id_turma');
        
        // Atualizar turmas quando o curso for alterado
        if (cursoSelect && turmaSelect) {
            cursoSelect.addEventListener('change', function() {
                const cursoId = this.value;
                
                // Limpar o select de turmas
                turmaSelect.innerHTML = '<option value="">---------</option>';
                
                if (cursoId) {
                    // Fazer uma requisição AJAX para obter as turmas do curso
                    fetch(`/api/cursos/${cursoId}/turmas/`)
                        .then(response => response.json())
                        .then(data => {
                            data.forEach(turma => {
                                const option = document.createElement('option');
                                option.value = turma.id;
                                option.textContent = turma.nome;
                                turmaSelect.appendChild(option);
                            });
                        })
                        .catch(error => {
                            console.error('Erro ao carregar turmas:', error);
                        });
                }
            });
        }
        
        // Verificar se o aluno está matriculado na turma selecionada
        if (alunoSelect && turmaSelect) {
            function verificarMatricula() {
                const alunoCpf = alunoSelect.value;
                const turmaId = turmaSelect.value;
                
                if (alunoCpf && turmaId) {
                    // Fazer uma requisição AJAX para verificar se o aluno está matriculado na turma
                    fetch(`/api/alunos/${alunoCpf}/matriculado/${turmaId}/`)
                        .then(response => response.json())
                        .then(data => {
                            if (!data.matriculado) {
                                // Mostrar alerta se o aluno não estiver matriculado
                                const alertDiv = document.createElement('div');
                                alertDiv.className = 'alert alert-warning mt-3';
                                alertDiv.id = 'alerta-matricula';
                                alertDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Atenção: Este aluno não está matriculado nesta turma.';
                                
                                // Remover alerta existente, se houver
                                const alertaExistente = document.getElementById('alerta-matricula');
                                if (alertaExistente) {
                                    alertaExistente.remove();
                                }
                                
                                // Adicionar o alerta após o select de turma
                                turmaSelect.parentElement.appendChild(alertDiv);
                            } else {
                                // Remover alerta se o aluno estiver matriculado
                                const alertaExistente = document.getElementById('alerta-matricula');
                                if (alertaExistente) {
                                    alertaExistente.remove();
                                }
                            }
                        })
                        .catch(error => {
                            console.error('Erro ao verificar matrícula:', error);
                        });
                }
            }
            
            // Verificar quando o aluno ou a turma mudar
            alunoSelect.addEventListener('change', verificarMatricula);
            turmaSelect.addEventListener('change', verificarMatricula);
            
            // Verificar na inicialização, se ambos já estiverem selecionados
            if (alunoSelect.value && turmaSelect.value) {
                verificarMatricula();
            }
        }
    });
</script>
{% endblock %}



### Arquivo: notas\templates\notas\listar_notas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Notas{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Lista de Notas</h1>
        <div>
            <a href="{% url 'notas:criar_nota' %}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Nova Nota
            </a>
            <a href="{% url 'notas:exportar_notas_csv' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-success">
                <i class="fas fa-file-csv"></i> Exportar CSV
            </a>
            <a href="{% url 'notas:exportar_notas_excel' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-info">
                <i class="fas fa-file-excel"></i> Exportar Excel
            </a>
            <a href="{% url 'notas:dashboard_notas' %}" class="btn btn-secondary">
                <i class="fas fa-chart-bar"></i> Dashboard
            </a>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="aluno" class="form-label">Aluno</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos os alunos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.cpf }}" {% if filtros.aluno == aluno.cpf %}selected{% endif %}>
                                {{ aluno.nome }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="curso" class="form-label">Curso</label>
                    <select name="curso" id="curso" class="form-select">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                            <option value="{{ curso.id }}" {% if filtros.curso == curso.id|stringformat:"s" %}selected{% endif %}>
                                {{ curso.nome }}
                            </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="periodo" class="form-label">Período</label>
                    <select name="periodo" id="periodo" class="form-select">
                        <option value="">Todo o período</option>
                        <option value="atual" {% if filtros.periodo == 'atual' %}selected{% endif %}>Mês atual</option>
                        <option value="ultimo_mes" {% if filtros.periodo == 'ultimo_mes' %}selected{% endif %}>Último mês</option>
                        <option value="ultimo_trimestre" {% if filtros.periodo == 'ultimo_trimestre' %}selected{% endif %}>Último trimestre</option>
                        <option value="ultimo_semestre" {% if filtros.periodo == 'ultimo_semestre' %}selected{% endif %}>Último semestre</option>
                    </select>
                </div>
                <div class="col-12 text-end">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'notas:listar_notas' %}" class="btn btn-secondary">
                        <i class="fas fa-broom"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Resumo estatístico -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Notas</h5>
                    <p class="card-text display-6">{{ estatisticas.total_notas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Média Geral</h5>
                    <p class="card-text display-6">{{ estatisticas.media_geral|floatformat:1 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-info text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Nota Máxima</h5>
                    <p class="card-text display-6">{{ estatisticas.nota_maxima|floatformat:1 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body text-center">
                    <h5 class="card-title">Nota Mínima</h5>
                    <p class="card-text display-6">{{ estatisticas.nota_minima|floatformat:1 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de notas -->
    <div class="card">
        <div class="card-header bg-light">
            <h5 class="mb-0">Notas</h5>
        </div>
        <div class="card-body">
            {% if notas %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Curso</th>
                                <th>Nota</th>
                                <th>Data</th>
                                <th>Tipo</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for nota in notas %}
                                <tr>
                                    <td>{{ nota.aluno.nome }}</td>
                                    <td>{{ nota.curso.nome }}</td>
                                    <td>
                                        <span class="badge {% if nota.valor >= 7 %}bg-success{% elif nota.valor >= 5 %}bg-warning{% else %}bg-danger{% endif %}">
                                            {{ nota.valor|floatformat:1 }}
                                        </span>
                                    </td>
                                    <td>{{ nota.data|date:"d/m/Y" }}</td>
                                    <td>{{ nota.get_tipo_avaliacao_display }}</td>
                                    <td>
                                        <a href="{% url 'notas:detalhar_nota' nota.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'notas:editar_nota' nota.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                        <a href="{% url 'notas:excluir_nota' nota.id %}" class="btn btn-sm btn-danger">
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
                    <i class="fas fa-info-circle"></i> Nenhuma nota encontrada.
                </div>
            {% endif %}
        </div>
    </div>
    
    <div class="mt-4">
        <a href="javascript:history.back()" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
</div>
{% endblock %}



### Arquivo: notas\templates\notas\pdf\notas_pdf.html

html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Relatório de Notas</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            font-size: 12px;
        }
        h1, h2 {
            text-align: center;
            color: #333;
        }
        .header {
            margin-bottom: 20px;
            text-align: center;
        }
        .info {
            margin-bottom: 20px;
            border: 1px solid #ddd;
            padding: 10px;
            background-color: #f9f9f9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 10px;
            color: #666;
        }
        .aluno-section {
            margin-bottom: 30px;
            page-break-inside: avoid;
        }
        .nota-alta {
            color: green;
            font-weight: bold;
        }
        .nota-media {
            color: orange;
            font-weight: bold;
        }
        .nota-baixa {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Notas</h1>
        <p>Data de geração: {{ data_geracao|date:"d/m/Y H:i" }}</p>
    </div>
    
    <div class="info">
        <h3>Filtros Aplicados</h3>
        <p>Aluno: {{ filtros.aluno|default:"Todos" }}</p>
        <p>Curso: {{ filtros.curso|default:"Todos" }}</p>
    </div>
    
    {% for aluno_media in alunos_medias %}
        <div class="aluno-section">
            <h2>{{ aluno_media.aluno.nome }}</h2>
            <p><strong>CPF:</strong> {{ aluno_media.aluno.cpf }}</p>
            <p><strong>Média Geral:</strong> 
                <span class="{% if aluno_media.media >= 7 %}nota-alta{% elif aluno_media.media >= 5 %}nota-media{% else %}nota-baixa{% endif %}">
                    {{ aluno_media.media|floatformat:1 }}
                </span>
            </p>
            
            <table>
                <thead>
                    <tr>
                        <th>Curso</th>
                        <th>Tipo de Avaliação</th>
                        <th>Nota</th>
                        <th>Data</th>
                    </tr>
                </thead>
                <tbody>
                    {% for nota in aluno_media.notas %}
                        <tr>
                            <td>{{ nota.curso.nome }}</td>
                            <td>{{ nota.get_tipo_avaliacao_display }}</td>
                            <td class="{% if nota.valor >= 7 %}nota-alta{% elif nota.valor >= 5 %}nota-media{% else %}nota-baixa{% endif %}">
                                {{ nota.valor|floatformat:1 }}
                            </td>
                            <td>{{ nota.data|date:"d/m/Y" }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% endfor %}
    
    <div class="footer">
        <p>Relatório gerado pelo sistema OMAUM</p>
    </div>
</body>
</html>



### Arquivo: notas\templates\notas\relatorio_notas_aluno.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Notas - {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório de Notas - {{ aluno.nome }}</h1>
        <div>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary me-2">
                <i class="fas fa-user"></i> Perfil do Aluno
            </a>
            <a href="{% url 'notas:criar_nota' %}?aluno={{ aluno.cpf }}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Nova Nota
            </a>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Resumo Acadêmico</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card bg-primary text-white">
                        <div class="card-body text-center">
                            <h5 class="card-title">Média Geral</h5>
                            <p class="card-text display-6">{{ media_geral|floatformat:1 }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-success text-white">
                        <div class="card-body text-center">
                            <h5 class="card-title">Aprovações</h5>
                            <p class="card-text display-6">{{ total_aprovacoes }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card bg-danger text-white">
                        <div class="card-body text-center">
                            <h5 class="card-title">Reprovações</h5>
                            <p class="card-text display-6">{{ total_reprovacoes }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    {% if cursos_com_notas %}
        {% for curso in cursos_com_notas %}
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">{{ curso.nome }}</h5>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-4">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Média do Curso</h5>
                                    <p class="card-text display-6 
                                        {% if curso.media >= 7 %}text-success
                                        {% elif curso.media >= 5 %}text-warning
                                        {% else %}text-danger{% endif %}">
                                        {{ curso.media|floatformat:1 }}
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Situação</h5>
                                    <p class="card-text display-6">
                                        {% if curso.media >= 7 %}
                                            <span class="badge bg-success">Aprovado</span>
                                        {% elif curso.media >= 5 %}
                                            <span class="badge bg-warning text-dark">Recuperação</span>
                                        {% else %}
                                            <span class="badge bg-danger">Reprovado</span>
                                        {% endif %}
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Total de Avaliações</h5>
                                    <p class="card-text display-6">{{ curso.notas|length }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Turma</th>
                                    <th>Tipo</th>
                                    <th>Nota</th>
                                    <th>Peso</th>
                                    <th>Data</th>
                                    <th>Ações</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for nota in curso.notas %}
                                    <tr>
                                        <td>{{ nota.turma.nome }}</td>
                                        <td>{{ nota.get_tipo_avaliacao_display }}</td>
                                        <td>
                                            <span class="badge {% if nota.valor >= 7 %}bg-success{% elif nota.valor >= 5 %}bg-warning text-dark{% else %}bg-danger{% endif %}">
                                                {{ nota.valor|floatformat:1 }}
                                            </span>
                                        </td>
                                        <td>{{ nota.peso|floatformat:1 }}</td>
                                        <td>{{ nota.data|date:"d/m/Y" }}</td>
                                        <td>
                                            <a href="{% url 'notas:detalhar_nota' nota.id %}" class="btn btn-sm btn-info">
                                                <i class="fas fa-eye"></i>
                                            </a>
                                            <a href="{% url 'notas:editar_nota' nota.id %}" class="btn btn-sm btn-warning">
                                                <i class="fas fa-edit"></i>
                                            </a>
                                        </td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    
                    {% if curso.grafico_data %}
                        <div class="mt-4">
                            <h6>Evolução das Notas</h6>
                            <canvas id="grafico-{{ curso.id }}" height="200"></canvas>
                        </div>
                    {% endif %}
                </div>
            </div>
        {% endfor %}
    {% else %}
        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i> Este aluno não possui notas registradas.
        </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        {% for curso in cursos_com_notas %}
            {% if curso.grafico_data %}
                const ctx{{ curso.id }} = document.getElementById('grafico-{{ curso.id }}').getContext('2d');
                new Chart(ctx{{ curso.id }}, {
                    type: 'line',
                    data: {
                        labels: [{% for item in curso.grafico_data %}'{{ item.data|date:"d/m/Y" }}',{% endfor %}],
                        datasets: [{
                            label: 'Notas',
                            data: [{% for item in curso.grafico_data %}{{ item.valor }},{% endfor %}],
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            tension: 0.1,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 10,
                                ticks: {
                                    stepSize: 1
                                }
                            }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return `Nota: ${context.raw}`;
                                    }
                                }
                            }
                        }
                    }
                });
            {% endif %}
        {% endfor %}
    });
</script>
{% endblock %}

