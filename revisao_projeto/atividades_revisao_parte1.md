'''
# Revisão da Funcionalidade: atividades

## Arquivos forms.py:


### Arquivo: atividades\forms.py

python
print("ARQUIVO FORMS.PY CARREGADO")
from django import forms
from django.core.validators import RegexValidator
from importlib import import_module

# resto do código...


def get_atividade_academica_model():
    try:
        atividades_module = import_module("atividades.models")
        return getattr(atividades_module, "AtividadeAcademica")
    except (ImportError, AttributeError):
        return None


def get_atividade_ritualistica_model():
    try:
        atividades_module = import_module("atividades.models")
        return getattr(atividades_module, "AtividadeRitualistica")
    except (ImportError, AttributeError):
        return None


class AtividadeAcademicaForm(forms.ModelForm):
    todas_turmas = forms.BooleanField(
        required=False, 
        label="Aplicar a todas as turmas ativas", 
        initial=False
    )
    
    class Meta:
        model = get_atividade_academica_model()
        fields = ["nome", "descricao", "data_inicio", "data_fim", "turmas", "responsavel", 
                  "local", "tipo_atividade", "status"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "data_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "data_fim": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "turmas": forms.SelectMultiple(attrs={"class": "form-control"}),
            "responsavel": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_atividade": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar o campo turmas não obrigatório, já que pode ser preenchido automaticamente
        self.fields['turmas'].required = False
        
        # Converter o formato da data para YYYY-MM-DD se estiver editando uma atividade existente
        if self.instance and self.instance.pk and self.instance.data_inicio:
            # Converter para o formato esperado pelo input type="date"
            self.initial['data_inicio'] = self.instance.data_inicio.strftime('%Y-%m-%d')
            if self.instance.data_fim:
                self.initial['data_fim'] = self.instance.data_fim.strftime('%Y-%m-%d')


class AtividadeRitualisticaForm(forms.ModelForm):
    todos_alunos = forms.BooleanField(
        required=False, label="Incluir todos os alunos da turma", initial=False
    )

    class Meta:
        model = get_atividade_ritualistica_model()
        fields = [
            "nome",
            "descricao",
            "data",
            "hora_inicio",
            "hora_fim",
            "local",
            "turma",
            "participantes",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "data": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hora_inicio": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "hora_fim": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "turma": forms.Select(attrs={"class": "form-control"}),
            "participantes": forms.SelectMultiple(
                attrs={"class": "form-control"}
            ),
        }


def criar_form_atividade_academica():
    return AtividadeAcademicaForm


def criar_form_atividade_ritualistica():
    return AtividadeRitualisticaForm



## Arquivos urls.py:


### Arquivo: atividades\urls.py

python
from django.urls import path
from . import views

app_name = "atividades"  # Definindo o namespace

urlpatterns = [
    path("", views.listar_atividades, name="listar_atividades"),
    # Atividades Acadêmicas
    path(
        "academicas/",
        views.listar_atividades_academicas,
        name="listar_atividades_academicas",
    ),
    path(
        "academicas/criar/",
        views.criar_atividade_academica,
        name="criar_atividade_academica",
    ),
    path(
        "academicas/editar/<int:pk>/",
        views.editar_atividade_academica,
        name="editar_atividade_academica",
    ),
    path(
        "academicas/excluir/<int:pk>/",
        views.excluir_atividade_academica,
        name="excluir_atividade_academica",
    ),
    path(
        "academicas/detalhar/<int:pk>/",
        views.detalhar_atividade_academica,
        name="detalhar_atividade_academica",
    ),
    path(
        "academicas/confirmar-exclusao/<int:pk>/",
        views.confirmar_exclusao_academica,
        name="confirmar_exclusao_academica",
    ),
    path(
        "academicas/<int:id>/copiar/",
        views.copiar_atividade_academica,
        name="copiar_atividade_academica",
    ),
    # Atividades Ritualísticas
    path(
        "ritualisticas/",
        views.listar_atividades_ritualisticas,
        name="listar_atividades_ritualisticas",
    ),
    path(
        "ritualisticas/criar/",
        views.criar_atividade_ritualistica,
        name="criar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/editar/<int:pk>/",
        views.editar_atividade_ritualistica,
        name="editar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/excluir/<int:pk>/",
        views.excluir_atividade_ritualistica,
        name="excluir_atividade_ritualistica",
    ),
    path(
        "ritualisticas/detalhar/<int:pk>/",
        views.detalhar_atividade_ritualistica,
        name="detalhar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/confirmar-exclusao/<int:pk>/",
        views.confirmar_exclusao_ritualistica,
        name="confirmar_exclusao_ritualistica",
    ),
    path(
        "ritualisticas/<int:id>/copiar/",
        views.copiar_atividade_ritualistica,
        name="copiar_atividade_ritualistica",
    ),
    # Novas funcionalidades
    path("relatorio/", views.relatorio_atividades, name="relatorio_atividades"),
    path("exportar/<str:formato>/", views.exportar_atividades, name="exportar_atividades"),
    path("calendario/", views.calendario_atividades, name="calendario_atividades"),
    path("dashboard/", views.dashboard_atividades, name="dashboard_atividades"),
    # APIs
    path("api/eventos/", views.api_eventos_calendario, name="api_eventos_calendario"),
    path("api/evento/<int:evento_id>/", views.api_detalhe_evento, name="api_detalhe_evento"),
]



## Arquivos models.py:


### Arquivo: atividades\models.py

python
# Adicione o seguinte código temporário para diagnóstico no início do arquivo:

print("CARREGANDO MODELS.PY")
# Imprimir os campos do modelo para diagnóstico
try:
    from django.db import models
    import inspect

    # Carregar o módulo atual
    import sys

    current_module = sys.modules[__name__]

    # Encontrar todas as classes de modelo no módulo
    for name, obj in inspect.getmembers(current_module):
        if (
            inspect.isclass(obj)
            and issubclass(obj, models.Model)
            and obj != models.Model
        ):
            print(f"Modelo: {name}")
            for field in obj._meta.fields:
                print(f"  - {field.name} ({field.__class__.__name__})")
except Exception as e:
    print(f"Erro ao inspecionar modelos: {e}")

from django.db import models
from django.utils import timezone
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


class AtividadeAcademica(models.Model):
    TIPO_CHOICES = (
        ("aula", "Aula"),
        ("palestra", "Palestra"),
        ("workshop", "Workshop"),
        ("seminario", "Seminário"),
        ("outro", "Outro"),
    )

    STATUS_CHOICES = (
        ("agendada", "Agendada"),
        ("em_andamento", "Em Andamento"),
        ("concluida", "Concluída"),
        ("cancelada", "Cancelada"),
    )

    nome = models.CharField(max_length=100)

    @property
    def titulo(self):
        return self.nome

    @titulo.setter
    def titulo(self, value):
        self.nome = value

    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )
    data_inicio = models.DateTimeField(
        default=timezone.now, verbose_name="Data de Início"
    )
    data_fim = models.DateTimeField(
        blank=True, null=True, verbose_name="Data de Término"
    )
    responsavel = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Responsável"
    )
    local = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Local"
    )
    tipo_atividade = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="aula",
        verbose_name="Tipo de Atividade",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="agendada",
        verbose_name="Status",
    )
    
    # Novo campo para múltiplas turmas
    turmas = models.ManyToManyField(
        "turmas.Turma",
        related_name="atividades_academicas",
        verbose_name="Turmas"
    )

    def __str__(self):
        return self.titulo or self.nome

    class Meta:
        verbose_name = "Atividade Acadêmica"
        verbose_name_plural = "Atividades Acadêmicas"


class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )
    data = models.DateField(verbose_name="Data")
    hora_inicio = models.TimeField(verbose_name="Hora de Início")
    hora_fim = models.TimeField(verbose_name="Hora de Término")
    local = models.CharField(max_length=100, verbose_name="Local")
    turma = models.ForeignKey(
        get_turma_model(), on_delete=models.CASCADE, verbose_name="Turma"
    )
    participantes = models.ManyToManyField(
        get_aluno_model(),
        blank=True,
        verbose_name="Participantes",
        related_name="atividades_ritualisticas",
    )

    def __str__(self):
        return f"{self.nome} - {self.data}"

    class Meta:
        verbose_name = "Atividade Ritualística"
        verbose_name_plural = "Atividades Ritualísticas"
        ordering = ["-data", "hora_inicio"]



## Arquivos de Template:


### Arquivo: atividades\templates\atividades\calendario_atividades.html

html
{% extends 'base.html' %}

{% block title %}Calendário de Atividades{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.css">
<style>
    #calendar {
        max-width: 1100px;
        margin: 0 auto;
    }
    
    .fc-event {
        cursor: pointer;
    }
    
    .fc-event-title {
        font-weight: bold;
    }
    
    .fc-event-time {
        font-size: 0.9em;
    }
    
    .academica-event {
        background-color: #0d6efd;
        border-color: #0d6efd;
    }
    
    .ritualistica-event {
        background-color: #17a2b8;
        border-color: #17a2b8;
    }
    
    .agendada-event {
        border-left: 5px solid #ffc107;
    }
    
    .em_andamento-event {
        border-left: 5px solid #0dcaf0;
    }
    
    .concluida-event {
        border-left: 5px solid #198754;
    }
    
    .cancelada-event {
        border-left: 5px solid #dc3545;
        text-decoration: line-through;
        opacity: 0.7;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Calendário de Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:dashboard_atividades' %}" class="btn btn-success me-2">
                <i class="fas fa-chart-bar"></i> Dashboard
            </a>
            <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-warning me-2">
                <i class="fas fa-file-alt"></i> Relatórios
            </a>
            <div class="btn-group">
                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-outline-primary">Atividades Acadêmicas</a>
                <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-outline-info">Atividades Ritualísticas</a>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Filtros</h5>
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="mostrar-concluidas" checked>
                    <label class="form-check-label" for="mostrar-concluidas">Mostrar atividades concluídas</label>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="filtro-tipo" class="form-label">Tipo de Atividade</label>
                        <select id="filtro-tipo" class="form-select">
                            <option value="todas" selected>Todas</option>
                            <option value="academicas">Acadêmicas</option>
                            <option value="ritualisticas">Ritualísticas</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="filtro-turma" class="form-label">Turma</label>
                        <select id="filtro-turma" class="form-select">
                            <option value="todas" selected>Todas</option>
                            {% for turma in turmas %}
                                <option value="{{ turma.id }}">{{ turma.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-body">
            <div id="calendar"></div>
        </div>
    </div>
    
    <!-- Modal para detalhes da atividade -->
    <div class="modal fade" id="atividadeModal" tabindex="-1" aria-labelledby="atividadeModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="atividadeModalLabel">Detalhes da Atividade</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
                </div>
                <div class="modal-body" id="atividadeModalBody">
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Carregando...</span>
                        </div>
                        <p>Carregando detalhes da atividade...</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    <a href="#" class="btn btn-primary" id="verDetalhesBtn">Ver Detalhes Completos</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/locales-all.min.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar o calendário
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
            },
            locale: 'pt-br',
            buttonText: {
                today: 'Hoje',
                month: 'Mês',
                week: 'Semana',
                day: 'Dia',
                list: 'Lista'
            },
            events: function(info, successCallback, failureCallback) {
                // Obter filtros
                const tipoFiltro = document.getElementById('filtro-tipo').value;
                const turmaFiltro = document.getElementById('filtro-turma').value;
                const mostrarConcluidas = document.getElementById('mostrar-concluidas').checked;
                
                // Construir URL com parâmetros de filtro
                let url = '{% url "atividades:api_eventos_calendario" %}';
                url += '?start=' + info.startStr + '&end=' + info.endStr;
                url += '&tipo=' + tipoFiltro;
                url += '&turma=' + turmaFiltro;
                url += '&concluidas=' + (mostrarConcluidas ? '1' : '0');
                
                // Fazer requisição AJAX
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        successCallback(data);
                    })
                    .catch(error => {
                        console.error('Erro ao carregar eventos:', error);
                        failureCallback(error);
                    });
            },
            eventClick: function(info) {
                // Abrir modal com detalhes do evento
                const modal = new bootstrap.Modal(document.getElementById('atividadeModal'));
                const modalBody = document.getElementById('atividadeModalBody');
                const verDetalhesBtn = document.getElementById('verDetalhesBtn');
                
                // Limpar conteúdo anterior e mostrar loader
                modalBody.innerHTML = `
                    <div class="text-center">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Carregando...</span>
                        </div>
                        <p>Carregando detalhes da atividade...</p>
                    </div>
                `;
                
                // Configurar link para detalhes completos
                const eventoId = info.event.id;
                const tipoEvento = info.event.extendedProps.tipo;
                
                if (tipoEvento === 'academica') {
                    verDetalhesBtn.href = '{% url "atividades:detalhar_atividade_academica" 0 %}'.replace('0', eventoId);
                } else {
                    verDetalhesBtn.href = '{% url "atividades:detalhar_atividade_ritualistica" 0 %}'.replace('0', eventoId);
                }
                
                // Carregar detalhes do evento via AJAX
                fetch(`/atividades/api/evento/${eventoId}/?tipo=${tipoEvento}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Renderizar detalhes do evento
                            if (tipoEvento === 'academica') {
                                modalBody.innerHTML = `
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p><strong>Nome:</strong> ${data.evento.nome}</p>
                                            <p><strong>Tipo:</strong> ${data.evento.tipo_display}</p>
                                            <p><strong>Status:</strong> <span class="badge ${getStatusBadgeClass(data.evento.status)}">${data.evento.status_display}</span></p>
                                            <p><strong>Responsável:</strong> ${data.evento.responsavel || 'Não informado'}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <p><strong>Data de Início:</strong> ${data.evento.data_inicio}</p>
                                            <p><strong>Data de Término:</strong> ${data.evento.data_fim || 'Não definida'}</p>
                                            <p><strong>Local:</strong> ${data.evento.local || 'Não informado'}</p>
                                            <p><strong>Turma:</strong> ${data.evento.turma}</p>
                                        </div>
                                    </div>
                                    <hr>
                                    <div>
                                        <h6>Descrição:</h6>
                                        <p>${data.evento.descricao || 'Sem descrição'}</p>
                                    </div>
                                `;
                            } else {
                                modalBody.innerHTML = `
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p><strong>Nome:</strong> ${data.evento.nome}</p>
                                            <p><strong>Data:</strong> ${data.evento.data}</p>
                                            <p><strong>Horário:</strong> ${data.evento.hora_inicio} - ${data.evento.hora_fim}</p>
                                            <p><strong>Local:</strong> ${data.evento.local}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <p><strong>Turma:</strong> ${data.evento.turma}</p>
                                            <p><strong>Total de Participantes:</strong> ${data.evento.total_participantes}</p>
                                        </div>
                                    </div>
                                    <hr>
                                    <div>
                                        <h6>Descrição:</h6>
                                        <p>${data.evento.descricao || 'Sem descrição'}</p>
                                    </div>
                                `;
                            }
                        } else {
                            modalBody.innerHTML = `<div class="alert alert-danger">Erro ao carregar detalhes: ${data.error}</div>`;
                        }
                    })
                    .catch(error => {
                        console.error('Erro ao carregar detalhes do evento:', error);
                        modalBody.innerHTML = `<div class="alert alert-danger">Erro ao carregar detalhes do evento.</div>`;
                    });
                
                modal.show();
            },
            eventClassNames: function(arg) {
                const classes = [];
                
                // Adicionar classe baseada no tipo de atividade
                if (arg.event.extendedProps.tipo === 'academica') {
                    classes.push('academica-event');
                } else {
                    classes.push('ritualistica-event');
                }
                
                // Adicionar classe baseada no status (apenas para atividades acadêmicas)
                if (arg.event.extendedProps.status) {
                    classes.push(arg.event.extendedProps.status + '-event');
                }
                
                return classes;
            }
        });
        
        calendar.render();
        
        // Função auxiliar para obter classe CSS do badge de status
        function getStatusBadgeClass(status) {
            switch (status) {
                case 'agendada': return 'bg-warning';
                case 'em_andamento': return 'bg-info';
                case 'concluida': return 'bg-success';
                case 'cancelada': return 'bg-secondary';
                default: return 'bg-secondary';
            }
        }
        
        // Atualizar calendário quando os filtros mudarem
        document.getElementById('filtro-tipo').addEventListener('change', function() {
            calendar.refetchEvents();
        });
        
        document.getElementById('filtro-turma').addEventListener('change', function() {
            calendar.refetchEvents();
        });
        
        document.getElementById('mostrar-concluidas').addEventListener('change', function() {
            calendar.refetchEvents();
        });
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\confirmar_copia_academica.html

html
{% extends 'base.html' %}

{% block title %}Copiar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Copiar Atividade Acadêmica</h1>
    
    <div class="alert alert-info">
        <p>Você está prestes a criar uma cópia da atividade acadêmica <strong>"{{ atividade.nome }}"</strong>.</p>
        <p>A nova atividade terá os mesmos dados da original, mas com o status definido como "Agendada".</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade Original</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turmas:</strong> 
                {% for turma in atividade.turmas.all %}
                    {{ turma.nome }}{% if not forloop.last %}, {% endif %}
                {% empty %}
                    Nenhuma turma associada
                {% endfor %}
            </p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-primary me-2">Criar Cópia</button>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\confirmar_copia_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Copiar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Copiar Atividade Ritualística</h1>
    
    <div class="alert alert-info">
        <p>Você está prestes a criar uma cópia da atividade ritualística <strong>"{{ atividade.nome }}"</strong>.</p>
        <p>A nova atividade terá os mesmos dados e participantes da original.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade Original</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-primary me-2">Criar Cópia</button>
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\confirmar_exclusao_academica.html

html
{% extends 'base.html' %}

{% block title %}Confirmar Exclusão de Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Confirmar Exclusão</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade acadêmica "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma.nome }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <!-- Adicionar um campo oculto para a URL de retorno -->
        <input type="hidden" name="return_url" value="{{ return_url }}">
        <button type="submit" class="btn btn-danger">Sim, excluir</button>
        <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
    </form></div>
{% endblock %}




### Arquivo: atividades\templates\atividades\confirmar_exclusao_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Ritualística</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade ritualística "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <input type="hidden" name="return_url" value="{{ return_url }}">
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\copiar_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Copiar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Copiar Atividade Acadêmica</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Atividade Original</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nome:</strong> {{ atividade_original.nome }}</p>
                    <p><strong>Tipo:</strong> {{ atividade_original.get_tipo_atividade_display }}</p>
                    <p><strong>Responsável:</strong> {{ atividade_original.responsavel|default:"Não informado" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Data de Início:</strong> {{ atividade_original.data_inicio|date:"d/m/Y" }}</p>
                    <p><strong>Data de Término:</strong> {{ atividade_original.data_fim|date:"d/m/Y"|default:"Não definida" }}</p>
                    <p><strong>Turma:</strong> {{ atividade_original.turma.nome }}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <p><strong>Descrição:</strong></p>
                    <p>{{ atividade_original.descricao|default:"Sem descrição"|linebreaks }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações da Nova Atividade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
                <div class="form-check mt-3">
                    <input class="form-check-input" type="checkbox" id="copiar_frequencias" name="copiar_frequencias">
                    <label class="form-check-label" for="copiar_frequencias">
                        Copiar registros de frequência (se aplicável)
                    </label>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Cópia</button>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\copiar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Copiar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Copiar Atividade Ritualística</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Atividade Original</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Nome:</strong> {{ atividade_original.nome }}</p>
                    <p><strong>Data:</strong> {{ atividade_original.data|date:"d/m/Y" }}</p>
                    <p><strong>Horário:</strong> {{ atividade_original.hora_inicio }} - {{ atividade_original.hora_fim }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Local:</strong> {{ atividade_original.local }}</p>
                    <p><strong>Turma:</strong> {{ atividade_original.turma.nome }}</p>
                    <p><strong>Participantes:</strong> {{ atividade_original.participantes.count }}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <p><strong>Descrição:</strong></p>
                    <p>{{ atividade_original.descricao|default:"Sem descrição"|linebreaks }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações da Nova Atividade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
                <div class="form-check mt-3">
                    <input class="form-check-input" type="checkbox" id="copiar_participantes" name="copiar_participantes" checked>
                    <label class="form-check-label" for="copiar_participantes">
                        Copiar lista de participantes da atividade original
                    </label>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Cópia</button>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: atividades\templates\atividades\criar_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Criar Nova Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Nova Atividade Acadêmica</h1>
        <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=<form action="" class="nome"></form> %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}
<div class="d-flex justify-content-between mb-5">
    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para a lista</a>
    <button type="submit" class="btn btn-primary">Criar Atividade</button>
</div>



### Arquivo: atividades\templates\atividades\criar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Criar Nova Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Nova Atividade Ritualística</h1>
        <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.todos_alunos %}
                        <small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>
                    </div>
                </div>
                
                <div class="row mt-3" id="participantes-container">
                    <div class="col-md-12">
                        <label for="{{ form.participantes.id_for_label }}">{{ form.participantes.label }}</label>
                        <div class="border p-3 rounded">
                            {{ form.participantes }}
                        </div>
                        {% if form.participantes.errors %}
                            <div class="text-danger">
                                {{ form.participantes.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('{{ form.todos_alunos.id_for_label }}');
        const participantesContainer = document.getElementById('participantes-container');
        
        function toggleParticipantes() {
            if (todosAlunosCheckbox.checked) {
                participantesContainer.style.display = 'none';
            } else {
                participantesContainer.style.display = 'block';
            }
        }
        
        // Inicializar
        toggleParticipantes();
        
        // Adicionar listener para mudanças
        todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
    });
</script>
{% endblock %}




### Arquivo: atividades\templates\atividades\dashboard.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Atividades{% endblock %}

{% block extra_css %}
<style>
    .stat-card {
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
        margin-bottom: 20px;
    }
    
    .activity-item {
        border-left: 4px solid #dee2e6;
        padding-left: 15px;
        margin-bottom: 15px;
        position: relative;
    }
    
    .activity-item.academica {
        border-left-color: #0d6efd;
    }
    
    .activity-item.ritualistica {
        border-left-color: #17a2b8;
    }
    
    .activity-item .date {
        font-size: 0.85rem;
        color: #6c757d;
    }
    
    .activity-item .title {
        font-weight: 600;
        margin: 5px 0;
    }
    
    .activity-item .status {
        position: absolute;
        top: 0;
        right: 0;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:calendario_atividades' %}" class="btn btn-info me-2">
                <i class="fas fa-calendar-alt"></i> Calendário
            </a>
            <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-warning me-2">
                <i class="fas fa-file-alt"></i> Relatórios
            </a>
            <div class="btn-group">
                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-outline-primary">Atividades Acadêmicas</a>
                <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-outline-info">Atividades Ritualísticas</a>
            </div>
        </div>
    </div>
    
    <!-- Estatísticas Gerais -->
    <div class="row mb-4">
        <div class="col-md-4 mb-3">
            <div class="card stat-card h-100 border-primary">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Atividades</h5>
                    <p class="display-4">{{ total_academicas|add:total_ritualisticas }}</p>
                    <div class="d-flex justify-content-around mt-3">
                        <div>
                            <span class="badge bg-primary">Acadêmicas</span>
                            <h5>{{ total_academicas }}</h5>
                        </div>
                        <div>
                            <span class="badge bg-info">Ritualísticas</span>
                            <h5>{{ total_ritualisticas }}</h5>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card stat-card h-100 border-success">
                <div class="card-body">
                    <h5 class="card-title text-center">Atividades por Status</h5>
                    <div class="mt-3">
                        <div class="d-flex justify-content-between mb-2">
                            <span>Agendadas</span>
                            <span class="badge bg-warning">{{ academicas_por_status.agendada|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-warning" role="progressbar" 
                                 style="width: {% widthratio academicas_por_status.agendada|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_status.agendada|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Em Andamento</span>
                            <span class="badge bg-info">{{ academicas_por_status.em_andamento|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-info" role="progressbar" 
                                 style="width: {% widthratio academicas_por_status.em_andamento|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_status.em_andamento|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Concluídas</span>
                            <span class="badge bg-success">{{ academicas_por_status.concluida|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-success" role="progressbar" 
                                 style="width: {% widthratio academicas_por_status.concluida|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_status.concluida|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Canceladas</span>
                            <span class="badge bg-danger">{{ academicas_por_status.cancelada|default:"0" }}</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar bg-danger" role="progressbar" 
                                 style="width: {% widthratio academicas_por_status.cancelada|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_status.cancelada|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4 mb-3">
            <div class="card stat-card h-100 border-info">
                <div class="card-body">
                    <h5 class="card-title text-center">Atividades por Tipo</h5>
                    <div class="mt-3">
                        <div class="d-flex justify-content-between mb-2">
                            <span>Aulas</span>
                            <span class="badge bg-primary">{{ academicas_por_tipo.aula|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-primary" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.aula|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.aula|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Palestras</span>
                            <span class="badge bg-success">{{ academicas_por_tipo.palestra|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-success" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.palestra|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.palestra|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Workshops</span>
                            <span class="badge bg-warning">{{ academicas_por_tipo.workshop|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-warning" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.workshop|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.workshop|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Seminários</span>
                            <span class="badge bg-info">{{ academicas_por_tipo.seminario|default:"0" }}</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-info" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.seminario|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.seminario|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Outros</span>
                            <span class="badge bg-secondary">{{ academicas_por_tipo.outro|default:"0" }}</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar bg-secondary" role="progressbar" 
                                 style="width: {% widthratio academicas_por_tipo.outro|default:0 total_academicas 100 %}%" 
                                 aria-valuenow="{{ academicas_por_tipo.outro|default:0 }}" 
                                 aria-valuemin="0" aria-valuemax="{{ total_academicas }}"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráfico de Atividades por Mês -->
    <div class="card mb-4">
        <div class="card-header">
            <h5>Atividades por Mês (Últimos 6 Meses)</h5>
        </div>
        <div class="card-body">
            <div class="chart-container">
                <canvas id="atividadesPorMesChart"></canvas>
            </div>
        </div>
    </div>
    
    <!-- Atividades Recentes -->
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Atividades Acadêmicas Recentes</h5>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        {% for atividade in atividades_academicas_recentes %}
                            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="list-group-item list-group-item-action">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ atividade.nome }}</h6>
                                    <small>{{ atividade.data_inicio|date:"d/m/Y" }}</small>
                                </div>
                                <p class="mb-1">{{ atividade.descricao|truncatechars:100 }}</p>
                                <small>
                                    <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                        {{ atividade.get_status_display }}
                                    </span>
                                    <span class="badge bg-primary">{{ atividade.get_tipo_atividade_display }}</span>
                                </small>
                            </a>
                        {% empty %}
                            <div class="list-group-item">
                                <p class="mb-0 text-muted">Nenhuma atividade acadêmica recente.</p>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Atividades Ritualísticas Recentes</h5>
                </div>
                <div class="card-body">
                    <div class="list-group">
                        {% for atividade in atividades_ritualisticas_recentes %}
                            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="list-group-item list-group-item-action">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ atividade.nome }}</h6>
                                    <small>{{ atividade.data|date:"d/m/Y" }}</small>
                                </div>
                                <p class="mb-1">{{ atividade.descricao|truncatechars:100 }}</p>
                                <small>
                                    <span class="badge bg-info">{{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</span>
                                    <span class="badge bg-secondary">{{ atividade.local }}</span>
                                </small>
                            </a>
                        {% empty %}
                            <div class="list-group-item">
                                <p class="mb-0 text-muted">Nenhuma atividade ritualística recente.</p>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Dados para o gráfico de atividades por mês
        var ctx = document.getElementById('atividadesPorMesChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {{ meses|safe }},
                datasets: [
                    {
                        label: 'Atividades Acadêmicas',
                        data: {{ dados_academicas }},
                        backgroundColor: 'rgba(13, 110, 253, 0.7)',
                        borderColor: 'rgba(13, 110, 253, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Atividades Ritualísticas',
                        data: {{ dados_ritualisticas }},
                        backgroundColor: 'rgba(23, 162, 184, 0.7)',
                        borderColor: 'rgba(23, 162, 184, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Atividades por Mês'
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\dashboard_atividades.html

html
{% extends 'base.html' %}

{% block title %}Dashboard de Atividades{% endblock %}

{% block extra_css %}
<style>
    .stat-card {
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .chart-container {
        position: relative;
        height: 300px;
        margin-bottom: 20px;
    }
    
    .activity-item {
        border-left: 4px solid #dee2e6;
        padding-left: 15px;
        margin-bottom: 15px;
        position: relative;
    }
    
    .activity-item.academica {
        border-left-color: #0d6efd;
    }
    
    .activity-item.ritualistica {
        border-left-color: #17a2b8;
    }
    
    .activity-item .date {
        font-size: 0.85rem;
        color: #6c757d;
    }
    
    .activity-item .title {
        font-weight: 600;
        margin: 5px 0;
    }
    
    .activity-item .status {
        position: absolute;
        top: 0;
        right: 0;
    }
</style>
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard de Atividades</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:calendario_atividades' %}" class="btn btn-primary me-2">Calendário</a>
            <a href="{% url 'atividades:relatorio_atividades' %}" class="btn btn-success">Relatório</a>
        </div>
    </div>
    
    <!-- Cards de estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card stat-card bg-primary text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Total de Atividades</h5>
                    <p class="display-4">{{ total_atividades }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card bg-success text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="display-4">{{ total_academicas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card bg-info text-white">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="display-4">{{ total_ritualisticas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card bg-warning text-dark">
                <div class="card-body text-center">
                    <h5 class="card-title">Atividades Agendadas</h5>
                    <p class="display-4">{{ total_agendadas }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Atividades por Tipo</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="tipoAtividadesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Atividades por Status</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="statusAtividadesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <h5>Atividades por Mês</h5>
                </div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="atividadesPorMesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Próximas atividades e atividades recentes -->
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Próximas Atividades</h5>
                </div>
                <div class="card-body">
                    {% if proximas_atividades %}
                        {% for atividade in proximas_atividades %}
                            <div class="activity-item {% if atividade.tipo == 'academica' %}academica{% else %}ritualistica{% endif %}">
                                <div class="date">
                                    {% if atividade.tipo == 'academica' %}
                                        {{ atividade.data_inicio|date:"d/m/Y" }}
                                    {% else %}
                                        {{ atividade.data|date:"d/m/Y" }} ({{ atividade.hora_inicio }} - {{ atividade.hora_fim }})
                                    {% endif %}
                                </div>
                                <div class="title">{{ atividade.nome }}</div>
                                <div class="details">
                                    {% if atividade.tipo == 'academica' %}
                                        <span class="badge bg-primary">Acadêmica</span>
                                        <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                            {{ atividade.get_status_display }}
                                        </span>
                                    {% else %}
                                        <span class="badge bg-info">Ritualística</span>
                                    {% endif %}
                                </div>
                                <div class="mt-2">
                                    {% if atividade.tipo == 'academica' %}
                                        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-sm btn-outline-primary">Ver Detalhes</a>
                                    {% else %}
                                        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-outline-info">Ver Detalhes</a>
                                    {% endif %}
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-muted">Não há atividades agendadas para os próximos dias.</p>
                    {% endif %}
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5>Atividades Recentes</h5>
                </div>
                <div class="card-body">
                    {% if atividades_recentes %}
                        {% for atividade in atividades_recentes %}
                            <div class="activity-item {% if atividade.tipo == 'academica' %}academica{% else %}ritualistica{% endif %}">
                                <div class="date">
                                    {% if atividade.tipo == 'academica' %}
                                        {{ atividade.data_inicio|date:"d/m/Y" }}
                                    {% else %}
                                        {{ atividade.data|date:"d/m/Y" }} ({{ atividade.hora_inicio }} - {{ atividade.hora_fim }})
                                    {% endif %}
                                </div>
                                <div class="title">{{ atividade.nome }}</div>
                                <div class="details">
                                    {% if atividade.tipo == 'academica' %}
                                        <span class="badge bg-primary">Acadêmica</span>
                                        <span class="badge {% if atividade.status == 'agendada' %}bg-warning{% elif atividade.status == 'em_andamento' %}bg-info{% elif atividade.status == 'concluida' %}bg-success{% else %}bg-secondary{% endif %}">
                                            {{ atividade.get_status_display }}
                                        </span>
                                    {% else %}
                                        <span class="badge bg-info">Ritualística</span>
                                    {% endif %}
                                </div>
                                <div class="mt-2">
                                    {% if atividade.tipo == 'academica' %}
                                        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-sm btn-outline-primary">Ver Detalhes</a>
                                    {% else %}
                                        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-outline-info">Ver Detalhes</a>
                                    {% endif %}
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-muted">Não há atividades recentes.</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Gráfico de atividades por tipo
        var tipoCtx = document.getElementById('tipoAtividadesChart').getContext('2d');
        var tipoChart = new Chart(tipoCtx, {
            type: 'pie',
            data: {
                labels: ['Acadêmicas', 'Ritualísticas'],
                datasets: [{
                    data: [{{ total_academicas }}, {{ total_ritualisticas }}],
                    backgroundColor: [
                        'rgba(13, 110, 253, 0.8)',
                        'rgba(23, 162, 184, 0.8)'
                    ],
                    borderColor: [
                        'rgba(13, 110, 253, 1)',
                        'rgba(23, 162, 184, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribuição por Tipo de Atividade'
                    }
                }
            }
        });
        
        // Gráfico de atividades por status
        var statusCtx = document.getElementById('statusAtividadesChart').getContext('2d');
        var statusChart = new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Agendadas', 'Em Andamento', 'Concluídas', 'Canceladas'],
                datasets: [{
                    data: [
                        {{ status_counts.agendada|default:0 }}, 
                        {{ status_counts.em_andamento|default:0 }}, 
                        {{ status_counts.concluida|default:0 }}, 
                        {{ status_counts.cancelada|default:0 }}
                    ],
                    backgroundColor: [
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(13, 202, 240, 0.8)',
                        'rgba(25, 135, 84, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(255, 193, 7, 1)',
                        'rgba(13, 202, 240, 1)',
                        'rgba(25, 135, 84, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribuição por Status'
                    }
                }
            }
        });
        
        // Gráfico de atividades por mês
        var mesCtx = document.getElementById('atividadesPorMesChart').getContext('2d');
        var mesChart = new Chart(mesCtx, {
            type: 'bar',
            data: {
                labels: {{ meses|safe }},
                datasets: [
                    {
                        label: 'Atividades Acadêmicas',
                        data: {{ academicas_por_mes|safe }},
                        backgroundColor: 'rgba(13, 110, 253, 0.5)',
                        borderColor: 'rgba(13, 110, 253, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Atividades Ritualísticas',
                        data: {{ ritualisticas_por_mes|safe }},
                        backgroundColor: 'rgba(23, 162, 184, 0.5)',
                        borderColor: 'rgba(23, 162, 184, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Atividades por Mês'
                    }
                }
            }
        });
    });
</script>
{% endblock %}



### Arquivo: atividades\templates\atividades\detalhar_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Atividade Acadêmica</h1>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">{{ atividade.nome }}</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
                    <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
                    <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
                    <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
                    <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
                    <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
                    
                    <!-- Mostrar todas as turmas associadas -->
                    <p><strong>Turmas:</strong></p>
                    <ul class="list-group">
                        {% for turma in atividade.turmas.all %}
                            <li class="list-group-item">
                                <a href="{% url 'turmas:detalhar_turma' turma.id %}">{{ turma.nome }}</a>
                                {% if turma.curso %}
                                    - {{ turma.curso.nome }}
                                {% endif %}
                            </li>
                        {% empty %}
                            <li class="list-group-item">Nenhuma turma associada</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            
            <div class="mt-3">
                <a href="{% url 'atividades:editar_atividade_academica' atividade.pk %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">Editar</a>
                <a href="{% url 'atividades:confirmar_exclusao_academica' atividade.pk %}?return_url={{ request.path|urlencode }}" class="btn btn-danger">Excluir</a>
                <!-- Novo botão para copiar atividade -->
                <a href="{% url 'atividades:copiar_atividade_academica' atividade.id %}" class="btn btn-secondary">Copiar</a>
                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para Lista</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\detalhar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{{ atividade.nome }}</h1>
        <div>
            <a href="{{ return_url }}" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary me-2">Lista de Atividades</a>
            <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}?return_url={{ request.path|urlencode }}" class="btn btn-warning me-2">Editar</a>
            <!-- Novo botão para copiar atividade -->
            <a href="{% url 'atividades:copiar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary me-2">Copiar</a>
            <a href="{% url 'atividades:confirmar_exclusao_ritualistica' atividade.id %}?return_url={{ request.path|urlencode }}" class="btn btn-danger">Excluir</a>
        </div>
    </div>    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Informações Básicas</h5>
                </div>
                <div class="card-body">
                    <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
                    <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
                    <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
                    <p><strong>Local:</strong> {{ atividade.local }}</p>
                    <p><strong>Turma:</strong> {{ atividade.turma }}</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Estatísticas</h5>
                </div>
                <div class="card-body">
                    <p><strong>Total de Participantes:</strong> {{ total_participantes }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Participantes</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Número Iniciático</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in atividade.participantes.all %}
                            <tr>
                                <td>{{ aluno.nome }}</td>
                                <td>{{ aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td>{{ aluno.email }}</td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="3" class="text-center">
                                    <p class="my-3">Nenhum participante cadastrado para esta atividade.</p>
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




### Arquivo: atividades\templates\atividades\editar_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Editar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Acadêmica</h1>
        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Voltar para detalhes</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\editar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Editar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Ritualística</h1>
        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Voltar para detalhes</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.todos_alunos %}
                        <small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>
                    </div>
                </div>
                
                <div class="row mt-3" id="participantes-container">
                    <div class="col-md-12">
                        <label for="{{ form.participantes.id_for_label }}">{{ form.participantes.label }}</label>
                        <div class="border p-3 rounded">
                            {{ form.participantes }}
                        </div>
                        {% if form.participantes.errors %}
                            <div class="text-danger">
                                {{ form.participantes.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('{{ form.todos_alunos.id_for_label }}');
        const participantesContainer = document.getElementById('participantes-container');
        
        function toggleParticipantes() {
            if (todosAlunosCheckbox.checked) {
                participantesContainer.style.display = 'none';
            } else {
                participantesContainer.style.display = 'block';
            }
        }
        
        // Inicializar
        toggleParticipantes();
        
        // Adicionar listener para mudanças
        todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
    });
</script>
{% endblock %}




### Arquivo: atividades\templates\atividades\excluir_atividade_academica.html

html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Acadêmica</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade acadêmica "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}




### Arquivo: atividades\templates\atividades\excluir_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Ritualística</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade ritualística "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



'''