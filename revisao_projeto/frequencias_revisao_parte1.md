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



### Arquivo: frequencias\templates\frequencias\dashboard.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Frequências{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Dashboard de Frequências</h1>
        <div>
            <a href="{% url 'frequencias:relatorio_carencias' %}" class="btn btn-primary">
                <i class="fas fa-file-alt"></i> Relatório de Carências
            </a>
            <a href="{% url 'frequencias:notificacoes_carencia' %}" class="btn btn-info">
                <i class="fas fa-envelope"></i> Notificações
            </a>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="periodo" class="form-label">Período</label>
                    <select class="form-select" id="periodo" name="periodo">
                        <option value="">Todos os períodos</option>
                        {% for ano in anos %}
                            <optgroup label="{{ ano }}">
                                {% for mes in meses %}
                                <option value="{{ ano }}-{{ mes.0 }}" 
                                        {% if filtros.periodo == ano|stringformat:"s"|add:"-"|add:mes.0 %}selected{% endif %}>
                                    {{ mes.1 }}/{{ ano }}
                                </option>
                                {% endfor %}
                            </optgroup>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-3">
                    <label for="curso" class="form-label">Curso</label>
                    <select class="form-select" id="curso" name="curso">
                        <option value="">Todos os cursos</option>
                        {% for curso in cursos %}
                        <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == filtros.curso %}selected{% endif %}>
                            {{ curso.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select class="form-select" id="turma" name="turma">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                        <option value="{{ turma.id }}" {% if turma.id|stringformat:"s" == filtros.turma %}selected{% endif %}>
                            {{ turma.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'frequencias:dashboard' %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Cards de estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-white bg-primary h-100">
                <div class="card-body">
                    <h5 class="card-title">Média de Frequência</h5>
                    <p class="card-text display-4">{{ estatisticas.media_frequencia|floatformat:1 }}%</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <small>Média geral de frequência</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-success h-100">
                <div class="card-body">
                    <h5 class="card-title">Alunos Regulares</h5>
                    <p class="card-text display-4">{{ estatisticas.alunos_regulares }}</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <small>Alunos com frequência ≥ 75%</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-danger h-100">
                <div class="card-body">
                    <h5 class="card-title">Alunos em Carência</h5>
                    <p class="card-text display-4">{{ estatisticas.alunos_carencia }}</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <small>Alunos com frequência < 75%</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card text-white bg-info h-100">
                <div class="card-body">
                    <h5 class="card-title">Total de Alunos</h5>
                    <p class="card-text display-4">{{ estatisticas.total_alunos }}</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <small>Alunos ativos no período</small>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Frequência por Curso</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoFrequenciaCursos" height="300"></canvas>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Evolução da Frequência</h5>
                </div>
                <div class="card-body">
                    <canvas id="graficoEvolucaoFrequencia" height="300"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Tabela de turmas com menor frequência -->
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">Turmas com Menor Frequência</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Turma</th>
                            <th>Curso</th>
                            <th>Período</th>
                            <th>Média de Frequência</th>
                            <th>Alunos em Carência</th>
                            <th>Total de Alunos</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for turma in turmas_menor_frequencia %}
                        <tr>
                            <td>{{ turma.nome }}</td>
                            <td>{{ turma.curso.nome }}</td>
                            <td>{{ turma.periodo_mes }}/{{ turma.periodo_ano }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar {% if turma.media_frequencia < 75 %}bg-danger{% elif turma.media_frequencia < 85 %}bg-warning{% else %}bg-success{% endif %}" 
                                         role="progressbar" style="width: {{ turma.media_frequencia }}%;" 
                                         aria-valuenow="{{ turma.media_frequencia }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ turma.media_frequencia|floatformat:1 }}%
                                    </div>
                                </div>
                            </td>
                            <td>{{ turma.alunos_carencia }} / {{ turma.total_alunos }}</td>
                            <td>{{ turma.total_alunos }}</td>
                            <td>
                                <a href="{% url 'frequencias:listar_frequencias' %}?turma={{ turma.id }}" class="btn btn-sm btn-primary">
                                    <i class="fas fa-list"></i> Ver Frequências
                                </a>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="7" class="text-center py-3">
                                <p class="mb-0">Nenhuma turma encontrada com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Alunos com menor frequência -->
    <div class="card mb-4">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Alunos com Menor Frequência</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Turma</th>
                            <th>Curso</th>
                            <th>Período</th>
                            <th>Frequência</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in alunos_menor_frequencia %}
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    {% if aluno.foto %}
                                    <img src="{{ aluno.foto.url }}" alt="{{ aluno.nome }}" 
                                         class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                                    {% else %}
                                    <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                         style="width: 40px; height: 40px; color: white;">
                                        {{ aluno.nome|first|upper }}
                                    </div>
                                    {% endif %}
                                    <div>
                                        <div>{{ aluno.nome }}</div>
                                        <small class="text-muted">{{ aluno.email }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>{{ aluno.turma }}</td>
                            <td>{{ aluno.curso }}</td>
                            <td>{{ aluno.periodo_mes }}/{{ aluno.periodo_ano }}</td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar bg-danger" role="progressbar" 
                                         style="width: {{ aluno.percentual_presenca }}%;" 
                                         aria-valuenow="{{ aluno.percentual_presenca }}" aria-valuemin="0" aria-valuemax="100">
                                        {{ aluno.percentual_presenca }}%
                                    </div>
                                </div>
                            </td>
                            <td>
                                {% if aluno.status_carencia == 'PENDENTE' %}
                                <span class="badge bg-danger">Pendente</span>
                                {% elif aluno.status_carencia == 'EM_ACOMPANHAMENTO' %}
                                <span class="badge bg-warning text-dark">Em Acompanhamento</span>
                                {% elif aluno.status_carencia == 'RESOLVIDO' %}
                                <span class="badge bg-success">Resolvido</span>
                                {% endif %}
                            </td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-user"></i>
                                    </a>
                                    {% if aluno.carencia_id %}
                                    <a href="{% url 'frequencias:detalhar_carencia' aluno.carencia_id %}" class="btn btn-sm btn-warning">
                                        <i class="fas fa-exclamation-triangle"></i>
                                    </a>
                                    {% if aluno.status_carencia != 'RESOLVIDO' %}
                                    <a href="{% url 'frequencias:resolver_carencia' aluno.carencia_id %}" class="btn btn-sm btn-success">
                                        <i class="fas fa-check"></i>
                                    </a>
                                    {% endif %}
                                    {% endif %}
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="7" class="text-center py-3">
                                <p class="mb-0">Nenhum aluno em carência encontrado com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de frequência por curso
        const ctxCursos = document.getElementById('graficoFrequenciaCursos').getContext('2d');
        new Chart(ctxCursos, {
            type: 'bar',
            data: {
                labels: {{ cursos_labels|safe }},
                datasets: [{
                    label: 'Média de Frequência (%)',
                    data: {{ frequencia_por_curso|safe }},
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(199, 199, 199, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(199, 199, 199, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
        
        // Gráfico de evolução da frequência
        const ctxEvolucao = document.getElementById('graficoEvolucaoFrequencia').getContext('2d');
        new Chart(ctxEvolucao, {
            type: 'line',
            data: {
                labels: {{ periodos_labels|safe }},
                datasets: [{
                    label: 'Média de Frequência (%)',
                    data: {{ evolucao_frequencia|safe }},
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
        
        // Atualizar turmas quando o curso for alterado
        const cursoSelect = document.getElementById('curso');
        const turmaSelect = document.getElementById('turma');
        
        cursoSelect.addEventListener('change', function() {
            const cursoId = this.value;
            
            // Limpar o select de turmas
            turmaSelect.innerHTML = '<option value="">Todas as turmas</option>';
            
            if (cursoId) {
                // Fazer uma requisição AJAX para buscar as turmas do curso
                fetch(`/frequencias/api/turmas-por-curso/${cursoId}/`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.turmas) {
                            data.turmas.forEach(turma => {
                                const option = document.createElement('option');
                                option.value = turma.id;
                                option.textContent = turma.nome;
                                turmaSelect.appendChild(option);
                            });
                        }
                    })
                    .catch(error => console.error('Erro ao buscar turmas:', error));
            }
        });
    });
</script>
{% endblock %}
{% endblock %}



### Arquivo: frequencias\templates\frequencias\detalhar_carencia.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Carência{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Padronizar botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Detalhes da Carência</h1>
        <div>
            <a href="{% url 'frequencias:listar_carencias' %}" class="btn btn-secondary me-2">
                <i class="fas fa-list"></i> Lista de Carências
            </a>
            <a href="javascript:history.back()" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
    </div>
    
    <!-- Status da carência -->
    <div class="alert 
        {% if carencia.status == 'PENDENTE' %}alert-danger
        {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}alert-warning
        {% elif carencia.status == 'RESOLVIDO' %}alert-success
        {% endif %}">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h5 class="alert-heading mb-1">
                    {% if carencia.status == 'PENDENTE' %}
                    <i class="fas fa-exclamation-circle"></i> Carência Pendente
                    {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                    <i class="fas fa-clock"></i> Carência em Acompanhamento
                    {% elif carencia.status == 'RESOLVIDO' %}
                    <i class="fas fa-check-circle"></i> Carência Resolvida
                    {% endif %}
                </h5>
                <p class="mb-0">
                    {% if carencia.status == 'PENDENTE' %}
                    Esta carência foi identificada em {{ carencia.data_identificacao|date:"d/m/Y" }} e ainda não foi tratada.
                    {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                    Esta carência está sendo acompanhada desde {{ carencia.data_acompanhamento|date:"d/m/Y" }}.
                    {% elif carencia.status == 'RESOLVIDO' %}
                    Esta carência foi resolvida em {{ carencia.data_resolucao|date:"d/m/Y" }}.
                    {% endif %}
                </p>
            </div>
            <div>
                {% if carencia.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:iniciar_acompanhamento' carencia.id %}" class="btn btn-warning">
                    <i class="fas fa-clock"></i> Iniciar Acompanhamento
                </a>
                {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                <a href="{% url 'frequencias:resolver_carencia' carencia.id %}" class="btn btn-success">
                    <i class="fas fa-check"></i> Resolver Carência
                </a>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Informações do aluno -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="d-flex align-items-center">
                        {% if carencia.aluno.foto %}
                        <img src="{{ carencia.aluno.foto.url }}" alt="{{ carencia.aluno.nome }}" 
                             class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                        {% else %}
                        <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                             style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                            {{ carencia.aluno.nome|first|upper }}
                        </div>
                        {% endif %}
                        <div>
                            <h5 class="mb-1">{{ carencia.aluno.nome }}</h5>
                            <p class="mb-0">{{ carencia.aluno.email }}</p>
                            <p class="mb-0">CPF: {{ carencia.aluno.cpf }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 text-md-end">
                    <a href="{% url 'alunos:detalhar_aluno' carencia.aluno.cpf %}" class="btn btn-outline-primary">
                        <i class="fas fa-user"></i> Ver Perfil Completo
                    </a>
                    <a href="{% url 'frequencias:historico_frequencia' carencia.aluno.cpf %}" class="btn btn-outline-info">
                        <i class="fas fa-history"></i> Histórico de Frequência
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Informações da frequência -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Informações da Frequência</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Curso:</strong> {{ carencia.frequencia_mensal.turma.curso.nome }}</p>
                    <p><strong>Turma:</strong> {{ carencia.frequencia_mensal.turma.nome }}</p>
                    <p><strong>Período:</strong> {{ carencia.frequencia_mensal.get_mes_display }}/{{ carencia.frequencia_mensal.ano }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Total de Aulas:</strong> {{ carencia.frequencia_mensal.total_aulas }}</p>
                    <p><strong>Presenças:</strong> {{ carencia.frequencia_mensal.presencas }}</p>
                    <p><strong>Faltas:</strong> {{ carencia.frequencia_mensal.faltas }}</p>
                </div>
            </div>
            
            <div class="mt-3">
                <h6>Percentual de Presença:</h6>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar bg-danger" role="progressbar" 
                         style="width: {{ carencia.percentual_presenca }}%;" 
                         aria-valuenow="{{ carencia.percentual_presenca }}" aria-valuemin="0" aria-valuemax="100">
                        {{ carencia.percentual_presenca|floatformat:1 }}%
                    </div>
                </div>
                <div class="d-flex justify-content-between mt-1">
                    <small class="text-muted">0%</small>
                    <small class="text-danger">Mínimo: 75%</small>
                    <small class="text-muted">100%</small>
                </div>
            </div>
            
            <div class="mt-3 text-end">
                <a href="{% url 'frequencias:detalhar_frequencia_mensal' carencia.frequencia_mensal.id %}" class="btn btn-outline-info">
                    <i class="fas fa-calendar-alt"></i> Ver Detalhes da Frequência Mensal
                </a>
            </div>
        </div>
    </div>
    
    <!-- Notificações -->
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Notificações</h5>
                {% if not carencia.notificacao and carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:criar_notificacao' carencia.id %}" class="btn btn-sm btn-primary">
                    <i class="fas fa-plus"></i> Criar Notificação
                </a>
                {% endif %}
            </div>
        </div>
        <div class="card-body">
            {% if carencia.notificacao %}
            <div class="card mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="mb-0">{{ carencia.notificacao.assunto }}</h6>
                        <span class="badge 
                            {% if carencia.notificacao.status == 'PENDENTE' %}bg-secondary
                            {% elif carencia.notificacao.status == 'ENVIADA' %}bg-info
                            {% elif carencia.notificacao.status == 'LIDA' %}bg-primary
                            {% elif carencia.notificacao.status == 'RESPONDIDA' %}bg-success
                            {% endif %}">
                            {{ carencia.notificacao.get_status_display }}
                        </span>
                    </div>
                    <p class="mb-2">{{ carencia.notificacao.mensagem|truncatechars:150 }}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            Criada em: {{ carencia.notificacao.data_criacao|date:"d/m/Y H:i" }}
                            {% if carencia.notificacao.data_envio %}
                            | Enviada em: {{ carencia.notificacao.data_envio|date:"d/m/Y H:i" }}
                            {% endif %}
                        </small>
                        <a href="{% url 'frequencias:detalhar_notificacao' carencia.notificacao.id %}" class="btn btn-sm btn-outline-primary">
                            Ver Detalhes
                        </a>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="alert alert-info mb-0">
                <i class="fas fa-info-circle"></i> Nenhuma notificação foi criada para esta carência.
                {% if carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:criar_notificacao' carencia.id %}" class="btn btn-sm btn-primary ms-2">
                    Criar Notificação
                </a>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Resolução (se resolvida) -->
    {% if carencia.status == 'RESOLVIDO' %}
    <div class="card mb-4 border-success">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Resolução da Carência</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Motivo da Resolução:</h6>
                <p class="mb-0">{{ carencia.get_motivo_resolucao_display }}</p>
            </div>
            
            <div class="mb-3">
                <h6>Observações:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ carencia.observacoes_resolucao|linebreaks }}
                </div>
            </div>
            
            {% if carencia.documentos_resolucao.all %}
            <div>
                <h6>Documentos:</h6>
                <ul class="list-group">
                    {% for documento in carencia.documentos_resolucao.all %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>{{ documento.nome }}</span>
                        <a href="{{ documento.arquivo.url }}" class="btn btn-sm btn-outline-primary" download>
                            <i class="fas fa-download"></i> Download
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
            
            <div class="mt-3">
                <p class="text-muted mb-0">
                    <small>Resolvida por: {{ carencia.resolvido_por.get_full_name|default:carencia.resolvido_por.username }} em {{ carencia.data_resolucao|date:"d/m/Y H:i" }}</small>
                </p>
            </div>
        </div>
    </div>
    {% endif %}
    
    <!-- Padronizar botões de ações na seção de ações -->
    <div class="card mb-4">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Ações</h5>
        </div>
        <div class="card-body">
            <div class="d-flex flex-wrap gap-2">
                {% if carencia.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:iniciar_acompanhamento' carencia.id %}" class="btn btn-warning">
                    <i class="fas fa-clock"></i> Iniciar Acompanhamento
                </a>
                {% endif %}
                
                {% if carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:resolver_carencia' carencia.id %}" class="btn btn-success">
                    <i class="fas fa-check"></i> Resolver Carência
                </a>
                {% endif %}
                
                {% if not carencia.notificacao and carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:criar_notificacao' carencia.id %}" class="btn btn-primary">
                    <i class="fas fa-envelope"></i> Criar Notificação
                </a>
                {% endif %}
                
                <a href="{% url 'frequencias:historico_frequencia' carencia.aluno.cpf %}" class="btn btn-info">
                    <i class="fas fa-history"></i> Ver Histórico de Frequência
                </a>
                
                <a href="{% url 'alunos:detalhar_aluno' carencia.aluno.cpf %}" class="btn btn-primary">
                    <i class="fas fa-user"></i> Ver Perfil do Aluno
                </a>
            </div>
        </div>
    </div>
    
    <!-- Histórico de ações -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Histórico de Ações</h5>
        </div>
        <div class="card-body p-0">
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-exclamation-circle text-danger"></i> 
                            <strong>Carência identificada</strong>
                            {% if carencia.identificado_por %}
                            por {{ carencia.identificado_por.get_full_name|default:carencia.identificado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.data_identificacao|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                
                {% if carencia.data_acompanhamento %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-clock text-warning"></i> 
                            <strong>Acompanhamento iniciado</strong>
                            {% if carencia.acompanhado_por %}
                            por {{ carencia.acompanhado_por.get_full_name|default:carencia.acompanhado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.data_acompanhamento|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if carencia.notificacao %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-envelope text-primary"></i> 
                            <strong>Notificação criada</strong>
                            {% if carencia.notificacao.criado_por %}
                            por {{ carencia.notificacao.criado_por.get_full_name|default:carencia.notificacao.criado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.notificacao.data_criacao|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                
                {% if carencia.notificacao.data_envio %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-paper-plane text-info"></i> 
                            <strong>Notificação enviada</strong>
                            {% if carencia.notificacao.enviado_por %}
                            por {{ carencia.notificacao.enviado_por.get_full_name|default:carencia.notificacao.enviado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.notificacao.data_envio|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if carencia.notificacao.data_leitura %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-envelope-open text-primary"></i> 
                            <strong>Notificação lida</strong> pelo aluno
                        </div>
                        <div>{{ carencia.notificacao.data_leitura|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if carencia.notificacao.data_resposta %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-reply text-success"></i> 
                            <strong>Notificação respondida</strong> pelo aluno
                        </div>
                        <div>{{ carencia.notificacao.data_resposta|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                {% endif %}
                
                {% if carencia.data_resolucao %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-check-circle text-success"></i> 
                            <strong>Carência resolvida</strong>
                            {% if carencia.resolvido_por %}
                            por {{ carencia.resolvido_por.get_full_name|default:carencia.resolvido_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ carencia.data_resolucao|date:"d/m/Y H:i" }}</div>
                    </div>
                    {% if carencia.observacoes_resolucao %}
                    <div class="mt-1 text-muted">
                        <small>{{ carencia.observacoes_resolucao|truncatewords:20 }}</small>
                    </div>
                    {% endif %}
                </li>
                {% endif %}
                
                {% for log in carencia.logs.all %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas {{ log.get_icone }} {{ log.get_cor }}"></i> 
                            <strong>{{ log.acao }}</strong>
                            {% if log.usuario %}
                            por {{ log.usuario.get_full_name|default:log.usuario.username }}
                            {% endif %}
                        </div>
                        <div>{{ log.data|date:"d/m/Y H:i" }}</div>
                    </div>
                    {% if log.detalhes %}
                    <div class="mt-1 text-muted">
                        <small>{{ log.detalhes }}</small>
                    </div>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\detalhar_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes da Frequência</h1>
    
  {% if messages %}
      {% for message in messages %}
          <div class="alert alert-{{ message.tags }}">
              {{ message }}
          </div>
      {% endfor %}
  {% endif %}
    
  <div class="card">
      <div class="card-header">
          <h5 class="mb-0">Informações da Frequência</h5>
      </div>
      <div class="card-body">
          <div class="row mb-3">
              <div class="col-md-6">
                  <p><strong>Aluno:</strong> {{ frequencia.aluno.nome }}</p>
                  <p><strong>Turma:</strong> {{ frequencia.turma.id }}</p>
                  <p><strong>Data:</strong> {{ frequencia.data }}</p>
              </div>
              <div class="col-md-6">
                  <p>
                      <strong>Status:</strong> 
                      {% if frequencia.presente %}
                          <span class="badge bg-success">Presente</span>
                      {% else %}
                          <span class="badge bg-danger">Ausente</span>
                      {% endif %}
                  </p>
                  <p><strong>Registrado por:</strong> {{ frequencia.registrado_por|default:"Não informado" }}</p>
                  <p><strong>Data de registro:</strong> {{ frequencia.data_registro }}</p>
              </div>
          </div>
            
          {% if not frequencia.presente %}
          <div class="mb-3">
              <h6>Justificativa:</h6>
              <div class="p-3 bg-light rounded">
                  {% if frequencia.justificativa %}
                      {{ frequencia.justificativa|linebreaks }}
                  {% else %}
                      <em>Nenhuma justificativa fornecida.</em>
                  {% endif %}
              </div>
          </div>
          {% endif %}
            
          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <a href="{% url 'frequencias:editar_frequencia' frequencia.id %}" class="btn btn-warning">Editar</a>
              <a href="{% url 'frequencias:excluir_frequencia' frequencia.id %}" class="btn btn-danger">Excluir</a>
              <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Voltar</a>
          </div>
      </div>
  </div>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\detalhar_frequencia_mensal.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Frequência Mensal{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Padronizar botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Detalhes da Frequência Mensal</h1>
        <div class="btn-group">
            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'frequencias:editar_frequencia_mensal' frequencia.id %}" class="btn btn-warning">
                <i class="fas fa-edit"></i> Editar
            </a>
            <a href="{% url 'frequencias:excluir_frequencia_mensal' frequencia.id %}" class="btn btn-danger">
                <i class="fas fa-trash"></i> Excluir
            </a>
            <a href="{% url 'frequencias:recalcular_carencias' frequencia.id %}" class="btn btn-primary">
                <i class="fas fa-sync"></i> Recalcular Carências
            </a>
            <a href="{% url 'frequencias:exportar_frequencia_csv' frequencia.id %}" class="btn btn-success">
                <i class="fas fa-file-csv"></i> Exportar CSV
            </a>
        </div>
    </div>
    
    <!-- Informações da frequência -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações Gerais</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Turma:</strong> {{ frequencia.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ frequencia.turma.curso.nome }}</p>
                    <p><strong>Período:</strong> {{ frequencia.get_mes_display }}/{{ frequencia.ano }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Percentual Mínimo:</strong> {{ frequencia.percentual_minimo }}%</p>
                    <p><strong>Criado em:</strong> {{ frequencia.created_at|date:"d/m/Y H:i" }}</p>
                    <p><strong>Última atualização:</strong> {{ frequencia.updated_at|date:"d/m/Y H:i" }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Estatísticas -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Estatísticas</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Alunos</h5>
                            <p class="card-text display-4">{{ total_alunos }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Alunos em Carência</h5>
                            <p class="card-text display-4">{{ carencias|length }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Percentual de Carência</h5>
                            <p class="card-text display-4">
                                {% if total_alunos > 0 %}
                                {{ carencias|length|multiply:100|divide:total_alunos|floatformat:1 }}%
                                {% else %}
                                0%
                                {% endif %}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <canvas id="grafico-frequencia"></canvas>
            </div>
        </div>
    </div>
    
    <!-- Alunos em carência -->
    <div class="card">
        <div class="card-header bg-danger text-white">
            <h5 class="mb-0">Alunos em Carência</h5>
        </div>
        <div class="card-body">
            {% if carencias %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Aluno</th>
                            <th>Percentual de Presença</th>
                            <th>Status</th>
                            <th>Observações</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for carencia in carencias %}
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    {% if carencia.aluno.foto %}
                                    <img src="{{ carencia.aluno.foto.url }}" alt="{{ carencia.aluno.nome }}" 
                                         class="rounded-circle me-2" width="40" height="40">
                                    {% else %}
                                    <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                         style="width: 40px; height: 40px; color: white;">
                                        {{ carencia.aluno.nome|first|upper }}
                                    </div>
                                    {% endif %}
                                    <div>
                                        <div>{{ carencia.aluno.nome }}</div>
                                        <small class="text-muted">{{ carencia.aluno.cpf }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar {% if carencia.percentual_presenca < frequencia.percentual_minimo %}bg-danger{% else %}bg-success{% endif %}" role="progressbar" 
                                         style="width: {{ carencia.percentual_presenca }}%;" 
                                         aria-valuenow="{{ carencia.percentual_presenca }}" 
                                         aria-valuemin="0" aria-valuemax="100">
                                        {{ carencia.percentual_presenca }}%
                                    </div>
                                </div>
                            </td>
                            <td>
                                {% if carencia.status == 'PENDENTE' %}
                                <span class="badge bg-danger">Pendente</span>
                                {% elif carencia.status == 'EM_ACOMPANHAMENTO' %}
                                <span class="badge bg-warning text-dark">Em Acompanhamento</span>
                                {% elif carencia.status == 'RESOLVIDO' %}
                                <span class="badge bg-success">Resolvido</span>
                                {% endif %}
                            </td>
                            <td>{{ carencia.observacoes|default:"Sem observações"|truncatechars:50 }}</td>
                            <td>
                                <div class="btn-group">
                                    <a href="{% url 'frequencias:editar_carencia' carencia.id %}" 
                                       class="btn btn-sm btn-warning" title="Editar">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <a href="{% url 'frequencias:detalhar_carencia' carencia.id %}" 
                                       class="btn btn-sm btn-info" title="Detalhes">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    <a href="{% url 'alunos:detalhar_aluno' carencia.aluno.cpf %}" 
                                       class="btn btn-sm btn-primary" title="Ver aluno">
                                        <i class="fas fa-user"></i>
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-success">
                <i class="fas fa-check-circle me-2"></i>
                Não há alunos em carência para esta frequência mensal.
            </div>
            {% endif %}
        </div>
        <div class="card-footer">
            <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">
                <i class="fas fa-list"></i> Voltar para a lista
            </a>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de frequência
        const ctxFrequencia = document.getElementById('grafico-frequencia').getContext('2d');
        new Chart(ctxFrequencia, {
            type: 'bar',
            data: {
                labels: {{ alunos_labels|safe }},
                datasets: [{
                    label: 'Percentual de Presença',
                    data: {{ percentuais_presenca|safe }},
                    backgroundColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < {{ frequencia.percentual_minimo }} ? 
                            'rgba(220, 53, 69, 0.7)' : 'rgba(40, 167, 69, 0.7)';
                    },
                    borderColor: function(context) {
                        const value = context.dataset.data[context.dataIndex];
                        return value < {{ frequencia.percentual_minimo }} ? 
                            'rgba(220, 53, 69, 1)' : 'rgba(40, 167, 69, 1)';
                    },
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\detalhar_notificacao.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Notificação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Detalhes da Notificação</h1>
        <div>
            {% if notificacao.carencia %}
            <a href="{% url 'frequencias:detalhar_carencia' notificacao.carencia.id %}" class="btn btn-secondary me-2">
                <i class="fas fa-exclamation-triangle"></i> Ver Carência
            </a>
            {% endif %}
            <a href="javascript:history.back()" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
        </div>
    </div>
    
    <!-- Status da notificação -->
    <div class="alert 
        {% if notificacao.status == 'PENDENTE' %}alert-secondary
        {% elif notificacao.status == 'ENVIADA' %}alert-info
        {% elif notificacao.status == 'LIDA' %}alert-primary
        {% elif notificacao.status == 'RESPONDIDA' %}alert-success
        {% endif %}">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h5 class="alert-heading mb-1">
                    {% if notificacao.status == 'PENDENTE' %}
                    <i class="fas fa-clock"></i> Notificação Pendente
                    {% elif notificacao.status == 'ENVIADA' %}
                    <i class="fas fa-paper-plane"></i> Notificação Enviada
                    {% elif notificacao.status == 'LIDA' %}
                    <i class="fas fa-envelope-open"></i> Notificação Lida
                    {% elif notificacao.status == 'RESPONDIDA' %}
                    <i class="fas fa-reply"></i> Notificação Respondida
                    {% endif %}
                </h5>
                <p class="mb-0">
                    {% if notificacao.status == 'PENDENTE' %}
                    Esta notificação ainda não foi enviada ao aluno.
                    {% elif notificacao.status == 'ENVIADA' %}
                    Esta notificação foi enviada em {{ notificacao.data_envio|date:"d/m/Y H:i" }}.
                    {% elif notificacao.status == 'LIDA' %}
                    Esta notificação foi lida pelo aluno em {{ notificacao.data_leitura|date:"d/m/Y H:i" }}.
                    {% elif notificacao.status == 'RESPONDIDA' %}
                    Esta notificação foi respondida pelo aluno em {{ notificacao.data_resposta|date:"d/m/Y H:i" }}.
                    {% endif %}
                </p>
            </div>
            <div>
                {% if notificacao.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:enviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i> Enviar Agora
                </a>
                {% elif notificacao.status == 'ENVIADA' or notificacao.status == 'LIDA' %}
                <a href="{% url 'frequencias:reenviar_notificacao' notificacao.id %}" class="btn btn-outline-primary">
                    <i class="fas fa-sync"></i> Reenviar
                </a>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Informações do destinatário -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Destinatário</h5>
        </div>
        <div class="card-body">
            <div class="d-flex align-items-center">
                {% if notificacao.aluno.foto %}
                <img src="{{ notificacao.aluno.foto.url }}" alt="{{ notificacao.aluno.nome }}" 
                     class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                {% else %}
                <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                     style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                    {{ notificacao.aluno.nome|first|upper }}
                </div>
                {% endif %}
                <div>
                    <h5 class="mb-1">{{ notificacao.aluno.nome }}</h5>
                    <p class="mb-0">{{ notificacao.aluno.email }}</p>
                    {% if notificacao.aluno.celular_primeiro_contato %}
                    <p class="mb-0">{{ notificacao.aluno.celular_primeiro_contato }}</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Conteúdo da notificação -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Conteúdo da Notificação</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p class="mb-0">{{ notificacao.assunto }}</p>
            </div>
            
            <div class="mb-3">
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ notificacao.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if notificacao.anexos.all %}
            <div>
                <h6>Anexos:</h6>
                <ul class="list-group">
                    {% for anexo in notificacao.anexos.all %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>{{ anexo.nome }}</span>
                        <a href="{{ anexo.arquivo.url }}" class="btn btn-sm btn-outline-primary" download>
                            <i class="fas fa-download"></i> Download
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
            
            <div class="mt-3">
                <p class="text-muted mb-0">
                    <small>Criada por: {{ notificacao.criado_por.get_full_name|default:notificacao.criado_por.username }} em {{ notificacao.data_criacao|date:"d/m/Y H:i" }}</small>
                </p>
            </div>
        </div>
    </div>
    
    <!-- Resposta do aluno (se houver) -->
    {% if notificacao.resposta %}
    <div class="card mb-4 border-success">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Resposta do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="mb-3">
                <h6>Assunto:</h6>
                <p class="mb-0">{{ notificacao.resposta.assunto }}</p>
            </div>
            
            <div class="mb-3">
                <h6>Mensagem:</h6>
                <div class="p-3 bg-light rounded border">
                    {{ notificacao.resposta.mensagem|linebreaks }}
                </div>
            </div>
            
            {% if notificacao.resposta.anexos.all %}
            <div>
                <h6>Anexos:</h6>
                <ul class="list-group">
                    {% for anexo in notificacao.resposta.anexos.all %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>{{ anexo.nome }}</span>
                        <a href="{{ anexo.arquivo.url }}" class="btn btn-sm btn-outline-primary" download>
                            <i class="fas fa-download"></i> Download
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
            
            <div class="mt-3">
                <p class="text-muted mb-0">
                    <small>Respondido em: {{ notificacao.data_resposta|date:"d/m/Y H:i" }}</small>
                </p>
            </div>
            
            {% if notificacao.resposta.solicitar_compensacao %}
            <div class="alert alert-warning mt-3">
                <i class="fas fa-exclamation-circle"></i> O aluno solicitou opções de compensação de faltas.
            </div>
            {% endif %}
        </div>
    </div>
    {% endif %}
    
    <!-- Ações -->
    <div class="card mb-4">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Ações</h5>
        </div>
        <div class="card-body">
            <div class="d-flex flex-wrap gap-2">
                {% if notificacao.status == 'PENDENTE' %}
                <a href="{% url 'frequencias:editar_notificacao' notificacao.id %}" class="btn btn-warning">
                    <i class="fas fa-edit"></i> Editar Notificação
                </a>
                <a href="{% url 'frequencias:enviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-paper-plane"></i> Enviar Notificação
                </a>
                {% elif notificacao.status == 'ENVIADA' or notificacao.status == 'LIDA' %}
                <a href="{% url 'frequencias:reenviar_notificacao' notificacao.id %}" class="btn btn-primary">
                    <i class="fas fa-sync"></i> Reenviar Notificação
                </a>
                {% endif %}
                
                {% if notificacao.status == 'RESPONDIDA' %}
                <a href="{% url 'frequencias:responder_aluno' notificacao.id %}" class="btn btn-success">
                    <i class="fas fa-reply"></i> Responder ao Aluno
                </a>
                {% endif %}
                
                {% if notificacao.carencia and notificacao.carencia.status != 'RESOLVIDO' %}
                <a href="{% url 'frequencias:resolver_carencia' notificacao.carencia.id %}" class="btn btn-success">
                    <i class="fas fa-check"></i> Resolver Carência
                </a>
                {% endif %}
                
                <a href="{% url 'frequencias:historico_frequencia' notificacao.aluno.cpf %}" class="btn btn-info">
                    <i class="fas fa-history"></i> Ver Histórico de Frequência
                </a>
                
                <a href="{% url 'alunos:detalhar_aluno' notificacao.aluno.cpf %}" class="btn btn-primary">
                    <i class="fas fa-user"></i> Ver Perfil do Aluno
                </a>
            </div>
        </div>
    </div>
    
    <!-- Histórico de ações -->
    <div class="card mb-4">
        <div class="card-header bg-light">
            <h5 class="mb-0">Histórico de Ações</h5>
        </div>
        <div class="card-body p-0">
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-plus-circle text-success"></i> 
                            <strong>Notificação criada</strong> por {{ notificacao.criado_por.get_full_name|default:notificacao.criado_por.username }}
                        </div>
                        <div>{{ notificacao.data_criacao|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                
                {% if notificacao.data_envio %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-paper-plane text-primary"></i> 
                            <strong>Notificação enviada</strong>
                            {% if notificacao.enviado_por %}
                            por {{ notificacao.enviado_por.get_full_name|default:notificacao.enviado_por.username }}
                            {% endif %}
                        </div>
                        <div>{{ notificacao.data_envio|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if notificacao.data_leitura %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-envelope-open text-info"></i> 
                            <strong>Notificação lida</strong> pelo aluno
                        </div>
                        <div>{{ notificacao.data_leitura|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% if notificacao.data_resposta %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas fa-reply text-success"></i> 
                            <strong>Notificação respondida</strong> pelo aluno
                        </div>
                        <div>{{ notificacao.data_resposta|date:"d/m/Y H:i" }}</div>
                    </div>
                </li>
                {% endif %}
                
                {% for log in notificacao.logs.all %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div>
                            <i class="fas {{ log.get_icone }} {{ log.get_cor }}"></i> 
                            <strong>{{ log.acao }}</strong>
                            {% if log.usuario %}
                            por {{ log.usuario.get_full_name|default:log.usuario.username }}
                            {% endif %}
                        </div>
                        <div>{{ log.data|date:"d/m/Y H:i" }}</div>
                    </div>
                    {% if log.detalhes %}
                    <div class="mt-1 text-muted">
                        <small>{{ log.detalhes }}</small>
                    </div>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}


'''