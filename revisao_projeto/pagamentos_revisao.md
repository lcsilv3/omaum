# Revisão da Funcionalidade: pagamentos

## Arquivos forms.py:


### Arquivo: pagamentos\forms.py

python
from django import forms
from .models import Pagamento
from alunos.models import Aluno

class PagamentoForm(forms.ModelForm):
    """
    Formulário para criação e edição de pagamentos.
    """
    
    class Meta:
        model = Pagamento
        fields = ['aluno', 'valor', 'data_pagamento', 'status']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'data_pagamento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'aluno': 'Aluno',
            'valor': 'Valor (R$)',
            'data_pagamento': 'Data do Pagamento',
            'status': 'Status'
        }
        help_texts = {
            'valor': 'Valor em reais',
            'data_pagamento': 'Data em que o pagamento foi realizado ou está previsto',
            'status': 'Situação atual do pagamento'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas alunos ativos
        self.fields['aluno'].queryset = Aluno.objects.filter(situacao='ATIVO')
        
        # Adicionar classes CSS para estilização
        for field_name, field in self.fields.items():
            if field_name not in ['aluno', 'status']:
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_valor(self):
        """Validação personalizada para o campo valor."""
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise forms.ValidationError("O valor do pagamento deve ser maior que zero.")
        return valor
        return cleaned_data


## Arquivos views.py:


### Arquivo: pagamentos\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count
from .models import Pagamento
from alunos.models import Aluno
import csv
import datetime

@login_required
def listar_pagamentos(request):
    """Lista todos os pagamentos cadastrados."""
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    status = request.GET.get('status', '')
    periodo = request.GET.get('periodo', '')
    
    # Iniciar queryset
    pagamentos = Pagamento.objects.all().select_related('aluno')
    
    # Aplicar filtros
    if aluno_id:
        pagamentos = pagamentos.filter(aluno__cpf=aluno_id)
    
    if status:
        pagamentos = pagamentos.filter(status=status)
    
    if periodo:
        hoje = datetime.datetime.now().date()
        
        if periodo == 'atual':
            # Mês atual
            pagamentos = pagamentos.filter(data_pagamento__month=hoje.month, data_pagamento__year=hoje.year)
        elif periodo == 'ultimo_mes':
            # Último mês
            um_mes_atras = hoje - datetime.timedelta(days=30)
            pagamentos = pagamentos.filter(data_pagamento__gte=um_mes_atras)
        elif periodo == 'ultimo_trimestre':
            # Último trimestre
            tres_meses_atras = hoje - datetime.timedelta(days=90)
            pagamentos = pagamentos.filter(data_pagamento__gte=tres_meses_atras)
        elif periodo == 'ultimo_semestre':
            # Último semestre
            seis_meses_atras = hoje - datetime.timedelta(days=180)
            pagamentos = pagamentos.filter(data_pagamento__gte=seis_meses_atras)
    
    # Calcular estatísticas
    estatisticas = {
        'total_pagamentos': pagamentos.count(),
        'valor_total': pagamentos.aggregate(Sum('valor'))['valor__sum'] or 0,
        'pagamentos_pendentes': pagamentos.filter(status='pendente').count(),
        'valor_pendente': pagamentos.filter(status='pendente').aggregate(Sum('valor'))['valor__sum'] or 0,
    }
    
    # Obter alunos para os filtros
    alunos = Aluno.objects.filter(situacao='ATIVO')
    
    context = {
        'pagamentos': pagamentos,
        'estatisticas': estatisticas,
        'alunos': alunos,
        'filtros': {
            'aluno': aluno_id,
            'status': status,
            'periodo': periodo
        }
    }
    
    return render(request, "pagamentos/listar_pagamentos.html", context)


@login_required
def detalhar_pagamento(request, pagamento_id):
    """Exibe os detalhes de um pagamento."""
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    return render(request, "pagamentos/detalhar_pagamento.html", {"pagamento": pagamento})


@login_required
def criar_pagamento(request):
    """Cria um novo pagamento."""
    if request.method == "POST":
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, "Pagamento cadastrado com sucesso!")
            return redirect("pagamentos:detalhar_pagamento", pagamento_id=pagamento.id)
    else:
        form = PagamentoForm()
    
    return render(request, "pagamentos/formulario_pagamento.html", {"form": form})


@login_required
def editar_pagamento(request, pagamento_id):
    """Edita um pagamento existente."""
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    
    if request.method == "POST":
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, "Pagamento atualizado com sucesso!")
            return redirect("pagamentos:detalhar_pagamento", pagamento_id=pagamento.id)
    else:
        form = PagamentoForm(instance=pagamento)
    
    return render(request, "pagamentos/formulario_pagamento.html", {"form": form, "pagamento": pagamento})


@login_required
def excluir_pagamento(request, pagamento_id):
    """Exclui um pagamento."""
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    
    if request.method == "POST":
        pagamento.delete()
        messages.success(request, "Pagamento excluído com sucesso!")
        return redirect("pagamentos:listar_pagamentos")
    
    return render(request, "pagamentos/excluir_pagamento.html", {"pagamento": pagamento})


