'''
# Revisão da Funcionalidade: atividades

## Arquivos forms.py:


### Arquivo: atividades\forms.py

python
"""Formulários para o módulo de atividades."""

import logging
from importlib import import_module

from django import forms

logger = logging.getLogger(__name__)


def get_models():
    """
    Obtém todos os modelos necessários dinamicamente.

    Returns:
        dict: Dicionário com todos os modelos necessários
    Raises:
        ImportError: Se algum módulo não puder ser importado
        AttributeError: Se algum modelo não for encontrado no módulo
    """
    try:
        atividades_module = import_module("atividades.models")
        cursos_module = import_module("cursos.models")
        turmas_module = import_module("turmas.models")
        alunos_module = import_module("alunos.models")

        return {
            'AtividadeAcademica': getattr(atividades_module, "AtividadeAcademica"),
            'AtividadeRitualistica': getattr(atividades_module, "AtividadeRitualistica"),
            'Curso': getattr(cursos_module, "Curso"),
            'Turma': getattr(turmas_module, "Turma"),
            'Aluno': getattr(alunos_module, "Aluno"),
        }
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter modelos: %s", e)
        raise


class AtividadeAcademicaFiltroForm(forms.Form):
    """Filtro de atividades acadêmicas."""

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome ou descrição...'
        })
    )

    curso = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Todos os cursos",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    turma = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Todas as turmas",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        """Inicializa o filtro com os querysets corretos."""
        super().__init__(*args, **kwargs)
        try:
            models = get_models()
            self.fields['curso'].queryset = models['Curso'].objects.all()
            self.fields['turma'].queryset = models['Turma'].objects.all()
            if 'curso' in self.data and self.data['curso']:
                try:
                    curso_id = int(self.data['curso'])
                    self.fields['turma'].queryset = (
                        models['Turma'].objects.filter(curso_id=curso_id)
                    )
                except (ValueError, TypeError):
                    logger.warning(
                        "Valor inválido para curso_id: %s", self.data['curso']
                    )
        except Exception as e:
            logger.error(
                "Erro ao inicializar AtividadeAcademicaFiltroForm: %s", e
            )
            self.fields['curso'].queryset = []
            self.fields['turma'].queryset = []


def get_atividade_academica_model():
    """Retorna o modelo AtividadeAcademica."""
    return get_models()['AtividadeAcademica']


class AtividadeAcademicaForm(forms.ModelForm):
    """Formulário para criação e edição de atividades acadêmicas."""

    class Meta:
        model = get_atividade_academica_model()
        fields = [
            'nome', 'descricao', 'tipo_atividade', 'data_inicio', 'data_fim',
            'hora_inicio', 'hora_fim', 'local', 'responsavel', 'status',
            'curso', 'turmas'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'tipo_atividade': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'data_fim': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'hora_inicio': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'hora_fim': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'turmas': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome da Atividade',
            'descricao': 'Descrição',
            'tipo_atividade': 'Tipo de Atividade',
            'data_inicio': 'Data de Início',
            'data_fim': 'Data de Término',
            'hora_inicio': 'Hora de Início',
            'hora_fim': 'Hora de Término',
            'local': 'Local',
            'responsavel': 'Responsável',
            'status': 'Status',
            'curso': 'Curso',
            'turmas': 'Turmas',
        }
        help_texts = {
            'data_fim': (
                'Opcional. Se não informada, será considerada a mesma data de início.'
            ),
            'hora_fim': (
                'Opcional. Se não informada, será considerada 1 hora após o início.'
            ),
            'turmas': 'Selecione uma ou mais turmas para esta atividade.',
        }

    def __init__(self, *args, **kwargs):
        """Inicializa o formulário filtrando as turmas pelo curso."""
        super().__init__(*args, **kwargs)
        models = get_models()
        Turma = models['Turma']
        curso_id = self.initial.get('curso') or self.data.get('curso')
        if curso_id:
            self.fields['turmas'].queryset = Turma.objects.filter(
                curso_id=curso_id
            )
        else:
            self.fields['turmas'].queryset = Turma.objects.none()
        self.fields['curso'].empty_label = "Selecione um curso"


def get_atividade_ritualistica_model():
    """Retorna o modelo AtividadeRitualistica."""
    return get_models()['AtividadeRitualistica']


class AtividadeRitualisticaForm(forms.ModelForm):
    """Formulário para criação e edição de atividades ritualísticas."""

    class Meta:
        model = get_atividade_ritualistica_model()
        fields = [
            'nome', 'descricao', 'data', 'hora_inicio', 'hora_fim',
            'local', 'responsavel', 'status', 'participantes'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'data': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'hora_inicio': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'hora_fim': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'participantes': forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'nome': 'Nome da Atividade',
            'descricao': 'Descrição',
            'data': 'Data',
            'hora_inicio': 'Hora de Início',
            'hora_fim': 'Hora de Término',
            'local': 'Local',
            'responsavel': 'Responsável',
            'status': 'Status',
            'participantes': 'Participantes',
        }
        help_texts = {
            'hora_fim': (
                'Opcional. Se não informada, será considerada 1 hora após o início.'
            ),
            'participantes': (
                'Selecione um ou mais participantes para esta atividade.'
            ),
        }

    def clean(self):
        """Valida o formulário de atividade ritualística."""
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')

        if hora_inicio and hora_fim and hora_fim < hora_inicio:
            self.add_error(
                'hora_fim',
                'A hora de término não pode ser anterior à hora de início.'
            )

        return cleaned_data


def get_curso_queryset():
    """Retorna o queryset de cursos."""
    Curso = import_module("cursos.models").Curso
    return Curso.objects.all()


def get_turma_queryset():
    """Retorna o queryset de turmas."""
    Turma = import_module("turmas.models").Turma
    return Turma.objects.all()


class FiltroAtividadesForm(forms.Form):
    """Filtro alternativo para atividades."""
    curso = forms.ModelChoiceField(
        queryset=get_curso_queryset(),
        required=False,
        label="Curso",
        widget=forms.Select(attrs={"class": "form-select", "id": "filtro-curso"})
    )
    turma = forms.ModelChoiceField(
        queryset=get_turma_queryset(),
        required=False,
        label="Turma",
        widget=forms.Select(attrs={"class": "form-select", "id": "filtro-turma"})
    )
    q = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Buscar por nome ou descrição..."}
        )
    )


## Arquivos views.py:


### Arquivo: atividades\views.py

python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .utils import get_models, get_cursos


def relatorio_atividades(request):
    models = get_models()
    AtividadeAcademica = models['AtividadeAcademica']
    Curso = models['Curso']

    atividades = AtividadeAcademica.objects.prefetch_related('turmas__curso').all()
    curso_id = request.GET.get("curso")
    if curso_id:
        atividades = atividades.filter(turmas__curso__codigo_curso=curso_id)
    cursos_dict = {}
    for atividade in atividades:
        curso = atividade.curso
        if curso not in cursos_dict:
            cursos_dict[curso] = []
        cursos_dict[curso].append(atividade)
    cursos = get_cursos()
    return render(request, "atividades/relatorio_atividades.html", {
        "atividades": atividades,
        "cursos_dict": cursos_dict,
        "cursos": cursos,
        "curso_id": curso_id,
    })


@login_required
def listar_atividades_academicas(request):
    """
    Lista atividades acadêmicas com filtros dinâmicos por curso e turma.
    Suporta AJAX para atualização parcial da tabela e dos selects.
    """
    query = request.GET.get("q", "")
    curso_id = request.GET.get("curso", "")
    turma_id = request.GET.get("turma", "")
    models = get_models()
    Curso = models['Curso']
    Turma = models['Turma']
    AtividadeAcademica = models['AtividadeAcademica']

    cursos = Curso.objects.all()
    turmas = Turma.objects.all()
    atividades = AtividadeAcademica.objects.all()

    if query:
        atividades = atividades.filter(nome__icontains=query)
    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
        turmas = turmas.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
        cursos = cursos.filter(id__in=Turma.objects.filter(id=turma_id).values_list('curso_id', flat=True))

    context = {
        "atividades": atividades,
        "cursos": cursos,
        "turmas": turmas,
        "query": query,
        "curso_selecionado": curso_id,
        "turma_selecionada": turma_id,
    }
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        tabela_html = render_to_string("atividades/academicas/partials/atividades_tabela.html", context, request=request)
        cursos_html = render_to_string("atividades/academicas/partials/cursos_options.html", context, request=request)
        turmas_html = render_to_string("atividades/academicas/partials/turmas_options.html", context, request=request)
        return JsonResponse({
            "tabela_html": tabela_html,
            "cursos_html": cursos_html,
            "turmas_html": turmas_html,
        })
    return render(request, "atividades/academicas/listar_atividades_academicas.html", context)


def ajax_atividades_filtradas(request):
    # ... lógica de filtro ...
    # Sugestão: use get_models() e get_cursos() se necessário
    return render(request, "atividades/partials/atividades_tabela_body.html", {"atividades": atividades})
    return render(request, "atividades/partials/atividades_tabela_body.html", {"atividades": atividades})


## Arquivos urls.py:


### Arquivo: atividades\urls.py

python
from django.urls import path
from . import views
from . import views_api
from .views.relatorios_academicos import relatorio_atividades_academicas
from .views.relatorios_ritualisticos import relatorio_atividades_ritualisticas
from .views import importacao

app_name = "atividades"

urlpatterns = [
    # Atividades Acadêmicas
    path("academicas/", views.academicas.listar_atividades_academicas, name="listar_atividades_academicas"),
    path("academicas/criar/", views.academicas.criar_atividade_academica, name="criar_atividade_academica"),
    path("academicas/<int:id>/editar/", views.academicas.editar_atividade_academica, name="editar_atividade_academica"),
    path("academicas/<int:id>/detalhes/", views.academicas.detalhar_atividade_academica, name="detalhar_atividade_academica"),
    path("academicas/<int:id>/excluir/", views.academicas.excluir_atividade_academica, name="excluir_atividade_academica"),
    path("academicas/<int:id>/copiar/", views.academicas.copiar_atividade_academica, name="copiar_atividade_academica"),

    # AJAX: turmas por curso (listagem)
    path("ajax/turmas-por-curso/", views.academicas.ajax_turmas_por_curso, name="ajax_turmas_por_curso"),
    # AJAX: atividades filtradas (listagem)
    path("ajax/atividades-filtradas/", views.academicas.ajax_atividades_filtradas, name="ajax_atividades_filtradas"),

    # Relatório de atividades por curso/turma
    path(
        "relatorio/curso-turma/",
        views.relatorios.relatorio_atividades_curso_turma,
        name="relatorio_atividades"
    ),
    # Relatório de atividades acadêmicas
    path(
        "relatorio/academicas/",
        relatorio_atividades_academicas,
        name="relatorio_atividades_academicas"
    ),
    # Relatório de atividades ritualísticas
    path(
        "relatorio/ritualisticas/",
        relatorio_atividades_ritualisticas,
        name="relatorio_atividades_ritualisticas"
    ),
    # AJAX: turmas por curso (relatório)
    path("ajax/relatorio/turmas-por-curso/", views.relatorios.ajax_turmas_por_curso_relatorio, name="ajax_turmas_por_curso_relatorio"),
    # AJAX: atividades filtradas (relatório)
    path("ajax/relatorio/atividades-filtradas/", views.relatorios.ajax_atividades_filtradas_relatorio, name="ajax_atividades_filtradas_relatorio"),

    # Dashboard de atividades
    path("dashboard/", views.dashboard.dashboard_atividades, name="dashboard_atividades"),
    # AJAX: turmas por curso (dashboard)
    path("ajax/dashboard/turmas-por-curso/", views.dashboard.ajax_turmas_por_curso_dashboard, name="ajax_turmas_por_curso_dashboard"),
    # AJAX: dashboard filtrado
    path("ajax/dashboard/conteudo/", views.dashboard.ajax_dashboard_conteudo, name="ajax_dashboard_conteudo"),

    # Atividades Ritualísticas
    path("ritualisticas/", views.ritualisticas.listar_atividades_ritualisticas, name="listar_atividades_ritualisticas"),
    path("ritualisticas/criar/", views.ritualisticas.criar_atividade_ritualistica, name="criar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/editar/", views.ritualisticas.editar_atividade_ritualistica, name="editar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/detalhes/", views.ritualisticas.detalhar_atividade_ritualistica, name="detalhar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/excluir/", views.ritualisticas.excluir_atividade_ritualistica, name="excluir_atividade_ritualistica"),
    path("ritualisticas/<int:id>/copiar/", views.ritualisticas.copiar_atividade_ritualistica, name="copiar_atividade_ritualistica"),

    # Calendário de Atividades
    path("calendario_atividades/", views.calendario.calendario_atividades, name="calendario_atividades"),

    # API
    path("api/filtrar-atividades/", views_api.api_filtrar_atividades, name="api_filtrar_atividades"),

    # Importação de Atividades
    path(
        "academicas/importar/",
        importacao.importar_atividades_academicas,
        name="importar_atividades_academicas"
    ),
    path(
        "ritualisticas/importar/",
        importacao.importar_atividades_ritualisticas,
        name="importar_atividades_ritualisticas"
    ),
]


## Arquivos models.py:


### Arquivo: atividades\models.py

python
from django.db import models
from django.utils import timezone

class AtividadeAcademica(models.Model):
    """
    Modelo para atividades acadêmicas como aulas, palestras, workshops, etc.
    """
    TIPO_CHOICES = [
        ('AULA', 'Aula'),
        ('PALESTRA', 'Palestra'),
        ('WORKSHOP', 'Workshop'),
        ('SEMINARIO', 'Seminário'),
        ('OUTRO', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    tipo_atividade = models.CharField(
        max_length=20, 
        choices=TIPO_CHOICES,
        default='AULA'
    )
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField(blank=True, null=True)
    local = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    # Relacionamentos
    curso = models.ForeignKey(
        'cursos.Curso', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='atividades'
    )
    turmas = models.ManyToManyField(
        'turmas.Turma', 
        blank=True,
        related_name='atividades'
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Acadêmica'
        verbose_name_plural = 'Atividades Acadêmicas'
        ordering = ['-data_inicio', 'hora_inicio']

class AtividadeRitualistica(models.Model):
    """
    Modelo para atividades ritualísticas.
    """
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField(blank=True, null=True)
    local = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    # Relacionamentos
    participantes = models.ManyToManyField(
        'alunos.Aluno', 
        blank=True,
        related_name='atividades_ritualisticas'
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Ritualística'
        verbose_name_plural = 'Atividades Ritualísticas'
        ordering = ['-data', 'hora_inicio']



## Arquivos de Views Modulares:


### Arquivo: atividades\views\__init__.py

python
from .academicas import (
    listar_atividades_academicas,
    criar_atividade_academica,
    editar_atividade_academica,
    detalhar_atividade_academica,
    excluir_atividade_academica,
    confirmar_exclusao_academica,
    copiar_atividade_academica,
    alunos_por_turma,
    api_get_turmas_por_curso,
    api_get_cursos_por_turma,
)

from .ritualisticas import (
    listar_atividades_ritualisticas,
    criar_atividade_ritualistica,
    editar_atividade_ritualistica,
    detalhar_atividade_ritualistica,
    excluir_atividade_ritualistica,
)

from .dashboard import (
    dashboard_atividades,
)

from .relatorios import (
    relatorio_atividades,
    relatorio_atividades_curso_turma,
    exportar_atividades,
    exportar_atividades_csv,
    exportar_atividades_pdf,
    exportar_atividades_excel,
)

from .importacao import (
    importar_atividades_academicas,
    importar_atividades_ritualisticas,
)

from .calendario import (
    api_eventos_calendario,
    api_detalhe_evento,
    calendario_atividades,
)




### Arquivo: atividades\views\academicas.py

python
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from importlib import import_module
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET

from .utils import (
    get_models,
    get_form_class,
    get_model_class,
    get_turma_model,
    get_aluno_model,
    get_cursos,
    get_turmas,
    get_atividades_academicas,
)

logger = logging.getLogger(__name__)

@login_required
def listar_atividades_academicas(request):
    query = request.GET.get('q', '')
    curso_id = request.GET.get('curso', '')
    turma_id = request.GET.get('turma', '')

    atividades = get_atividades_academicas().select_related('curso').prefetch_related('turmas')
    cursos = get_cursos()
    turmas = get_turmas()

    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
        turmas = turmas.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    if query:
        atividades = atividades.filter(nome__icontains=query)

    context = {
        'atividades': atividades.distinct(),
        'cursos': cursos,
        'turmas': turmas,
        'curso_selecionado': curso_id,
        'turma_selecionada': turma_id,
        'query': query,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request,
            "atividades/academicas/partials/atividades_tabela.html",
            context
        )
    return render(
        request,
        "atividades/academicas/listar_atividades_academicas.html",
        context
    )
@require_GET
@login_required
def ajax_turmas_por_curso(request):
    curso_id = request.GET.get("curso") or request.GET.get("curso_id")
    models = get_models()
    Turma = models['Turma']
    if curso_id:
        turmas = Turma.objects.filter(curso_id=curso_id)
    else:
        turmas = Turma.objects.all()
    data = [{"id": turma.id, "nome": turma.nome} for turma in turmas]
    return JsonResponse({"turmas": data})

@require_GET
@login_required
def ajax_atividades_filtradas(request):
    return listar_atividades_academicas(request)

@login_required
def criar_atividade_academica(request):
    try:
        AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST)
            if form.is_valid():
                atividade = form.save()
                messages.success(
                    request,
                    "Atividade acadêmica criada com sucesso!"
                )
                return redirect("atividades:listar_atividades_academicas")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeAcademicaForm()
        return render(
            request,
            "atividades/academicas/criar_atividade_academica.html",  # <-- Corrija aqui
            {"form": form}
        )
    except Exception as e:
        logger.error(
            f"Erro ao criar atividade acadêmica: {str(e)}",
            exc_info=True
        )
        messages.error(
            request,
            f"Ocorreu um erro ao criar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def editar_atividade_academica(request, id):
    try:
        models = get_models()
        AtividadeAcademica = models['AtividadeAcademica']
        AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
        atividade = get_object_or_404(AtividadeAcademica, id=id)
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST, instance=atividade)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Atividade acadêmica atualizada com sucesso!"
                )
                return redirect("atividades:listar_atividades_academicas")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeAcademicaForm(instance=atividade)
        return render(
            request,
            "atividades/academicas/editar_atividade_academica.html",
            {"form": form, "atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao editar atividade acadêmica {id}: {str(e)}",
            exc_info=True
        )
        messages.error(
            request,
            f"Ocorreu um erro ao editar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def detalhar_atividade_academica(request, id):
    try:
        models = get_models()
        AtividadeAcademica = models['AtividadeAcademica']
        atividade = get_object_or_404(
            AtividadeAcademica.objects.select_related("curso").prefetch_related("turmas"),
            id=id
        )
        return render(
            request,
            "atividades/academicas/detalhar_atividade_academica.html",
            {"atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao detalhar atividade acadêmica {id}: {str(e)}",
            exc_info=True
        )
        messages.error(
            request,
            f"Ocorreu um erro ao exibir os detalhes da atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def excluir_atividade_academica(request, id):
    try:
        models = get_models()
        AtividadeAcademica = models['AtividadeAcademica']
        atividade = get_object_or_404(AtividadeAcademica, id=id)
        if request.method == "POST":
            atividade.delete()
            messages.success(
                request,
                "Atividade acadêmica excluída com sucesso!"
            )
            return redirect("atividades:listar_atividades_academicas")
        return render(
            request,
            "atividades/academicas/excluir_atividade_academica.html",
            {"atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao excluir atividade acadêmica {id}: {str(e)}",
            exc_info=True
        )
        messages.error(
            request,
            f"Ocorreu um erro ao excluir a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def confirmar_exclusao_academica(request, pk):
    try:
        AtividadeAcademica = get_model_class("AtividadeAcademica")
        atividade = get_object_or_404(AtividadeAcademica, pk=pk)
        return_url = request.GET.get(
            "return_url",
            reverse("atividades:listar_atividades_academicas")
        )
        if request.method == "POST":
            try:
                nome_atividade = atividade.nome
                atividade.delete()
                messages.success(
                    request,
                    f"Atividade acadêmica '{nome_atividade}' excluída com sucesso."
                )
                return redirect(return_url)
            except (AtividadeAcademica.DoesNotExist, ValueError) as e:
                logger.error(
                    f"Erro ao excluir atividade acadêmica: {str(e)}",
                    exc_info=True
                )
                messages.error(
                    request,
                    f"Erro ao excluir atividade acadêmica: {str(e)}"
                )
                return redirect("atividades:detalhar_atividade_academica", pk=pk)
        return render(
            request,
            "atividades/confirmar_exclusao_academica.html",
            {"atividade": atividade, "return_url": return_url},
        )
    except Exception as e:
        logger.error(
            f"Erro ao processar confirmação de exclusão: {str(e)}",
            exc_info=True
        )
        messages.error(
            request,
            f"Ocorreu um erro ao processar a solicitação: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def copiar_atividade_academica(request, id):
    try:
        AtividadeAcademica = get_model_class("AtividadeAcademica")
        AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
        atividade_original = get_object_or_404(AtividadeAcademica, id=id)
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST)
            if form.is_valid():
                nova_atividade = form.save(commit=False)
                # Se quiser copiar algum campo fixo da original, faça aqui
                nova_atividade.save()
                form.save_m2m()
                messages.success(request, "Atividade copiada com sucesso!")
                return redirect("atividades:listar_atividades_academicas")
        else:
            # Pré-preenche o formulário com os dados da atividade original
            form = AtividadeAcademicaForm(instance=atividade_original)
            form.initial['nome'] = f"Cópia de {atividade_original.nome}"
        return render(
            request,
            "atividades/academicas/copiar_atividade_academica.html",
            {
                "form": form,
                "atividade_original": atividade_original,
            },
        )
    except (ImportError, AttributeError, ValueError) as e:
        logger.error(
            "Erro ao copiar atividade acadêmica %s: %s",
            id,
            str(e),
            exc_info=True
        )
        messages.error(
            request,
            f"Ocorreu um erro ao copiar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")
    except ObjectDoesNotExist as e:
        logger.error(
            "Objeto não encontrado ao copiar atividade acadêmmica %s: %s",
            id,
            str(e),
            exc_info=True
        )
        messages.error(
            request,
            f"Atividade acadêmica não encontrada: {str(e)}"
        )
        return redirect("atividades:listar_atividades_academicas")

@login_required
def alunos_por_turma(request, turma_id):
    try:
        Matricula = import_module("matriculas.models").Matricula
        alunos = Matricula.objects.filter(
            turma_id=turma_id
        ).select_related('aluno')
        data = [
            {
                "nome": m.aluno.nome,
                "foto": m.aluno.foto.url if m.aluno.foto else None,
                "cpf": m.aluno.cpf,
            }
            for m in alunos
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        logger.error(
            "Erro ao obter alunos da turma %s: %s",
            turma_id,
            str(e),
            exc_info=True
        )
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def api_get_turmas_por_curso(request):
    try:
        curso_id = request.GET.get("curso") or request.GET.get("curso_id")
        models = get_models()
        Turma = models['Turma']
        if curso_id:
            try:
                curso_id = int(curso_id)
                turmas = Turma.objects.filter(curso_id=curso_id)
            except ValueError:
                return JsonResponse(
                    {
                        "error": "ID do curso inválido. Deve ser um número inteiro."
                    },
                    status=400
                )
        else:
            turmas = Turma.objects.all()
        data = [
            {
                "id": turma.id,
                "nome": turma.nome,
                "codigo": turma.codigo if hasattr(turma, 'codigo') else None,
            }
            for turma in turmas
        ]
        return JsonResponse({"turmas": data})
    except Exception as e:
        logger.error(
            "Erro ao obter turmas por curso: %s",
            str(e),
            exc_info=True
        )
        return JsonResponse(
            {
                "error": "Erro ao processar a solicitação. Tente novamente."
            },
            status=500
        )

@login_required
def api_get_cursos_por_turma(request):
    try:
        turma_id = request.GET.get("turma_id")
        if not turma_id:
            models = get_models()
            Curso = models['Curso']
            cursos = Curso.objects.all()
            data = [
                {
                    "id": curso.id,
                    "nome": curso.nome,
                    "codigo_curso": (
                        curso.codigo_curso
                        if hasattr(curso, 'codigo_curso')
                        else None
                    ),
                }
                for curso in cursos
            ]
            return JsonResponse({"cursos": data})
        try:
            turma_id = int(turma_id)
        except ValueError:
            return JsonResponse(
                {
                    "error": "ID da turma inválido. Deve ser um número inteiro."
                },
                status=400
            )
        models = get_models()
        Turma = models['Turma']
        try:
            turma = Turma.objects.get(id=turma_id)
            curso = turma.curso
            if curso:
                data = {
                    "id": curso.id,
                    "nome": curso.nome,
                    "codigo_curso": (
                        curso.codigo_curso
                        if hasattr(curso, 'codigo_curso')
                        else None
                    ),
                }
                return JsonResponse({"cursos": [data]})
            else:
                return JsonResponse({"cursos": []})
        except Turma.DoesNotExist:
            return JsonResponse(
                {"error": "Turma não encontrada."},
                status=404
            )
    except Exception as e:
        logger.error(
            "Erro ao obter cursos por turma: %s",
            str(e),
            exc_info=True
        )
        return JsonResponse(
            {
                "error": "Erro ao processar a solicitação. Tente novamente."
            },
            status=500
        )




### Arquivo: atividades\views\calendario.py

python
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from .utils import get_model_class

# Set up logger
logger = logging.getLogger(__name__)

@login_required
def calendario_atividades(request):
    """Exibe o calendário de atividades."""
    # Obter todas as turmas para o filtro
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status='A')  # Apenas turmas ativas
    
    return render(
        request,
        "atividades/calendario_atividades.html",
        {
            "turmas": turmas,
        },
    )

@login_required
def api_eventos_calendario(request):
    """API para fornecer eventos para o calendário."""
    # Obter parâmetros
    start_date = request.GET.get('start', '')
    end_date = request.GET.get('end', '')
    tipo_filtro = request.GET.get('tipo', 'todas')
    turma_filtro = request.GET.get('turma', 'todas')
    mostrar_concluidas = request.GET.get('concluidas', '1') == '1'
    
    # Obter modelos
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    eventos = []
    
    # Adicionar atividades acadêmicas
    if tipo_filtro in ['todas', 'academicas']:
        atividades_academicas = AtividadeAcademica.objects.all()
        
        # Aplicar filtro de data
        if start_date:
            atividades_academicas = atividades_academicas.filter(data_inicio__gte=start_date)
        if end_date:
            atividades_academicas = atividades_academicas.filter(data_inicio__lte=end_date)
        
        # Aplicar filtro de turma
        if turma_filtro != 'todas':
            atividades_academicas = atividades_academicas.filter(turmas__id=turma_filtro)
        
        # Aplicar filtro de status concluído
        if not mostrar_concluidas:
            atividades_academicas = atividades_academicas.exclude(status='concluida')
        
        # Converter para formato de evento do FullCalendar
        for atividade in atividades_academicas:
            evento = {
                'id': atividade.id,
                'title': atividade.nome,
                'start': atividade.data_inicio.isoformat(),
                'end': atividade.data_fim.isoformat() if atividade.data_fim else None,
                'allDay': True,  # Por padrão, eventos de dia inteiro
                'tipo': 'academica',
                'status': atividade.status,
                'description': atividade.descricao or '',
            }
            eventos.append(evento)
    
    # Adicionar atividades ritualísticas
    if tipo_filtro in ['todas', 'ritualisticas']:
        atividades_ritualisticas = AtividadeRitualistica.objects.all()
        
        # Aplicar filtro de data
        if start_date:
            atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=start_date)
        if end_date:
            atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=end_date)
        
        # Aplicar filtro de turma
        if turma_filtro != 'todas':
            atividades_ritualisticas = atividades_ritualisticas.filter(turma_id=turma_filtro)
        
        # Converter para formato de evento do FullCalendar
        for atividade in atividades_ritualisticas:
            # Combinar data e hora para criar datetime completo
            data = atividade.data
            
            # Converter hora_inicio e hora_fim para objetos time
            hora_inicio = atividade.hora_inicio
            hora_fim = atividade.hora_fim
            
            # Criar datetime para início e fim
            start_datetime = datetime.combine(data, hora_inicio)
            end_datetime = datetime.combine(data, hora_fim)
            
            evento = {
                'id': atividade.id,
                'title': atividade.nome,
                'start': start_datetime.isoformat(),
                'end': end_datetime.isoformat(),
                'allDay': False,  # Eventos ritualísticos têm horário específico
                'tipo': 'ritualistica',
                'description': atividade.descricao or '',
            }
            eventos.append(evento)
    
    return JsonResponse(eventos, safe=False)

@login_required
def api_detalhe_evento(request, evento_id):
    """API para fornecer detalhes de um evento específico."""
    tipo = request.GET.get('tipo', '')
    
    try:
        if tipo == 'academica':
            AtividadeAcademica = get_model_class("AtividadeAcademica")
            atividade = get_object_or_404(AtividadeAcademica, id=evento_id)
            
            # Formatar dados para resposta JSON
            evento = {
                'nome': atividade.nome,
                'descricao': atividade.descricao,
                'data_inicio': atividade.data_inicio.strftime('%d/%m/%Y'),
                'data_fim': atividade.data_fim.strftime('%d/%m/%Y') if atividade.data_fim else None,
                'responsavel': atividade.responsavel,
                'local': atividade.local,
                'tipo': atividade.tipo_atividade,
                'tipo_display': atividade.get_tipo_atividade_display(),
                'status': atividade.status,
                'status_display': atividade.get_status_display(),
                'turmas': [turma.nome for turma in atividade.turmas.all()]
            }
            
            return JsonResponse({'success': True, 'evento': evento})
        
        elif tipo == 'ritualistica':
            AtividadeRitualistica = get_model_class("AtividadeRitualistica")
            atividade = get_object_or_404(AtividadeRitualistica, id=evento_id)
            
            # Formatar dados para resposta JSON
            evento = {
                'nome': atividade.nome,
                'descricao': atividade.descricao,
                'data': atividade.data.strftime('%d/%m/%Y'),
                'hora_inicio': atividade.hora_inicio.strftime('%H:%M'),
                'hora_fim': atividade.hora_fim.strftime('%H:%M'),
                'local': atividade.local,
                'turma': atividade.turma.nome if atividade.turma else 'Sem turma',
                'total_participantes': atividade.participantes.count(),
            }
            
            return JsonResponse({'success': True, 'evento': evento})
        
        else:
            return JsonResponse({'success': False, 'error': 'Tipo de evento inválido'}, status=400)
    
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do evento: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



### Arquivo: atividades\views\dashboard.py

python
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from importlib import import_module

from ..models import AtividadeAcademica

@login_required
def dashboard_atividades(request):
    """
    Dashboard de atividades com filtros dinâmicos por curso e turma.
    Suporta AJAX para atualização dos cards/gráficos/tabelas.
    """
    Curso = import_module("cursos.models").Curso
    Turma = import_module("turmas.models").Turma

    cursos = Curso.objects.all()
    turmas = Turma.objects.all()

    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")

    atividades = AtividadeAcademica.objects.all()

    if curso_id:
        atividades = atividades.filter(turma__curso_id=curso_id)
        turmas = turmas.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)

    atividades = atividades.select_related("curso").prefetch_related("turmas").distinct()

    # Exemplo de dados para cards
    total_atividades = atividades.count()
    total_turmas = turmas.count()
    total_cursos = cursos.count()

    context = {
        "atividades": atividades,
        "cursos": cursos,
        "turmas": turmas,
        "curso_selecionado": curso_id,
        "turma_selecionada": turma_id,
        "total_atividades": total_atividades,
        "total_turmas": total_turmas,
        "total_cursos": total_cursos,
    }

    # AJAX: retorna apenas o conteúdo do dashboard para atualização dinâmica
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "atividades/_dashboard_conteudo.html", context)

    return render(request, "atividades/dashboard.html", context)

@require_GET
@login_required
def ajax_turmas_por_curso_dashboard(request):
    """
    Endpoint AJAX: retorna as turmas de um curso em JSON (para dashboard).
    """
    curso_id = request.GET.get("curso_id")
    Turma = import_module("turmas.models").Turma
    turmas = Turma.objects.filter(curso_id=curso_id).values("id", "nome")
    return JsonResponse(list(turmas), safe=False)

@require_GET
@login_required
def ajax_dashboard_conteudo(request):
    """
    Endpoint AJAX: retorna conteúdo do dashboard filtrado.
    """
    return dashboard_atividades(request)




### Arquivo: atividades\views\importacao.py

python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from io import TextIOWrapper
import csv
import datetime

from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from alunos.models import Aluno

def parse_date(date_str):
    """Converte uma string de data para um objeto date."""
    if not date_str:
        return None
    
    # Tentar diferentes formatos
    formats = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"Formato de data inválido: {date_str}")

def parse_time(time_str):
    """Converte uma string de hora para um objeto time."""
    if not time_str:
        return None
    
    # Tentar diferentes formatos
    formats = ["%H:%M", "%H:%M:%S"]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    
    raise ValueError(f"Formato de hora inválido: {time_str}")

@login_required
def importar_atividades_academicas(request):
    """Importa atividades acadêmicas a partir de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
        reader = csv.DictReader(csv_file)
        count = 0
        errors = []
        for row in reader:
            try:
                atividade = AtividadeAcademica(
                    nome=row.get("Nome", "").strip(),
                    descricao=row.get("Descricao", "").strip(),
                    tipo_atividade=row.get("Tipo", "AULA").strip().upper(),
                    data_inicio=parse_date(row.get("Data_Inicio", "")),
                    data_fim=parse_date(row.get("Data_Fim", "")),
                    hora_inicio=parse_time(row.get("Hora_Inicio", "")),
                    hora_fim=parse_time(row.get("Hora_Fim", "")),
                    local=row.get("Local", "").strip(),
                    responsavel=row.get("Responsavel", "").strip(),
                    status=row.get("Status", "PENDENTE").strip().upper(),
                )
                atividade.full_clean()
                atividade.save()
                # Turmas (opcional)
                turmas_str = row.get("Turmas", "").strip()
                if turmas_str:
                    turmas_ids = [t.strip() for t in turmas_str.split(",")]
                    for turma_id in turmas_ids:
                        try:
                            turma = Turma.objects.get(id=turma_id)
                            atividade.turmas.add(turma)
                        except Turma.DoesNotExist:
                            errors.append(f"Turma com ID {turma_id} não encontrada para '{atividade.nome}'")
                count += 1
            except Exception as e:
                errors.append(f"Erro na linha {count+1}: {str(e)}")
        if errors:
            messages.warning(request, f"{count} atividades importadas com {len(errors)} erros.")
            for error in errors[:5]:
                messages.error(request, error)
        else:
            messages.success(request, f"{count} atividades importadas com sucesso!")
        return redirect("atividades:listar_atividades_academicas")
    return render(request, "atividades/importar_atividades_academicas.html")

@login_required
def importar_atividades_ritualisticas(request):
    """Importa atividades ritualísticas a partir de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
        reader = csv.DictReader(csv_file)
        count = 0
        errors = []
        for row in reader:
            try:
                atividade = AtividadeRitualistica(
                    nome=row.get("Nome", "").strip(),
                    descricao=row.get("Descricao", "").strip(),
                    data=parse_date(row.get("Data", "")),
                    hora_inicio=parse_time(row.get("Hora_Inicio", "")),
                    hora_fim=parse_time(row.get("Hora_Fim", "")),
                    local=row.get("Local", "").strip(),
                    responsavel=row.get("Responsavel", "").strip(),
                    status=row.get("Status", "PENDENTE").strip().upper(),
                )
                atividade.full_clean()
                atividade.save()
                # Participantes (opcional)
                participantes_str = row.get("Participantes", "").strip()
                if participantes_str:
                    cpfs = [p.strip() for p in participantes_str.split(",")]
                    for cpf in cpfs:
                        try:
                            aluno = Aluno.objects.get(cpf=cpf)
                            atividade.participantes.add(aluno)
                        except Aluno.DoesNotExist:
                            errors.append(f"Aluno com CPF {cpf} não encontrado para '{atividade.nome}'")
                count += 1
            except Exception as e:
                errors.append(f"Erro na linha {count+1}: {str(e)}")
        if errors:
            messages.warning(request, f"{count} atividades importadas com {len(errors)} erros.")
            for error in errors[:5]:
                messages.error(request, error)
        else:
            messages.success(request, f"{count} atividades importadas com sucesso!")
        return redirect("atividades:listar_atividades_ritualisticas")
    return render(request, "atividades/importar_atividades_ritualisticas.html")



### Arquivo: atividades\views\relatorios.py

python
import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime, timedelta
from django.views.decorators.http import require_GET

from .utils import get_model_class

# Set up logger
logger = logging.getLogger(__name__)

@login_required
def relatorio_atividades(request):
    """Gera um relatório de atividades com base nos filtros aplicados."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    # Obter parâmetros de filtro
    tipo = request.GET.get('tipo', 'todas')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
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
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Calcular totais
    total_academicas = atividades_academicas.count()
    total_ritualisticas = atividades_ritualisticas.count()
    total_atividades = total_academicas + total_ritualisticas
    
    return render(
        request,
        "atividades/relatorio_atividades.html",
        {
            "atividades_academicas": atividades_academicas,
            "atividades_ritualisticas": atividades_ritualisticas,
            "total_academicas": total_academicas,
            "total_ritualisticas": total_ritualisticas,
            "total_atividades": total_atividades,
            "tipo": tipo,
            "status": status,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        },
    )

@login_required
def exportar_atividades(request, formato):
    """Exporta as atividades filtradas para o formato especificado."""
    # Obter os mesmos filtros que no relatório
    tipo = request.GET.get('tipo', 'todas')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Obter atividades filtradas (mesmo código do relatório)
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    atividades_academicas = AtividadeAcademica.objects.all()
    if status:
        atividades_academicas = atividades_academicas.filter(status=status)
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)
    
    atividades_ritualisticas = AtividadeRitualistica.objects.all()
    if data_inicio:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=data_inicio)
    if data_fim:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)
    
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Exportar para o formato solicitado
    if formato == 'csv':
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)
    elif formato == 'excel':
        return exportar_atividades_excel(atividades_academicas, atividades_ritualisticas)
    elif formato == 'pdf':
        return exportar_atividades_pdf(atividades_academicas, atividades_ritualisticas)
    else:
        messages.error(request, f"Formato de exportação '{formato}' não suportado.")
        return redirect('atividades:relatorio_atividades')

def exportar_atividades_csv(atividades_academicas, atividades_ritualisticas):
    """Exporta as atividades para CSV."""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="atividades.csv"'
    
    writer = csv.writer(response)
    
    # Cabeçalho para atividades acadêmicas
    writer.writerow(['Tipo', 'Nome', 'Descrição', 'Data de Início', 'Data de Término', 
                     'Responsável', 'Local', 'Status', 'Tipo de Atividade'])
    
    # Dados das atividades acadêmicas
    for atividade in atividades_academicas:
        writer.writerow([
            'Acadêmica',
            atividade.nome,
            atividade.descricao or '',
            atividade.data_inicio.strftime('%d/%m/%Y'),
            atividade.data_fim.strftime('%d/%m/%Y') if atividade.data_fim else '',
            atividade.responsavel or '',
            atividade.local or '',
            atividade.get_status_display(),
            atividade.get_tipo_atividade_display(),
        ])
    
    # Dados das atividades ritualísticas
    for atividade in atividades_ritualisticas:
        writer.writerow([
            'Ritualística',
            atividade.nome,
            atividade.descricao or '',
            atividade.data.strftime('%d/%m/%Y'),
            '',  # Não tem data_fim
            '',  # Não tem responsável
            atividade.local,
            '',  # Não tem status
            '',  # Não tem tipo_atividade
        ])
    
    return response

def exportar_atividades_excel(atividades_academicas, atividades_ritualisticas):
    """Exporta as atividades para Excel."""
    # Implementação básica usando pandas
    try:
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        # Criar DataFrames para cada tipo de atividade
        dados_academicas = []
        for atividade in atividades_academicas:
            dados_academicas.append({
                'Tipo': 'Acadêmica',
                'Nome': atividade.nome,
                'Descrição': atividade.descricao or '',
                'Data de Início': atividade.data_inicio,
                'Data de Término': atividade.data_fim,
                'Responsável': atividade.responsavel or '',
                'Local': atividade.local or '',
                'Status': atividade.get_status_display(),
                'Tipo de Atividade': atividade.get_tipo_atividade_display(),
            })
        
        dados_ritualisticas = []
        for atividade in atividades_ritualisticas:
            dados_ritualisticas.append({
                'Tipo': 'Ritualística',
                'Nome': atividade.nome,
                'Descrição': atividade.descricao or '',
                'Data': atividade.data,
                'Horário': f"{atividade.hora_inicio} - {atividade.hora_fim}",
                'Local': atividade.local,
                'Turma': atividade.turma.nome,
                'Participantes': atividade.participantes.count(),
            })
        
        # Criar arquivo Excel com múltiplas abas
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            if dados_academicas:
                df_academicas = pd.DataFrame(dados_academicas)
                df_academicas.to_excel(writer, sheet_name='Atividades Acadêmicas', index=False)
            
            if dados_ritualisticas:
                df_ritualisticas = pd.DataFrame(dados_ritualisticas)
                df_ritualisticas.to_excel(writer, sheet_name='Atividades Ritualísticas', index=False)
        
        # Configurar resposta HTTP
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="atividades.xlsx"'
        
        return response
    except ImportError:
        # Fallback para CSV se pandas não estiver disponível
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)

def exportar_atividades_pdf(atividades_academicas, atividades_ritualisticas):
    """Exporta as atividades para PDF."""
    # Implementação básica usando reportlab
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from django.http import HttpResponse
        import io
        
        # Configurar buffer e documento
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        subtitle_style = styles['Heading2']
        
        # Título
        elements.append(Paragraph("Relatório de Atividades", title_style))
        elements.append(Spacer(1, 12))
        
        # Atividades Acadêmicas
        if atividades_academicas:
            elements.append(Paragraph("Atividades Acadêmicas", subtitle_style))
            elements.append(Spacer(1, 6))
            
            # Dados para a tabela
            data = [['Nome', 'Tipo', 'Data de Início', 'Status', 'Responsável']]
            
            for atividade in atividades_academicas:
                data.append([
                    atividade.nome,
                    atividade.get_tipo_atividade_display(),
                    atividade.data_inicio.strftime('%d/%m/%Y'),
                    atividade.get_status_display(),
                    atividade.responsavel or 'Não informado',
                ])
            
            # Criar tabela
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 12))
        
        # Atividades Ritualísticas
        if atividades_ritualisticas:
            elements.append(Paragraph("Atividades Ritualísticas", subtitle_style))
            elements.append(Spacer(1, 6))
            
            # Dados para a tabela
            data = [['Nome', 'Data', 'Horário', 'Local', 'Turma', 'Participantes']]
            
            for atividade in atividades_ritualisticas:
                data.append([
                    atividade.nome,
                    atividade.data.strftime('%d/%m/%Y'),
                    f"{atividade.hora_inicio} - {atividade.hora_fim}",
                    atividade.local,
                    atividade.turma.nome,
                    str(atividade.participantes.count()),
                ])
            
            # Criar tabela
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(table)
        
        # Gerar PDF
        doc.build(elements)
        
        # Configurar resposta HTTP
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="atividades.pdf"'
        
        return response
    except ImportError:
        # Fallback para CSV se reportlab não estiver disponível
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from importlib import import_module

from ..models import AtividadeAcademica

@login_required
def relatorio_atividades_curso_turma(request):
    """
    Relatório de atividades acadêmicas filtrado por curso e turma.
    Suporta AJAX para atualização parcial da tabela.
    """
    Curso = import_module("cursos.models").Curso
    Turma = import_module("turmas.models").Turma

    cursos = Curso.objects.all()
    turmas = Turma.objects.all()

    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")

    atividades = AtividadeAcademica.objects.all()

    if curso_id:
        atividades = atividades.filter(turma__curso_id=curso_id)
        turmas = turmas.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)

    atividades = atividades.select_related("curso").prefetch_related("turmas").distinct()

    context = {
        "atividades": atividades,
        "cursos": cursos,
        "turmas": turmas,
        "curso_selecionado": curso_id,
        "turma_selecionada": turma_id,
    }

    # AJAX: retorna apenas o corpo da tabela para atualização dinâmica
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "atividades/_tabela_atividades.html", context)

    return render(request, "atividades/relatorio_atividades_curso_turma.html", context)

@require_GET
@login_required
def ajax_turmas_por_curso_relatorio(request):
    """
    Endpoint AJAX: retorna as turmas de um curso em JSON (para relatório).
    """
    curso_id = request.GET.get("curso_id")
    Turma = import_module("turmas.models").Turma
    turmas = Turma.objects.filter(curso_id=curso_id).values("id", "nome")
    return JsonResponse(list(turmas), safe=False)

@require_GET
@login_required
def ajax_atividades_filtradas_relatorio(request):
    """
    Endpoint AJAX: retorna atividades filtradas por curso/turma para relatório.
    Retorna HTML parcial da tabela.
    """
    return relatorio_atividades_curso_turma(request)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import AtividadeRitualistica
from ..views.utils import get_model_class

@login_required
def relatorio_atividades_ritualisticas(request):
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status='A')
    turma_id = request.GET.get("turma")
    data = request.GET.get("data")

    atividades = AtividadeRitualistica.objects.all()
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    if data:
        atividades = atividades.filter(data=data)

    return render(
        request,
        "atividades/ritualisticas/relatorio_ritualisticas.html",
        {
            "atividades": atividades,
            "turmas": turmas,
            "turma_selecionada": turma_id,
            "data_selecionada": data,
        }
    )




### Arquivo: atividades\views\relatorios_academicos.py

python
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..views.utils import get_cursos, get_turmas, get_atividades_academicas

logger = logging.getLogger(__name__)

@login_required
def relatorio_atividades_academicas(request):
    cursos = get_cursos()
    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")
    query = request.GET.get("q", "")

    atividades = get_atividades_academicas(curso_id=curso_id, turma_id=turma_id, query=query)

    # Organiza atividades por curso
    cursos_dict = {}
    for atividade in atividades:
        curso_nome = atividade.curso.nome if atividade.curso else "Sem curso"
        cursos_dict.setdefault(curso_nome, []).append(atividade)

    context = {
        "cursos": cursos,
        "curso_id": curso_id,
        "cursos_dict": cursos_dict,
    }
    return render(request, "atividades/academicas/relatorio_atividades_academicas.html", context)



### Arquivo: atividades\views\relatorios_ritualisticos.py

python
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..views.utils import get_model_class, get_turma_model

logger = logging.getLogger(__name__)

@login_required
def relatorio_atividades_ritualisticas(request):
    Turma = get_turma_model()
    turmas = Turma.objects.filter(status='A')
    turma_id = request.GET.get("turma")
    data = request.GET.get("data")

    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividades = AtividadeRitualistica.objects.all()
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    if data:
        atividades = atividades.filter(data=data)

    context = {
        "atividades": atividades,
        "turmas": turmas,
        "turma_selecionada": turma_id,
        "data_selecionada": data,
    }
    return render(
        request,
        "atividades/ritualisticas/relatorio_atividades_ritualisticas.html",
        context
    )



### Arquivo: atividades\views\ritualisticas.py

python
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from importlib import import_module

from .utils import get_form_class, get_model_class

# Configurar logger
logger = logging.getLogger(__name__)


@login_required
def listar_atividades_ritualisticas(request):
    """Lista todas as atividades ritualísticas."""
    try:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        
        # Obter parâmetros de filtro
        query = request.GET.get("q", "")
        
        # Consulta base
        atividades = AtividadeRitualistica.objects.all().prefetch_related("participantes")
        
        # Aplicar filtros
        if query:
            atividades = atividades.filter(
                Q(nome__icontains=query) |
                Q(descricao__icontains=query)
            )
        
        # Paginação
        paginator = Paginator(atividades, 10)  # 10 itens por página
        page = request.GET.get('page')
        
        try:
            atividades_paginadas = paginator.page(page)
        except PageNotAnInteger:
            atividades_paginadas = paginator.page(1)
        except EmptyPage:
            atividades_paginadas = paginator.page(paginator.num_pages)
        
        context = {
            "atividades": atividades_paginadas,
            "page_obj": atividades_paginadas,
            "query": query,
            "total_atividades": atividades.count(),
        }
        
        return render(
            request, 
            "atividades/ritualisticas/listar_atividades_ritualisticas.html", 
            context
        )
    except Exception as e:
        logger.error(
            f"Erro ao listar atividades ritualísticas: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao listar as atividades: {str(e)}"
        )
        return render(
            request,
            "atividades/ritualisticas/listar_atividades_ritualisticas.html",
            {
                "atividades": [],
                "page_obj": None,
                "query": "",
                "error_message": f"Erro ao listar atividades: {str(e)}",
            }
        )

@login_required
def criar_atividade_ritualistica(request):
    """Cria uma nova atividade ritualística."""
    try:
        AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
        
        if request.method == "POST":
            form = AtividadeRitualisticaForm(request.POST)
            if form.is_valid():
                atividade = form.save()
                messages.success(
                    request, 
                    "Atividade ritualística criada com sucesso!"
                )
                return redirect("atividades:listar_atividades_ritualisticas")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeRitualisticaForm()
        
        return render(
            request, 
            "atividades/ritualisticas/form_atividade_ritualistica.html", 
            {"form": form}
        )
    except Exception as e:
        logger.error(
            f"Erro ao criar atividade ritualística: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao criar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_ritualisticas")

@login_required
def editar_atividade_ritualistica(request, id):
    """Edita uma atividade ritualística existente."""
    try:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
        
        atividade = get_object_or_404(AtividadeRitualistica, id=id)
        
        if request.method == "POST":
            form = AtividadeRitualisticaForm(request.POST, instance=atividade)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 
                    "Atividade ritualística atualizada com sucesso!"
                )
                return redirect("atividades:listar_atividades_ritualisticas")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeRitualisticaForm(instance=atividade)
        
        return render(
            request, 
            "atividades/ritualisticas/form_atividade_ritualistica.html", 
            {"form": form, "atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao editar atividade ritualística {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao editar a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_ritualisticas")

@login_required
def detalhar_atividade_ritualistica(request, id):
    """Exibe detalhes de uma atividade ritualística."""
    try:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        
        atividade = get_object_or_404(
            AtividadeRitualistica.objects.prefetch_related("participantes"),
            id=id
        )
        
        return render(
            request, 
            "atividades/ritualisticas/detalhar_atividade_ritualistica.html", 
            {"atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao detalhar atividade ritualística {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao exibir os detalhes da atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_ritualisticas")

@login_required
def excluir_atividade_ritualistica(request, id):
    """Exclui uma atividade ritualística."""
    try:
        AtividadeRitualistica = get_model_class("AtividadeRitualistica")
        
        atividade = get_object_or_404(AtividadeRitualistica, id=id)
        
        if request.method == "POST":
            atividade.delete()
            messages.success(
                request, 
                "Atividade ritualística excluída com sucesso!"
            )
            return redirect("atividades:listar_atividades_ritualisticas")
        
        return render(
            request, 
            "atividades/ritualisticas/excluir_atividade_ritualistica.html", 
            {"atividade": atividade}
        )
    except Exception as e:
        logger.error(
            f"Erro ao excluir atividade ritualística {id}: {str(e)}", 
            exc_info=True
        )
        messages.error(
            request, 
            f"Ocorreu um erro ao excluir a atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades_ritualisticas")

@login_required
def copiar_atividade_ritualistica(request, id):
    """Cria uma cópia de uma atividade ritualística existente."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    
    # Obter atividade original
    atividade_original = get_object_or_404(AtividadeRitualistica, id=id)
    
    if request.method == "POST":
        # Criar formulário com dados do POST
        form = AtividadeRitualisticaForm(request.POST)
        
        if form.is_valid():
            # Salvar nova atividade sem os participantes
            nova_atividade = form.save(commit=False)
            nova_atividade.save()
            
            # Verificar se deve copiar participantes
            copiar_participantes = request.POST.get('copiar_participantes') == 'on'
            
            if copiar_participantes:
                # Copiar participantes da atividade original
                for participante in atividade_original.participantes.all():
                    nova_atividade.participantes.add(participante)
                
                messages.success(
                    request, 
                    f"Atividade copiada com sucesso! {atividade_original.participantes.count()} participantes foram copiados."
                )
            else:
                # Salvar apenas os participantes selecionados no formulário
                form.save_m2m()
                messages.success(request, "Atividade copiada com sucesso!")
            
            return redirect("atividades:detalhar_atividade_ritualistica", pk=nova_atividade.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        # Pré-preencher formulário com dados da atividade original
        initial_data = {
            'nome': f"Cópia de {atividade_original.nome}",
            'descricao': atividade_original.descricao,
            'data': atividade_original.data,
            'hora_inicio': atividade_original.hora_inicio,
            'hora_fim': atividade_original.hora_fim,
            'local': atividade_original.local,
            'turma': atividade_original.turma,
        }
        form = AtividadeRitualisticaForm(initial=initial_data)
    
    context = {
        "form": form,
        "atividade_original": atividade_original,
    }
    
    return render(request, "atividades/copiar_atividade_ritualistica.html", context)



### Arquivo: atividades\views\utils.py

python
import logging
from django.shortcuts import get_object_or_404
from importlib import import_module

# Set up logger
logger = logging.getLogger(__name__)


def get_return_url(request, default_url):
    """Obtém a URL de retorno do request ou usa o valor padrão."""
    return_url = request.GET.get("return_url", "")
    # Verificação básica de segurança
    if not return_url or not return_url.startswith("/"):
        return default_url
    return return_url


def get_form_class(form_name, app_name="atividades"):
    """Obtém uma classe de formulário dinamicamente."""
    try:
        forms_module = import_module(f"{app_name}.forms")
        return getattr(forms_module, form_name)
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter formulário %s: %s", form_name, str(e))
        raise


def get_model_class(model_name, app_name="atividades"):
    """Obtém uma classe de modelo dinamicamente."""
    try:
        models_module = import_module(f"{app_name}.models")
        return getattr(models_module, model_name)
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter modelo %s: %s", model_name, str(e))
        raise
def get_messages():
    """Importa o módulo messages do Django."""
    from django.contrib import messages
    return messages

def get_models():
    """Obtém os modelos necessários dinamicamente."""
    try:
        atividades_module = import_module("atividades.models")
        cursos_module = import_module("cursos.models")
        turmas_module = import_module("turmas.models")
        
        return {
            'AtividadeAcademica': getattr(atividades_module, "AtividadeAcademica"),
            'Curso': getattr(cursos_module, "Curso"),
            'Turma': getattr(turmas_module, "Turma"),
        }
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter modelos: %s", str(e), exc_info=True)
        raise

def get_forms():
    """Obtém os formulários AtividadeAcademicaForm e AtividadeRitualisticaForm."""
    atividades_forms = import_module("atividades.forms")
    AtividadeAcademicaForm = getattr(atividades_forms, "AtividadeAcademicaForm")
    AtividadeRitualisticaForm = getattr(atividades_forms, "AtividadeRitualisticaForm")
    return AtividadeAcademicaForm, AtividadeRitualisticaForm


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

from importlib import import_module

def get_cursos():
    Curso = import_module("cursos.models").Curso
    return Curso.objects.all()

def get_turmas(curso_id=None):
    Turma = import_module("turmas.models").Turma
    if curso_id:
        return Turma.objects.filter(curso_id=curso_id)
    return Turma.objects.all()

def get_atividades_academicas(curso_id=None, turma_id=None, query=None):
    from ..models import AtividadeAcademica
    atividades = AtividadeAcademica.objects.all()
    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    if query:
        from django.db.models import Q
        atividades = atividades.filter(
            Q(nome__icontains=query) | Q(descricao__icontains=query)
        )
    return atividades.select_related("curso").prefetch_related("turmas").distinct()


## Arquivos de Template:


### Arquivo: atividades\templates\atividades\academicas\confirmar_copia_academica.html

html
{% extends 'base.html' %}
{% load static %}
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



### Arquivo: atividades\templates\atividades\academicas\confirmar_exclusao_academica.html

html
{% extends 'base.html' %}
{% load static %}
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




### Arquivo: atividades\templates\atividades\academicas\copiar_atividade_academica.html

html
{% extends 'base.html' %}
{% load static %}
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


'''