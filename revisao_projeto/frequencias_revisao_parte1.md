'''
# Revisão da Funcionalidade: frequencias

## Arquivos forms.py:


### Arquivo: frequencias\forms.py

python
from django import forms
from django.utils import timezone
from importlib import import_module

def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

class FrequenciaMensalForm(forms.ModelForm):
    """Formulário para criação e edição de frequência mensal."""
    
    class Meta:
        FrequenciaMensal, _ = get_models()
        model = FrequenciaMensal
        fields = ['turma', 'mes', 'ano', 'percentual_minimo']
        widgets = {
            'percentual_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar campos
        self.fields['turma'].queryset = get_turma_model().objects.filter(status='A')
        self.fields['turma'].widget.attrs.update({'class': 'form-control select2'})
        
        self.fields['mes'].widget.attrs.update({'class': 'form-control'})
        
        # Definir ano padrão como o atual
        if not self.instance.pk:
            self.fields['ano'].initial = timezone.now().year
        
        self.fields['ano'].widget.attrs.update({'class': 'form-control', 'min': '2000', 'max': '2100'})
    
    def clean(self):
        cleaned_data = super().clean()
        turma = cleaned_data.get('turma')
        mes = cleaned_data.get('mes')
        ano = cleaned_data.get('ano')
        
        # Validar se já existe frequência para esta turma/mês/ano
        if turma and mes and ano:
            FrequenciaMensal, _ = get_models()
            
            # Verificar se já existe, excluindo a instância atual em caso de edição
            query = FrequenciaMensal.objects.filter(turma=turma, mes=mes, ano=ano)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                self.add_error(None, 'Já existe uma frequência mensal para esta turma, mês e ano.')
        
        return cleaned_data

class FiltroPainelFrequenciasForm(forms.Form):
    """Formulário para filtrar o painel de frequências."""
    
    turma = forms.ModelChoiceField(
        label='Turma',
        queryset=get_turma_model().objects.filter(status='A'),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    mes_inicio = forms.ChoiceField(
        label='Mês Inicial',
        choices=get_models()[0].MES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    ano_inicio = forms.IntegerField(
        label='Ano Inicial',
        initial=timezone.now().year,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '2000', 'max': '2100'})
    )
    
    mes_fim = forms.ChoiceField(
        label='Mês Final',
        choices=get_models()[0].MES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    ano_fim = forms.IntegerField(
        label='Ano Final',
        initial=timezone.now().year,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '2000', 'max': '2100'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        mes_inicio = int(cleaned_data.get('mes_inicio', 1))
        ano_inicio = cleaned_data.get('ano_inicio')
        mes_fim = int(cleaned_data.get('mes_fim', 12))
        ano_fim = cleaned_data.get('ano_fim')
        
        # Validar período
        if ano_inicio and ano_fim:
            data_inicio = ano_inicio * 12 + mes_inicio
            data_fim = ano_fim * 12 + mes_fim
            
            if data_fim < data_inicio:
                self.add_error(None, 'O período final deve ser posterior ao período inicial.')
        
        return cleaned_data



## Arquivos views.py:


### Arquivo: frequencias\views.py

python
"""
Views para o aplicativo de frequências.

Este arquivo agora funciona como um agregador que importa todas as funções
dos módulos separados para manter a compatibilidade com o código existente.
"""

import logging

from .views.frequencia_mensal import (
    listar_frequencias,
    criar_frequencia_mensal,
    editar_frequencia_mensal,
    excluir_frequencia_mensal,
    detalhar_frequencia_mensal,
    recalcular_carencias
)

from .views.carencia import (
    editar_carencia,
    resolver_carencia,
    detalhar_carencia,
    iniciar_acompanhamento
)

from .views.notificacao import (
    criar_notificacao,
    detalhar_notificacao,
    editar_notificacao,
    enviar_notificacao,
    reenviar_notificacao,
    responder_aluno,
    listar_notificacoes_carencia
)

from .views.relatorio import (
    relatorio_frequencias,
    exportar_frequencia_csv,
    historico_frequencia,
    exportar_historico
)

from .views.dashboard import (
    dashboard,
    painel_frequencias,
    visualizar_painel_frequencias
)

from .views.api_views import (
    obter_dados_frequencia,
    obter_dados_painel_frequencias
)

# Importar as novas funções do módulo de exportação
from .views.exportacao import (
    exportar_frequencias,
    importar_frequencias
)

# Importar funções utilitárias do módulo utils
from .utils import (
    get_models,
    get_forms,
    get_turma_model,
    get_model_dynamically
)

# Configurar logger
logger = logging.getLogger(__name__)


## Arquivos urls.py:


### Arquivo: frequencias\urls.py

python
from django.urls import path
from .views import (
    listar_frequencias,
    criar_frequencia_mensal,
    editar_frequencia_mensal,
    excluir_frequencia_mensal,
    detalhar_frequencia_mensal,
    recalcular_carencias,
    editar_carencia,
    resolver_carencia,
    detalhar_carencia,
    iniciar_acompanhamento,
    listar_notificacoes_carencia,
    criar_notificacao,
    detalhar_notificacao,
    editar_notificacao,
    enviar_notificacao,
    reenviar_notificacao,
    responder_aluno,
    relatorio_frequencias,
    exportar_frequencia_csv,
    historico_frequencia,
    exportar_historico,
    dashboard,
    painel_frequencias,
    visualizar_painel_frequencias,
    exportar_frequencias,
    importar_frequencias
)
from .views import api_views

app_name = 'frequencias'

urlpatterns = [
    # Views principais
    path('', listar_frequencias, name='listar_frequencias'),
    path('criar/', criar_frequencia_mensal, name='criar_frequencia_mensal'),
    path('editar/<int:frequencia_id>/', editar_frequencia_mensal, name='editar_frequencia_mensal'),
    path('excluir/<int:frequencia_id>/', excluir_frequencia_mensal, name='excluir_frequencia_mensal'),
    path('detalhar/<int:frequencia_id>/', detalhar_frequencia_mensal, name='detalhar_frequencia_mensal'),
    path('recalcular/<int:frequencia_id>/', recalcular_carencias, name='recalcular_carencias'),
    
    # Carências
    path('carencias/editar/<int:carencia_id>/', editar_carencia, name='editar_carencia'),
    path('carencias/resolver/<int:carencia_id>/', resolver_carencia, name='resolver_carencia'),
    path('carencias/detalhar/<int:carencia_id>/', detalhar_carencia, name='detalhar_carencia'),
    path('carencias/iniciar-acompanhamento/<int:carencia_id>/', iniciar_acompanhamento, name='iniciar_acompanhamento'),
    
    # Notificações
    path('notificacoes/', listar_notificacoes_carencia, name='listar_notificacoes_carencia'),
    path('notificacoes/criar/<int:carencia_id>/', criar_notificacao, name='criar_notificacao'),
    path('notificacoes/detalhar/<int:notificacao_id>/', detalhar_notificacao, name='detalhar_notificacao'),
    path('notificacoes/editar/<int:notificacao_id>/', editar_notificacao, name='editar_notificacao'),
    path('notificacoes/enviar/<int:notificacao_id>/', enviar_notificacao, name='enviar_notificacao'),
    path('notificacoes/reenviar/<int:notificacao_id>/', reenviar_notificacao, name='reenviar_notificacao'),
    path('notificacoes/responder/<int:notificacao_id>/', responder_aluno, name='responder_aluno'),
    
    # Exportação e relatórios
    path('exportar/<int:frequencia_id>/', exportar_frequencia_csv, name='exportar_frequencia_csv'),
    path('painel/', painel_frequencias, name='painel_frequencias'),
    path('painel/visualizar/<int:turma_id>/<int:mes_inicio>/<int:ano_inicio>/<int:mes_fim>/<int:ano_fim>/', 
         visualizar_painel_frequencias, name='visualizar_painel_frequencias'),
    path('relatorio/', relatorio_frequencias, name='relatorio_frequencias'),
    path('historico/<str:aluno_cpf>/', historico_frequencia, name='historico_frequencia'),
    path('historico/<str:aluno_cpf>/exportar/', exportar_historico, name='exportar_historico'),
    path("exportar/", exportar_frequencias, name="exportar_frequencias"),
    path("importar/", importar_frequencias, name="importar_frequencias"),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # APIs
    path('api/dados-frequencia/<int:frequencia_id>/', api_views.obter_dados_frequencia, name='api_obter_dados_frequencia'),
    path('api/dados-painel-frequencias/', api_views.obter_dados_painel_frequencias, name='api_obter_dados_painel_frequencias'),
]



## Arquivos models.py:


### Arquivo: frequencias\models.py

python
from django.db import models
from django.utils import timezone
from importlib import import_module
from decimal import Decimal

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_presenca_model():
    """Obtém o modelo Presenca."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

class FrequenciaMensal(models.Model):
    """Modelo para controle de frequência mensal de uma turma."""
    
    MES_CHOICES = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro'),
    ]
    
    turma = models.ForeignKey(
        get_turma_model(),
        on_delete=models.CASCADE,
        verbose_name="Turma"
    )
    
    mes = models.IntegerField(
        choices=MES_CHOICES,
        verbose_name="Mês"
    )
    
    ano = models.IntegerField(
        verbose_name="Ano"
    )
    
    percentual_minimo = models.IntegerField(
        default=75,
        verbose_name="Percentual Mínimo (%)"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Frequência Mensal"
        verbose_name_plural = "Frequências Mensais"
        ordering = ['-ano', '-mes', 'turma__nome']
        unique_together = ['turma', 'mes', 'ano']
    
    def __str__(self):
        return f"{self.turma.nome} - {self.get_mes_display()}/{self.ano}"
    
    @property
    def total_alunos(self):
        """Retorna o total de alunos com carência nesta frequência."""
        return self.carencia_set.count()
    
    @property
    def alunos_liberados(self):
        """Retorna o total de alunos liberados."""
        return self.carencia_set.filter(liberado=True).count()
    
    @property
    def alunos_com_carencia(self):
        """Retorna o total de alunos com carência."""
        return self.carencia_set.filter(liberado=False).count()
    
    def calcular_carencias(self):
        """Calcula as carências para todos os alunos da turma."""
        from django.db import transaction
        import calendar
        from datetime import date
        
        # Obter modelos
        Matricula = get_model_dynamically("matriculas", "Matricula")
        Presenca = get_model_dynamically("presencas", "Presenca")
        Aluno = get_model_dynamically("alunos", "Aluno")
        Carencia = get_model_dynamically("frequencias", "Carencia")
        
        # Obter matrículas ativas na turma
        matriculas = Matricula.objects.filter(turma=self.turma, status='A')
        
        # Determinar o primeiro e último dia do mês
        ultimo_dia = calendar.monthrange(self.ano, self.mes)[1]
        data_inicio = date(self.ano, self.mes, 1)
        data_fim = date(self.ano, self.mes, ultimo_dia)
        
        # Obter atividades do mês
        Atividade = get_model_dynamically("atividades", "AtividadeAcademica")
        atividades = Atividade.objects.filter(
            turmas=self.turma,
            data_inicio__date__gte=data_inicio,
            data_inicio__date__lte=data_fim
        )
        
        total_atividades = atividades.count()
        
        # Se não houver atividades, não há como calcular carências
        if total_atividades == 0:
            return
        
        with transaction.atomic():
            # Limpar carências existentes
            Carencia.objects.filter(frequencia_mensal=self).delete()
            
            # Calcular carências para cada aluno
            for matricula in matriculas:
                aluno = matricula.aluno
                
                # Contar presenças do aluno nas atividades do mês
                presencas = Presenca.objects.filter(
                    aluno=aluno,
                    atividade__in=atividades,
                    data__gte=data_inicio,
                    data__lte=data_fim,
                    presente=True
                ).count()
                
                # Calcular percentual de presença
                percentual_presenca = (presencas / total_atividades) * 100 if total_atividades > 0 else 0
                
                # Determinar se o aluno está liberado
                liberado = percentual_presenca >= self.percentual_minimo
                
                # Calcular número de carências (aulas que faltou)
                numero_carencias = total_atividades - presencas
                
                # Criar registro de carência
                Carencia.objects.create(
                    frequencia_mensal=self,
                    aluno=aluno,
                    total_presencas=presencas,
                    total_atividades=total_atividades,
                    percentual_presenca=percentual_presenca,
                    numero_carencias=numero_carencias,
                    liberado=liberado,
                    data_identificacao=date.today(),
                    status='PENDENTE' if not liberado else None
                )

class Carencia(models.Model):
    """Modelo para registro de carências de alunos em uma frequência mensal."""
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ACOMPANHAMENTO', 'Em Acompanhamento'),
        ('RESOLVIDO', 'Resolvido'),
    ]
    
    frequencia_mensal = models.ForeignKey(
        FrequenciaMensal,
        on_delete=models.CASCADE,
        verbose_name="Frequência Mensal"
    )
    
    aluno = models.ForeignKey(
        get_aluno_model(),
        on_delete=models.CASCADE,
        verbose_name="Aluno"
    )
    
    total_presencas = models.IntegerField(
        default=0,
        verbose_name="Total de Presenças"
    )
    
    total_atividades = models.IntegerField(
        default=0,
        verbose_name="Total de Atividades"
    )
    
    percentual_presenca = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Percentual de Presença"
    )
    
    numero_carencias = models.IntegerField(
        default=0,
        verbose_name="Número de Carências"
    )
    
    liberado = models.BooleanField(
        default=False,
        verbose_name="Liberado"
    )
    
    # Adicionando o campo status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name="Status",
        null=True,
        blank=True
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Carência"
        verbose_name_plural = "Carências"
        ordering = ['frequencia_mensal', 'aluno__nome']
        unique_together = ['frequencia_mensal', 'aluno']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.frequencia_mensal}"



## Arquivos de Views Modulares:


### Arquivo: frequencias\views\__init__.py

python
"""
Pacote de views para o aplicativo de frequências.
Este arquivo permite que o diretório views seja tratado como um pacote Python.
"""

# Importar todas as funções de views que você quer expor
from .frequencia_mensal import (
    listar_frequencias,
    criar_frequencia_mensal,
    editar_frequencia_mensal,
    excluir_frequencia_mensal,
    detalhar_frequencia_mensal,
    recalcular_carencias
)

from .carencia import (
    editar_carencia,
    resolver_carencia,
    detalhar_carencia,
    iniciar_acompanhamento
)

from .notificacao import (
    criar_notificacao,
    detalhar_notificacao,
    editar_notificacao,
    enviar_notificacao,
    reenviar_notificacao,
    responder_aluno,
    listar_notificacoes_carencia
)

from .relatorio import (
    relatorio_frequencias,
    exportar_frequencia_csv,
    historico_frequencia,
    exportar_historico
)

from .dashboard import (
    dashboard,
    painel_frequencias,
    visualizar_painel_frequencias
)

from .api_views import (
    obter_dados_frequencia,
    obter_dados_painel_frequencias
)

# Importar as novas funções
from .exportacao import (
    exportar_frequencias,
    importar_frequencias
)



### Arquivo: frequencias\views\api_views.py

python
"""
API views para o aplicativo de frequências.
"""

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from importlib import import_module
import logging
import json

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

@login_required
def obter_dados_frequencia(request, frequencia_id):
    """API para obter dados de uma frequência mensal."""
    try:
        FrequenciaMensal, Carencia = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Obter carências
        carencias = Carencia.objects.filter(frequencia_mensal=frequencia).select_related('aluno')
        
        # Preparar dados
        dados = {
            'frequencia': {
                'id': frequencia.id,
                'turma': frequencia.turma.nome,
                'mes': frequencia.get_mes_display(),
                'ano': frequencia.ano,
                'percentual_minimo': frequencia.percentual_minimo
            },
            'carencias': []
        }
        
        for carencia in carencias:
            dados['carencias'].append({
                'id': carencia.id,
                'aluno': {
                    'cpf': carencia.aluno.cpf,
                    'nome': carencia.aluno.nome,
                    'email': carencia.aluno.email
                },
                'percentual_presenca': float(carencia.percentual_presenca),
                'total_presencas': carencia.total_presencas,
                'total_atividades': carencia.total_atividades,
                'liberado': carencia.liberado,
                'observacoes': carencia.observacoes or ''
            })
        
        return JsonResponse({'success': True, 'dados': dados})
    
    except Exception as e:
        logger.error(f"Erro ao obter dados da frequência: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def obter_dados_painel_frequencias(request):
    """API para obter dados para o painel de frequências."""
    try:
        # Obter parâmetros
        turma_id = request.GET.get('turma')
        mes_inicio = request.GET.get('mes_inicio')
        ano_inicio = request.GET.get('ano_inicio')
        mes_fim = request.GET.get('mes_fim')
        ano_fim = request.GET.get('ano_fim')
        
        if not all([turma_id, mes_inicio, ano_inicio, mes_fim, ano_fim]):
            return JsonResponse({'success': False, 'error': 'Parâmetros incompletos'}, status=400)
        
        FrequenciaMensal, Carencia = get_models()
        Turma = get_turma_model()
        
        # Obter turma
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Converter parâmetros para inteiros
        mes_inicio = int(mes_inicio)
        ano_inicio = int(ano_inicio)
        mes_fim = int(mes_fim)
        ano_fim = int(ano_fim)
        
        # Calcular período em meses
        data_inicio = ano_inicio * 12 + mes_inicio
        data_fim = ano_fim * 12 + mes_fim
        
        # Obter frequências no período
        frequencias = FrequenciaMensal.objects.filter(
            turma=turma
        ).prefetch_related('turmas')
        
        # Filtrar pelo período
        frequencias_filtradas = [
            f for f in frequencias
            if data_inicio <= (f.ano * 12 + f.mes) <= data_fim
        ]
        
        # Ordenar por ano e mês
        frequencias_filtradas.sort(key=lambda x: (x.ano, x.mes))
        
        # Preparar dados
        dados = {
            'turma': {
                'id': turma.id,
                'nome': turma.nome,
                'curso': turma.curso.nome if turma.curso else 'Sem curso'
            },
            'periodo': {
                'mes_inicio': mes_inicio,
                'ano_inicio': ano_inicio,
                'mes_fim': mes_fim,
                'ano_fim': ano_fim
            },
            'frequencias': []
        }
        
        for frequencia in frequencias_filtradas:
            # Obter carências
            carencias = Carencia.objects.filter(frequencia_mensal=frequencia)
            
            # Calcular estatísticas
            total_alunos = carencias.count()
            alunos_carencia = carencias.filter(percentual_presenca__lt=frequencia.percentual_minimo).count()
            
            # Adicionar dados da frequência
            dados['frequencias'].append({
                'id': frequencia.id,
                'mes': frequencia.get_mes_display(),
                'ano': frequencia.ano,
                'percentual_minimo': frequencia.percentual_minimo,
                'total_alunos': total_alunos,
                'alunos_carencia': alunos_carencia,
                'percentual_carencia': (alunos_carencia / total_alunos * 100) if total_alunos > 0 else 0
            })
        
        return JsonResponse({'success': True, 'dados': dados})
    
    except Exception as e:
        logger.error(f"Erro ao obter dados do painel: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



### Arquivo: frequencias\views\carencia.py

python
"""
Views para gerenciamento de carências.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

# Importar funções utilitárias do módulo utils
from ..utils import (
    get_models,
    get_forms,
    get_turma_model,
    get_model_dynamically
)

logger = logging.getLogger(__name__)

@login_required
def editar_carencia(request, carencia_id):
    """Edita uma carência específica."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        if request.method == 'POST':
            # Atualizar campos da carência
            liberado = request.POST.get('liberado') == 'on'
            observacoes = request.POST.get('observacoes', '')
            
            carencia.liberado = liberado
            carencia.observacoes = observacoes
            carencia.save()
            
            messages.success(request, "Carência atualizada com sucesso!")
            return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=carencia.frequencia_mensal.id)
        
        context = {
            'carencia': carencia
        }
        
        return render(request, 'frequencias/editar_carencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao editar carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar carência: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def resolver_carencia(request, carencia_id):
    """Resolve uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        if request.method == 'POST':
            # Atualizar status da carência
            carencia.status = 'RESOLVIDO'
            carencia.data_resolucao = timezone.now()
            carencia.resolvido_por = request.user
            carencia.motivo_resolucao = request.POST.get('motivo_resolucao')
            carencia.observacoes_resolucao = request.POST.get('observacoes_resolucao', '')
            carencia.liberado = True
            carencia.save()
            
            # Processar documentos anexados
            for arquivo in request.FILES.getlist('documentos'):
                Documento = get_model_dynamically("documentos", "Documento")
                
                documento = Documento.objects.create(
                    nome=arquivo.name,
                    arquivo=arquivo,
                    tipo='CARENCIA',
                    aluno=carencia.aluno,
                    uploaded_by=request.user
                )
                
                # Associar documento à carência
                carencia.documentos_resolucao.add(documento)
            
            messages.success(request, "Carência resolvida com sucesso!")
            return redirect('frequencias:detalhar_carencia', carencia_id=carencia.id)
        
        context = {
            'carencia': carencia
        }
        
        return render(request, 'frequencias/resolver_carencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao resolver carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao resolver carência: {str(e)}")
        return redirect('frequencias:detalhar_carencia', carencia_id=carencia_id)

@login_required
def detalhar_carencia(request, carencia_id):
    """Exibe os detalhes de uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        context = {
            'carencia': carencia
        }
        
        return render(request, 'frequencias/detalhar_carencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao detalhar carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar carência: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def iniciar_acompanhamento(request, carencia_id):
    """Inicia o acompanhamento de uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        if request.method == 'POST':
            # Atualizar status da carência
            carencia.status = 'EM_ACOMPANHAMENTO'
            carencia.data_acompanhamento = timezone.now()
            carencia.acompanhado_por = request.user
            carencia.observacoes = request.POST.get('observacoes', '')
            carencia.prazo_resolucao = request.POST.get('prazo_resolucao')
            carencia.save()
            
            # Criar notificação se solicitado
            if request.POST.get('criar_notificacao'):
                Notificacao = get_model_dynamically("notificacoes", "Notificacao")
                
                notificacao = Notificacao.objects.create(
                    aluno=carencia.aluno,
                    carencia=carencia,
                    assunto=request.POST.get('assunto'),
                    mensagem=request.POST.get('mensagem'),
                    criado_por=request.user,
                    data_criacao=timezone.now()
                )
                
                # Enviar notificação imediatamente se solicitado
                if request.POST.get('enviar_agora'):
                    notificacao.status = 'ENVIADA'
                    notificacao.data_envio = timezone.now()
                    notificacao.enviado_por = request.user
                    notificacao.save()
                    
                    # Lógica para enviar a notificação (e-mail, SMS, etc.)
                    try:
                        # Implementar envio de notificação
                        pass
                    except Exception as e:
                        logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                        messages.warning(request, f"Acompanhamento iniciado, mas houve um erro ao enviar a notificação: {str(e)}")
                        return redirect('frequencias:detalhar_carencia', carencia_id=carencia.id)
            
            messages.success(request, "Acompanhamento iniciado com sucesso!")
            return redirect('frequencias:detalhar_carencia', carencia_id=carencia.id)
        
        context = {
            'carencia': carencia,
            'data_atual': timezone.now().date()
        }
        
        return render(request, 'frequencias/iniciar_acompanhamento.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao iniciar acompanhamento: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao iniciar acompanhamento: {str(e)}")
        return redirect('frequencias:detalhar_carencia', carencia_id=carencia_id)



### Arquivo: frequencias\views\dashboard.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Case, When, IntegerField
from django.utils import timezone
from importlib import import_module
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia

def get_forms():
    """Obtém os formulários relacionados a frequências."""
    frequencias_forms = import_module("frequencias.forms")
    return (
        getattr(frequencias_forms, "FrequenciaMensalForm"),
        getattr(frequencias_forms, "FiltroPainelFrequenciasForm")
    )

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def dashboard(request):
    """Exibe um dashboard com estatísticas de frequência."""
    try:
        FrequenciaMensal, Carencia = get_models()
        
        # Obter parâmetros de filtro
        periodo = request.GET.get('periodo')
        curso_id = request.GET.get('curso')
        turma_id = request.GET.get('turma')
        
        # Construir query base
        frequencias = FrequenciaMensal.objects.all().prefetch_related('turmas')
        carencias = Carencia.objects.all().select_related('frequencia_mensal', 'aluno')
        
        # Aplicar filtros
        if periodo:
            ano, mes = periodo.split('-')
            frequencias = frequencias.filter(ano=ano, mes=mes)
            carencias = carencias.filter(frequencia_mensal__ano=ano, frequencia_mensal__mes=mes)
        
        if curso_id:
            frequencias = frequencias.filter(turma__curso__codigo_curso=curso_id)
            carencias = carencias.filter(frequencia_mensal__turma__curso__codigo_curso=curso_id)
        
        if turma_id:
            frequencias = frequencias.filter(turma__id=turma_id)
            carencias = carencias.filter(frequencia_mensal__turma__id=turma_id)
        
        # Calcular estatísticas
        total_alunos = carencias.values('aluno').distinct().count()
        alunos_regulares = carencias.filter(percentual_presenca__gte=75).values('aluno').distinct().count()
        alunos_carencia = carencias.filter(percentual_presenca__lt=75).values('aluno').distinct().count()
        
        # Calcular média de frequência
        from django.db.models import Avg
        media_frequencia = carencias.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
        
        # Obter turmas com menor frequência
        turmas_menor_frequencia = []
        turmas_ids = frequencias.values_list('turma__id', flat=True).distinct()
        
        for turma_id in turmas_ids:
            carencias_turma = carencias.filter(frequencia_mensal__turma__id=turma_id)
            if carencias_turma.exists():
                media_turma = carencias_turma.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
                alunos_carencia_turma = carencias_turma.filter(percentual_presenca__lt=75).count()
                total_alunos_turma = carencias_turma.count()
                
                # Obter informações da turma
                turma = get_turma_model().objects.get(id=turma_id)
                
                # Obter período (mês/ano) da frequência mais recente
                ultima_frequencia = frequencias.filter(turma__id=turma_id).order_by('-ano', '-mes').first()
                
                turmas_menor_frequencia.append({
                    'id': turma_id,
                    'nome': turma.nome,
                    'curso': turma.curso,
                    'media_frequencia': media_turma,
                    'alunos_carencia': alunos_carencia_turma,
                    'total_alunos': total_alunos_turma,
                    'periodo_mes': ultima_frequencia.get_mes_display() if ultima_frequencia else '',
                    'periodo_ano': ultima_frequencia.ano if ultima_frequencia else ''
                })
        
        # Ordenar turmas por média de frequência (ascendente)
        turmas_menor_frequencia.sort(key=lambda x: x['media_frequencia'])
        
        # Limitar a 5 turmas
        turmas_menor_frequencia = turmas_menor_frequencia[:5]
        
        # Obter alunos com menor frequência
        alunos_menor_frequencia = []
        alunos_ids = carencias.filter(percentual_presenca__lt=75).values_list('aluno__cpf', flat=True).distinct()
        
        for aluno_id in alunos_ids:
            carencia_aluno = carencias.filter(aluno__cpf=aluno_id).order_by('percentual_presenca').first()
            if carencia_aluno:
                alunos_menor_frequencia.append({
                    'cpf': aluno_id,
                    'nome': carencia_aluno.aluno.nome,
                    'email': carencia_aluno.aluno.email,
                    'foto': carencia_aluno.aluno.foto.url if carencia_aluno.aluno.foto else None,
                    'turma': carencia_aluno.frequencia_mensal.turma.nome,
                    'curso': carencia_aluno.frequencia_mensal.turma.curso.nome,
                    'percentual_presenca': carencia_aluno.percentual_presenca,
                    'periodo_mes': carencia_aluno.frequencia_mensal.get_mes_display(),
                    'periodo_ano': carencia_aluno.frequencia_mensal.ano,
                    'carencia_id': carencia_aluno.id,
                    'status_carencia': carencia_aluno.status if hasattr(carencia_aluno, 'status') else 'PENDENTE'
                })
        
        # Ordenar alunos por percentual de presença (ascendente)
        alunos_menor_frequencia.sort(key=lambda x: x['percentual_presenca'])
        
        # Limitar a 10 alunos
        alunos_menor_frequencia = alunos_menor_frequencia[:10]
        
        # Dados para gráficos
        # 1. Frequência por curso
        cursos_labels = []
        frequencia_por_curso = []
        
        Curso = get_model_dynamically("cursos", "Curso")
        cursos = Curso.objects.all()
        
        for curso in cursos:
            carencias_curso = carencias.filter(frequencia_mensal__turma__curso=curso)
            if carencias_curso.exists():
                media_curso = carencias_curso.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
                cursos_labels.append(curso.nome)
                frequencia_por_curso.append(float(media_curso))
        
        # 2. Evolução da frequência por período
        periodos_labels = []
        evolucao_frequencia = []
        
        # Obter últimos 6 meses
        hoje = datetime.now()
        for i in range(5, -1, -1):
            data = hoje - timedelta(days=30 * i)
            mes = data.month
            ano = data.year
            
            # Obter frequências do mês
            carencias_periodo = carencias.filter(frequencia_mensal__mes=mes, frequencia_mensal__ano=ano)
            if carencias_periodo.exists():
                media_periodo = carencias_periodo.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
                mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(mes)
                periodos_labels.append(f"{mes_nome}/{ano}")
                evolucao_frequencia.append(float(media_periodo))
            else:
                mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(mes)
                periodos_labels.append(f"{mes_nome}/{ano}")
                evolucao_frequencia.append(0)
        
        # Obter dados para filtros
        anos = FrequenciaMensal.objects.values_list('ano', flat=True).distinct().order_by('-ano')
        meses = FrequenciaMensal.MES_CHOICES
        
        # Obter contagem por status
        status_counts = {}
        for status, _ in getattr(FrequenciaMensal, 'STATUS_CHOICES', []):
            count = FrequenciaMensal.objects.filter(status=status).count()
            status_counts[status] = count
        
        # Obter contagem por tipo
        academicas_por_tipo = {}
        for tipo, _ in getattr(FrequenciaMensal, 'TIPO_CHOICES', []):
            count = FrequenciaMensal.objects.filter(tipo_atividade=tipo).count()
            academicas_por_tipo[tipo] = count
        
        context = {
            'estatisticas': {
                'total_alunos': total_alunos,
                'alunos_regulares': alunos_regulares,
                'alunos_carencia': alunos_carencia,
                'media_frequencia': media_frequencia
            },
            'turmas_menor_frequencia': turmas_menor_frequencia,
            'alunos_menor_frequencia': alunos_menor_frequencia,
            'cursos_labels': json.dumps(cursos_labels),
            'frequencia_por_curso': json.dumps(frequencia_por_curso),
            'periodos_labels': json.dumps(periodos_labels),
            'evolucao_frequencia': json.dumps(evolucao_frequencia),
            'filtros': {
                'periodo': periodo,
                'curso': curso_id,
                'turma': turma_id
            },
            'anos': anos,
            'meses': meses,
            'cursos': cursos,
            'turmas': get_turma_model().objects.filter(status='A'),
            'status_counts': status_counts,
            'academicas_por_tipo': academicas_por_tipo
        }
        
        return render(request, 'frequencias/dashboard.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao exibir dashboard: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exibir dashboard: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def painel_frequencias(request):
    """Exibe um painel de frequências para uma turma."""
    try:
        _, FiltroPainelFrequenciasForm = get_forms()
        
        if request.method == 'POST':
            form = FiltroPainelFrequenciasForm(request.POST)
            if form.is_valid():
                # Redirecionar para a página do painel com os parâmetros
                return redirect('frequencias:visualizar_painel_frequencias', 
                               turma_id=form.cleaned_data['turma'].id,
                               mes_inicio=form.cleaned_data['mes_inicio'],
                               ano_inicio=form.cleaned_data['ano_inicio'],
                               mes_fim=form.cleaned_data['mes_fim'],
                               ano_fim=form.cleaned_data['ano_fim'])
        else:
            form = FiltroPainelFrequenciasForm()
        
        context = {
            'form': form
        }
        
        return render(request, 'frequencias/painel_frequencias_form.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao acessar painel de frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao acessar painel de frequências: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def visualizar_painel_frequencias(request, turma_id, mes_inicio, ano_inicio, mes_fim, ano_fim):
    """Visualiza o painel de frequências para uma turma em um período."""
    try:
        FrequenciaMensal, _ = get_models()
        Turma = get_turma_model()
        
        # Obter turma
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Converter parâmetros para inteiros
        mes_inicio = int(mes_inicio)
        ano_inicio = int(ano_inicio)
        mes_fim = int(mes_fim)
        ano_fim = int(ano_fim)
        
        # Calcular período em meses
        data_inicio = ano_inicio * 12 + mes_inicio
        data_fim = ano_fim * 12 + mes_fim
        
        # Obter frequências no período
        frequencias = FrequenciaMensal.objects.filter(
            turma=turma
        ).prefetch_related('turmas')
        
        # Filtrar pelo período
        frequencias_filtradas = [
            f for f in frequencias
            if data_inicio <= (f.ano * 12 + f.mes) <= data_fim
        ]
        
        # Ordenar por ano e mês
        frequencias_filtradas.sort(key=lambda x: (x.ano, x.mes))
        
        context = {
            'turma': turma,
            'mes_inicio': mes_inicio,
            'ano_inicio': ano_inicio,
            'mes_fim': mes_fim,
            'ano_fim': ano_fim,
            'frequencias': frequencias_filtradas
        }
        
        return render(request, 'frequencias/visualizar_painel_frequencias.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao visualizar painel de frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao visualizar painel de frequências: {str(e)}")
        return redirect('frequencias:painel_frequencias')



### Arquivo: frequencias\views\exportacao.py

python
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from ..utils import get_model_dynamically

logger = logging.getLogger(__name__)

@login_required
def exportar_frequencias(request):
    """Exporta os dados de frequências mensais para um arquivo CSV."""
    try:
        import csv
        
        FrequenciaMensal = get_model_dynamically("frequencias", "FrequenciaMensal")
        frequencias = FrequenciaMensal.objects.all().select_related('turma', 'turma__curso')
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="frequencias.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "ID",
            "Turma",
            "Curso",
            "Mês",
            "Ano",
            "Percentual Mínimo",
            "Total de Alunos",
            "Alunos com Carência",
            "Alunos Liberados"
        ])
        
        for freq in frequencias:
            writer.writerow([
                freq.id,
                freq.turma.nome,
                freq.turma.curso.nome if freq.turma.curso else "",
                freq.get_mes_display(),
                freq.ano,
                freq.percentual_minimo,
                freq.total_alunos,
                freq.alunos_com_carencia,
                freq.alunos_liberados
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar frequências: {str(e)}")
        return redirect("frequencias:listar_frequencias")

@login_required
def importar_frequencias(request):
    """Importa frequências mensais de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper
            
            FrequenciaMensal = get_model_dynamically("frequencias", "FrequenciaMensal")
            Turma = get_model_dynamically("turmas", "Turma")
            
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Buscar turma pelo nome ou ID
                    turma = None
                    turma_nome = row.get("Turma", "").strip()
                    if turma_nome:
                        try:
                            turma = Turma.objects.get(nome=turma_nome)
                        except Turma.DoesNotExist:
                            try:
                                turma = Turma.objects.get(id=turma_nome)
                            except (Turma.DoesNotExist, ValueError):
                                errors.append(f"Turma não encontrada: {turma_nome}")
                                continue
                    else:
                        errors.append("Turma não especificada")
                        continue
                    
                    # Processar mês
                    mes = None
                    mes_nome = row.get("Mês", "").strip()
                    if mes_nome:
                        # Mapear nome do mês para número
                        meses = {
                            "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
                            "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
                            "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
                        }
                        mes = meses.get(mes_nome)
                        if not mes:
                            try:
                                mes = int(mes_nome)
                                if mes < 1 or mes > 12:
                                    errors.append(f"Mês inválido: {mes_nome}")
                                    continue
                            except ValueError:
                                errors.append(f"Mês inválido: {mes_nome}")
                                continue
                    else:
                        errors.append("Mês não especificado")
                        continue
                    
                    # Processar ano
                    ano = None
                    try:
                        ano = int(row.get("Ano", "").strip())
                    except ValueError:
                        errors.append(f"Ano inválido: {row.get('Ano', '')}")
                        continue
                    
                    # Processar percentual mínimo
                    percentual_minimo = 75  # Valor padrão
                    try:
                        if row.get("Percentual Mínimo"):
                            percentual_minimo = int(row.get("Percentual Mínimo"))
                    except ValueError:
                        errors.append(f"Percentual mínimo inválido: {row.get('Percentual Mínimo', '')}")
                        continue
                    
                    # Verificar se já existe uma frequência para esta turma/mês/ano
                    if FrequenciaMensal.objects.filter(turma=turma, mes=mes, ano=ano).exists():
                        errors.append(f"Já existe uma frequência para a turma {turma.nome} no mês {mes}/{ano}")
                        continue
                    
                    # Criar a frequência mensal
                    frequencia = FrequenciaMensal.objects.create(
                        turma=turma,
                        mes=mes,
                        ano=ano,
                        percentual_minimo=percentual_minimo
                    )
                    
                    # Calcular carências
                    frequencia.calcular_carencias()
                    
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(
                    request,
                    f"{count} frequências importadas com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} frequências importadas com sucesso!"
                )
            return redirect("frequencias:listar_frequencias")
        except Exception as e:
            messages.error(request, f"Erro ao importar frequências: {str(e)}")
    
    return render(request, "frequencias/importar_frequencias.html")



### Arquivo: frequencias\views\frequencia_mensal.py

python
"""
Views para gerenciamento de frequências mensais.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import logging
import json

# Importar funções utilitárias do módulo utils
from frequencias.utils import (
    get_models,
    get_forms,
    get_turma_model,
    get_model_dynamically
)

logger = logging.getLogger(__name__)

@login_required
def listar_frequencias(request):
    """Lista todas as frequências mensais."""
    try:
        FrequenciaMensal, _ = get_models()
        
        # Aplicar filtros
        frequencias = FrequenciaMensal.objects.all().prefetch_related('turmas')
        
        # Filtrar por turma
        turma_id = request.GET.get('turma')
        if turma_id:
            frequencias = frequencias.filter(turma_id=turma_id)
        
        # Filtrar por ano
        ano = request.GET.get('ano')
        if ano:
            frequencias = frequencias.filter(ano=ano)
        
        # Ordenar
        frequencias = frequencias.order_by('-ano', '-mes', 'turma__nome')
        
        # Paginação
        paginator = Paginator(frequencias, 20)  # 20 itens por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Obter turmas para filtro
        Turma = get_turma_model()
        turmas = Turma.objects.filter(status='A')
        
        # Obter anos disponíveis
        anos = FrequenciaMensal.objects.values_list('ano', flat=True).distinct().order_by('-ano')
        
        context = {
            'frequencias': page_obj,
            'page_obj': page_obj,
            'turmas': turmas,
            'anos': anos,
            'turma_selecionada': turma_id,
            'ano_selecionado': ano
        }
        
        return render(request, 'frequencias/listar_frequencias.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao listar frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao listar frequências: {str(e)}")
        return redirect('home')

@login_required
def criar_frequencia_mensal(request):
    """Cria uma nova frequência mensal."""
    try:
        FrequenciaMensalForm, _ = get_forms()
        
        if request.method == 'POST':
            form = FrequenciaMensalForm(request.POST)
            if form.is_valid():
                frequencia = form.save()
                
                # Calcular carências automaticamente
                frequencia.calcular_carencias()
                
                messages.success(request, "Frequência mensal criada com sucesso!")
                return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia.id)
        else:
            form = FrequenciaMensalForm()
        
        context = {
            'form': form,
            'titulo': 'Criar Frequência Mensal'
        }
        
        return render(request, 'frequencias/formulario_frequencia_mensal.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao criar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao criar frequência mensal: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def editar_frequencia_mensal(request, frequencia_id):
    """Edita uma frequência mensal existente."""
    try:
        FrequenciaMensal, _ = get_models()
        FrequenciaMensalForm, _ = get_forms()
        
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        if request.method == 'POST':
            form = FrequenciaMensalForm(request.POST, instance=frequencia)
            if form.is_valid():
                frequencia = form.save()
                
                # Recalcular carências se necessário
                if 'recalcular' in request.POST:
                    frequencia.calcular_carencias()
                    messages.success(request, "Frequência mensal atualizada e carências recalculadas!")
                else:
                    messages.success(request, "Frequência mensal atualizada com sucesso!")
                
                return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia.id)
        else:
            form = FrequenciaMensalForm(instance=frequencia)
        
        context = {
            'form': form,
            'frequencia': frequencia,
            'titulo': 'Editar Frequência Mensal'
        }
        
        return render(request, 'frequencias/formulario_frequencia_mensal.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao editar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar frequência mensal: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def excluir_frequencia_mensal(request, frequencia_id):
    """Exclui uma frequência mensal."""
    try:
        FrequenciaMensal, _ = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        if request.method == 'POST':
            frequencia.delete()
            messages.success(request, "Frequência mensal excluída com sucesso!")
            return redirect('frequencias:listar_frequencias')
        
        context = {
            'frequencia': frequencia
        }
        
        return render(request, 'frequencias/excluir_frequencia_mensal.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao excluir frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao excluir frequência mensal: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def detalhar_frequencia_mensal(request, frequencia_id):
    """Exibe os detalhes de uma frequência mensal."""
    try:
        FrequenciaMensal, Carencia = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Obter carências
        carencias = Carencia.objects.filter(frequencia_mensal=frequencia).select_related('aluno')
        
        # Ordenar carências
        carencias = carencias.order_by('liberado', 'aluno__nome')
        
        # Preparar dados para gráfico
        alunos_labels = []
        percentuais_presenca = []
        
        for carencia in carencias:
            alunos_labels.append(carencia.aluno.nome)
            percentuais_presenca.append(float(carencia.percentual_presenca))
        
        # Calcular total de alunos
        total_alunos = carencias.count()
        
        context = {
            'frequencia': frequencia,
            'carencias': carencias,
            'total_alunos': total_alunos,
            'alunos_labels': json.dumps(alunos_labels),
            'percentuais_presenca': json.dumps(percentuais_presenca)
        }
        
        return render(request, 'frequencias/detalhar_frequencia_mensal.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao detalhar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar frequência mensal: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def recalcular_carencias(request, frequencia_id):
    """Recalcula as carências de uma frequência mensal."""
    try:
        FrequenciaMensal, _ = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Recalcular carências
        frequencia.calcular_carencias()
        
        messages.success(request, "Carências recalculadas com sucesso!")
        return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia.id)
    
    except Exception as e:
        logger.error(f"Erro ao recalcular carências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao recalcular carências: {str(e)}")
        return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia_id)



### Arquivo: frequencias\views\notificacao.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from importlib import import_module
import logging

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def criar_notificacao(request, carencia_id):
    """Cria uma notificação para uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)
        
        if request.method == 'POST':
            Notificacao = get_model_dynamically("notificacoes", "Notificacao")
            
            notificacao = Notificacao.objects.create(
                aluno=carencia.aluno,
                carencia=carencia,
                assunto=request.POST.get('assunto'),
                mensagem=request.POST.get('mensagem'),
                tipo_notificacao=request.POST.get('tipo_notificacao'),
                prioridade=request.POST.get('prioridade'),
                criado_por=request.user,
                data_criacao=timezone.now()
            )
            
            # Processar anexos
            for arquivo in request.FILES.getlist('anexos'):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                
                anexo = Anexo.objects.create(
                    notificacao=notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user
                )
            
            # Enviar notificação imediatamente se solicitado
            if request.POST.get('enviar_agora'):
                notificacao.status = 'ENVIADA'
                notificacao.data_envio = timezone.now()
                notificacao.enviado_por = request.user
                notificacao.save()
                
                # Lógica para enviar a notificação (e-mail, SMS, etc.)
                try:
                    # Implementar envio de notificação
                    pass
                except Exception as e:
                    logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                    messages.warning(request, f"Notificação criada, mas houve um erro ao enviá-la: {str(e)}")
                    return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
            
            messages.success(request, "Notificação criada com sucesso!")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        context = {
            'carencia': carencia
        }
        
        return render(request, 'frequencias/criar_notificacao.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao criar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao criar notificação: {str(e)}")
        return redirect('frequencias:detalhar_carencia', carencia_id=carencia_id)

@login_required
def detalhar_notificacao(request, notificacao_id):
    """Exibe os detalhes de uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        context = {
            'notificacao': notificacao
        }
        
        return render(request, 'frequencias/detalhar_notificacao.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao detalhar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar notificação: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def editar_notificacao(request, notificacao_id):
    """Edita uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        # Verificar se a notificação já foi enviada
        if notificacao.status != 'PENDENTE':
            messages.warning(request, "Esta notificação já foi enviada e não pode ser editada.")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        if request.method == 'POST':
            action = request.POST.get('action', 'salvar')
            
            # Atualizar dados da notificação
            notificacao.assunto = request.POST.get('assunto')
            notificacao.mensagem = request.POST.get('mensagem')
            
            # Processar anexos
            for arquivo in request.FILES.getlist('anexos'):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                
                anexo = Anexo.objects.create(
                    notificacao=notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user
                )
            
            # Remover anexos selecionados
            for anexo_id in request.POST.getlist('remover_anexos'):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                anexo = get_object_or_404(Anexo, id=anexo_id)
                anexo.delete()
            
            notificacao.save()
            
            # Enviar notificação se solicitado
            if action == 'salvar_enviar':
                notificacao.status = 'ENVIADA'
                notificacao.data_envio = timezone.now()
                notificacao.enviado_por = request.user
                notificacao.save()
                
                # Lógica para enviar a notificação (e-mail, SMS, etc.)
                try:
                    # Implementar envio de notificação
                    pass
                except Exception as e:
                    logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                    messages.warning(request, f"Notificação atualizada, mas houve um erro ao enviá-la: {str(e)}")
                    return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
                
                messages.success(request, "Notificação atualizada e enviada com sucesso!")
            else:
                messages.success(request, "Notificação atualizada com sucesso!")
            
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        context = {
            'notificacao': notificacao
        }
        
        return render(request, 'frequencias/editar_notificacao.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao editar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar notificação: {str(e)}")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao_id)

@login_required
def enviar_notificacao(request, notificacao_id):
    """Envia uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        # Verificar se a notificação já foi enviada
        if notificacao.status != 'PENDENTE':
            messages.warning(request, "Esta notificação já foi enviada.")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        if request.method == 'POST':
            # Atualizar status da notificação
            notificacao.status = 'ENVIADA'
            notificacao.data_envio = timezone.now()
            notificacao.enviado_por = request.user
            
            # Atualizar status da carência se solicitado
            if request.POST.get('marcar_acompanhamento') and notificacao.carencia and notificacao.carencia.status == 'PENDENTE':
                notificacao.carencia.status = 'EM_ACOMPANHAMENTO'
                notificacao.carencia.data_acompanhamento = timezone.now()
                notificacao.carencia.acompanhado_por = request.user
                notificacao.carencia.save()
            
            notificacao.save()
            
            # Enviar cópia para o usuário se solicitado
            enviar_copia = request.POST.get('enviar_copia')
            
            # Lógica para enviar a notificação (e-mail, SMS, etc.)
            try:
                # Implementar envio de notificação
                pass
            except Exception as e:
                logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                messages.warning(request, f"Houve um erro ao enviar a notificação: {str(e)}")
                return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
            
            messages.success(request, "Notificação enviada com sucesso!")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        context = {
            'notificacao': notificacao
        }
        
        return render(request, 'frequencias/enviar_notificacao.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao enviar notificação: {str(e)}")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao_id)

@login_required
def reenviar_notificacao(request, notificacao_id):
    """Reenvia uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        # Verificar se a notificação pode ser reenviada
        if notificacao.status not in ['ENVIADA', 'LIDA']:
            messages.warning(request, "Esta notificação não pode ser reenviada.")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        # Atualizar data de envio
        notificacao.data_envio = timezone.now()
        notificacao.enviado_por = request.user
        notificacao.save()
        
        # Lógica para reenviar a notificação (e-mail, SMS, etc.)
        try:
            # Implementar reenvio de notificação
            pass
        except Exception as e:
            logger.error(f"Erro ao reenviar notificação: {str(e)}", exc_info=True)
            messages.warning(request, f"Houve um erro ao reenviar a notificação: {str(e)}")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        messages.success(request, "Notificação reenviada com sucesso!")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
    
    except Exception as e:
        logger.error(f"Erro ao reenviar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao reenviar notificação: {str(e)}")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao_id)

@login_required
def responder_aluno(request, notificacao_id):
    """Responde a uma notificação do aluno."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)
        
        # Verificar se a notificação pode ser respondida
        if notificacao.status != 'RESPONDIDA':
            messages.warning(request, "Esta notificação não possui resposta do aluno.")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao.id)
        
        if request.method == 'POST':
            # Criar nova notificação como resposta
            nova_notificacao = Notificacao.objects.create(
                aluno=notificacao.aluno,
                carencia=notificacao.carencia,
                assunto=f"RE: {notificacao.assunto}",
                mensagem=request.POST.get('mensagem'),
                tipo_notificacao=notificacao.tipo_notificacao,
                prioridade=notificacao.prioridade,
                criado_por=request.user,
                data_criacao=timezone.now(),
                notificacao_pai=notificacao
            )
            
            # Processar anexos
            for arquivo in request.FILES.getlist('anexos'):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                
                anexo = Anexo.objects.create(
                    notificacao=nova_notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user
                )
            
            # Enviar notificação imediatamente
            nova_notificacao.status = 'ENVIADA'
            nova_notificacao.data_envio = timezone.now()
            nova_notificacao.enviado_por = request.user
            nova_notificacao.save()
            
            # Lógica para enviar a notificação (e-mail, SMS, etc.)
            try:
                # Implementar envio de notificação
                pass
            except Exception as e:
                logger.error(f"Erro ao enviar resposta: {str(e)}", exc_info=True)
                messages.warning(request, f"Resposta criada, mas houve um erro ao enviá-la: {str(e)}")
                return redirect('frequencias:detalhar_notificacao', notificacao_id=nova_notificacao.id)
            
            messages.success(request, "Resposta enviada com sucesso!")
            return redirect('frequencias:detalhar_notificacao', notificacao_id=nova_notificacao.id)
        
        context = {
            'notificacao': notificacao
        }
        
        return render(request, 'frequencias/responder_aluno.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao responder aluno: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao responder aluno: {str(e)}")
        return redirect('frequencias:detalhar_notificacao', notificacao_id=notificacao_id)

@login_required
def listar_notificacoes_carencia(request):
    """Lista todas as notificações de carência."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        
        # Obter parâmetros de filtro
        status = request.GET.get('status')
        aluno_id = request.GET.get('aluno')
        tipo = request.GET.get('tipo')
        
        # Construir query base
        notificacoes = Notificacao.objects.filter(carencia__isnull=False).select_related('aluno', 'carencia')
        
        # Aplicar filtros
        if status:
            notificacoes = notificacoes.filter(status=status)
        
        if aluno_id:
            notificacoes = notificacoes.filter(aluno__cpf=aluno_id)
        
        if tipo:
            notificacoes = notificacoes.filter(tipo_notificacao=tipo)
            
        # Ordenar por data de criação (mais recente primeiro)
        notificacoes = notificacoes.order_by('-data_criacao')
        
        # Paginação
        paginator = Paginator(notificacoes, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'notificacoes': page_obj,
            'page_obj': page_obj,
            'filtros': {
                'status': status,
                'aluno': aluno_id,
                'tipo': tipo
            }
        }
        
        return render(request, 'frequencias/listar_notificacoes.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao listar notificações: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao listar notificações: {str(e)}")
        return redirect('frequencias:listar_frequencias')



### Arquivo: frequencias\views\relatorio.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Case, When, IntegerField
from django.http import HttpResponse
from importlib import import_module
import logging
import csv
import json

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def relatorio_frequencias(request):
    """Exibe um relatório de frequências."""
    try:
        FrequenciaMensal, Carencia = get_models()
        
        # Estatísticas gerais
        total_frequencias = FrequenciaMensal.objects.count()
        
        # Obter total de alunos com carência
        total_carencias = Carencia.objects.count()
        total_liberados = Carencia.objects.filter(liberado=True).count()
        total_nao_liberados = total_carencias - total_liberados
        
        # Percentuais
        percentual_liberados = (total_liberados / total_carencias * 100) if total_carencias > 0 else 0
        percentual_nao_liberados = (total_nao_liberados / total_carencias * 100) if total_carencias > 0 else 0
        
        # Frequências por mês
        from django.db.models import Count
        from django.db.models.functions import TruncMonth
        
        # Agrupar por mês e ano
        frequencias_por_mes = FrequenciaMensal.objects.values('mes', 'ano').annotate(
            total=Count('id')
        ).order_by('ano', 'mes')
        
        # Formatar dados para gráficos
        meses = []
        dados_frequencias = []
        
        for item in frequencias_por_mes:
            mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(item['mes'])
            meses.append(f"{mes_nome}/{item['ano']}")
            dados_frequencias.append(item['total'])
        
        context = {
            'total_frequencias': total_frequencias,
            'total_carencias': total_carencias,
            'total_liberados': total_liberados,
            'total_nao_liberados': total_nao_liberados,
            'percentual_liberados': percentual_liberados,
            'percentual_nao_liberados': percentual_nao_liberados,
            'meses': meses,
            'dados_frequencias': dados_frequencias
        }
        
        return render(request, 'frequencias/relatorio_frequencias.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao gerar relatório: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def exportar_frequencia_csv(request, frequencia_id):
    """Exporta os dados de uma frequência mensal para CSV."""
    try:
        FrequenciaMensal, Carencia = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Obter carências
        carencias = Carencia.objects.filter(frequencia_mensal=frequencia).select_related('aluno')
        
        # Criar resposta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="frequencia_{frequencia.turma.nome}_{frequencia.get_mes_display()}_{frequencia.ano}.csv"'
        
        # Escrever cabeçalho e dados
        writer = csv.writer(response)
        writer.writerow(['CPF', 'Aluno', 'Presenças', 'Total Atividades', 'Percentual', 'Carências', 'Liberado', 'Observações'])
        
        for carencia in carencias:
            writer.writerow([
                carencia.aluno.cpf,
                carencia.aluno.nome,
                carencia.total_presencas,
                carencia.total_atividades,
                f"{carencia.percentual_presenca:.2f}",
                carencia.numero_carencias,
                'Sim' if carencia.liberado else 'Não',
                carencia.observacoes or ''
            ])
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao exportar frequência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar frequência: {str(e)}")
        return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia_id)

@login_required
def historico_frequencia(request, aluno_cpf):
    """Exibe o histórico de frequência de um aluno."""
    try:
        FrequenciaMensal, Carencia = get_models()
        Aluno = get_model_dynamically("alunos", "Aluno")
        
        # Obter aluno
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        
        # Obter parâmetros de filtro
        curso_id = request.GET.get('curso')
        turma_id = request.GET.get('turma')
        periodo = request.GET.get('periodo')
        
        # Construir query base
        carencias = Carencia.objects.filter(aluno=aluno).select_related('frequencia_mensal', 'frequencia_mensal__turma')
        
        # Aplicar filtros
        if curso_id:
            carencias = carencias.filter(frequencia_mensal__turma__curso__codigo_curso=curso_id)
        
        if turma_id:
            carencias = carencias.filter(frequencia_mensal__turma__id=turma_id)
        
        if periodo:
            ano, mes = periodo.split('-')
            carencias = carencias.filter(frequencia_mensal__ano=ano, frequencia_mensal__mes=mes)
        
        # Ordenar por período (mais recente primeiro)
        carencias = carencias.order_by('-frequencia_mensal__ano', '-frequencia_mensal__mes')
        
        # Paginação
        paginator = Paginator(carencias, 10)  # 10 itens por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Calcular média geral de frequência
        from django.db.models import Avg
        media_geral = carencias.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
        
        # Dados para gráfico de evolução
        periodos_labels = []
        percentuais_presenca = []
        
        # Limitar a 12 períodos mais recentes
        for carencia in carencias[:12]:
            periodo_label = f"{carencia.frequencia_mensal.get_mes_display()}/{carencia.frequencia_mensal.ano}"
            periodos_labels.append(periodo_label)
            percentuais_presenca.append(float(carencia.percentual_presenca))
        
        # Inverter para ordem cronológica
        periodos_labels.reverse()
        percentuais_presenca.reverse()
        
        # Obter dados para filtros
        Curso = get_model_dynamically("cursos", "Curso")
        cursos = Curso.objects.all()
        
        Turma = get_turma_model()
        turmas = Turma.objects.filter(matriculas__aluno=aluno).distinct()
        
        anos = FrequenciaMensal.objects.filter(carencia__aluno=aluno).values_list('ano', flat=True).distinct().order_by('-ano')
        meses = FrequenciaMensal.MES_CHOICES
        
        context = {
            'aluno': aluno,
            'registros': page_obj,
            'total_registros': carencias.count(),
            'media_geral': media_geral,
            'carencias': carencias.filter(percentual_presenca__lt=75),
            'periodos_labels': json.dumps(periodos_labels),
            'percentuais_presenca': json.dumps(percentuais_presenca),
            'filtros': {
                'curso': curso_id,
                'turma': turma_id,
                'periodo': periodo
            },
            'cursos': cursos,
            'turmas': turmas,
            'anos': anos,
            'meses': meses
        }
        
        return render(request, 'frequencias/historico_frequencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao exibir histórico de frequência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exibir histórico de frequência: {str(e)}")
        return redirect('alunos:detalhar_aluno', cpf=aluno_cpf)

@login_required
def exportar_historico(request, aluno_cpf):
    """Exporta o histórico de frequência de um aluno para CSV."""
    try:
        _, Carencia = get_models()
        Aluno = get_model_dynamically("alunos", "Aluno")
        
        # Obter aluno
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        
        # Obter carências
        carencias = Carencia.objects.filter(aluno=aluno).select_related('frequencia_mensal', 'frequencia_mensal__turma')
        
        # Criar resposta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="historico_frequencia_{aluno.nome}.csv"'
        
        # Escrever cabeçalho e dados
        writer = csv.writer(response)
        writer.writerow(['Curso', 'Turma', 'Período', 'Presenças', 'Faltas', 'Total Aulas', 'Percentual', 'Status'])
        
        for carencia in carencias:
            writer.writerow([
                carencia.frequencia_mensal.turma.curso.nome,
                carencia.frequencia_mensal.turma.nome,
                f"{carencia.frequencia_mensal.get_mes_display()}/{carencia.frequencia_mensal.ano}",
                carencia.total_presencas,
                carencia.total_atividades - carencia.total_presencas,
                carencia.total_atividades,
                f"{carencia.percentual_presenca:.2f}",
                'Regular' if carencia.percentual_presenca >= 75 else 'Carência'
            ])
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao exportar histórico: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar histórico: {str(e)}")
        return redirect('frequencias:historico_frequencia', aluno_cpf=aluno_cpf)


## Arquivos de Template:


### Arquivo: frequencias\includes\form_frequencia.html

html
{% comment %}
Componente para renderizar formulários de frequência
Uso: {% include 'frequencias/includes/form_frequencia.html' with form=form %}
{% endcomment %}

{% if form.non_field_errors %}
<div class="alert alert-danger">
    {% for error in form.non_field_errors %}
    <p>{{ error }}</p>
    {% endfor %}
</div>
{% endif %}

<div class="mb-3">
    <label for="{{ form.turma.id_for_label }}" class="form-label">{{ form.turma.label }}</label>
    {{ form.turma }}
    {% if form.turma.errors %}
    <div class="invalid-feedback d-block">
        {% for error in form.turma.errors %}
        {{ error }}
        {% endfor %}
    </div>
    {% endif %}
    {% if form.turma.help_text %}
    <div class="form-text">{{ form.turma.help_text }}</div>
    {% endif %}
</div>

<div class="row">
    <div class="col-md-6">
        <div class="mb-3">
            <label for="{{ form.mes.id_for_label }}" class="form-label">{{ form.mes.label }}</label>
            {{ form.mes }}
            {% if form.mes.errors %}
            <div class="invalid-feedback d-block">
                {% for error in form.mes.errors %}
                {{ error }}
                {% endfor %}
            </div>
            {% endif %}
            {% if form.mes.help_text %}
            <div class="form-text">{{ form.mes.help_text }}</div>
            {% endif %}
        </div>
    </div>
    <div class="col-md-6">
        <div class="mb-3">
            <label for="{{ form.ano.id_for_label }}" class="form-label">{{ form.ano.label }}</label>
            {{ form.ano }}
            {% if form.ano.errors %}
            <div class="invalid-feedback d-block">
                {% for error in form.ano.errors %}
                {{ error }}
                {% endfor %}
            </div>
            {% endif %}
            {% if form.ano.help_text %}
            <div class="form-text">{{ form.ano.help_text }}</div>
            {% endif %}
        </div>
    </div>
</div>

<div class="mb-3">
    <label for="{{ form.percentual_minimo.id_for_label }}" class="form-label">
        {{ form.percentual_minimo.label }}
    </label>
    <div class="input-group">
        {{ form.percentual_minimo }}
        <span class="input-group-text">%</span>
    </div>
    {% if form.percentual_minimo.errors %}
    <div class="invalid-feedback d-block">
        {% for error in form.percentual_minimo.errors %}
        {{ error }}
        {% endfor %}
    </div>
    {% endif %}
    {% if form.percentual_minimo.help_text %}
    <div class="form-text">{{ form.percentual_minimo.help_text }}</div>
    {% endif %}
</div>



### Arquivo: frequencias\templates\frequencias\criar_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Criar Notificação de Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Criar Notificação de Carência</h1>
        <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Informações da carência -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Informações da Carência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ carencia.aluno.nome }}</p>
                    <p><strong>Curso:</strong> {{ carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Turma:</strong> {{ carencia.frequencia_mensal.turma.nome }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Período:</strong> {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                    <p><strong>Percentual de Presença:</strong> {{ carencia.percentual_presenca }}%</p>
                    <p><strong>Status:</strong> {{ carencia.get_status_display }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Formulário de notificação -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Nova Notificação</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="assunto" class="form-label">Assunto</label>
                    <input type="text" class="form-control" id="assunto" name="assunto" 
                           value="Notificação de Carência - {{ carencia.frequencia_mensal.turma.curso.nome }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem" class="form-label">Mensagem</label>
                    <textarea class="form-control" id="mensagem" name="mensagem" rows="10" required>Prezado(a) {{ carencia.aluno.nome }},

Identificamos que sua frequência no curso {{ carencia.frequencia_mensal.turma.curso.nome }}, turma {{ carencia.frequencia_mensal.turma.nome }}, no período de {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }} está abaixo do mínimo necessário (75%).

Seu percentual atual de presença é de {{ carencia.percentual_presenca }}%.

Por favor, entre em contato com a secretaria para regularizar sua situação.

Atenciosamente,
Equipe OMAUM</textarea>
                </div>
                
                <div class="mb-3">
                    <label for="tipo_notificacao" class="form-label">Tipo de Notificação</label>
                    <select class="form-select" id="tipo_notificacao" name="tipo_notificacao" required>
                        <option value="EMAIL">E-mail</option>
                        <option value="SMS">SMS</option>
                        <option value="SISTEMA">Sistema</option>
                        <option value="WHATSAPP">WhatsApp</option>
                    </select>
                </div>
                
                <div class="mb-3">
                    <label for="prioridade" class="form-label">Prioridade</label>
                    <select class="form-select" id="prioridade" name="prioridade" required>
                        <option value="BAIXA">Baixa</option>
                        <option value="MEDIA" selected>Média</option>
                        <option value="ALTA">Alta</option>
                        <option value="URGENTE">Urgente</option>
                    </select>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="enviar_agora" name="enviar_agora" checked>
                    <label class="form-check-label" for="enviar_agora">
                        Enviar notificação imediatamente
                    </label>
                </div>
                
                <div class="mb-3" id="data_envio_div" style="display: none;">
                    <label for="data_envio" class="form-label">Data de Envio</label>
                    <input type="datetime-local" class="form-control" id="data_envio" name="data_envio">
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" class="btn btn-secondary">
                        Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-envelope"></i> Criar Notificação
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const enviarAgoraCheckbox = document.getElementById('enviar_agora');
        const dataEnvioDiv = document.getElementById('data_envio_div');
        const dataEnvioInput = document.getElementById('data_envio');
        
        enviarAgoraCheckbox.addEventListener('change', function() {
            dataEnvioDiv.style.display = this.checked ? 'none' : 'block';
            
            if (!this.checked && !dataEnvioInput.value) {
                // Definir data padrão para amanhã às 9h
                const amanha = new Date();
                amanha.setDate(amanha.getDate() + 1);
                amanha.setHours(9, 0, 0, 0);
                
                const ano = amanha.getFullYear();
                const mes = String(amanha.getMonth() + 1).padStart(2, '0');
                const dia = String(amanha.getDate()).padStart(2, '0');
                const hora = String(amanha.getHours()).padStart(2, '0');
                const minuto = String(amanha.getMinutes()).padStart(2, '0');
                
                dataEnvioInput.value = `${ano}-${mes}-${dia}T${hora}:${minuto}`;
            }
        });
        
        // Ajustar o template da mensagem com base no tipo de notificação
        const tipoNotificacaoSelect = document.getElementById('tipo_notificacao');
        const mensagemTextarea = document.getElementById('mensagem');
        const mensagemOriginal = mensagemTextarea.value;
        
        tipoNotificacaoSelect.addEventListener('change', function() {
            const tipo = this.value;
            
            if (tipo === 'SMS' || tipo === 'WHATSAPP') {
                // Versão mais curta para SMS e WhatsApp
                mensagemTextarea.value = `OMAUM: Olá, ${carencia.aluno.nome}. Sua frequência no curso ${carencia.frequencia_mensal.turma.curso.nome} está em ${carencia.percentual_presenca}%, abaixo do mínimo (75%). Entre em contato com a secretaria.`;
            } else {
                // Versão completa para e-mail e sistema
                mensagemTextarea.value = mensagemOriginal;
            }
        });
    });
</script>
{% endblock %}


'''