def obter_pagamentos_filtrados(request):
    """Obtém os pagamentos com base nos filtros aplicados."""
    aluno_id = request.GET.get('aluno', '')
    status = request.GET.get('status', '')
    periodo = request.GET.get('periodo', '')
    
    pagamentos = Pagamento.objects.all().select_related('aluno')
    
    if aluno_id:
        pagamentos = pagamentos.filter(aluno__cpf=aluno_id)
    
    if status:
        pagamentos = pagamentos.filter(status=status)
    
    if periodo:
        hoje = datetime.datetime.now().date()
        
        if periodo == 'atual':
            # Mês atual
            pagamentos = pagamentos.filter(data_pagamento__month=hoje.month, data_pagamento__year=hoje.year)
        elif periodo == 'ultimo_mes':
            # Último mês
            um_mes_atras = hoje - datetime.timedelta(days=30)
            pagamentos = pagamentos.filter(data_pagamento__gte=um_mes_atras)
        elif periodo == 'ultimo_trimestre':
            # Último trimestre
            tres_meses_atras = hoje - datetime.timedelta(days=90)
            pagamentos = pagamentos.filter(data_pagamento__gte=tres_meses_atras)
        elif periodo == 'ultimo_semestre':
            # Último semestre
            seis_meses_atras = hoje - datetime.timedelta(days=180)
            pagamentos = pagamentos.filter(data_pagamento__gte=seis_meses_atras)
    
    return pagamentos


