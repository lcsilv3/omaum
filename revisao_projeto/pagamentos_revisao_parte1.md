'''
# Revisão da Funcionalidade: pagamentos

## Arquivos forms.py:


### Arquivo: pagamentos\forms.py

python
"""
Formulários para o aplicativo de pagamentos.
"""
from django import forms
from django.core.validators import MinValueValidator
from django.utils import timezone
from importlib import import_module

from .models import Pagamento  # <-- Adicione esta linha

def get_aluno_model():
    """Importa o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

class PagamentoForm(forms.ModelForm):
    """Formulário para criação e edição de pagamentos."""
    
    class Meta:
        model = Pagamento
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Aluno = get_aluno_model()
        self.fields['aluno'].queryset = Aluno.objects.filter(situacao='ATIVO')

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        data_pagamento = cleaned_data.get('data_pagamento')
        
        # Se o status for PAGO, a data de pagamento é obrigatória
        if status == 'PAGO' and not data_pagamento:
            self.add_error('data_pagamento', 'A data de pagamento é obrigatória quando o status é Pago.')
        
        # Se o status não for PAGO, a data de pagamento deve ser None
        if status != 'PAGO' and data_pagamento:
            cleaned_data['data_pagamento'] = None
        
        return cleaned_data


class PagamentoRapidoForm(forms.ModelForm):
    """Formulário simplificado para registro rápido de pagamentos."""
    
    aluno_cpf = forms.CharField(
        label="CPF do Aluno",
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF do aluno'})
    )
    
    class Meta:
        from .models import Pagamento
        model = Pagamento
        fields = [
            'valor',
            'data_vencimento',
            'status',
            'metodo_pagamento',
            'observacoes',
        ]
        widgets = {
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir valores padrão
        self.fields['data_vencimento'].initial = timezone.now().date()
        self.fields['status'].initial = 'PENDENTE'
    
    def clean_aluno_cpf(self):
        cpf = self.cleaned_data.get('aluno_cpf')
        if cpf:
            # Remover caracteres não numéricos
            cpf = ''.join(filter(str.isdigit, cpf))
            
            # Verificar se o CPF tem 11 dígitos
            if len(cpf) != 11:
                raise forms.ValidationError("O CPF deve conter 11 dígitos.")
            
            # Verificar se o aluno existe
            Aluno = get_aluno_model()
            try:
                aluno = Aluno.objects.get(cpf=cpf)
                return aluno
            except Aluno.DoesNotExist:
                raise forms.ValidationError("Aluno não encontrado com este CPF.")
        
        return cpf
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.aluno = self.cleaned_data.get('aluno_cpf')
        
        if commit:
            instance.save()
        
        return instance


class FiltroPagamentosForm(forms.Form):
    """
    Formulário para filtrar pagamentos.
    """
    q = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por aluno, CPF ou observações...'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'Todos')] + list(Pagamento.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    data_inicio = forms.DateField(
        required=False,
        label="Data início",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    data_fim = forms.DateField(
        required=False,
        label="Data fim",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


## Arquivos views.py:


### Arquivo: pagamentos\views.py

python
import logging
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse
from .forms import PagamentoForm, FiltroPagamentosForm, PagamentoRapidoForm
from .models import Pagamento
from .exporters import exportar_pagamentos_csv, exportar_pagamentos_excel, exportar_pagamentos_pdf
from pagamentos.helpers import get_aluno_model  # helpers.py deve conter get_aluno_model

from .views.pagamento_views import (
    listar_pagamentos,
    criar_pagamento,
    editar_pagamento,
    excluir_pagamento,
    detalhar_pagamento,
    pagamentos_aluno,
    registrar_pagamento_rapido,
    importar_pagamentos_csv,
    exportar_pagamentos_csv,
    exportar_pagamentos_excel,
    exportar_pagamentos_pdf,
)

from .views.relatorio_views import (
    relatorio_financeiro,
    exportar_pagamentos_excel,
    exportar_pagamentos_pdf,
    dados_grafico_pagamentos,
    pagamentos_por_turma,
    dados_distribuicao_pagamentos,
)

from .views.dashboard_views import (
    dashboard,
    dashboard_pagamentos,
    dashboard_financeiro,
)

def editar_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, id=id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, request.FILES, instance=pagamento)
        if form.is_valid():
            form.save()
            # redirecione conforme sua lógica
        else:
            # Se inválido, o form já vem preenchido com os dados e erros
            pass
    else:
        form = PagamentoForm(instance=pagamento)
    return render(request, 'pagamentos/editar_pagamento.html', {
        'form': form,
        'pagamento': pagamento,
    })


## Arquivos urls.py:


### Arquivo: pagamentos\urls.py

python
from django.urls import path
from .views.pagamento_views import (
    listar_pagamentos, criar_pagamento, editar_pagamento, excluir_pagamento,
    detalhar_pagamento, pagamentos_aluno, registrar_pagamento_rapido,
    importar_pagamentos_csv, exportar_pagamentos_csv, exportar_pagamentos_excel,
    exportar_pagamentos_pdf, turmas_por_curso, buscar_alunos
)
from .views.relatorio_views import (
    relatorio_financeiro, pagamentos_por_turma,
    dados_grafico_pagamentos, dados_distribuicao_pagamentos
)
from .views.dashboard_views import dashboard, dashboard_pagamentos, dashboard_financeiro

app_name = 'pagamentos'

urlpatterns = [
    # Pagamentos
    path('', listar_pagamentos, name='listar_pagamentos'),
    path('novo/', criar_pagamento, name='criar_pagamento'),
    path('<int:pagamento_id>/editar/', editar_pagamento, name='editar_pagamento'),
    path('<int:pagamento_id>/excluir/', excluir_pagamento, name='excluir_pagamento'),
    path('<int:pagamento_id>/', detalhar_pagamento, name='detalhar_pagamento'),

    # Pagamentos por aluno e pagamento rápido
    path('aluno/<str:cpf>/', pagamentos_aluno, name='pagamentos_aluno'),
    path('aluno/<str:cpf>/registrar-rapido/', registrar_pagamento_rapido, name='registrar_pagamento_rapido'),

    # Importação e exportação
    path('importar/', importar_pagamentos_csv, name='importar_pagamentos_csv'),
    path('exportar/csv/', exportar_pagamentos_csv, name='exportar_pagamentos_csv'),
    path('exportar/excel/', exportar_pagamentos_excel, name='exportar_pagamentos_excel'),
    path('exportar/pdf/', exportar_pagamentos_pdf, name='exportar_pagamentos_pdf'),

    # Relatórios
    path('relatorio/', relatorio_financeiro, name='relatorio_financeiro'),
    path('relatorio/turma/', pagamentos_por_turma, name='relatorio_pagamentos_turma'),

    # Dashboards
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/pagamentos/', dashboard_pagamentos, name='dashboard_pagamentos'),
    path('dashboard/financeiro/', dashboard_financeiro, name='dashboard_financeiro'),

    # APIs para gráficos
    path('pagamentos/grafico-pagamentos/', dados_grafico_pagamentos, name='dados_grafico_pagamentos'),
    path('pagamentos/distribuicao-pagamentos/', dados_distribuicao_pagamentos, name='dados_distribuicao_pagamentos'),

    # Turmas por curso
    path('turmas-por-curso/', turmas_por_curso, name='turmas_por_curso'),

    # Buscar alunos (API)
    path('alunos/buscar/', buscar_alunos, name='buscar_alunos'),
]


## Arquivos models.py:


### Arquivo: pagamentos\models.py

python
"""
Modelos para o aplicativo de pagamentos.
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


class Pagamento(models.Model):
    """
    Modelo para armazenar informações de pagamentos dos alunos.
    """
    # Opções para o campo status
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    # Opções para o campo método de pagamento
    METODO_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('TRANSFERENCIA', 'Transferência Bancária'),
        ('BOLETO', 'Boleto'),
        ('OUTRO', 'Outro'),
    ]
    
    # Relacionamentos
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        verbose_name=_('Aluno')
    )
    
    # Campos de pagamento
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Valor')
    )
    
    data_vencimento = models.DateField(
        verbose_name=_('Data de Vencimento')
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name=_('Status')
    )
    
    data_pagamento = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Data de Pagamento')
    )
    
    valor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Valor Pago')
    )
    
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=METODO_PAGAMENTO_CHOICES,
        null=True,
        blank=True,
        verbose_name=_('Método de Pagamento')
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Observações')
    )
    
    # Metadados
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Criado em')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atualizado em')
    )
    
    class Meta:
        verbose_name = _('Pagamento')
        verbose_name_plural = _('Pagamentos')
        ordering = ['-data_vencimento']
    
    def __str__(self):
        return f"Pagamento de {self.aluno.nome} - R$ {self.valor} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        """Sobrescreve o método save para atualizar campos automaticamente."""
        # Se o status for PAGO e não houver data de pagamento, definir como hoje
        if self.status == 'PAGO' and not self.data_pagamento:
            self.data_pagamento = timezone.now().date()
        
        # Se o status for PAGO e não houver valor_pago, usar o valor original
        if self.status == 'PAGO' and not self.valor_pago:
            self.valor_pago = self.valor
        
        # Verificar se o pagamento está atrasado
        hoje = timezone.now().date()
        if self.status == 'PENDENTE' and self.data_vencimento < hoje:
            self.status = 'ATRASADO'
        
        super().save(*args, **kwargs)



## Arquivos de Views Modulares:


### Arquivo: pagamentos\views\__init__.py

python
# Este arquivo será atualizado gradualmente à medida que as views forem refatoradas



### Arquivo: pagamentos\views\base.py

python
"""
Módulo base com funções e classes utilitárias compartilhadas entre as views.
"""
import logging
from importlib import import_module
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


def get_pagamento_model():
    """Obtém o modelo Pagamento dinamicamente."""
    pagamentos_module = import_module("pagamentos.models")
    return getattr(pagamentos_module, "Pagamento")


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_pagamento_or_404(pagamento_id):
    """Obtém um pagamento pelo ID ou retorna 404."""
    Pagamento = get_pagamento_model()
    return get_object_or_404(Pagamento, id=pagamento_id)


# Verificar disponibilidade de bibliotecas para exportação
try:
    import xlsxwriter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

try:
    from weasyprint import HTML
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Decorator composto para views que precisam de autenticação e modelo de pagamento
def pagamento_view(view_func):
    """
    Decorator que combina login_required e fornece o modelo Pagamento.
    Também captura exceções comuns.
    """
    @login_required
    def wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro na view {view_func.__name__}: {str(e)}", exc_info=True)
            from django.contrib import messages
            messages.error(request, f"Erro: {str(e)}")
            from django.shortcuts import redirect
            return redirect('pagamentos:listar_pagamentos')
    
    return wrapped_view



### Arquivo: pagamentos\views\dashboard_views.py

python
"""
Views relacionadas ao dashboard financeiro.
"""
import datetime
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Importação dinâmica para evitar referências circulares
def get_pagamento_model():
    from pagamentos.models import Pagamento
    return Pagamento

def get_aluno_model():
    from alunos.models import Aluno
    return Aluno

@login_required
def dashboard(request):
    """
    Dashboard principal do módulo de pagamentos.
    Exibe estatísticas gerais e links para outras seções.
    """
    Pagamento = get_pagamento_model()
    Aluno = get_aluno_model()
    total_alunos = Aluno.objects.count()
    total_pagamentos = Pagamento.objects.count()
    pagamentos_pagos = Pagamento.objects.filter(status='PAGO').count()
    pagamentos_pendentes = Pagamento.objects.filter(status='PENDENTE').count()
    pagamentos_atrasados = Pagamento.objects.filter(status='ATRASADO').count()
    total_pago = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in Pagamento.objects.filter(status='PAGO')])
    total_pendente = Pagamento.objects.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
    total_atrasado = Pagamento.objects.filter(status='ATRASADO').aggregate(Sum('valor'))['valor__sum'] or 0
    pagamentos_recentes = Pagamento.objects.all().order_by('-data_pagamento')[:5]
    hoje = timezone.now().date()
    data_limite = hoje + datetime.timedelta(days=7)
    pagamentos_proximos = Pagamento.objects.filter(
        status='PENDENTE',
        data_vencimento__gte=hoje,
        data_vencimento__lte=data_limite
    ).order_by('data_vencimento')[:5]
    context = {
        'total_alunos': total_alunos,
        'total_pagamentos': total_pagamentos,
        'pagamentos_pagos': pagamentos_pagos,
        'pagamentos_pendentes': pagamentos_pendentes,
        'pagamentos_atrasados': pagamentos_atrasados,
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'total_atrasado': total_atrasado,
        'pagamentos_recentes': pagamentos_recentes,
        'pagamentos_proximos': pagamentos_proximos,
    }
    return render(request, 'pagamentos/dashboard.html', context)

@login_required
def dashboard_pagamentos(request):
    """
    Dashboard específico para análise de pagamentos.
    Exibe gráficos e estatísticas sobre pagamentos.
    """
    Pagamento = get_pagamento_model()
    hoje = timezone.now().date()
    mes_atual = hoje.replace(day=1)
    if mes_atual.month == 12:
        proximo_mes = mes_atual.replace(year=mes_atual.year + 1, month=1)
    else:
        proximo_mes = mes_atual.replace(month=mes_atual.month + 1)
    pagamentos_mes = Pagamento.objects.filter(
        data_vencimento__gte=mes_atual,
        data_vencimento__lt=proximo_mes
    )
    pagos_mes = pagamentos_mes.filter(status='PAGO').count()
    pendentes_mes = pagamentos_mes.filter(status='PENDENTE').count()
    atrasados_mes = pagamentos_mes.filter(status='ATRASADO').count()
    valor_pago_mes = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in pagamentos_mes.filter(status='PAGO')])
    valor_pendente_mes = pagamentos_mes.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
    valor_atrasado_mes = pagamentos_mes.filter(status='ATRASADO').aggregate(Sum('valor'))['valor__sum'] or 0
    dias = []
    valores_por_dia = []
    for dia in range(1, (proximo_mes - mes_atual).days):
        data = mes_atual + datetime.timedelta(days=dia-1)
        if data > hoje:
            break
        pagamentos_dia = Pagamento.objects.filter(
            data_pagamento=data,
            status='PAGO'
        )
        valor_dia = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in pagamentos_dia])
        dias.append(data.strftime('%d/%m'))
        valores_por_dia.append(float(valor_dia))
    pagamentos_por_metodo = pagamentos_mes.filter(status='PAGO').values('metodo_pagamento').annotate(
        total=Count('id')
    ).order_by('-total')
    metodos = []
    contagens = []
    for item in pagamentos_por_metodo:
        metodo = dict(Pagamento.METODO_PAGAMENTO_CHOICES).get(item['metodo_pagamento'], 'Não informado')
        metodos.append(metodo)
        contagens.append(item['total'])
    hoje = timezone.now().date()
    atrasados_ate_15 = Pagamento.objects.filter(
        status='ATRASADO',
        data_vencimento__gte=hoje - datetime.timedelta(days=15)
    ).count()
    atrasados_15_30 = Pagamento.objects.filter(
        status='ATRASADO',
        data_vencimento__lt=hoje - datetime.timedelta(days=15),
        data_vencimento__gte=hoje - datetime.timedelta(days=30)
    ).count()
    atrasados_mais_30 = Pagamento.objects.filter(
        status='ATRASADO',
        data_vencimento__lt=hoje - datetime.timedelta(days=30)
    ).count()
    context = {
        'pagos_mes': pagos_mes,
        'pendentes_mes': pendentes_mes,
        'atrasados_mes': atrasados_mes,
        'valor_pago_mes': valor_pago_mes,
        'valor_pendente_mes': valor_pendente_mes,
        'valor_atrasado_mes': valor_atrasado_mes,
        'dias': json.dumps(dias),
        'valores_por_dia': json.dumps(valores_por_dia),
        'metodos': json.dumps(metodos),
        'contagens': json.dumps(contagens),
        'atrasados_ate_15': atrasados_ate_15,
        'atrasados_15_30': atrasados_15_30,
        'atrasados_mais_30': atrasados_mais_30,
        'mes_atual': mes_atual.strftime('%B/%Y')
    }
    return render(request, 'pagamentos/dashboard_pagamentos.html', context)

@login_required
def dashboard_financeiro(request):
    """Exibe o dashboard financeiro."""
    Pagamento = get_pagamento_model()
    hoje = timezone.now().date()
    pagamentos_pagos = Pagamento.objects.filter(status='PAGO')
    pagamentos_pendentes = Pagamento.objects.filter(status='PENDENTE')
    pagamentos_atrasados = Pagamento.objects.filter(status='ATRASADO')
    total_pago = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in pagamentos_pagos])
    total_pendente = pagamentos_pendentes.aggregate(Sum('valor'))['valor__sum'] or 0
    total_atrasado = pagamentos_atrasados.aggregate(Sum('valor'))['valor__sum'] or 0
    pagamentos_por_mes = []
    meses = []
    valores_pagos = []
    valores_pendentes = []
    for i in range(5, -1, -1):
        mes_data = hoje.replace(day=1)
        if i > 0:
            ano = mes_data.year
            mes = mes_data.month - i
            if mes <= 0:
                mes = 12 + mes
                ano -= 1
            mes_data = mes_data.replace(year=ano, month=mes)
        if mes_data.month == 12:
            ultimo_dia = mes_data.replace(year=mes_data.year + 1, month=1, day=1) - datetime.timedelta(days=1)
        else:
            ultimo_dia = mes_data.replace(month=mes_data.month + 1, day=1) - datetime.timedelta(days=1)
        pagamentos_mes = Pagamento.objects.filter(
            data_vencimento__gte=mes_data,
            data_vencimento__lte=ultimo_dia
        )
        total_pago_mes = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in pagamentos_mes.filter(status='PAGO')])
        total_pendente_mes = pagamentos_mes.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
        meses.append(mes_data.strftime('%b/%Y'))
        valores_pagos.append(float(total_pago_mes))
        valores_pendentes.append(float(total_pendente_mes))
    pagamentos_por_metodo = pagamentos_pagos.values('metodo_pagamento').annotate(
        total=Count('id')
    ).order_by('-total')
    metodos = []
    contagens = []
    for item in pagamentos_por_metodo:
        metodo = dict(Pagamento.METODO_PAGAMENTO_CHOICES).get(item['metodo_pagamento'], 'Não informado')
        metodos.append(metodo)
        contagens.append(item['total'])
    context = {
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'total_atrasado': total_atrasado,
        'meses': json.dumps(meses),
        'valores_pagos': json.dumps(valores_pagos),
        'valores_pendentes': json.dumps(valores_pendentes),
        'metodos': json.dumps(metodos),
        'contagens': json.dumps(contagens)
    }
    return render(request, 'pagamentos/dashboard_financeiro.html', context)



### Arquivo: pagamentos\views\exportacao.py

python
@login_required
def exportar_atividades(request, formato):
    """Exporta as atividades para um arquivo no formato especificado."""
    AtividadeAcademica, AtividadeRitualistica = get_models()

    # Obter parâmetros de filtro
    tipo = request.GET.get("tipo", "todas")
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    # Filtrar atividades acadêmicas
    atividades_academicas = AtividadeAcademica.objects.all()
    if status:
        atividades_academicas = atividades_academicas.filter(status=status)
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)

    # Filtrar atividades ritualísticas
    atividades_ritualisticas = AtividadeRitualistica.objects.all()
    if data_inicio:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=data_inicio)
    if data_fim:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)

    # Aplicar filtro por tipo
    if tipo == "academicas":
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == "ritualisticas":
        atividades_academicas = AtividadeAcademica.objects.none()

    # Exportar para CSV
    if formato == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="atividades.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Tipo", "Nome", "Descrição", "Data", "Local", "Status", "Turma(s)"
        ])

        # Adicionar atividades acadêmicas
        for atividade in atividades_academicas:
            turmas = ", ".join([t.nome for t in atividade.turmas.all()])
            writer.writerow([
                "Acadêmica",
                atividade.nome,
                atividade.descricao,
                atividade.data_inicio.strftime("%d/%m/%Y"),
                atividade.local,
                atividade.get_status_display(),
                turmas
            ])

        # Adicionar atividades ritualísticas
        for atividade in atividades_ritualisticas:
            writer.writerow([
                "Ritualística",
                atividade.nome,
                atividade.descricao,
                atividade.data.strftime("%d/%m/%Y"),
                atividade.local,
                "N/A",  # Atividades ritualísticas não têm status
                atividade.turma.nome
            ])

        return response

    # Exportar para Excel
    elif formato == "excel":
        try:
            import xlwt

            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = 'attachment; filename="atividades.xls"'

            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Atividades")

            # Estilos
            header_style = xlwt.easyxf("font: bold on; align: wrap on, vert centre, horiz center")
            date_style = xlwt.easyxf("align: wrap on, vert centre, horiz left", num_format_str="DD/MM/YYYY")

            # Cabeçalho
            row_num = 0
            columns = [
                "Tipo", "Nome", "Descrição", "Data", "Local", "Status", "Turma(s)"
            ]

            for col_num, column_title in enumerate(columns):
                ws.write(row_num, col_num, column_title, header_style)

            # Adicionar atividades acadêmicas
            for atividade in atividades_academicas:
                row_num += 1
                turmas = ", ".join([t.nome for t in atividade.turmas.all()])

                ws.write(row_num, 0, "Acadêmica")
                ws.write(row_num, 1, atividade.nome)
                ws.write(row_num, 2, atividade.descricao)
                ws.write(row_num, 3, atividade.data_inicio, date_style)
                ws.write(row_num, 4, atividade.local)
                ws.write(row_num, 5, atividade.get_status_display())
                ws.write(row_num, 6, turmas)

            # Adicionar atividades ritualísticas
            for atividade in atividades_ritualisticas:
                row_num += 1

                ws.write(row_num, 0, "Ritualística")
                ws.write(row_num, 1, atividade.nome)
                ws.write(row_num, 2, atividade.descricao)
                ws.write(row_num, 3, atividade.data, date_style)
                ws.write(row_num, 4, atividade.local)
                ws.write(row_num, 5, "N/A")  # Atividades ritualísticas não têm status
                ws.write(row_num, 6, atividade.turma.nome)

            wb.save(response)
            return response
        except ImportError:
            messages.error(request, "A biblioteca xlwt não está instalada. Instale-a para exportar para Excel.")
            return redirect("atividades:relatorio_atividades")

    # Exportar para PDF
    elif formato == "pdf":
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
            from reportlab.lib.styles import getSampleStyleSheet
            from io import BytesIO

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
            elements = []

            # Estilos
            styles = getSampleStyleSheet()
            title_style = styles["Heading1"]

            # Título
            elements.append(Paragraph("Relatório de Atividades", title_style))

            # Dados da tabela
            data = [["Tipo", "Nome", "Descrição", "Data", "Local", "Status", "Turma(s)"]]

            # Adicionar atividades acadêmicas
            for atividade in atividades_academicas:
                turmas = ", ".join([t.nome for t in atividade.turmas.all()])
                data.append([
                    "Acadêmica",
                    atividade.nome,
                    atividade.descricao,
                    atividade.data_inicio.strftime("%d/%m/%Y"),
                    atividade.local,
                    atividade.get_status_display(),
                    turmas
                ])

            # Adicionar atividades ritualísticas
            for atividade in atividades_ritualisticas:
                data.append([
                    "Ritualística",
                    atividade.nome,
                    atividade.descricao,
                    atividade.data.strftime("%d/%m/%Y"),
                    atividade.local,
                    "N/A",  # Atividades ritualísticas não têm status
                    atividade.turma.nome
                ])

            # Criar tabela
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)

            # Gerar PDF
            doc.build(elements)

            # Retornar resposta
            buffer.seek(0)
            response = HttpResponse(buffer, content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="atividades.pdf"'

            return response
        except ImportError:
            messages.error(request, "As bibliotecas necessárias para gerar PDF não estão instaladas.")
            return redirect("atividades:relatorio_atividades")

    # Formato não suportado
    else:
        messages.error(request, f"Formato de exportação '{formato}' não suportado.")
        return redirect("atividades:relatorio_atividades")



### Arquivo: pagamentos\views\pagamento_views.py

python
"""Views relacionadas às operações básicas de pagamentos (CRUD, exportação e importação)."""

import csv
import datetime
import logging
from io import TextIOWrapper

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_GET

from pagamentos.models import Pagamento  # ajuste o import conforme seu projeto
from ..forms import PagamentoForm, PagamentoRapidoForm
from .base import get_pagamento_model, get_aluno_model
from turmas.models import Turma
from cursos.models import Curso  # ajuste o import conforme seu projeto

logger = logging.getLogger(__name__)


@login_required
def listar_pagamentos(request):
    """Lista todos os pagamentos com filtros e exportação."""
    try:
        Pagamento = get_pagamento_model()

        # Obter parâmetros de filtro
        query = request.GET.get('q', '')
        status = request.GET.get('status', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')
        exportar = request.GET.get('exportar', '')  # 'csv', 'excel', 'pdf'

        # Filtrar pagamentos
        pagamentos = Pagamento.objects.all()

        if query:
            pagamentos = pagamentos.filter(
                Q(aluno__nome__icontains=query) |
                Q(aluno__cpf__icontains=query) |
                Q(observacoes__icontains=query)
            )

        if status:
            pagamentos = pagamentos.filter(status=status)

        if data_inicio:
            pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio)

        if data_fim:
            pagamentos = pagamentos.filter(data_vencimento__lte=data_fim)

        # Totais filtrados
        total_pago = pagamentos.filter(status='PAGO').aggregate(total=Sum('valor'))['total'] or 0
        total_pendente = pagamentos.filter(status='PENDENTE').aggregate(total=Sum('valor'))['total'] or 0
        total_atrasado = pagamentos.filter(status='ATRASADO').aggregate(total=Sum('valor'))['total'] or 0
        total_cancelados = pagamentos.filter(status='CANCELADO').aggregate(total=Sum('valor'))['total'] or 0
        total_geral = pagamentos.aggregate(total=Sum('valor'))['total'] or 0

        # Paginação
        paginator = Paginator(pagamentos, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'pagamentos': page_obj,
            'total_pago': total_pago,
            'total_pendente': total_pendente,
            'total_atrasado': total_atrasado,
            'total_cancelados': total_cancelados,
            'total_geral': total_geral,
            'query': query,
            'status': status,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
        }

        return render(request, 'pagamentos/listar_pagamentos.html', context)

    except Exception as e:
        logger.error(f"Erro ao listar pagamentos: {str(e)}")
        messages.error(request, f"Erro ao listar pagamentos: {str(e)}")
        return render(request, 'pagamentos/listar_pagamentos.html', {'pagamentos': []})


@login_required
def criar_pagamento(request):
    """Cria um novo pagamento."""
    PagamentoModel = get_pagamento_model()
    Aluno = get_aluno_model()
    from cursos.models import Curso

    cursos = Curso.objects.all().order_by('nome')

    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        # Defina o queryset de alunos mesmo em POST
        form.fields['aluno'].queryset = Aluno.objects.all()
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, "Pagamento criado com sucesso!")
            return redirect('pagamentos:detalhar_pagamento', pagamento_id=pagamento.id)
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = PagamentoForm()
        form.fields['aluno'].queryset = Aluno.objects.all()

    return render(
        request,
        'pagamentos/criar_pagamento.html',
        {'form': form, 'cursos': cursos}
    )


@login_required
def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    try:
        if request.method == 'POST':
            form = PagamentoForm(request.POST, request.FILES, instance=pagamento)
            if form.is_valid():
                form.save()
                messages.success(request, "Pagamento atualizado com sucesso!")
                return redirect('pagamentos:detalhar_pagamento', pagamento_id=pagamento.id)
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = PagamentoForm(instance=pagamento)
        return render(
            request,
            'pagamentos/editar_pagamento.html',
            {'form': form, 'pagamento': pagamento}
        )
    except Exception as e:
        logger.error("Erro ao editar pagamento: %s", str(e))
        messages.error(request, f"Erro ao editar pagamento: {str(e)}")
        return redirect('pagamentos:listar_pagamentos')


@login_required
def excluir_pagamento(request, pagamento_id):
    """Exclui um pagamento."""
    Pagamento = get_pagamento_model()
    try:
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        if request.method == 'POST':
            pagamento.delete()
            messages.success(request, "Pagamento excluído com sucesso!")
            return redirect('pagamentos:listar_pagamentos')
        return render(request, 'pagamentos/excluir_pagamento.html', {'pagamento': pagamento})
    except Exception as e:
        logger.error("Erro ao excluir pagamento: %s", str(e))
        messages.error(request, f"Erro ao excluir pagamento: {str(e)}")
        return redirect('pagamentos:listar_pagamentos')


@login_required
def pagamentos_aluno(request, cpf):
    """Exibe os pagamentos de um aluno específico."""
    try:
        Aluno = get_aluno_model()
        Pagamento = get_pagamento_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)

        status = request.GET.get('status', '')
        data_inicio = request.GET.get('data_inicio', '')
        data_fim = request.GET.get('data_fim', '')

        pagamentos = Pagamento.objects.filter(aluno=aluno)

        if status:
            pagamentos = pagamentos.filter(status=status)
        if data_inicio:
            try:
                data_inicio_dt = datetime.datetime.strptime(data_inicio, '%Y-%m-%d').date()
                pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio_dt)
            except ValueError:
                pass
        if data_fim:
            try:
                data_fim_dt = datetime.datetime.strptime(data_fim, '%Y-%m-%d').date()
                pagamentos = pagamentos.filter(data_vencimento__lte=data_fim_dt)
            except ValueError:
                pass

        pagamentos = pagamentos.order_by('-data_vencimento')

        total_pago = pagamentos.filter(status='PAGO').aggregate(Sum('valor'))['valor__sum'] or 0
        total_pendente = pagamentos.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
        total_atrasado = pagamentos.filter(status='ATRASADO').aggregate(Sum('valor'))['valor__sum'] or 0

        paginator = Paginator(pagamentos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'aluno': aluno,
            'pagamentos': page_obj,
            'page_obj': page_obj,
            'status': status,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'total_pago': total_pago,
            'total_pendente': total_pendente,
            'total_atrasado': total_atrasado,
            'total_geral': total_pago + total_pendente + total_atrasado
        }

        return render(request, 'pagamentos/pagamentos_aluno.html', context)
    except Exception as e:
        logger.error(f"Erro ao listar pagamentos do aluno {cpf}: {str(e)}")
        messages.error(request, f"Erro ao listar pagamentos do aluno: {str(e)}")
        return redirect('pagamentos:listar_pagamentos')


@login_required
def registrar_pagamento_rapido(request, cpf):
    Aluno = get_aluno_model()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == 'POST':
        form = PagamentoRapidoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.aluno = aluno
            pagamento.save()
            messages.success(request, "Pagamento registrado com sucesso!")
            return redirect('pagamentos:pagamentos_aluno', cpf=aluno.cpf)
    else:
        form = PagamentoRapidoForm()
    return render(request, 'pagamentos/registrar_pagamento_rapido.html', {'form': form, 'aluno': aluno})


@login_required
def importar_pagamentos_csv(request):
    """
    Importa pagamentos a partir de um arquivo CSV enviado pelo usuário.
    Espera um arquivo com cabeçalhos: aluno_cpf, valor, data_vencimento, status, observacoes
    """
    Pagamento = get_pagamento_model()
    Aluno = get_aluno_model()
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        try:
            # Decodifica o arquivo para leitura universal
            decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(decoded_file)
            criados = 0
            erros = []
            for idx, row in enumerate(reader, start=2):  # start=2 para considerar o cabeçalho
                try:
                    aluno_cpf = row.get('aluno_cpf')
                    valor = float(row.get('valor', 0))
                    data_vencimento = datetime.datetime.strptime(row.get('data_vencimento'), '%Y-%m-%d').date()
                    status = row.get('status', 'PENDENTE')
                    observacoes = row.get('observacoes', '')

                    aluno = Aluno.objects.get(cpf=aluno_cpf)
                    Pagamento.objects.create(
                        aluno=aluno,
                        valor=valor,
                        data_vencimento=data_vencimento,
                        status=status,
                        observacoes=observacoes
                    )
                    criados += 1
                except Exception as e:
                    erros.append(f"Linha {idx}: {str(e)}")
            if criados:
                messages.success(request, f"{criados} pagamentos importados com sucesso!")
            if erros:
                messages.warning(request, "Algumas linhas não foram importadas:\n" + "\n".join(erros))
            return redirect('pagamentos:listar_pagamentos')
        except Exception as e:
            logger.error(f"Erro ao importar pagamentos CSV: {str(e)}")
            messages.error(request, f"Erro ao importar pagamentos: {str(e)}")
    return render(request, 'pagamentos/importar_pagamentos.html')


def exportar_pagamentos_csv(pagamentos_queryset):
    """Exporta pagamentos para CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagamentos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Aluno', 'Valor', 'Vencimento', 'Status', 'Data Pagamento', 'Método', 'Observações'])
    for p in pagamentos_queryset:
        writer.writerow([
            p.aluno.nome,
            f"{p.valor:.2f}",
            p.data_vencimento.strftime('%d/%m/%Y'),
            p.get_status_display(),
            p.data_pagamento.strftime('%d/%m/%Y') if p.data_pagamento else '',
            p.get_metodo_pagamento_display() if hasattr(p, 'get_metodo_pagamento_display') and p.metodo_pagamento else '',
            p.observacoes or ''
        ])
    return response


def exportar_pagamentos_excel(pagamentos_queryset):
    """Exporta pagamentos para Excel (formato CSV para compatibilidade)."""
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="pagamentos.xls"'
    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['Aluno', 'Valor', 'Vencimento', 'Status', 'Data Pagamento', 'Método', 'Observações'])
    for p in pagamentos_queryset:
        writer.writerow([
            p.aluno.nome,
            f"{p.valor:.2f}",
            p.data_vencimento.strftime('%d/%m/%Y'),
            p.get_status_display(),
            p.data_pagamento.strftime('%d/%m/%Y') if p.data_pagamento else '',
            p.get_metodo_pagamento_display() if hasattr(p, 'get_metodo_pagamento_display') and p.metodo_pagamento else '',
            p.observacoes or ''
        ])
    return response


@login_required
def exportar_pagamentos_pdf(request):
    """View para exportar pagamentos filtrados para PDF."""
    Pagamento = get_pagamento_model()

    # Obter filtros da query string
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    pagamentos = Pagamento.objects.all().select_related('aluno')

    if query:
        pagamentos = pagamentos.filter(
            Q(aluno__nome__icontains=query) |
            Q(aluno__cpf__icontains=query) |
            Q(observacoes__icontains=query)
        )
    if status:
        pagamentos = pagamentos.filter(status=status)
    if data_inicio:
        try:
            data_inicio_dt = datetime.datetime.strptime(data_inicio, '%Y-%m-%d').date()
            pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio_dt)
        except ValueError:
            data_inicio_dt = ''
    else:
        data_inicio_dt = ''
    if data_fim:
        try:
            data_fim_dt = datetime.datetime.strptime(data_fim, '%Y-%m-%d').date()
            pagamentos = pagamentos.filter(data_vencimento__lte=data_fim_dt)
        except ValueError:
            data_fim_dt = ''
    else:
        data_fim_dt = ''

    # Totais
    total_pago = pagamentos.filter(status='PAGO').aggregate(Sum('valor'))['valor__sum'] or 0
    total_pendente = pagamentos.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
    total_geral = total_pago + total_pendente

    context = {
        'pagamentos': pagamentos,
        'data_geracao': timezone.now(),
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'total_geral': total_geral,
        'filtros': {
            'status': dict(Pagamento.STATUS_CHOICES).get(status) if status else 'Todos',
            'data_inicio': data_inicio_dt,
            'data_fim': data_fim_dt,
        }
    }
    return exportar_pagamentos_pdf_util(pagamentos, context)


# Renomeie a função utilitária para evitar conflito de nomes:
def exportar_pagamentos_pdf_util(pagamentos_queryset, context):
    """Exporta pagamentos para PDF usando um template HTML."""
    from django.template.loader import render_to_string
    html = render_to_string('pagamentos/pdf/pagamentos_pdf.html', context)
    return HttpResponse(html)


@login_required
def detalhar_pagamento(request, pagamento_id):
    """Exibe os detalhes de um pagamento."""
    Pagamento = get_pagamento_model()
    try:
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        return render(request, 'pagamentos/detalhar_pagamento.html', {'pagamento': pagamento})
    except Exception as e:
        logger.error("Erro ao detalhar pagamento: %s", str(e))
        messages.error(request, f"Erro ao detalhar pagamento: {str(e)}")
        return redirect('pagamentos:listar_pagamentos')


def turmas_por_curso(request):
    curso_id = request.GET.get('curso_id')
    turmas = []
    if curso_id:
        turmas = list(Turma.objects.filter(curso_id=curso_id).values('id', 'nome'))
    return JsonResponse(turmas, safe=False)


@require_GET
@login_required
def buscar_alunos(request):
    termo = request.GET.get('q', '').strip()
    Aluno = get_aluno_model()
    alunos = []
    if termo and len(termo) >= 2:
        alunos = Aluno.objects.filter(
            Q(nome__icontains=termo) | Q(cpf__icontains=termo)
        ).values('cpf', 'nome')[:10]  # <-- Corrigido aqui!
    return JsonResponse(list(alunos), safe=False)





### Arquivo: pagamentos\views\relatorio_views.py

python
import datetime
import io
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils import timezone
from django.views.decorators.http import require_GET

import xlsxwriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

# Importação dinâmica para evitar referências circulares
def get_pagamento_model():
    from pagamentos.models import Pagamento
    return Pagamento

@login_required
def relatorio_financeiro(request):
    """
    Exibe um relatório financeiro com dados de pagamentos.
    """
    Pagamento = get_pagamento_model()
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)

    total_pago = Pagamento.objects.filter(status='PAGO').aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
    total_pendente = Pagamento.objects.filter(status='PENDENTE').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    total_atrasado = Pagamento.objects.filter(status='ATRASADO').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    total_cancelado = Pagamento.objects.filter(status='CANCELADO').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    total_geral = total_pago + total_pendente + total_atrasado + total_cancelado

    pagamentos_mes = Pagamento.objects.filter(
        data_vencimento__gte=primeiro_dia_mes,
        data_vencimento__lte=hoje
    ).order_by('-data_vencimento')

    pagos_mes = pagamentos_mes.filter(status='PAGO').count()
    pendentes_mes = pagamentos_mes.filter(status='PENDENTE').count()
    atrasados_mes = pagamentos_mes.filter(status='ATRASADO').count()
    cancelados_mes = pagamentos_mes.filter(status='CANCELADO').count()

    meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    mes_atual = meses[hoje.month - 1]

    context = {
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'total_atrasado': total_atrasado,
        'total_cancelado': total_cancelado,
        'total_geral': total_geral,
        'pagamentos_mes': pagamentos_mes,
        'pagos_mes': pagos_mes,
        'pendentes_mes': pendentes_mes,
        'atrasados_mes': atrasados_mes,
        'cancelados_mes': cancelados_mes,
        'mes_atual': mes_atual,
    }
    return render(request, 'pagamentos/relatorio_financeiro.html', context)

@login_required
def exportar_pagamentos_excel(request):
    """
    Exporta os pagamentos para um arquivo Excel.
    """
    Pagamento = get_pagamento_model()
    
    # Obter filtros da requisição
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Filtrar pagamentos
    pagamentos = Pagamento.objects.all().order_by('-data_vencimento')
    
    if status:
        pagamentos = pagamentos.filter(status=status)
    
    if data_inicio:
        try:
            data_inicio_obj = datetime.datetime.strptime(data_inicio, '%Y-%m-%d').date()
            pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio_obj)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_obj = datetime.datetime.strptime(data_fim, '%Y-%m-%d').date()
            pagamentos = pagamentos.filter(data_vencimento__lte=data_fim_obj)
        except ValueError:
            pass
    
    # Criar arquivo Excel em memória
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Pagamentos')
    
    # Formatos
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    money_format = workbook.add_format({'num_format': 'R$ #,##0.00'})
    
    # Cabeçalhos
    headers = [
        'ID', 'Aluno', 'CPF', 'Valor', 'Vencimento', 
        'Status', 'Data Pagamento', 'Valor Pago', 'Método'
    ]
    
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    # Dados
    for row, pagamento in enumerate(pagamentos, start=1):
        worksheet.write(row, 0, pagamento.id)
        worksheet.write(row, 1, pagamento.aluno.nome)
        worksheet.write(row, 2, pagamento.aluno.cpf)
        worksheet.write(row, 3, float(pagamento.valor), money_format)
        worksheet.write(row, 4, pagamento.data_vencimento, date_format)
        worksheet.write(row, 5, pagamento.get_status_display())
        
        if pagamento.data_pagamento:
            worksheet.write(row, 6, pagamento.data_pagamento, date_format)
        else:
            worksheet.write(row, 6, '-')
            
        if pagamento.valor_pago:
            worksheet.write(row, 7, float(pagamento.valor_pago), money_format)
        else:
            worksheet.write(row, 7, '-')
            
        if pagamento.metodo_pagamento:
            worksheet.write(row, 8, pagamento.get_metodo_pagamento_display())
        else:
            worksheet.write(row, 8, '-')
    
    # Ajustar largura das colunas
    worksheet.set_column('A:A', 5)  # ID
    worksheet.set_column('B:B', 30)  # Aluno
    worksheet.set_column('C:C', 15)  # CPF
    worksheet.set_column('D:D', 12)  # Valor
    worksheet.set_column('E:E', 12)  # Vencimento
    worksheet.set_column('F:F', 12)  # Status
    worksheet.set_column('G:G', 15)  # Data Pagamento
    worksheet.set_column('H:H', 12)  # Valor Pago
    worksheet.set_column('I:I', 15)  # Método
    
    workbook.close()
    
    # Preparar resposta
    output.seek(0)
    
    hoje = datetime.datetime.now().strftime('%Y%m%d')
    filename = f'pagamentos_{hoje}.xlsx'
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
def exportar_pagamentos_pdf(request):
    """
    Exporta os pagamentos para um arquivo PDF.
    """
    Pagamento = get_pagamento_model()
    
    # Obter filtros da requisição
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Filtrar pagamentos
    pagamentos = Pagamento.objects.all().order_by('-data_vencimento')
    
    if status:
        pagamentos = pagamentos.filter(status=status)
    
    if data_inicio:
        try:
            data_inicio_obj = datetime.datetime.strptime(data_inicio, '%Y-%m-%d').date()
            pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio_obj)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_obj = datetime.datetime.strptime(data_fim, '%Y-%m-%d').date()
            pagamentos = pagamentos.filter(data_vencimento__lte=data_fim_obj)
        except ValueError:
            pass
    
    # Calcular totais
    total_pago = pagamentos.filter(status='PAGO').aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
    total_pendente = pagamentos.filter(Q(status='PENDENTE') | Q(status='ATRASADO')).aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    total_geral = total_pago + total_pendente
    
    # Preparar dados para o template
    filtros = {
        'status': dict(Pagamento.STATUS_CHOICES).get(status, 'Todos') if status else 'Todos',
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    
    # Renderizar o HTML
    template = get_template('pagamentos/pdf/pagamentos_pdf.html')
    html = template.render({
        'pagamentos': pagamentos,
        'filtros': filtros,
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'total_geral': total_geral,
        'data_geracao': timezone.now(),
    })
    
    # Gerar PDF usando ReportLab
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = 1  # Centralizado
    
    # Título
    elements.append(Paragraph("Relatório de Pagamentos", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Dados para a tabela
    data = [['Aluno', 'CPF', 'Valor', 'Vencimento', 'Status', 'Data Pagamento']]
    
    for pagamento in pagamentos:
        data.append([
            pagamento.aluno.nome,
            pagamento.aluno.cpf,
            f"R$ {pagamento.valor:.2f}",
            pagamento.data_vencimento.strftime('%d/%m/%Y'),
            pagamento.get_status_display(),
            pagamento.data_pagamento.strftime('%d/%m/%Y') if pagamento.data_pagamento else '-'
        ])
    
    # Criar tabela
    table = Table(data)    # Estilo da tabela
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # Alinhar valores à direita
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ])
    
    # Aplicar estilos alternados para as linhas
    for i in range(1, len(data)):
        if i % 2 == 0:
            table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
    
    table.setStyle(table_style)
    elements.append(table)
    
    # Adicionar informações de totais
    elements.append(Spacer(1, 0.5*inch))
    
    # Estilo para o resumo
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=12,
        alignment=2,  # Alinhado à direita
        spaceAfter=6
    )
    
    elements.append(Paragraph(f"Total Pago: R$ {total_pago:.2f}", summary_style))
    elements.append(Paragraph(f"Total Pendente: R$ {total_pendente:.2f}", summary_style))
    elements.append(Paragraph(f"Total Geral: R$ {total_geral:.2f}", summary_style))
    
    # Adicionar rodapé com data de geração
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1  # Centralizado
    )
    
    data_geracao = timezone.now().strftime('%d/%m/%Y %H:%M:%S')
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Relatório gerado em {data_geracao}", footer_style))
    
    # Construir o PDF
    doc.build(elements)
    
    # Preparar resposta
    buffer.seek(0)
    
    hoje = timezone.now().strftime('%Y%m%d')
    filename = f'pagamentos_{hoje}.pdf'
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@require_GET
def dados_grafico_pagamentos(request):
    """
    Retorna dados para o gráfico de pagamentos.
    """
    Pagamento = get_pagamento_model()
    
    # Obter período (padrão: últimos 6 meses)
    meses = int(request.GET.get('meses', 6))
    if meses > 12:
        meses = 12  # Limitar a 12 meses
    
    # Data atual e data inicial
    data_final = timezone.now().date()
    data_inicial = (data_final - datetime.timedelta(days=30 * meses)).replace(day=1)
    
    # Preparar dados
    labels = []
    dados_pagos = []
    dados_pendentes = []
    dados_atrasados = []
    
    # Gerar dados para cada mês
    data_atual = data_inicial
    while data_atual <= data_final:
        # Último dia do mês
        if data_atual.month == 12:
            ultimo_dia = data_atual.replace(day=31)
        else:
            ultimo_dia = data_atual.replace(month=data_atual.month + 1, day=1) - datetime.timedelta(days=1)
        
        # Filtrar pagamentos do mês
        pagamentos_mes = Pagamento.objects.filter(
            data_vencimento__gte=data_atual,
            data_vencimento__lte=ultimo_dia
        )
        
        # Calcular totais
        total_pago = pagamentos_mes.filter(status='PAGO').aggregate(total=Sum('valor_pago'))['total'] or 0
        total_pendente = pagamentos_mes.filter(status='PENDENTE').aggregate(total=Sum('valor'))['total'] or 0
        total_atrasado = pagamentos_mes.filter(status='ATRASADO').aggregate(total=Sum('valor'))['total'] or 0
        
        # Adicionar aos dados
        mes_nome = data_atual.strftime('%b/%Y')
        labels.append(mes_nome)
        dados_pagos.append(float(total_pago))
        dados_pendentes.append(float(total_pendente))
        dados_atrasados.append(float(total_atrasado))
        
        # Avançar para o próximo mês
        if data_atual.month == 12:
            data_atual = data_atual.replace(year=data_atual.year + 1, month=1)
        else:
            data_atual = data_atual.replace(month=data_atual.month + 1)
    
    # Retornar dados em formato JSON
    return JsonResponse({
        'labels': labels,
        'datasets': [
            {
                'label': 'Pagos',
                'data': dados_pagos,
                'backgroundColor': 'rgba(40, 167, 69, 0.7)',
                'borderColor': 'rgba(40, 167, 69, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Pendentes',
                'data': dados_pendentes,
                'backgroundColor': 'rgba(255, 193, 7, 0.7)',
                'borderColor': 'rgba(255, 193, 7, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Atrasados',
                'data': dados_atrasados,
                'backgroundColor': 'rgba(220, 53, 69, 0.7)',
                'borderColor': 'rgba(220, 53, 69, 1)',
                'borderWidth': 1
            }
        ]
    })

@login_required
def pagamentos_por_turma(request):
    """
    Exibe um relatório de pagamentos agrupados por turma.
    """
    Pagamento = get_pagamento_model()
    
    # Importar modelo de Turma dinamicamente para evitar referências circulares
    try:
        from turmas.models import Turma
        from matriculas.models import Matricula
    except ImportError:
        messages.error(request, "Módulo de turmas ou matrículas não disponível")
        return redirect('pagamentos:relatorio_financeiro')
    
    # Obter todas as turmas ativas
    turmas = Turma.objects.filter(ativa=True).order_by('nome')
    
    # Dados para o relatório
    dados_turmas = []
    
    for turma in turmas:
        # Obter alunos matriculados nesta turma
        matriculas = Matricula.objects.filter(turma=turma, ativa=True)
        alunos_ids = matriculas.values_list('aluno_id', flat=True)
        
        # Obter pagamentos destes alunos
        pagamentos = Pagamento.objects.filter(aluno_id__in=alunos_ids)
        
        # Calcular totais
        total_pago = pagamentos.filter(status='PAGO').aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
        total_pendente = pagamentos.filter(status='PENDENTE').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        total_atrasado = pagamentos.filter(status='ATRASADO').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        total_cancelado = pagamentos.filter(status='CANCELADO').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        
        # Adicionar dados da turma
        dados_turmas.append({
            'turma': turma,
            'total_alunos': matriculas.count(),
            'total_pago': total_pago,
            'total_pendente': total_pendente,
            'total_atrasado': total_atrasado,
            'total_cancelado': total_cancelado,
            'total_geral': total_pago + total_pendente + total_atrasado + total_cancelado
        })
    
    context = {
        'dados_turmas': dados_turmas,
        'data_geracao': timezone.now()
    }
    
    return render(request, 'pagamentos/relatorio_pagamentos_turma.html', context)

@login_required
@require_GET
def dados_distribuicao_pagamentos(request):
    """
    Retorna dados para o gráfico de distribuição de pagamentos.
    """
    Pagamento = get_pagamento_model()
    
    # Obter data atual e primeiro dia do mês
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)
    
    # Obter pagamentos do mês atual
    pagamentos_mes = Pagamento.objects.filter(
        data_vencimento__gte=primeiro_dia_mes,
        data_vencimento__lte=hoje
    )
    
    # Contar por status
    pagos = pagamentos_mes.filter(status='PAGO').count()
    pendentes = pagamentos_mes.filter(status='PENDENTE').count()
    atrasados = pagamentos_mes.filter(status='ATRASADO').count()
    cancelados = pagamentos_mes.filter(status='CANCELADO').count()
    
    # Retornar dados em formato JSON
    return JsonResponse({
        'labels': ['Pagos', 'Pendentes', 'Atrasados', 'Cancelados'],
        'datasets': [{
            'data': [pagos, pendentes, atrasados, cancelados],
            'backgroundColor': [
                'rgba(40, 167, 69, 0.7)',  # Verde
                'rgba(255, 193, 7, 0.7)',  # Amarelo
                'rgba(220, 53, 69, 0.7)',  # Vermelho
                'rgba(108, 117, 125, 0.7)'  # Cinza
            ],
            'borderColor': [
                'rgba(40, 167, 69, 1)',
                'rgba(255, 193, 7, 1)',
                'rgba(220, 53, 69, 1)',
                'rgba(108, 117, 125, 1)'
            ],
            'borderWidth': 1
        }]
    })



### Arquivo: pagamentos\views\serializers.py

python
"""
Serializadores para a API de pagamentos.
"""
from rest_framework import serializers
from ..views.base import get_pagamento_model, get_aluno_model

Pagamento = get_pagamento_model()
Aluno = get_aluno_model()

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['cpf', 'nome', 'numero_iniciatico', 'email']

class PagamentoSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    metodo_pagamento_display = serializers.CharField(source='get_metodo_pagamento_display', read_only=True)
    
    class Meta:
        model = Pagamento
        fields = [
            'id', 'aluno', 'valor', 'data_vencimento', 'status', 'status_display',
            'observacoes', 'data_pagamento', 'valor_pago', 'metodo_pagamento',
            'metodo_pagamento_display', 'created_at', 'updated_at'
        ]



### Arquivo: pagamentos\views\viewsets.py

python
import datetime
import json
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from importlib import import_module

from ..models import Pagamento

logger = logging.getLogger(__name__)

def get_pagamento_model():
    pagamentos_module = import_module("pagamentos.models")
    return getattr(pagamentos_module, "Pagamento")

def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_pagamento_or_404(pagamento_id):
    Pagamento = get_pagamento_model()
    from django.shortcuts import get_object_or_404
    return get_object_or_404(Pagamento, id=pagamento_id)

@login_required
def buscar_alunos_com_pagamentos_pendentes(request):
    """
    API para buscar alunos com pagamentos pendentes ou atrasados.
    """
    try:
        query = request.GET.get('q', '')
        if len(query) < 2:
            return JsonResponse([], safe=False)
        Pagamento = get_pagamento_model()
        Aluno = get_aluno_model()
        alunos_com_pagamentos = Aluno.objects.filter(
            Q(nome__icontains=query) | Q(cpf__icontains=query) | Q(numero_iniciatico__icontains=query),
            pagamento__status__in=['PENDENTE', 'ATRASADO']
        ).distinct()[:10]
        resultados = []
        for aluno in alunos_com_pagamentos:
            pagamentos_pendentes = Pagamento.objects.filter(aluno=aluno, status='PENDENTE').count()
            pagamentos_atrasados = Pagamento.objects.filter(aluno=aluno, status='ATRASADO').count()
            resultados.append({
                'cpf': aluno.cpf,
                'nome': aluno.nome,
                'numero_iniciatico': aluno.numero_iniciatico or 'N/A',
                'foto': aluno.foto.url if hasattr(aluno, 'foto') and aluno.foto else None,
                'pagamentos_pendentes': pagamentos_pendentes,
                'pagamentos_atrasados': pagamentos_atrasados,
                'total_pendente': pagamentos_pendentes + pagamentos_atrasados
            })
        return JsonResponse(resultados, safe=False)
    except Exception as e:
        logger.error(f"Erro em buscar_alunos_com_pagamentos_pendentes: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': f'Erro ao buscar alunos: {str(e)}'}, status=500)

@login_required
def api_buscar_pagamentos_aluno(request, aluno_id):
    """
    API para buscar pagamentos de um aluno específico.
    """
    try:
        Pagamento = get_pagamento_model()
        Aluno = get_aluno_model()
        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
        except Aluno.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Aluno não encontrado.'}, status=404)
        pagamentos = Pagamento.objects.filter(aluno=aluno).order_by('-data_vencimento')
        resultados = []
        for pagamento in pagamentos:
            resultados.append({
                'id': pagamento.id,
                'valor': float(pagamento.valor),
                'data_vencimento': pagamento.data_vencimento.strftime('%d/%m/%Y'),
                'status': pagamento.status,
                'status_display': pagamento.get_status_display(),
                'observacoes': pagamento.observacoes,
                'data_pagamento': pagamento.data_pagamento.strftime('%d/%m/%Y') if pagamento.data_pagamento else None,
                'valor_pago': float(pagamento.valor_pago) if pagamento.valor_pago is not None else None,
                'metodo_pagamento': pagamento.metodo_pagamento,
                'metodo_pagamento_display': pagamento.get_metodo_pagamento_display() if pagamento.metodo_pagamento else None
            })
        return JsonResponse(resultados, safe=False)
    except Exception as e:
        logger.error(f"Erro em api_buscar_pagamentos_aluno: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': f'Erro ao buscar pagamentos: {str(e)}'}, status=500)

@login_required
@require_http_methods(["POST"])
def api_registrar_pagamento(request):
    """
    API para registrar um pagamento via AJAX.
    """
    try:
        data = json.loads(request.body)
        aluno_id = data.get('aluno_id')
        valor = data.get('valor')
        data_vencimento = data.get('data_vencimento')
        observacoes = data.get('observacoes', '')
        status = data.get('status', 'PENDENTE')
        if not aluno_id or not valor or not data_vencimento:
            return JsonResponse({'status': 'error', 'message': 'Aluno, valor e data de vencimento são obrigatórios.'}, status=400)
        Pagamento = get_pagamento_model()
        Aluno = get_aluno_model()
        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
        except Aluno.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Aluno não encontrado.'}, status=404)
        try:
            valor = float(valor)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Valor inválido.'}, status=400)
        try:
            data_vencimento = datetime.datetime.strptime(data_vencimento, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Data de vencimento inválida.'}, status=400)
        data_pagamento = None
        valor_pago = None
        metodo_pagamento = None
        if status == 'PAGO':
            data_pagamento_str = data.get('data_pagamento')
            valor_pago_str = data.get('valor_pago')
            metodo_pagamento = data.get('metodo_pagamento')
            if not data_pagamento_str:
                data_pagamento = timezone.now().date()
            else:
                try:
                    data_pagamento = datetime.datetime.strptime(data_pagamento_str, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Data de pagamento inválida.'}, status=400)
            if not valor_pago_str:
                valor_pago = valor
            else:
                try:
                    valor_pago = float(valor_pago_str)
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Valor pago inválido.'}, status=400)
        pagamento = Pagamento(
            aluno=aluno,
            valor=valor,
            data_vencimento=data_vencimento,
            observacoes=observacoes,
            status=status,
            data_pagamento=data_pagamento,
            valor_pago=valor_pago,
            metodo_pagamento=metodo_pagamento
        )
        pagamento.save()
        return JsonResponse({'status': 'success', 'message': 'Pagamento registrado com sucesso.', 'pagamento_id': pagamento.id})
    except Exception as e:
        logger.error(f"Erro em api_registrar_pagamento: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': f'Erro ao registrar pagamento: {str(e)}'}, status=500)

@login_required
@require_http_methods(["POST"])
def api_atualizar_pagamento(request, pagamento_id):
    """
    API para atualizar um pagamento via AJAX.
    """
    try:
        data = json.loads(request.body)
        pagamento = get_pagamento_or_404(pagamento_id)
        if 'valor' in data:
            try:
                pagamento.valor = float(data['valor'])
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Valor inválido.'}, status=400)
        if 'data_vencimento' in data:
            try:
                pagamento.data_vencimento = datetime.datetime.strptime(data['data_vencimento'], '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Data de vencimento inválida.'}, status=400)
        if 'observacoes' in data:
            pagamento.observacoes = data['observacoes']
        if 'status' in data:
            Pagamento = get_pagamento_model()
            status = data['status']
            if status not in [choice[0] for choice in Pagamento.STATUS_CHOICES]:
                return JsonResponse({'status': 'error', 'message': 'Status inválido.'}, status=400)
            pagamento.status = status
            if status == 'PAGO':
                if 'data_pagamento' in data:
                    try:
                        pagamento.data_pagamento = datetime.datetime.strptime(data['data_pagamento'], '%Y-%m-%d').date()
                    except ValueError:
                        return JsonResponse({'status': 'error', 'message': 'Data de pagamento inválida.'}, status=400)
                else:
                    pagamento.data_pagamento = timezone.now().date()
                if 'valor_pago' in data:
                    try:
                        pagamento.valor_pago = float(data['valor_pago'])
                    except ValueError:
                        return JsonResponse({'status': 'error', 'message': 'Valor pago inválido.'}, status=400)
                else:
                    pagamento.valor_pago = pagamento.valor
                if 'metodo_pagamento' in data:
                    pagamento.metodo_pagamento = data['metodo_pagamento']
            elif status != 'PAGO':
                pagamento.data_pagamento = None
                pagamento.valor_pago = None
                pagamento.metodo_pagamento = None
        pagamento.save()
        return JsonResponse({'status': 'success', 'message': 'Pagamento atualizado com sucesso.'})
    except Exception as e:
        logger.error(f"Erro em api_atualizar_pagamento: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': f'Erro ao atualizar pagamento: {str(e)}'}, status=500)

@login_required
@require_http_methods(["POST"])
def api_excluir_pagamento(request, pagamento_id):
    """
    API para excluir um pagamento via AJAX.
    """
    try:
        pagamento = get_pagamento_or_404(pagamento_id)
        pagamento.delete()
        return JsonResponse({'status': 'success', 'message': 'Pagamento excluído com sucesso.'})
    except Exception as e:
        logger.error(f"Erro em api_excluir_pagamento: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': f'Erro ao excluir pagamento: {str(e)}'}, status=500)

@login_required
@require_http_methods(["POST"])
def atualizar_status_pagamento(request, pagamento_id):
    """
    API para atualizar o status de um pagamento.
    """
    try:
        Pagamento = get_pagamento_model()
        pagamento = get_pagamento_or_404(pagamento_id)
        status = request.POST.get('status')
        if status not in [choice[0] for choice in Pagamento.STATUS_CHOICES]:
            return JsonResponse({'status': 'error', 'message': 'Status inválido.'}, status=400)
        if status == 'PAGO':
            data_pagamento = request.POST.get('data_pagamento')
            valor_pago = request.POST.get('valor_pago')
            metodo_pagamento = request.POST.get('metodo_pagamento')
            if not data_pagamento:
                data_pagamento = timezone.now().date()
            else:
                try:
                    data_pagamento = datetime.datetime.strptime(data_pagamento, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Data de pagamento inválida.'}, status=400)
            if not valor_pago:
                valor_pago = pagamento.valor
            else:
                try:
                    valor_pago = float(valor_pago)
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Valor pago inválido.'}, status=400)
            pagamento.status = status
            pagamento.data_pagamento = data_pagamento
            pagamento.valor_pago = valor_pago
            pagamento.metodo_pagamento = metodo_pagamento
        else:
            pagamento.status = status
            if status != 'PAGO':
                pagamento.data_pagamento = None
                pagamento.valor_pago = None
                pagamento.metodo_pagamento = None
        pagamento.save()
        return JsonResponse({'status': 'success', 'message': 'Status atualizado com sucesso.'})
    except Exception as e:
        logger.error(f"Erro em atualizar_status_pagamento: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def api_listar_pagamentos(request):
    Pagamento = get_pagamento_model()
    pagamentos = Pagamento.objects.select_related('aluno').all()
    data = [
        {
            'id': p.id,
            'aluno': p.aluno.nome,
            'valor': float(p.valor),
            'status': p.status,
            'data_vencimento': p.data_vencimento,
        }
        for p in pagamentos
    ]
    return JsonResponse(data, safe=False)


## Arquivos de Template:


### Arquivo: pagamentos\templates\pagamentos\criar_pagamento.html

html
{% extends 'base.html' %}

{% block title %}Criar Pagamento{% endblock %}

{% block content %}
<style>
@keyframes piscarBorda {
    0%   { box-shadow: 0 0 0 0 red; }
    50%  { box-shadow: 0 0 8px 2px red; }
    100% { box-shadow: 0 0 0 0 red; }
}
.piscar-erro {
    animation: piscarBorda 0.8s linear 2;
}
</style>
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Novo Pagamento</h1>
        <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}{% if message.tags == 'error' %} alert-danger{% endif %}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}

    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            {% for error in form.non_field_errors %}
                <div>{{ error }}</div>
            {% endfor %}
        </div>
    {% endif %}

    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Dados do Pagamento</h5>
                </div>
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data" id="pagamento-form" novalidate>
                        {% csrf_token %}
                        <!-- Busca de aluno -->
                        <div class="mb-3">
                            <label for="busca-aluno" class="form-label">Buscar Aluno <span class="text-danger">*</span></label>
                            <input type="text" id="busca-aluno" class="form-control{% if form.aluno.errors %} is-invalid piscar-erro{% endif %}" placeholder="Digite nome ou CPF do aluno" autocomplete="off">
                            <input type="hidden" name="aluno" id="id_aluno" value="{{ form.aluno.value|default_if_none:'' }}">
                            <div id="resultados-aluno" class="list-group mt-1"></div>
                            <div class="form-text">Digite pelo menos 2 letras para buscar.</div>
                            {% for error in form.aluno.errors %}
                                <div class="invalid-feedback d-block">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="id_valor" class="form-label">Valor (R$) <span class="text-danger">*</span></label>
                                    <input type="number" name="valor" step="0.01" required id="id_valor"
                                           class="form-control{% if form.valor.errors %} is-invalid piscar-erro{% endif %}"
                                           value="{{ form.valor.value|default_if_none:'' }}" placeholder="Ex: 100.00">
                                    {% for error in form.valor.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="id_data_vencimento" class="form-label">Data de Vencimento <span class="text-danger">*</span></label>
                                    <input type="date" name="data_vencimento" required id="id_data_vencimento"
                                           class="form-control{% if form.data_vencimento.errors %} is-invalid piscar-erro{% endif %}"
                                           value="{{ form.data_vencimento.value|default_if_none:'' }}">
                                    {% for error in form.data_vencimento.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="id_observacoes" class="form-label">Observações</label>
                            <textarea name="observacoes" cols="40" rows="3" id="id_observacoes"
                                      class="form-control{% if form.observacoes.errors %} is-invalid piscar-erro{% endif %}"
                                      placeholder="Observações adicionais...">{{ form.observacoes.value|default_if_none:'' }}</textarea>
                            {% for error in form.observacoes.errors %}
                                <div class="invalid-feedback">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="id_status" class="form-label">Status <span class="text-danger">*</span></label>
                                    <select name="status" id="id_status"
                                            class="form-select{% if form.status.errors %} is-invalid piscar-erro{% endif %}" required>
                                        <option value="PENDENTE" {% if form.status.value == 'PENDENTE' %}selected{% endif %}>Pendente</option>
                                        <option value="PAGO" {% if form.status.value == 'PAGO' %}selected{% endif %}>Pago</option>
                                        <option value="ATRASADO" {% if form.status.value == 'ATRASADO' %}selected{% endif %}>Atrasado</option>
                                        <option value="CANCELADO" {% if form.status.value == 'CANCELADO' %}selected{% endif %}>Cancelado</option>
                                    </select>
                                    {% for error in form.status.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3 metodo-pagamento-container" style="display: none;">
                                    <label for="id_metodo_pagamento" class="form-label">Método de Pagamento</label>
                                    <select name="metodo_pagamento" id="id_metodo_pagamento"
                                            class="form-select{% if form.metodo_pagamento.errors %} is-invalid piscar-erro{% endif %}">
                                        <option value="">Selecione um método</option>
                                        <option value="DINHEIRO" {% if form.metodo_pagamento.value == 'DINHEIRO' %}selected{% endif %}>Dinheiro</option>
                                        <option value="CARTAO_CREDITO" {% if form.metodo_pagamento.value == 'CARTAO_CREDITO' %}selected{% endif %}>Cartão de Crédito</option>
                                        <option value="CARTAO_DEBITO" {% if form.metodo_pagamento.value == 'CARTAO_DEBITO' %}selected{% endif %}>Cartão de Débito</option>
                                        <option value="BOLETO" {% if form.metodo_pagamento.value == 'BOLETO' %}selected{% endif %}>Boleto Bancário</option>
                                        <option value="TRANSFERENCIA" {% if form.metodo_pagamento.value == 'TRANSFERENCIA' %}selected{% endif %}>Transferência</option>
                                        <option value="PIX" {% if form.metodo_pagamento.value == 'PIX' %}selected{% endif %}>PIX</option>
                                        <option value="OUTRO" {% if form.metodo_pagamento.value == 'OUTRO' %}selected{% endif %}>Outro</option>
                                    </select>
                                    {% for error in form.metodo_pagamento.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3 data-pagamento-container" style="display: none;">
                                    <label for="id_data_pagamento" class="form-label">Data de Pagamento</label>
                                    <input type="date" name="data_pagamento" id="id_data_pagamento"
                                           class="form-control{% if form.data_pagamento.errors %} is-invalid piscar-erro{% endif %}"
                                           value="{{ form.data_pagamento.value|default_if_none:'' }}">
                                    {% for error in form.data_pagamento.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3 valor-pago-container" style="display: none;">
                                    <label for="id_valor_pago" class="form-label">Valor Pago (R$)</label>
                                    <input type="number" name="valor_pago" id="id_valor_pago"
                                           class="form-control{% if form.valor_pago.errors %} is-invalid piscar-erro{% endif %}"
                                           step="0.01" min="0" value="{{ form.valor_pago.value|default_if_none:'' }}">
                                    {% for error in form.valor_pago.errors %}
                                        <div class="invalid-feedback">{{ error }}</div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="id_comprovante" class="form-label">Comprovante de Pagamento</label>
                            <input type="file" name="comprovante" id="id_comprovante"
                                   class="form-control{% if form.comprovante.errors %} is-invalid piscar-erro{% endif %}">
                            <div class="form-text">Formatos aceitos: PDF, JPG, PNG. Tamanho máximo: 5MB</div>
                            {% for error in form.comprovante.errors %}
                                <div class="invalid-feedback">{{ error }}</div>
                            {% endfor %}
                        </div>
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'pagamentos:listar_pagamentos' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Cadastrar Pagamento
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Informações</h5>
                </div>
                <div class="card-body">
                    <p>Preencha os dados para cadastrar um novo pagamento.</p>
                    <p>Se o status for "Pago", informe também a data de pagamento e o método utilizado.</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const status = document.getElementById('id_status');
        const metodoPagamentoContainer = document.querySelector('.metodo-pagamento-container');
        const dataPagamentoContainer = document.querySelector('.data-pagamento-container');
        const valorPagoContainer = document.querySelector('.valor-pago-container');
        function togglePagamentoInfo() {
            if (status.value === 'PAGO') {
                metodoPagamentoContainer.style.display = '';
                dataPagamentoContainer.style.display = '';
                valorPagoContainer.style.display = '';
            } else {
                metodoPagamentoContainer.style.display = 'none';
                dataPagamentoContainer.style.display = 'none';
                valorPagoContainer.style.display = 'none';
            }
        }
        status.addEventListener('change', togglePagamentoInfo);
        togglePagamentoInfo();

        // Autocomplete para busca de aluno
        const busca = document.getElementById('busca-aluno');
        const resultados = document.getElementById('resultados-aluno');
        const idAluno = document.getElementById('id_aluno');
        busca.addEventListener('input', function() {
            const termo = this.value;
            if (termo.length < 2) {
                resultados.innerHTML = '';
                idAluno.value = '';
                return;
            }
            fetch(`/pagamentos/alunos/buscar/?q=${encodeURIComponent(termo)}`)
                .then(resp => resp.json())
                .then(data => {
                    let html = '';
                    data.forEach(aluno => {
                        html += `<button type="button" class="list-group-item list-group-item-action" data-id="${aluno.cpf}">${aluno.nome} (${aluno.cpf})</button>`;
                    });
                    resultados.innerHTML = html;
                    document.querySelectorAll('#resultados-aluno button').forEach(btn => {
                        btn.onclick = function() {
                            idAluno.value = this.dataset.id;
                            busca.value = this.textContent;
                            resultados.innerHTML = '';
                        }
                    });
                });
        });
    });
</script>
{% endblock %}


'''