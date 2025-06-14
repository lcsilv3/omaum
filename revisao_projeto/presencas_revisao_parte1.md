'''
# Revisão da Funcionalidade: presencas

## Arquivos forms.py:


### Arquivo: presencas\forms.py

python
from django import forms
from django.utils import timezone
from importlib import import_module

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_atividade_model():
    """Obtém o modelo Atividade."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "Atividade")

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

class PresencaForm(forms.ModelForm):
    """Formulário para registro e edição de presenças."""
    
    class Meta:
        model = get_model_dynamically("presencas", "Presenca")
        fields = ['aluno', 'atividade', 'data', 'presente', 'justificativa']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select select2'}),
            'atividade': forms.Select(attrs={'class': 'form-select select2'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalização adicional dos campos
        self.fields['justificativa'].required = False
        
        # Definir data padrão como hoje
        if not self.instance.pk:
            self.fields['data'].initial = timezone.now().date()
        
        # Adicionar classes CSS para validação
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'
    
    def clean(self):
        """Validação personalizada do formulário."""
        cleaned_data = super().clean()
        presente = cleaned_data.get('presente')
        justificativa = cleaned_data.get('justificativa')
        data = cleaned_data.get('data')
        
        # Verificar se a data não é futura
        if data and data > timezone.now().date():
            self.add_error('data', 'A data não pode ser futura.')
        
        # Verificar se há justificativa quando o aluno está ausente
        if presente is False and not justificativa:
            self.add_error('justificativa', 'É necessário fornecer uma justificativa para a ausência.')
        
        return cleaned_data

class PresencaMultiplaForm(forms.Form):
    """Formulário para registro de múltiplas presenças."""
    
    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date()
    )
    
    turmas = forms.ModelMultipleChoiceField(
        label='Turmas',
        queryset=get_turma_model().objects.filter(status='A'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'size': '5'}),
        help_text='Selecione uma ou mais turmas'
    )
    
    atividades = forms.ModelMultipleChoiceField(
        label='Atividades',
        queryset=get_atividade_model().objects.all().order_by('-data_inicio'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'size': '5'}),
        help_text='Selecione uma ou mais atividades'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        turmas = cleaned_data.get('turmas')
        atividades = cleaned_data.get('atividades')
        
        if not turmas:
            self.add_error('turmas', 'Selecione pelo menos uma turma.')
        
        if not atividades:
            self.add_error('atividades', 'Selecione pelo menos uma atividade.')
        
        return cleaned_data

class FiltroPresencaForm(forms.Form):
    """Formulário para filtrar presenças."""
    
    aluno = forms.ModelChoiceField(
        label='Aluno',
        queryset=get_aluno_model().objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    atividade = forms.ModelChoiceField(
        label='Atividade',
        queryset=get_atividade_model().objects.all().order_by('-data_inicio'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    
    data_inicio = forms.DateField(
        label='Data Inicial',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    data_fim = forms.DateField(
        label='Data Final',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    situacao = forms.ChoiceField(
        label='Situação',
        choices=[('', '-- Todas --')] + list(get_models().SITUACAO_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )



## Arquivos views.py:


### Arquivo: presencas\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module
from django.utils import timezone
from django.http import JsonResponse
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_model_academica():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "PresencaAcademica")

def get_model_ritualistica():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "PresencaRitualistica")

def get_model_observacao():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "ObservacaoPresenca")

def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_academica_model():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

def get_atividade_ritualistica_model():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeRitualistica")

@login_required
def listar_presencas_academicas(request):
    Presenca = get_model_academica()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    Atividade = get_atividade_academica_model()

    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    atividade_id = request.GET.get('atividade', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    presencas = Presenca.objects.all().select_related('aluno', 'turma', 'atividade')
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if atividade_id:
        presencas = presencas.filter(atividade__id=atividade_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()

    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'filtros': {
            'aluno': aluno_id,
            'turma': turma_id,
            'atividade': atividade_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        }
    }
    return render(request, 'presencas/listar_presencas_academicas.html', context)

@login_required
def listar_presencas_ritualisticas(request):
    Presenca = get_model_ritualistica()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    Atividade = get_atividade_ritualistica_model()

    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    atividade_id = request.GET.get('atividade', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    presencas = Presenca.objects.all().select_related('aluno', 'turma', 'atividade')
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if atividade_id:
        presencas = presencas.filter(atividade__id=atividade_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()

    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'filtros': {
            'aluno': aluno_id,
            'turma': turma_id,
            'atividade': atividade_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        }
    }
    return render(request, 'presencas/listar_presencas_ritualisticas.html', context)

@login_required
def registrar_presenca_academica(request):
    Presenca = get_model_academica()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    Atividade = get_atividade_academica_model()

    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        turma_id = request.POST.get('turma')
        atividade_id = request.POST.get('atividade')
        data = request.POST.get('data')
        presente = request.POST.get('presente') == 'on'
        observacao = request.POST.get('observacao', '')

        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
            turma = Turma.objects.get(id=turma_id)
            atividade = Atividade.objects.get(id=atividade_id)
            if Presenca.objects.filter(aluno=aluno, turma=turma, atividade=atividade, data=data).exists():
                messages.warning(request, f'Já existe um registro de presença para {aluno.nome} na turma {turma.nome} na data {data}.')
                return redirect('presencas:listar_presencas_academicas')
            presenca = Presenca(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                presente=presente,
                registrado_por=request.user.username,
                data_registro=timezone.now()
            )
            presenca.save()
            # Salvar observação, se houver
            if observacao:
                ObservacaoPresenca = get_model_observacao()
                ObservacaoPresenca.objects.create(
                    aluno=aluno,
                    turma=turma,
                    data=data,
                    atividade_academica=atividade,
                    texto=observacao,
                    registrado_por=request.user.username,
                    data_registro=timezone.now()
                )
            messages.success(request, f'Presença registrada com sucesso para {aluno.nome}.')
            return redirect('presencas:listar_presencas_academicas')
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')

    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    return render(request, 'presencas/registrar_presenca_academica.html', context)

@login_required
def registrar_presenca_ritualistica(request):
    Presenca = get_model_ritualistica()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    Atividade = get_atividade_ritualistica_model()

    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        turma_id = request.POST.get('turma')
        atividade_id = request.POST.get('atividade')
        data = request.POST.get('data')
        presente = request.POST.get('presente') == 'on'
        observacao = request.POST.get('observacao', '')

        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
            turma = Turma.objects.get(id=turma_id)
            atividade = Atividade.objects.get(id=atividade_id)
            if Presenca.objects.filter(aluno=aluno, turma=turma, atividade=atividade, data=data).exists():
                messages.warning(request, f'Já existe um registro de presença para {aluno.nome} na turma {turma.nome} na data {data}.')
                return redirect('presencas:listar_presencas_ritualisticas')
            presenca = Presenca(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                presente=presente,
                registrado_por=request.user.username,
                data_registro=timezone.now()
            )
            presenca.save()
            # Salvar observação, se houver
            if observacao:
                ObservacaoPresenca = get_model_observacao()
                ObservacaoPresenca.objects.create(
                    aluno=aluno,
                    turma=turma,
                    data=data,
                    atividade_ritualistica=atividade,
                    texto=observacao,
                    registrado_por=request.user.username,
                    data_registro=timezone.now()
                )
            messages.success(request, f'Presença registrada com sucesso para {aluno.nome}.')
            return redirect('presencas:listar_presencas_ritualisticas')
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')

    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    return render(request, 'presencas/registrar_presenca_ritualistica.html', context)

# As demais views (editar, excluir, detalhar, relatorio, etc.) devem ser duplicadas/adaptadas para cada tipo de presença,
# seguindo o mesmo padrão acima, usando o modelo correto e os templates correspondentes.

# Exemplo para ObservacaoPresenca:
@login_required
def listar_observacoes_presenca(request):
    ObservacaoPresenca = get_model_observacao()
    observacoes = ObservacaoPresenca.objects.select_related('aluno', 'turma', 'atividade_academica', 'atividade_ritualistica')
    return render(request, 'presencas/listar_observacoes_presenca.html', {'observacoes': observacoes})


## Arquivos urls.py:


### Arquivo: presencas\urls.py

python
from django.urls import path
from . import views

app_name = "presencas"

urlpatterns = [
    # Presenças acadêmicas
    path("academicas/", views.listar_presencas_academicas, name="listar_presencas_academicas"),
    path("academicas/registrar/", views.registrar_presenca_academica, name="registrar_presenca_academica"),
    path("academicas/editar/<int:pk>/", views.editar_presenca_academica, name="editar_presenca_academica"),
    path("academicas/excluir/<int:pk>/", views.excluir_presenca_academica, name="excluir_presenca_academica"),
    path("academicas/detalhar/<int:pk>/", views.detalhar_presenca_academica, name="detalhar_presenca_academica"),

    # Presenças ritualísticas
    path("ritualisticas/", views.listar_presencas_ritualisticas, name="listar_presencas_ritualisticas"),
    path("ritualisticas/registrar/", views.registrar_presenca_ritualistica, name="registrar_presenca_ritualistica"),
    path("ritualisticas/editar/<int:pk>/", views.editar_presenca_ritualistica, name="editar_presenca_ritualistica"),
    path("ritualisticas/excluir/<int:pk>/", views.excluir_presenca_ritualistica, name="excluir_presenca_ritualistica"),
    path("ritualisticas/detalhar/<int:pk>/", views.detalhar_presenca_ritualistica, name="detalhar_presenca_ritualistica"),

    # Observações de presença
    path("observacoes/", views.listar_observacoes_presenca, name="listar_observacoes_presenca"),
]



## Arquivos models.py:


### Arquivo: presencas\models.py

python
from django.db import models
from django.utils import timezone
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_model():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

class Presenca(models.Model):
    """
    Modelo para registro de presença de alunos em atividades.
    
    Este modelo armazena informações sobre a presença ou ausência de um aluno
    em uma determinada atividade, incluindo a data, status e justificativa
    em caso de ausência.
    
    Attributes:
        aluno (ForeignKey): Referência ao aluno cuja presença está sendo registrada.
        atividade (ForeignKey): Referência à atividade em que a presença está sendo registrada.
        data (DateField): Data do registro de presença.
        presente (BooleanField): Indica se o aluno estava presente (True) ou ausente (False).
        justificativa (TextField): Justificativa para a ausência, se aplicável.
        registrado_por (ForeignKey): Usuário que registrou a presença.
        data_registro (DateTimeField): Data e hora em que o registro foi criado.
    """
    
    aluno = models.ForeignKey(
        get_aluno_model(),
        on_delete=models.CASCADE,
        verbose_name="Aluno"
    )
    
    atividade = models.ForeignKey(
        get_atividade_model(),
        on_delete=models.CASCADE,
        verbose_name="Atividade",
        null=True,
        blank=True
    )
    
    turma = models.ForeignKey(
        get_turma_model(), 
        on_delete=models.CASCADE,
        verbose_name="Turma",
        null=True,
        blank=True
    )
    
    data = models.DateField(verbose_name="Data")
    
    presente = models.BooleanField(default=True, verbose_name="Presente")
    
    justificativa = models.TextField(blank=True, null=True, verbose_name="Justificativa")
    
    registrado_por = models.CharField(max_length=100, default="Sistema", verbose_name="Registrado por")
    
    data_registro = models.DateTimeField(default=timezone.now, verbose_name="Data de registro")
    
    class Meta:
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        ordering = ["-data", "aluno__nome"]
        unique_together = ["aluno", "turma", "data"]
    
    def __str__(self):
        """Retorna uma representação em string do objeto."""
        status = "Presente" if self.presente else "Ausente"
        return f"{self.aluno.nome} - {self.data} - {status}"
    
    def clean(self):
        """
        Valida os dados do modelo antes de salvar.
        
        Raises:
            ValidationError: Se a data for futura ou se a justificativa estiver
                            ausente quando o aluno estiver marcado como ausente.
        """
        super().clean()
        
        # Verificar se a data não é futura
        if self.data and self.data > timezone.now().date():
            raise ValidationError({"data": "A data não pode ser futura."})
        
        # Verificar se há justificativa quando o aluno está ausente
        if not self.presente and not self.justificativa:
            raise ValidationError(
                {"justificativa": "É necessário fornecer uma justificativa para a ausência."}
            )



## Arquivos de Views Modulares:


### Arquivo: presencas\views\__init__.py

python
# presencas/views/__init__.py

# Importar funções de listagem
from .listagem import (
    listar_presencas
)

# Importar funções de atividade
from .atividade import (
    registrar_presencas_atividade,
    editar_presenca
)

# Importar funções de múltiplas presenças
from .multiplas import (
    registrar_presencas_multiplas,
    formulario_presencas_multiplas
)

# Expor todas as funções para que possam ser importadas de presencas.views
__all__ = [
    'listar_presencas',
    'registrar_presencas_atividade',
    'editar_presenca',
    'registrar_presencas_multiplas',
    'formulario_presencas_multiplas'
]



### Arquivo: presencas\views\atividade.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

def get_form_dynamically(app_name, form_name):
    """Obtém um formulário dinamicamente."""
    module = import_module(f"{app_name}.forms")
    return getattr(module, form_name)

@login_required
def registrar_presencas_atividade(request):
    """Registra presenças para uma atividade específica."""
    AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
    Aluno = get_model_dynamically("alunos", "Aluno")
    Presenca = get_model_dynamically("presencas", "Presenca")
    
    if request.method == 'POST':
        atividade_id = request.POST.get('atividade')
        data = request.POST.get('data')
        
        if not atividade_id or not data:
            messages.error(request, "Atividade e data são obrigatórios.")
            return redirect('presencas:registrar_presencas_atividade')
        
        atividade = get_object_or_404(AtividadeAcademica, id=atividade_id)
        
        # Processar presenças
        presentes = request.POST.getlist('presentes', [])
        
        # Obter alunos da atividade
        alunos = []
        for turma in atividade.turmas.all():
            # Obter alunos matriculados na turma
            Matricula = get_model_dynamically("matriculas", "Matricula")
            matriculas = Matricula.objects.filter(turma=turma, status='A')
            alunos.extend([m.aluno for m in matriculas])
        
        # Remover duplicatas
        alunos = list(set(alunos))
        
        # Registrar presenças
        for aluno in alunos:
            presente = aluno.cpf in presentes
            justificativa = request.POST.get(f'justificativa_{aluno.cpf}', '') if not presente else ''
            
            # Verificar se já existe registro
            presenca, created = Presenca.objects.update_or_create(
                aluno=aluno,
                atividade=atividade,
                data=data,
                defaults={
                    'presente': presente,
                    'justificativa': justificativa,
                    'registrado_por': request.user
                }
            )
        
        messages.success(request, "Presenças registradas com sucesso!")
        return redirect('presencas:listar_presencas')
    else:
        # Obter atividades para o formulário
        atividades = AtividadeAcademica.objects.all().order_by('-data_inicio')
        
        context = {
            'atividades': atividades,
            'data_hoje': timezone.now().date().strftime('%Y-%m-%d')
        }
        
        return render(request, 'presencas/registrar_presencas_atividade.html', context)

@login_required
def editar_presenca(request, presenca_id):
    """Edita um registro de presença existente."""
    Presenca = get_model_dynamically("presencas", "Presenca")
    PresencaForm = get_form_dynamically("presencas", "PresencaForm")
    
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    if request.method == 'POST':
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, "Presença atualizada com sucesso!")
            return redirect('presencas:listar_presencas')
    else:
        form = PresencaForm(instance=presenca)
    
    context = {
        'form': form,
        'presenca': presenca
    }
    
    return render(request, 'presencas/editar_presenca.html', context)



### Arquivo: presencas\views\listagem.py

python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from importlib import import_module

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def listar_presencas(request):
    """Lista todas as presenças registradas."""
    Presenca = get_model_dynamically("presencas", "Presenca")
    
    # Aplicar filtros
    query = request.GET.get('q', '')
    aluno_id = request.GET.get('aluno', '')
    atividade_id = request.GET.get('atividade', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    presente = request.GET.get('presente', '')
    
    presencas = Presenca.objects.all().select_related('aluno', 'atividade')
    
    if query:
        presencas = presencas.filter(
            Q(aluno__nome__icontains=query) |
            Q(atividade__nome__icontains=query)
        )
    
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    
    if atividade_id:
        presencas = presencas.filter(atividade__id=atividade_id)
    
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    if presente:
        presencas = presencas.filter(presente=(presente == 'true'))
    
    # Ordenação
    presencas = presencas.order_by('-data', 'aluno__nome')
    
    # Paginação
    paginator = Paginator(presencas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obter modelos para filtros
    Aluno = get_model_dynamically("alunos", "Aluno")
    AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
    
    alunos = Aluno.objects.all()
    atividades = AtividadeAcademica.objects.all()
    
    context = {
        'presencas': page_obj,
        'page_obj': page_obj,
        'query': query,
        'alunos': alunos,
        'atividades': atividades,
        'filtros': {
            'aluno': aluno_id,
            'atividade': atividade_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'presente': presente
        }
    }
    
    return render(request, 'presencas/listar_presencas.html', context)



### Arquivo: presencas\views\multiplas.py

python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from importlib import import_module
import json

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def registrar_presencas_multiplas(request):
    """Registra presenças para múltiplos alunos em múltiplas atividades."""
    if request.method == 'POST':
        # Processar o formulário
        data = request.POST.get('data')
        turma_ids = request.POST.getlist('turmas')
        atividade_ids = request.POST.getlist('atividades')
        
        if not data or not turma_ids or not atividade_ids:
            messages.error(request, "Data, turmas e atividades são obrigatórios.")
            return redirect('presencas:registrar_presencas_multiplas')
        
        # Redirecionar para a página de registro com os parâmetros
        return redirect('presencas:formulario_presencas_multiplas', 
                       data=data, 
                       turmas=','.join(turma_ids), 
                       atividades=','.join(atividade_ids))
    else:
        # Exibir o formulário inicial
        Turma = get_model_dynamically("turmas", "Turma")
        AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
        
        turmas = Turma.objects.filter(status='A')
        atividades = AtividadeAcademica.objects.all().order_by('-data_inicio')
        
        context = {
            'turmas': turmas,
            'atividades': atividades,
            'data_hoje': timezone.now().date().strftime('%Y-%m-%d')
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas_passo1.html', context)

@login_required
def formulario_presencas_multiplas(request, data, turmas, atividades):
    """Exibe o formulário para registro de presenças múltiplas."""
    # Converter parâmetros
    turma_ids = turmas.split(',')
    atividade_ids = atividades.split(',')
    
    Turma = get_model_dynamically("turmas", "Turma")
    AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
    Aluno = get_model_dynamically("alunos", "Aluno")
    
    # Obter objetos
    turmas_obj = Turma.objects.filter(id__in=turma_ids)
    atividades_obj = AtividadeAcademica.objects.filter(id__in=atividade_ids)
    
    # Obter alunos das turmas
    alunos = []
    for turma in turmas_obj:
        # Obter alunos matriculados na turma
        Matricula = get_model_dynamically("matriculas", "Matricula")
        matriculas = Matricula.objects.filter(turma=turma, status='A')
        alunos.extend([m.aluno for m in matriculas])
    
    # Remover duplicatas
    alunos = list(set(alunos))
    
    if request.method == 'POST':
        # Processar o formulário
        Presenca = get_model_dynamically("presencas", "Presenca")
        presencas_data = json.loads(request.POST.get('presencas_data', '[]'))
        
        for presenca_info in presencas_data:
            aluno_id = presenca_info.get('aluno_id')
            atividade_id = presenca_info.get('atividade_id')
            presente = presenca_info.get('presente', True)
            justificativa = presenca_info.get('justificativa', '')
            
            aluno = get_object_or_404(Aluno, cpf=aluno_id)
            atividade = get_object_or_404(AtividadeAcademica, id=atividade_id)
            
            # Verificar se já existe registro
            presenca, created = Presenca.objects.update_or_create(
                aluno=aluno,
                atividade=atividade,
                data=data,
                defaults={
                    'presente': presente,
                    'justificativa': justificativa,
                    'registrado_por': request.user
                }
            )
        
        messages.success(request, "Presenças registradas com sucesso!")
        return redirect('presencas:listar_presencas')
    else:
        context = {
            'data': data,
            'turmas': turmas_obj,
            'atividades': atividades_obj,
            'alunos': alunos
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas.html', context)


## Arquivos de Template:


### Arquivo: presencas\templates\presencas\academicas\detalhar_presenca_academica.html

html
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
        <div class="card-footer">
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                <i class="fas fa-list"></i> Voltar para a lista
            </a>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\academicas\editar_presenca_academica.html

html
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




### Arquivo: presencas\templates\presencas\academicas\excluir_presenca_academica.html

html
{% extends 'base.html' %}

{% block title %}Excluir Presença{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">
                    <h4 class="mb-0">Confirmar Exclusão</h4>
                </div>
                <div class="card-body">
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Você está prestes a excluir o seguinte registro de presença:
                    </div>
                    
                    <div class="card mb-3">
                        <div class="card-body">
                            <p><strong>Aluno:</strong> {{ presenca.aluno.nome }}</p>
                            <p><strong>Atividade:</strong> {{ presenca.atividade.titulo }}</p>
                            <p><strong>Data:</strong> {{ presenca.data|date:"d/m/Y" }}</p>
                            <p><strong>Situação:</strong> 
                                {% if presenca.situacao == 'PRESENTE' %}
                                <span class="badge bg-success">Presente</span>
                                {% elif presenca.situacao == 'AUSENTE' %}
                                <span class="badge bg-danger">Ausente</span>
                                {% elif presenca.situacao == 'JUSTIFICADO' %}
                                <span class="badge bg-warning">Justificado</span>
                                {% endif %}
                            </p>
                            {% if presenca.justificativa %}
                            <p><strong>Justificativa:</strong> {{ presenca.justificativa }}</p>
                            {% endif %}
                        </div>
                    </div>
                    
                    <p class="text-danger">Esta ação não pode ser desfeita. Deseja continuar?</p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
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
    </div>
</div>
{% endblock %}




### Arquivo: presencas\templates\presencas\academicas\filtro_presencas_academica.html

html
{% extends 'base.html' %}

{% block title %}Filtrar Presenças{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Filtrar Presenças</h1>
        <div>
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Voltar para Lista
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
            <h5 class="mb-0">Filtros de Pesquisa</h5>
        </div>
        <div class="card-body">
            <form method="get" action="{% url 'presencas:listar_presencas' %}">
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="aluno" class="form-label">Aluno</label>
                        <select class="form-select" id="aluno" name="aluno">
                            <option value="">Todos os alunos</option>
                            {% for aluno in alunos %}
                            <option value="{{ aluno.cpf }}">{{ aluno.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-6">
                        <label for="turma" class="form-label">Turma</label>
                        <select class="form-select" id="turma" name="turma">
                            <option value="">Todas as turmas</option>
                            {% for turma in turmas %}
                            <option value="{{ turma.id }}">{{ turma.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="atividade" class="form-label">Atividade</label>
                        <select class="form-select" id="atividade" name="atividade">
                            <option value="">Todas as atividades</option>
                            {% for atividade in atividades %}
                            <option value="{{ atividade.id }}">{{ atividade.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-3">
                        <label for="data_inicio" class="form-label">Data Início</label>
                        <input type="date" class="form-control" id="data_inicio" name="data_inicio">
                    </div>
                    
                    <div class="col-md-3">
                        <label for="data_fim" class="form-label">Data Fim</label>
                        <input type="date" class="form-control" id="data_fim" name="data_fim">
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="status" class="form-label">Status</label>
                        <select class="form-select" id="status" name="status">
                            <option value="">Todos</option>
                            <option value="presente">Presente</option>
                            <option value="ausente">Ausente</option>
                        </select>
                    </div>
                    
                    <div class="col-md-6">
                        <label for="ordenar" class="form-label">Ordenar por</label>
                        <select class="form-select" id="ordenar" name="ordenar">
                            <option value="data">Data (mais recente primeiro)</option>
                            <option value="data_asc">Data (mais antiga primeiro)</option>
                            <option value="aluno">Nome do Aluno</option>
                            <option value="atividade">Nome da Atividade</option>
                        </select>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <button type="reset" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-search"></i> Pesquisar
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        if (typeof $.fn.select2 === 'function') {
            $('#aluno').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione um aluno',
                allowClear: true
            });
            
            $('#turma').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione uma turma',
                allowClear: true
            });
            
            $('#atividade').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione uma atividade',
                allowClear: true
            });
        }
        
        // Filtrar atividades por turma
        const turmaSelect = document.getElementById('turma');
        const atividadeSelect = document.getElementById('atividade');
        
        if (turmaSelect && atividadeSelect) {
            turmaSelect.addEventListener('change', function() {
                const turmaId = this.value;
                
                if (turmaId) {
                    // Fazer requisição AJAX para buscar atividades da turma
                    fetch(`/presencas/api/atividades-por-turma/${turmaId}/`)
                        .then(response => response.json())
                        .then(data => {
                            // Limpar select de atividades
                            atividadeSelect.innerHTML = '<option value="">Todas as atividades</option>';
                            
                            // Adicionar novas opções
                            if (data.success && data.atividades && data.atividades.length > 0) {
                                data.atividades.forEach(atividade => {
                                    const option = document.createElement('option');
                                    option.value = atividade.id;
                                    option.textContent = `${atividade.nome} (${atividade.data})`;
                                    atividadeSelect.appendChild(option);
                                });
                            }
                            
                            // Atualizar Select2 se estiver sendo usado
                            if (typeof $.fn.select2 === 'function') {
                                $(atividadeSelect).trigger('change');
                            }
                        })
                        .catch(error => console.error('Erro ao buscar atividades:', error));
                }
            });
        }
    });
</script>
{% endblock %}
{% endblock %}



### Arquivo: presencas\templates\presencas\academicas\formulario_presenca_academica.html

html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">{{ titulo }}</h4>
                </div>
                <div class="card-body">
                    <form method="post" novalidate>
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                        <div class="alert alert-danger">
                            {% for error in form.non_field_errors %}
                            <p>{{ error }}</p>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="{{ form.aluno.id_for_label }}" class="form-label">{{ form.aluno.label }}</label>
                            {{ form.aluno }}
                            {% if form.aluno.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.aluno.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.aluno.help_text %}
                            <div class="form-text">{{ form.aluno.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.atividade.id_for_label }}" class="form-label">{{ form.atividade.label }}</label>
                            {{ form.atividade }}
                            {% if form.atividade.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.atividade.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.atividade.help_text %}
                            <div class="form-text">{{ form.atividade.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.data.id_for_label }}" class="form-label">{{ form.data.label }}</label>
                            {{ form.data }}
                            {% if form.data.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.data.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.data.help_text %}
                            <div class="form-text">{{ form.data.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.situacao.id_for_label }}" class="form-label">{{ form.situacao.label }}</label>
                            {{ form.situacao }}
                            {% if form.situacao.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.situacao.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.situacao.help_text %}
                            <div class="form-text">{{ form.situacao.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3" id="justificativa-container">
                            <label for="{{ form.justificativa.id_for_label }}" class="form-label">{{ form.justificativa.label }}</label>
                            {{ form.justificativa }}
                            {% if form.justificativa.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.justificativa.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.justificativa.help_text %}
                            <div class="form-text">{{ form.justificativa.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Voltar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Salvar
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
        
        // Mostrar/ocultar campo de justificativa com base na situação
        const situacaoSelect = document.getElementById('id_situacao');
        const justificativaContainer = document.getElementById('justificativa-container');
        
        function toggleJustificativa() {
            if (situacaoSelect.value === 'JUSTIFICADO') {
                justificativaContainer.style.display = 'block';
                document.getElementById('id_justificativa').setAttribute('required', 'required');
            } else {
                justificativaContainer.style.display = 'none';
                document.getElementById('id_justificativa').removeAttribute('required');
            }
        }
        
        // Executar na inicialização
        toggleJustificativa();
        
        // Adicionar evento de mudança
        situacaoSelect.addEventListener('change', toggleJustificativa);
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\academicas\formulario_presencas_multiplas_academica.html

html
{% extends 'base.html' %}

{% block title %}Registro de Presenças{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registro de Presenças</h1>
        <div>
            <a href="{% url 'presencas:registrar_presencas_multiplas' %}" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-outline-secondary">
                <i class="fas fa-list"></i> Lista de Presenças
            </a>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Registro</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <p><strong>Data:</strong> {{ data|date:"d/m/Y" }}</p>
                </div>
                <div class="col-md-8">
                    <p><strong>Turmas:</strong> 
                        {% for turma in turmas %}
                            <span class="badge bg-info">{{ turma.nome }}</span>
                        {% endfor %}
                    </p>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <p><strong>Atividades:</strong> 
                        {% for atividade in atividades %}
                            <span class="badge bg-success">{{ atividade.titulo }}</span>
                        {% endfor %}
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Lista de Alunos</h5>
                <div>
                    <button type="button" class="btn btn-success btn-sm me-2" id="btn-marcar-todos-presentes">
                        <i class="fas fa-check"></i> Marcar Todos Presentes
                    </button>
                    <button type="button" class="btn btn-danger btn-sm" id="btn-marcar-todos-ausentes">
                        <i class="fas fa-times"></i> Marcar Todos Ausentes
                    </button>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover" id="tabela-alunos">
                    <thead class="table-light">
                        <tr>
                            <th style="width: 40%">Aluno</th>
                            <th style="width: 20%">Atividade</th>
                            <th style="width: 20%">Situação</th>
                            <th style="width: 20%">Justificativa</th>
                        </tr>
                    </thead>
                    <tbody id="tbody-alunos">
                        <tr>
                            <td colspan="4" class="text-center py-4">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Carregando...</span>
                                </div>
                                <p class="mt-2">Carregando alunos...</p>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <div class="d-flex justify-content-between">
                <a href="{% url 'presencas:registrar_presencas_multiplas' %}" class="btn btn-secondary">Cancelar</a>
                <button type="button" class="btn btn-primary" id="btn-salvar-presencas">
                    <i class="fas fa-save"></i> Salvar Presenças
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Template para linha de aluno -->
<template id="template-linha-aluno">
    <tr data-aluno-id="">
        <td>
            <div class="d-flex align-items-center">
                <div class="avatar-placeholder rounded-circle me-2 d-flex align-items-center justify-content-center" 
                     style="width: 40px; height: 40px; background-color: #6c757d; color: white;">
                </div>
                <div>
                    <div class="aluno-nome fw-bold"></div>
                    <small class="text-muted aluno-cpf"></small>
                </div>
            </div>
        </td>
        <td class="atividade-titulo"></td>
        <td>
            <select class="form-select form-select-sm situacao-select">
                <option value="PRESENTE">Presente</option>
                <option value="AUSENTE">Ausente</option>
                <option value="JUSTIFICADO">Justificado</option>
            </select>
        </td>
        <td>
            <input type="text" class="form-control form-control-sm justificativa-input" placeholder="Opcional" disabled>
        </td>
    </tr>
</template>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const data = '{{ data|date:"Y-m-d" }}';
        const turmasIds = [{% for turma in turmas %}'{{ turma.id }}'{% if not forloop.last %},{% endif %}{% endfor %}];
        const atividadesIds = [{% for atividade in atividades %}'{{ atividade.id }}'{% if not forloop.last %},{% endif %}{% endfor %}];
        
        const tbodyAlunos = document.getElementById('tbody-alunos');
        const templateLinhaAluno = document.getElementById('template-linha-aluno');
        const btnMarcarTodosPresentes = document.getElementById('btn-marcar-todos-presentes');
        const btnMarcarTodosAusentes = document.getElementById('btn-marcar-todos-ausentes');
        const btnSalvarPresencas = document.getElementById('btn-salvar-presencas');
        
        // Carregar alunos
        carregarAlunos();
        
        // Configurar eventos
        btnMarcarTodosPresentes.addEventListener('click', marcarTodosPresentes);
        btnMarcarTodosAusentes.addEventListener('click', marcarTodosAusentes);
        btnSalvarPresencas.addEventListener('click', salvarPresencas);
        
        // Função para carregar alunos
        function carregarAlunos() {
            fetch('{% url "presencas:api_obter_alunos_por_turmas" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    turmas_ids: turmasIds
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    mostrarErro(data.error);
                    return;
                }
                
                // Limpar tabela
                tbodyAlunos.innerHTML = '';
                
                // Verificar se há alunos
                if (data.alunos.length === 0) {
                    tbodyAlunos.innerHTML = `
                        <tr>
                            <td colspan="4" class="text-center py-4">
                                <p class="text-muted mb-0">Nenhum aluno encontrado nas turmas selecionadas.</p>
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                // Adicionar alunos à tabela
                data.alunos.forEach(aluno => {
                    atividadesIds.forEach(atividadeId => {
                        const atividade = data.atividades.find(a => a.id == atividadeId);
                        if (!atividade) return;
                        
                        adicionarLinhaAluno(aluno, atividade);
                    });
                });
                
                // Configurar eventos para os selects de situação
                document.querySelectorAll('.situacao-select').forEach(select => {
                    select.addEventListener('change', function() {
                        const justificativaInput = this.closest('tr').querySelector('.justificativa-input');
                        justificativaInput.disabled = this.value !== 'JUSTIFICADO';
                        
                        if (this.value !== 'JUSTIFICADO') {
                            justificativaInput.value = '';
                        }
                    });
                });
            })
            .catch(error => {
                console.error('Erro ao carregar alunos:', error);
                mostrarErro('Erro ao carregar alunos. Por favor, tente novamente.');
            });
        }
        
        // Função para adicionar linha de aluno
        function adicionarLinhaAluno(aluno, atividade) {
            const clone = document.importNode(templateLinhaAluno.content, true);
            const tr = clone.querySelector('tr');
            
            tr.dataset.alunoId = aluno.cpf;
            tr.dataset.atividadeId = atividade.id;
            
            // Configurar avatar
            const avatarPlaceholder = tr.querySelector('.avatar-placeholder');
            if (aluno.foto) {
                avatarPlaceholder.innerHTML = `<img src="${aluno.foto}" alt="Foto de ${aluno.nome}" class="rounded-circle" width="40" height="40" style="object-fit: cover;">`;
                avatarPlaceholder.className = 'me-2';
            } else {
                avatarPlaceholder.textContent = aluno.nome.charAt(0).toUpperCase();
            }
            
            // Configurar dados do aluno
            tr.querySelector('.aluno-nome').textContent = aluno.nome;
            tr.querySelector('.aluno-cpf').textContent = aluno.cpf;
            tr.querySelector('.atividade-titulo').textContent = atividade.titulo;
            
            tbodyAlunos.appendChild(tr);
        }
        
        // Função para marcar todos como presentes
        function marcarTodosPresentes() {
            document.querySelectorAll('.situacao-select').forEach(select => {
                select.value = 'PRESENTE';
                
                // Desabilitar campo de justificativa
                const justificativaInput = select.closest('tr').querySelector('.justificativa-input');
                justificativaInput.disabled = true;
                justificativaInput.value = '';
            });
        }
        
        // Função para marcar todos como ausentes
        function marcarTodosAusentes() {
            document.querySelectorAll('.situacao-select').forEach(select => {
                select.value = 'AUSENTE';
                
                // Desabilitar campo de justificativa
                const justificativaInput = select.closest('tr').querySelector('.justificativa-input');
                justificativaInput.disabled = true;
                justificativaInput.value = '';
            });
        }
        
        // Função para salvar presenças
        function salvarPresencas() {
            // Desabilitar botão para evitar múltiplos envios
            btnSalvarPresencas.disabled = true;
            btnSalvarPresencas.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Salvando...';
            
            // Coletar dados
            const presencas = [];
            
            document.querySelectorAll('#tbody-alunos tr[data-aluno-id]').forEach(tr => {
                const alunoId = tr.dataset.alunoId;
                const atividadeId = tr.dataset.atividadeId;
                const situacao = tr.querySelector('.situacao-select').value;
                const justificativa = tr.querySelector('.justificativa-input').value;
                
                presencas.push({
                    aluno_id: alunoId,
                    atividade_id: atividadeId,
                    data: data,
                    situacao: situacao,
                    justificativa: justificativa
                });
            });
            
            // Enviar dados
            fetch('{% url "presencas:api_salvar_presencas_multiplas" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    presencas: presencas
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    mostrarErro(data.error);
                    return;
                }
                
                // Redirecionar para a lista de presenças
                window.location.href = '{% url "presencas:listar_presencas" %}';
            })
            .catch(error => {
                console.error('Erro ao salvar presenças:', error);
                mostrarErro('Erro ao salvar presenças. Por favor, tente novamente.');
            })
            .finally(() => {
                // Reabilitar botão
                btnSalvarPresencas.disabled = false;
                btnSalvarPresencas.innerHTML = '<i class="fas fa-save"></i> Salvar Presenças';
            });
        }
        
        // Função para mostrar erro
        function mostrarErro(mensagem) {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger alert-dismissible fade show';
            alertDiv.innerHTML = `
                ${mensagem}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
            `;
            
            document.querySelector('.container-fluid').insertBefore(alertDiv, document.querySelector('.card'));
        }
        
        // Função para obter token CSRF
        function getCsrfToken() {
            return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || '';
        }
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\academicas\formulario_presencas_multiplas_academica_passo1.html

html
{% extends 'base.html' %}

{% block title %}Registro de Presenças Múltiplas{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-success text-white">
                    <h4 class="mb-0">Registro de Presenças Múltiplas - Passo 1</h4>
                </div>
                <div class="card-body">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        Selecione a data, as turmas e as atividades para registrar presenças em massa.
                    </div>
                    
                    <form method="post" id="form-passo1" novalidate>
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                        <div class="alert alert-danger">
                            {% for error in form.non_field_errors %}
                            <p>{{ error }}</p>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="{{ form.data.id_for_label }}" class="form-label">{{ form.data.label }}</label>
                            {{ form.data }}
                            {% if form.data.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.data.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.data.help_text %}
                            <div class="form-text">{{ form.data.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.turmas.id_for_label }}" class="form-label">{{ form.turmas.label }}</label>
                            {{ form.turmas }}
                            {% if form.turmas.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.turmas.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.turmas.help_text %}
                            <div class="form-text">{{ form.turmas.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.atividades.id_for_label }}" class="form-label">{{ form.atividades.label }}</label>
                            {{ form.atividades }}
                            {% if form.atividades.errors %}
                            <div class="invalid-feedback d-block">
                                {% for error in form.atividades.errors %}
                                {{ error }}
                                {% endfor %}
                            </div>
                            {% endif %}
                            {% if form.atividades.help_text %}
                            <div class="form-text">{{ form.atividades.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between mt-4">
                            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Voltar
                            </a>
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-arrow-right"></i> Próximo Passo
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        $('.select2').select2({
            theme: 'bootstrap-5',
            width: '100%'
        });
        
        // Atualizar atividades quando a data mudar
        const dataInput = document.getElementById('id_data');
        const atividadesSelect = document.getElementById('id_atividades');
        
        dataInput.addEventListener('change', function() {
            const data = this.value;
            
            if (!data) return;
            
            // Fazer requisição AJAX para obter atividades da data
            fetch(`/presencas/api/obter-atividades-por-data/?data=${data}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        return;
                    }
                    
                    // Limpar opções atuais
                    atividadesSelect.innerHTML = '';
                    
                    // Adicionar novas opções
                    data.atividades.forEach(atividade => {
                        const option = document.createElement('option');
                        option.value = atividade.id;
                        option.textContent = atividade.titulo;
                        atividadesSelect.appendChild(option);
                    });
                    
                    // Atualizar Select2
                    $(atividadesSelect).trigger('change');
                })
                .catch(error => {
                    console.error('Erro ao carregar atividades:', error);
                });
        });
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\academicas\formulario_presencas_multiplas_academica_passo2.html

html
{% extends 'base.html' %}

{% block title %}Registro de Presenças Múltiplas - Passo 2{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="card">
        <div class="card-header bg-success text-white">
            <div class="d-flex justify-content-between align-items-center">
                <h4 class="mb-0">Registro de Presenças Múltiplas - Passo 2</h4>
                <div>
                    <span class="badge bg-light text-dark">Data: {{ data_formatada }}</span>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                Marque a situação de presença para cada aluno nas atividades selecionadas.
            </div>
            
            <div class="mb-3">
                <h5>Turmas selecionadas:</h5>
                <div class="d-flex flex-wrap gap-2">
                    {% for turma in turmas %}
                    <span class="badge bg-primary">{{ turma.nome }}</span>
                    {% endfor %}
                </div>
            </div>
            
            <div class="mb-3">
                <h5>Atividades selecionadas:</h5>
                <div class="d-flex flex-wrap gap-2">
                    {% for atividade in atividades %}
                    <span class="badge bg-info">{{ atividade.titulo }}</span>
                    {% endfor %}
                </div>
            </div>
            
            <form id="form-presencas-multiplas">
                {% csrf_token %}
                <input type="hidden" name="data" value="{{ data }}">
                
                <div class="table-responsive">
                    <table class="table table-striped table-bordered">
                        <thead class="table-dark">
                            <tr>
                                <th style="width: 30%">Aluno</th>
                                {% for atividade in atividades %}
                                <th>{{ atividade.titulo }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for aluno in alunos %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        {% if aluno.foto %}
                                        <img src="{{ aluno.foto.url }}" alt="{{ aluno.nome }}" 
                                             class="rounded-circle me-2" width="40" height="40">
                                        {% else %}
                                        <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                             style="width: 40px; height: 40px; color: white;">
                                            {{ aluno.nome|first|upper }}
                                        </div>
                                        {% endif %}
                                        <div>
                                            <div>{{ aluno.nome }}</div>
                                            <small class="text-muted">{{ aluno.cpf }}</small>
                                        </div>
                                    </div>
                                </td>
                                
                                {% for atividade in atividades %}
                                <td>
                                    {% with key=aluno.cpf|add:'_'|add:atividade.id|stringformat:'s' %}
                                    {% with presenca=presencas_dict|get_item:key %}
                                    <div class="btn-group" role="group">
                                        <input type="radio" class="btn-check" name="presenca_{{ aluno.cpf }}_{{ atividade.id }}" 
                                               id="presente_{{ aluno.cpf }}_{{ atividade.id }}" value="PRESENTE"
                                               {% if presenca and presenca.situacao == 'PRESENTE' %}checked{% elif not presenca %}checked{% endif %}>
                                        <label class="btn btn-outline-success



### Arquivo: presencas\templates\presencas\academicas\historico_presencas_academica.html

html
{% extends 'base.html' %}

{% block title %}Histórico de Presenças - {{ aluno.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Histórico de Presenças</h1>
        <div>
            <a href="{% url 'alunos:detalhar_aluno' aluno.cpf %}" class="btn btn-secondary me-2">
                <i class="fas fa-user"></i> Perfil do Aluno
            </a>
            <a href="{% url 'presencas:exportar_historico' aluno.cpf %}" class="btn btn-success">
                <i class="fas fa-file-csv"></i> Exportar CSV
            </a>
        </div>
    </div>
    
    <!-- Informações do aluno -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="d-flex align-items-center">
                {% if aluno.foto %}
                <img src="{{ aluno.foto.url }}" alt="{{ aluno.nome }}" 
                     class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                {% else %}
                <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                     style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                    {{ aluno.nome|first|upper }}
                </div>
                {% endif %}
                <div>
                    <h5 class="mb-1">{{ aluno.nome }}</h5>
                    <p class="mb-0">{{ aluno.email }}</p>
                    <p class="mb-0">CPF: {{ aluno.cpf }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="atividade" class="form-label">Atividade</label>
                    <select class="form-select" id="atividade" name="atividade">
                        <option value="">Todas as atividades</option>
                        {% for atividade in atividades %}
                        <option value="{{ atividade.id }}" {% if filtros.atividade == atividade.id|stringformat:"s" %}selected{% endif %}>
                            {{ atividade.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-4">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ filtros.data_inicio }}">
                </div>
                
                <div class="col-md-4">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ filtros.data_fim }}">
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'presencas:historico_presencas' aluno.cpf %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Estatísticas -->
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Estatísticas</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Presenças</h5>
                            <p class="card-text display-4">{{ total_presencas }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Total de Faltas</h5>
                            <p class="card-text display-4">{{ total_faltas }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Percentual de Presença</h5>
                            <p class="card-text display-4">{{ percentual_presenca|floatformat:1 }}%</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Lista de presenças -->
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Registros de Presença</h5>
        </div>
        <div class="card-body">
            {% if presencas %}
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Data</th>
                            <th>Atividade</th>
                            <th>Turma</th>
                            <th>Status</th>
                            <th>Justificativa</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for presenca in presencas %}
                        <tr>
                            <td>{{ presenca.data|date:"d/m/Y" }}</td>
                            <td>{{ presenca.atividade.nome }}</td>
                            <td>{{ presenca.atividade.turma.nome }}</td>
                            <td>
                                {% if presenca.presente %}
                                <span class="badge bg-success">Presente</span>
                                {% else %}
                                <span class="badge bg-danger">Ausente</span>
                                {% endif %}
                            </td>
                            <td>{{ presenca.justificativa|default:"-"|truncatechars:50 }}</td>
                            <td>
                                <div class="table-actions">
                                    <a href="{% url 'presencas:detalhar_presenca' presenca.id %}" class="btn btn-sm btn-info" title="Ver detalhes da presença">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-sm btn-warning" title="Editar presença">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                Não há registros de presença para este aluno com os filtros selecionados.
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\academicas\importar_presencas_academica.html

html
{% extends 'base.html' %}

{% block title %}Importar Presenças{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Presenças</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados de presenças.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: Aluno (CPF), Turma, Data, Presente, Justificativa</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-link">Voltar para a lista de presenças</a>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\academicas\listar_observacoes_presenca_academica.html

html
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
        <div class="card-footer">
            <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                <i class="fas fa-list"></i> Voltar para a lista
            </a>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\academicas\listar_presencas_academica.html

html
{% extends 'base.html' %}

{% block title %}Lista de Presenças{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <!-- Padronizar cabeçalho com botões -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Presenças</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'presencas:registrar_presenca' %}" class="btn btn-primary me-2">
                <i class="fas fa-plus"></i> Registrar Presença
            </a>
            <a href="{% url 'presencas:exportar_presencas' %}" class="btn btn-success me-2">
                <i class="fas fa-file-export"></i> Exportar CSV
            </a>
            <a href="{% url 'presencas:importar_presencas' %}" class="btn btn-info">
                <i class="fas fa-file-import"></i> Importar CSV
            </a>
        </div>
    </div>
    
    <!-- Filtros avançados -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
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
                
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas as turmas</option>
                        {% for turma in turmas %}
                        <option value="{{ turma.id }}" {% if filtros.turma == turma.id|stringformat:"s" %}selected{% endif %}>
                            {{ turma.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="col-md-2">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ filtros.data_inicio }}">
                </div>
                
                <div class="col-md-2">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ filtros.data_fim }}">
                </div>
                
                <div class="col-md-2">
                    <label for="presente" class="form-label">Status</label>
                    <select name="presente" id="presente" class="form-select">
                        <option value="">Todos</option>
                        <option value="true" {% if filtros.presente == 'true' %}selected{% endif %}>Presente</option>
                        <option value="false" {% if filtros.presente == 'false' %}selected{% endif %}>Ausente</option>
                    </select>
                </div>
                
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                        <i class="fas fa-undo"></i> Limpar Filtros
                    </a>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Tabela de presenças -->
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Atividade</th>
                            <th>Turma</th>
                            <th>Data</th>
                            <th>Status</th>
                            <th>Justificativa</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for presenca in presencas %}
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    {% if presenca.aluno.foto %}
                                    <img src="{{ presenca.aluno.foto.url }}" alt="{{ presenca.aluno.nome }}" 
                                         class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                                    {% else %}
                                    <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-2"
                                         style="width: 40px; height: 40px; color: white;">
                                        {{ presenca.aluno.nome|first|upper }}
                                    </div>
                                    {% endif %}
                                    <div>
                                        <div>{{ presenca.aluno.nome }}</div>
                                        <small class="text-muted">{{ presenca.aluno.cpf }}</small>
                                    </div>
                                </div>
                            </td>
                            <td>{{ presenca.atividade.nome }}</td>
                            <td>{{ presenca.atividade.turma.nome }}</td>
                            <td>{{ presenca.data|date:"d/m/Y" }}</td>
                            <td>
                                {% if presenca.presente %}
                                <span class="badge bg-success">Presente</span>
                                {% else %}
                                <span class="badge bg-danger">Ausente</span>
                                {% endif %}
                            </td>
                            <td>{{ presenca.justificativa|truncatechars:30|default:"-" }}</td>
                            <td>
                                <div class="table-actions">
                                    <a href="{% url 'presencas:detalhar_presenca' presenca.id %}" class="btn btn-sm btn-info" title="Ver detalhes da presença">
                                        <i class="fas fa-eye"></i> Detalhes
                                    </a>
                                    <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-sm btn-warning" title="Editar presença">
                                        <i class="fas fa-edit"></i> Editar
                                    </a>
                                    <a href="{% url 'presencas:excluir_presenca' presenca.id %}" class="btn btn-sm btn-danger" title="Excluir presença">
                                        <i class="fas fa-trash"></i> Excluir
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="7" class="text-center py-3">
                                <p class="mb-0">Nenhum registro de presença encontrado com os filtros selecionados.</p>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
            <div>
                <p class="mb-0">Exibindo {{ presencas|length }} de {{ page_obj.paginator.count }} registros</p>
            </div>
            
            {% if page_obj.has_other_pages %}
            <nav aria-label="Paginação">
                <ul class="pagination mb-0">
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}" aria-label="Anterior">
                            <span aria-hidden="true">«</span>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link" aria-hidden="true">«</span>
                    </li>
                    {% endif %}
                    
                    {% for i in page_obj.paginator.page_range %}
                        {% if page_obj.number == i %}
                        <li class="page-item active"><span class="page-link">{{ i }}</span></li>
                        {% else %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ i }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}">{{ i }}</a>
                        </li>
                        {% endif %}
                    {% endfor %}
                    
                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in filtros.items %}&{{ key }}={{ value }}{% endfor %}" aria-label="Próxima">
                            <span aria-hidden="true">»</span>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link" aria-hidden="true">»</span>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar Select2 para melhorar a experiência de seleção
        if (typeof $.fn.select2 === 'function') {
            $('#aluno').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione um aluno',
                allowClear: true
            });
            
            $('#turma').select2({
                theme: 'bootstrap-5',
                placeholder: 'Selecione uma turma',
                allowClear: true
            });
        }
    });
</script>
{% endblock %}



'''