@login_required
def exportar_pagamentos_csv(request):
    """Exporta os dados dos pagamentos para um arquivo CSV."""
    try:
        # Obter pagamentos com os mesmos filtros da listagem
        pagamentos = obter_pagamentos_filtrados(request)
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="pagamentos.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Aluno",
            "Valor",
            "Data de Pagamento",
            "Status"
        ])
        
        for pagamento in pagamentos:
            writer.writerow([
                pagamento.aluno.nome,
                pagamento.valor,
                pagamento.data_pagamento.strftime("%d/%m/%Y"),
                pagamento.get_status_display()
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar pagamentos: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")


@login_required
def exportar_pagamentos_excel(request):
    """Exporta os dados dos pagamentos para um arquivo Excel."""
    try:
        import xlwt
        
        # Obter pagamentos com os mesmos filtros da listagem
        pagamentos = obter_pagamentos_filtrados(request)
        
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="pagamentos.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Pagamentos')
        
        # Estilos
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        # Cabeçalhos
        colunas = ['Aluno', 'Valor', 'Data de Pagamento', 'Status']
        for col_num, coluna in enumerate(colunas):
            ws.write(0, col_num, coluna, font_style)
        
        # Dados
        font_style = xlwt.XFStyle()
        for row_num, pagamento in enumerate(pagamentos, 1):
            ws.write(row_num, 0, pagamento.aluno.nome, font_style)
            ws.write(row_num, 1, float(pagamento.valor), font_style)
            ws.write(row_num, 2, pagamento.data_pagamento.strftime("%d/%m/%Y"), font_style)
            ws.write(row_num, 3, pagamento.get_status_display(), font_style)
        
        wb.save(response)
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar pagamentos para Excel: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")


@login_required
def dashboard_pagamentos(request):
    """Exibe o dashboard de pagamentos com estatísticas."""
    # Estatísticas gerais
    total_pagamentos = Pagamento.objects.count()
    valor_total = Pagamento.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    
    # Pagamentos por status
    pagamentos_por_status = Pagamento.objects.values('status').annotate(
        total=Count('id'),
        valor_total=Sum('valor')
    )
    
    # Pagamentos por mês (últimos 6 meses)
    hoje = datetime.datetime.now().date()
    seis_meses_atras = hoje - datetime.timedelta(days=180)
    
    pagamentos_por_mes = []
    for i in range(6):
        mes = hoje.month - i
        ano = hoje.year
        if mes <= 0:
            mes += 12
            ano -= 1
        
        pagamentos_mes = Pagamento.objects.filter(
            data_pagamento__month=mes,
            data_pagamento__year=ano
        )
        
        pagamentos_por_mes.append({
            'mes': datetime.date(ano, mes, 1).strftime('%b/%Y'),
            'total': pagamentos_mes.count(),
            'valor_total': pagamentos_mes.aggregate(Sum('valor'))['valor__sum'] or 0
        })
    
    # Pagamentos por aluno (top 5)
    pagamentos_por_aluno = Pagamento.objects.values('aluno__nome').annotate(
        total=Count('id'),
        valor_total=Sum('valor')
    ).order_by('-valor_total')[:5]
    
    context = {
        'total_pagamentos': total_pagamentos,
        'valor_total': valor_total,
        'pagamentos_por_status': pagamentos_por_status,
        'pagamentos_por_mes': pagamentos_por_mes,
        'pagamentos_por_aluno': pagamentos_por_aluno
    }
    
    return render(request, "pagamentos/dashboard_pagamentos.html", context)


## Arquivos urls.py:


### Arquivo: pagamentos\urls.py

python
from django.urls import path
from . import views

app_name = "pagamentos"

urlpatterns = [
    path("", views.listar_pagamentos, name="listar_pagamentos"),
    path("<int:pagamento_id>/", views.detalhar_pagamento, name="detalhar_pagamento"),
    path("criar/", views.criar_pagamento, name="criar_pagamento"),
    path("<int:pagamento_id>/editar/", views.editar_pagamento, name="editar_pagamento"),
    path("<int:pagamento_id>/excluir/", views.excluir_pagamento, name="excluir_pagamento"),
    path("exportar/csv/", views.exportar_pagamentos_csv, name="exportar_pagamentos_csv"),
    path("exportar/excel/", views.exportar_pagamentos_excel, name="exportar_pagamentos_excel"),
    path("dashboard/", views.dashboard_pagamentos, name="dashboard_pagamentos"),
]


## Arquivos models.py:


### Arquivo: pagamentos\models.py

python
from django.db import models
from django.utils import timezone
from alunos.models import Aluno
from matriculas.models import Matricula
from datetime import timedelta


class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODO_PAGAMENTO_CHOICES = [
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('boleto', 'Boleto Bancário'),
        ('dinheiro', 'Dinheiro'),
        ('transferencia', 'Transferência Bancária'),
        ('outro', 'Outro'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='pagamentos')
    matricula = models.ForeignKey(
        Matricula, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='pagamentos'
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    metodo_pagamento = models.CharField(
        max_length=20, 
        choices=METODO_PAGAMENTO_CHOICES, 
        null=True, 
        blank=True
    )
    comprovante = models.FileField(
        upload_to='pagamentos/comprovantes/', 
        null=True, 
        blank=True
    )
    numero_parcela = models.PositiveIntegerField(null=True, blank=True)
    total_parcelas = models.PositiveIntegerField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_vencimento']
    
    def __str__(self):
        return f"Pagamento de {self.aluno} - R$ {self.valor} ({self.get_status_display()})"
    
    @property
    def atrasado(self):
        """Verifica se o pagamento está atrasado."""
        return self.status == 'pendente' and self.data_vencimento < timezone.now().date()
    
    @property
    def dias_atraso(self):
        """Retorna o número de dias em atraso."""
        if not self.atrasado:
            return 0
        return (timezone.now().date() - self.data_vencimento).days
    
    @property
    def descricao_completa(self):
        """Retorna uma descrição completa do pagamento."""
        if self.matricula:
            desc = f"Pagamento de {self.matricula.turma.curso.nome} - {self.matricula.turma.nome}"
            if self.numero_parcela and self.total_parcelas:
                desc += f" ({self.numero_parcela}/{self.total_parcelas})"
            return desc
        return "Pagamento Avulso"
    
    def save(self, *args, **kwargs):
        # Se o status for alterado para 'pago' e não houver data de pagamento, definir como hoje
        if self.status == 'pago' and not self.data_pagamento:
            self.data_pagamento = timezone.now().date()
        
        # Se o status for alterado para 'pendente' ou 'cancelado', limpar a data de pagamento
        if self.status in ['pendente', 'cancelado']:
            self.data_pagamento = None
            self.metodo_pagamento = None
        
        super().save(*args, **kwargs)



## Arquivos de Template:


### Arquivo: pagamentos\templates\pagamentos\dashboard.html

html
{% extends 'base.html' %}

{% block title %}Dashboard Financeiro{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard Financeiro</h1>
        <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
            <i class="fas fa-list"></i> Listar Pagamentos
        </a>
    </div>
    
    <!-- Resumo financeiro -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Recebido</h5>
                    <p class="card-text display-6">R$ {{ total_recebido|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body text-center">
                    <h5 class="card-title">Total a Receber</h5>
                    <p class="card-text display-6">R$ {{ total_a_receber|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Atrasado</h5>
                    <p class="card-text display-6">R$ {{ total_atrasado|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-info text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Pagamentos do Mês</h5>
                    <p class="card-text display-6">R$ {{ pagamentos_mes_atual|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Pagamentos por Mês</h5>
                </div>
                <div class="card-body">
                    <canvas id="pagamentosPorMes" height="250"></canvas>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Pagamentos por Status</h5>
                </div>
                <div class="card-body">
                    <canvas id="pagamentosPorStatus" height="250"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Indicadores de desempenho -->
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Taxa de Inadimplência</h5>
                </div>
                <div class="card-body text-center">
                    <div class="progress mb-3" style="height: 25px;">
                        <div class="progress-bar {% if taxa_inadimplencia > 20 %}bg-danger{% elif taxa_inadimplencia > 10 %}bg-warning{% else %}bg-success{% endif %}" 
                             role="progressbar" 
                             style="width: {{ taxa_inadimplencia }}%;" 
                             aria-valuenow="{{ taxa_inadimplencia }}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                            {{ taxa_inadimplencia|floatformat:1 }}%
                        </div>
                    </div>
                    <p class="text-muted">Percentual de pagamentos atrasados em relação ao total</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Valor Médio de Pagamento</h5>
                </div>
                <div class="card-body text-center">
                    <h2 class="text-primary">R$ {{ valor_medio_pagamento|floatformat:2 }}</h2>
                    <p class="text-muted">Média de todos os pagamentos realizados</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Previsão para o Mês</h5>
                </div>
                <div class="card-body text-center">
                    <h2 class="text-success">R$ {{ previsao_mes|floatformat:2 }}</h2>
                    <p class="text-muted">Valor previsto para recebimento no mês atual</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Alunos com mais pagamentos -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Alunos com Maior Valor Pago</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Total Pago</th>
                            <th>Último Pagamento</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in alunos_maior_valor %}
                            <tr>
                                <td>{{ aluno.nome }}</td>
                                <td>R$ {{ aluno.total_pago|floatformat:2 }}</td>
                                <td>{{ aluno.ultimo_pagamento|date:"d/m/Y" }}</td>
                                <td>
                                    <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-user"></i> Perfil
                                    </a>
                                    <a href="{% url 'pagamentos:listar_pagamentos' %}?aluno={{ aluno.cpf }}" class="btn btn-sm btn-primary">
                                        <i class="fas fa-money-bill"></i> Pagamentos
                                    </a>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Pagamentos atrasados -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Pagamentos Atrasados</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_atrasados %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Dias em Atraso</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for pagamento in pagamentos_atrasados %}
                                <tr>
                                    <td>{{ pagamento.aluno.nome }}</td>
                                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>{{ pagamento.dias_atraso }} dias</td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-sm btn-success">
                                            <i class="fas fa-check"></i> Pagar
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i> Não há pagamentos atrasados.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de pagamentos por mês
        const ctxMes = document.getElementById('pagamentosPorMes').getContext('2d');
        new Chart(ctxMes, {
            type: 'bar',
            data: {
                labels: [{% for item in pagamentos_por_mes %}'{{ item.mes }}',{% endfor %}],
                datasets: [{
                    label: 'Valor Total',
                    data: [{% for item in pagamentos_por_mes %}{{ item.total }},{% endfor %}],
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
        
        // Gráfico de pagamentos por status
        const ctxStatus = document.getElementById('pagamentosPorStatus').getContext('2d');
        new Chart(ctxStatus, {
            type: 'pie',
            data: {
                labels: ['Pago', 'Pendente', 'Cancelado'],
                datasets: [{
                    data: [{{ total_pago }}, {{ total_pendente }}, {{ total_cancelado }}],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(201, 203, 207, 0.6)'
                    ],
                    borderColor: [
                        'rgb(75, 192, 192)',
                        'rgb(255, 205, 86)',
                        'rgb(201, 203, 207)'
                    ],
                    borderWidth: 1
                }]
            }
        });
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\dashboard_pagamentos.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Pagamentos{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Pagamentos</h1>
        <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
            <i class="fas fa-list"></i> Listar Pagamentos
        </a>
    </div>
    
    <!-- Resumo estatístico -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Pagamentos</h5>
                    <p class="card-text display-6">{{ total_pagamentos }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Valor Total</h5>
                    <p class="card-text display-6">R$ {{ valor_total|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Pagamentos por status -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Pagamentos por Status</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_por_status %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Status</th>
                                <th>Quantidade</th>
                                <th>Valor Total</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in pagamentos_por_status %}
                                <tr>
                                    <td>
                                        <span class="badge {% if item.status == 'pago' %}bg-success{% elif item.status == 'pendente' %}bg-warning{% else %}bg-danger{% endif %}">
                                            {% if item.status == 'pago' %}Pago{% elif item.status == 'pendente' %}Pendente{% else %}Cancelado{% endif %}
                                        </span>
                                    </td>
                                    <td>{{ item.total }}</td>
                                    <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                    <td>
                                        <a href="{% url 'pagamentos:listar_pagamentos' %}?status={{ item.status }}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i> Ver Pagamentos
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado.
                </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Pagamentos por mês -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Pagamentos por Mês (Últimos 6 meses)</h5>
        </div>
        <div class="card-body">
            {% if pagamentos_por_mes %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                                            <th>Mês</th>
                                                            <th>Quantidade</th>
                                                            <th>Valor Total</th>
                                                            <th>Média por Pagamento</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {% for item in pagamentos_por_mes %}
                                                            <tr>
                                                                <td>{{ item.mes }}</td>
                                                                <td>{{ item.total }}</td>
                                                                <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                                                <td>
                                                                    {% if item.total > 0 %}
                                                                        R$ {{ item.valor_total|floatformat:2|default:0|divisibleby:item.total }}
                                                                    {% else %}
                                                                        R$ 0,00
                                                                    {% endif %}
                                                                </td>
                                                            </tr>
                                                        {% endfor %}
                                                    </tbody>
                                                </table>
                                            </div>
                                        {% else %}
                                            <div class="alert alert-info">
                                                <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado nos últimos 6 meses.
                                            </div>
                                        {% endif %}
                                    </div>
                                </div>
    
                                <!-- Pagamentos por aluno -->
                                <div class="card mb-4">
                                    <div class="card-header bg-light">
                                        <h5 class="mb-0">Top 5 Alunos por Valor Total</h5>
                                    </div>
                                    <div class="card-body">
                                        {% if pagamentos_por_aluno %}
                                            <div class="table-responsive">
                                                <table class="table table-striped table-hover">
                                                    <thead>
                                                        <tr>
                                                            <th>Aluno</th>
                                                            <th>Quantidade de Pagamentos</th>
                                                            <th>Valor Total</th>
                                                            <th>Ações</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {% for item in pagamentos_por_aluno %}
                                                            <tr>
                                                                <td>{{ item.aluno__nome }}</td>
                                                                <td>{{ item.total }}</td>
                                                                <td>R$ {{ item.valor_total|floatformat:2 }}</td>
                                                                <td>
                                                                    <a href="{% url 'pagamentos:listar_pagamentos' %}?aluno={{ item.aluno__cpf }}" class="btn btn-sm btn-info">
                                                                        <i class="fas fa-eye"></i> Ver Pagamentos
                                                                    </a>
                                                                </td>
                                                            </tr>
                                                        {% endfor %}
                                                    </tbody>
                                                </table>
                                            </div>
                                        {% else %}
                                            <div class="alert alert-info">
                                                <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado.
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
{% endblock %}                                <th



### Arquivo: pagamentos\templates\pagamentos\detalhar_pagamento.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes do Pagamento</h1>
        <div>
            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary me-2">
                <i class="fas fa-list"></i> Voltar para a lista
            </a>
            <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-warning me-2">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'pagamentos:excluir_pagamento' pagamento.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Pagamento</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ pagamento.aluno.nome }}</p>
                    <p><strong>Valor:</strong> R$ {{ pagamento.valor|floatformat:2 }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Data do Pagamento:</strong> {{ pagamento.data_pagamento|date:"d/m/Y" }}</p>
                    <p><strong>Status:</strong> 
                        <span class="badge {% if pagamento.status == 'pago' %}bg-success{% elif pagamento.status == 'pendente' %}bg-warning{% else %}bg-danger{% endif %}">
                            {{ pagamento.get_status_display }}
                        </span>
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mt-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Informações do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>CPF:</strong> {{ pagamento.aluno.cpf }}</p>
                    <p><strong>Email:</strong> {{ pagamento.aluno.email }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Situação:</strong> {{ pagamento.aluno.get_situacao_display }}</p>
                    <p><strong>Número Iniciático:</strong> {{ pagamento.aluno.numero_iniciatico|default:"Não informado" }}</p>
                </div>
            </div>
            <div class="mt-3">
                <a href="{% url 'alunos:detalhar_aluno' pagamento.aluno.cpf %}" class="btn btn-info">
                    <i class="fas fa-user"></i> Ver Detalhes do Aluno
                </a>
            </div>
        </div>
    </div>
    
    <div class="mt-4">
        <a href="javascript:history.back()" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
</div>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\excluir_pagamento.html

html
{% extends 'base.html' %}

{% block title %}Excluir Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card border-danger">
        <div class="card-header bg-danger text-white">
            <h4 class="mb-0">Confirmar Exclusão</h4>
        </div>
        <div class="card-body">
            <p class="lead">Você tem certeza que deseja excluir este pagamento?</p>
            
            <div class="alert alert-warning">
                <p><strong>Aluno:</strong> {{ pagamento.aluno.nome }}</p>
                <p><strong>Valor:</strong> R$ {{ pagamento.valor|floatformat:2 }}</p>
                <p><strong>Data:</strong> {{ pagamento.data_pagamento|date:"d/m/Y" }}</p>
                <p><strong>Status:</strong> {{ pagamento.get_status_display }}</p>
            </div>
            
            <p class="text-danger"><strong>Atenção:</strong> Esta ação não pode ser desfeita!</p>
            
            <form method="post">
                {% csrf_token %}
                <div class="d-flex justify-content-between">
                    <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-secondary">
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
{% endblock %}{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\formulario_pagamento.html

html
{% extends 'base.html' %}

{% block title %}{% if pagamento %}Editar{% else %}Novo{% endif %} Pagamento{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if pagamento %}Editar{% else %}Novo{% endif %} Pagamento</h1>
        <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar para a lista
        </a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="{{ form.aluno.id_for_label }}" class="form-label">{{ form.aluno.label }}</label>
                        {{ form.aluno }}
                        {% if form.aluno.errors %}
                            <div class="alert alert-danger mt-1">
                                {{ form.aluno.errors }}
                            </div>
                        {% endif %}
                        {% if form.aluno.help_text %}
                            <div class="form-text">{{ form.aluno.help_text }}</div>
                        {% endif %}
                    </div>
                    <div class="col-md-6">
                        <label for="{{ form.valor.id_for_label }}" class="form-label">{{ form.valor.label }}</label>
                        {{ form.valor }}
                        {% if form.valor.errors %}
                            <div class="alert alert-danger mt-1">
                                {{ form.valor.errors }}
                            </div>
                        {% endif %}
                        {% if form.valor.help_text %}
                            <div class="form-text">{{ form.valor.help_text }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="{{ form.data_pagamento.id_for_label }}" class="form-label">{{ form.data_pagamento.label }}</label>
                        {{ form.data_pagamento }}
                        {% if form.data_pagamento.errors %}
                            <div class="alert alert-danger mt-1">
                                {{ form.data_pagamento.errors }}
                            </div>
                        {% endif %}
                        {% if form.data_pagamento.help_text %}
                            <div class="form-text">{{ form.data_pagamento.help_text }}</div>
                        {% endif %}
                    </div>
                    <div class="col-md-6">
                        <label for="{{ form.status.id_for_label }}" class="form-label">{{ form.status.label }}</label>
                        {{ form.status }}
                        {% if form.status.errors %}
                            <div class="alert alert-danger mt-1">
                                {{ form.status.errors }}
                            </div>
                        {% endif %}
                        {% if form.status.help_text %}
                            <div class="form-text">{{ form.status.help_text }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> {% if pagamento %}Atualizar{% else %}Cadastrar{% endif %} Pagamento
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\listar_pagamentos.html

html
{% extends 'base.html' %}

{% block title %}Lista de Pagamentos{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Lista de Pagamentos</h1>
        <div>
            <a href="{% url 'pagamentos:criar_pagamento' %}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Novo Pagamento
            </a>
            <a href="{% url 'pagamentos:exportar_pagamentos_csv' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-success">
                <i class="fas fa-file-csv"></i> Exportar CSV
            </a>
            <a href="{% url 'pagamentos:exportar_pagamentos_excel' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-info">
                <i class="fas fa-file-excel"></i> Exportar Excel
            </a>
            <a href="{% url 'pagamentos:dashboard_pagamentos' %}" class="btn btn-secondary">
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
                    <label for="status" class="form-label">Status</label>
                    <select name="status" id="status" class="form-select">
                        <option value="">Todos os status</option>
                        <option value="pendente" {% if filtros.status == 'pendente' %}selected{% endif %}>Pendente</option>
                        <option value="pago" {% if filtros.status == 'pago' %}selected{% endif %}>Pago</option>
                        <option value="cancelado" {% if filtros.status == 'cancelado' %}selected{% endif %}>Cancelado</option>
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
                    <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
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
                    <h5 class="card-title">Total de Pagamentos</h5>
                    <p class="card-text display-6">{{ estatisticas.total_pagamentos }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Valor Total</h5>
                    <p class="card-text display-6">R$ {{ estatisticas.valor_total|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body text-center">
                    <h5 class="card-title">Pagamentos Pendentes</h5>
                    <p class="card-text display-6">{{ estatisticas.pagamentos_pendentes }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Valor Pendente</h5>
                    <p class="card-text display-6">R$ {{ estatisticas.valor_pendente|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de pagamentos -->
    <div class="card">
        <div class="card-header bg-light">
            <h5 class="mb-0">Pagamentos</h5>
        </div>
        <div class="card-body">
            {% if pagamentos %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Valor</th>
                                <th>Data</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for pagamento in pagamentos %}
                                <tr>
                                    <td>{{ pagamento.aluno.nome }}</td>
                                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_pagamento|date:"d/m/Y" }}</td>
                                    <td>
                                        <span class="badge {% if pagamento.status == 'pago' %}bg-success{% elif pagamento.status == 'pendente' %}bg-warning{% else %}bg-danger{% endif %}">
                                            {{ pagamento.get_status_display }}
                                        </span>
                                    </td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                        <a href="{% url 'pagamentos:excluir_pagamento' pagamento.id %}" class="btn btn-sm btn-danger">
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
                    <i class="fas fa-info-circle"></i> Nenhum pagamento encontrado.
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



### Arquivo: pagamentos\templates\pagamentos\pagamentos_aluno.html

html
{% extends 'base.html' %}

{% block title %}Pagamentos de {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Pagamentos de {{ aluno.nome }}</h1>
        <div>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary me-2">
                <i class="fas fa-user"></i> Perfil do Aluno
            </a>
            <a href="{% url 'pagamentos:registrar_pagamento_rapido' aluno.cpf %}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Novo Pagamento
            </a>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Total Pago</h5>
                    <p class="card-text display-6">R$ {{ total_pago|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-warning text-dark">
                <div class="card-body">
                    <h5 class="card-title">Total Pendente</h5>
                    <p class="card-text display-6">R$ {{ total_pendente|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-danger text-white">
                <div class="card-body">
                    <h5 class="card-title">Total em Atraso</h5>
                    <p class="card-text display-6">R$ {{ valor_atrasados|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Lista de Pagamentos</h5>
        </div>
        <div class="card-body">
            {% if pagamentos %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Descrição</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Status</th>
                                <th>Pagamento</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for pagamento in pagamentos %}
                                <tr>
                                    <td>
                                        {% if pagamento.matricula %}
                                            {{ pagamento.matricula.turma.curso.nome }} - {{ pagamento.matricula.turma.nome }}
                                            {% if pagamento.numero_parcela %}
                                                <br><small>Parcela {{ pagamento.numero_parcela }}/{{ pagamento.total_parcelas }}</small>
                                            {% endif %}
                                        {% else %}
                                            Pagamento Avulso
                                        {% endif %}
                                    </td>
                                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>
                                        {% if pagamento.status == 'pago' %}
                                            <span class="badge bg-success">{{ pagamento.get_status_display }}</span>
                                        {% elif pagamento.status == 'pendente' %}
                                            {% if pagamento.atrasado %}
                                                <span class="badge bg-danger">Atrasado ({{ pagamento.dias_atraso }} dias)</span>
                                            {% else %}
                                                <span class="badge bg-warning text-dark">{{ pagamento.get_status_display }}</span>
                                            {% endif %}
                                        {% else %}
                                            <span class="badge bg-secondary">{{ pagamento.get_status_display }}</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if pagamento.data_pagamento %}
                                            {{ pagamento.data_pagamento|date:"d/m/Y" }}
                                            <br><small>{{ pagamento.get_metodo_pagamento_display }}</small>
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'pagamentos:editar_pagamento' pagamento.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                        {% if pagamento.status == 'pendente' %}
                                            <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-success">
                                                <i class="fas fa-check"></i>
                                            </a>
                                        {% endif %}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> Este aluno não possui pagamentos registrados.
                </div>
            {% endif %}
        </div>
        <div class="card-footer">
            <p class="mb-0">Total de pagamentos: {{ total_pagamentos }}</p>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: pagamentos\templates\pagamentos\relatorio_financeiro.html

html
{% extends 'base.html' %}

{% block title %}Relatório Financeiro{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Relatório Financeiro</h1>
        <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <label for="periodo" class="form-label">Período</label>
                    <select name="periodo" id="periodo" class="form-select">
                        <option value="mes" {% if periodo == 'mes' %}selected{% endif %}>Mês Atual</option>
                        <option value="trimestre" {% if periodo == 'trimestre' %}selected{% endif %}>Trimestre Atual</option>
                        <option value="semestre" {% if periodo == 'semestre' %}selected{% endif %}>Semestre Atual</option>
                        <option value="ano" {% if periodo == 'ano' %}selected{% endif %}>Ano Atual</option>
                        <option value="personalizado" {% if periodo == 'personalizado' %}selected{% endif %}>Personalizado</option>
                    </select>
                </div>
                
                <div class="col-md-3 periodo-personalizado" {% if periodo != 'personalizado' %}style="display: none;"{% endif %}>
                    <label for="data_inicio" class="form-label">Data Inicial</label>
                    <input type="date" name="data_inicio" id="data_inicio" class="form-control" value="{{ data_inicio|date:'Y-m-d' }}">
                </div>
                
                <div class="col-md-3 periodo-personalizado" {% if periodo != 'personalizado' %}style="display: none;"{% endif %}>
                    <label for="data_fim" class="form-label">Data Final</label>
                    <input type="date" name="data_fim" id="data_fim" class="form-control" value="{{ data_fim|date:'Y-m-d' }}">
                </div>
                
                <div class="col-12 text-end">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total</h5>
                    <p class="card-text display-6">R$ {{ total_pago|add:total_pendente|add:total_cancelado|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Pago</h5>
                    <p class="card-text display-6">R$ {{ total_pago|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body text-center">
                    <h5 class="card-title">Pendente</h5>
                    <p class="card-text display-6">R$ {{ total_pendente|floatformat:2 }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atrasado</h5>
                    <p class="card-text display-6">R$ {{ valor_atrasados|floatformat:2 }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Pagamentos por Status</h5>
                </div>
                <div class="card-body">
                    <canvas id="statusChart" height="250"></canvas>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Pagamentos por Mês</h5>
                </div>
                <div class="card-body">
                    <canvas id="monthlyChart" height="250"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    {% if pagamentos_atrasados %}
        <div class="card mb-4">
            <div class="card-header bg-danger text-white">
                <h5 class="mb-0">Pagamentos Atrasados</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Aluno</th>
                                <th>Descrição</th>
                                <th>Valor</th>
                                <th>Vencimento</th>
                                <th>Dias em Atraso</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for pagamento in pagamentos_atrasados %}
                                <tr>
                                    <td>
                                        <a href="{% url 'alunos:detalhar_aluno' pagamento.aluno.cpf %}">
                                            {{ pagamento.aluno.nome }}
                                        </a>
                                    </td>
                                    <td>
                                        {% if pagamento.matricula %}
                                            {{ pagamento.matricula.turma.curso.nome }} - {{ pagamento.matricula.turma.nome }}
                                            {% if pagamento.numero_parcela %}
                                                <br><small>Parcela {{ pagamento.numero_parcela }}/{{ pagamento.total_parcelas }}</small>
                                            {% endif %}
                                        {% else %}
                                            Pagamento Avulso
                                        {% endif %}
                                    </td>
                                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                                    <td>
                                        <span class="badge bg-danger">{{ pagamento.dias_atraso }} dias</span>
                                    </td>
                                    <td>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-info">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'pagamentos:detalhar_pagamento' pagamento.id %}" class="btn btn-sm btn-success">
                                            <i class="fas fa-check"></i> Pagar
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Mostrar/ocultar campos de data personalizada
        const periodoSelect = document.getElementById('periodo');
        const camposPersonalizados = document.querySelectorAll('.periodo-personalizado');
        
        periodoSelect.addEventListener('change', function() {
            if (this.value === 'personalizado') {
                camposPersonalizados.forEach(campo => {
                    campo.style.display = 'block';
                });
            } else {
                camposPersonalizados.forEach(campo => {
                    campo.style.display = 'none';
                });
            }
        });
        
        // Gráfico de status
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        const statusChart = new Chart(statusCtx, {
            type: 'pie',
            data: {
                labels: [
                    {% for item in pagamentos_por_status %}
                        '{{ item.status|capfirst }}',
                    {% endfor %}
                ],
                datasets: [{
                    data: [
                        {% for item in pagamentos_por_status %}
                            {{ item.valor_total }},
                        {% endfor %}
                    ],
                    backgroundColor: [
                        '#28a745',  // Verde para pago
                        '#ffc107',  // Amarelo para pendente
                        '#6c757d',  // Cinza para cancelado
                    ],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                return `${label}: R$ ${value.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
        
        // Gráfico mensal
        const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
        const monthlyChart = new Chart(monthlyCtx, {
            type: 'bar',
            data: {
                labels: [
                    {% for item in pagamentos_por_mes %}
                        '{{ item.mes|date:"M/Y" }}',
                    {% endfor %}
                ],
                datasets: [{
                    label: 'Valor Total',
                    data: [
                        {% for item in pagamentos_por_mes %}
                            {{ item.total }},
                        {% endfor %}
                    ],
                    backgroundColor: '#007bff',
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'R$ ' + value.toFixed(2);
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.raw || 0;
                                return `${label}: R$ ${value.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: pagamentos\templates\pdf\pagamentos_pdf.html

html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Relatório de Pagamentos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            font-size: 12px;
        }
        h1 {
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
        .totals {
            margin-top: 20px;
            text-align: right;
        }
        .status-pago {
            color: green;
            font-weight: bold;
        }
        .status-pendente {
            color: orange;
            font-weight: bold;
        }
        .status-cancelado {
            color: gray;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Pagamentos</h1>
        <p>Data de geração: {{ data_geracao|date:"d/m/Y H:i" }}</p>
    </div>
    
    <div class="info">
        <h3>Filtros Aplicados</h3>
        <p>Status: {{ filtros.status|default:"Todos" }}</p>
        <p>Período: {% if filtros.data_inicio or filtros.data_fim %}
            {% if filtros.data_inicio %}De: {{ filtros.data_inicio|date:"d/m/Y" }}{% endif %}
            {% if filtros.data_fim %}Até: {{ filtros.data_fim|date:"d/m/Y" }}{% endif %}
            {% else %}Todos{% endif %}
        </p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Valor</th>
                <th>Vencimento</th>
                <th>Status</th>
                <th>Data Pagamento</th>
            </tr>
        </thead>
        <tbody>
            {% for pagamento in pagamentos %}
                <tr>
                    <td>{{ pagamento.aluno.nome }}</td>
                    <td>R$ {{ pagamento.valor|floatformat:2 }}</td>
                    <td>{{ pagamento.data_vencimento|date:"d/m/Y" }}</td>
                    <td class="status-{{ pagamento.status }}">{{ pagamento.get_status_display }}</td>
                    <td>{{ pagamento.data_pagamento|date:"d/m/Y"|default:"-" }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="totals">
        <p><strong>Total Pago:</strong> R$ {{ total_pago|floatformat:2 }}</p>
        <p><strong>Total Pendente:</strong> R$ {{ total_pendente|floatformat:2 }}</p>
        <p><strong>Total Geral:</strong> R$ {{ total_geral|floatformat:2 }}</p>
    </div>
    
    <div class="footer">
        <p>Relatório gerado pelo sistema OMAUM - Página 1 de 1</p>
    </div>
</body>
</html>

