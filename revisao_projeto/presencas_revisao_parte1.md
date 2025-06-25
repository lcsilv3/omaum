'''
# Revisão da Funcionalidade: presencas

## Arquivos forms.py:


### Arquivo: presencas\forms.py

python
from django import forms
from importlib import import_module
from datetime import date

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_model():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_curso_model():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")

def get_matricula_model():
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")

class DadosBasicosPresencaForm(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=get_curso_model().objects.all(),
        label="Curso",
        required=True,
        empty_label="Selecione..."
    )
    turma = forms.ModelChoiceField(
        queryset=get_turma_model().objects.none(),
        label="Turma",
        required=True,
        empty_label="Selecione..."
    )
    ano = forms.IntegerField(label="Ano", required=True)
    mes = forms.IntegerField(label="Mês", required=True, min_value=1, max_value=12)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['turma'].queryset = get_turma_model().objects.filter(curso_id=curso_id, status='A')
            except (ValueError, TypeError):
                self.fields['turma'].queryset = get_turma_model().objects.none()
        elif self.initial.get('curso'):
            curso_id = self.initial.get('curso').id if hasattr(self.initial.get('curso'), 'id') else self.initial.get('curso')
            self.fields['turma'].queryset = get_turma_model().objects.filter(curso_id=curso_id, status='A')
        else:
            self.fields['turma'].queryset = get_turma_model().objects.none()

class TotaisAtividadesPresencaForm(forms.Form):
    def __init__(self, *args, atividades=None, **kwargs):
        super().__init__(*args, **kwargs)
        if atividades is not None:
            for atividade in atividades:
                self.fields[f'qtd_ativ_{atividade.id}'] = forms.IntegerField(
                    label=atividade.nome,
                    min_value=0,
                    max_value=999,
                    required=True,
                    widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qtd. dias'})
                )
        self.atividades = atividades

    def clean(self):
        cleaned_data = super().clean()
        faltantes = []
        for atividade in getattr(self, 'atividades', []):
            key = f'qtd_ativ_{atividade.id}'
            if cleaned_data.get(key) in [None, '']:
                faltantes.append(atividade.nome)
        if faltantes:
            raise forms.ValidationError(
                f"As seguintes atividades não tiveram quantidade informada: {', '.join(faltantes)}. "
                "As atividades não informadas não poderão sofrer alterações na seção seguinte."
            )
        return cleaned_data

class AlunosPresencaForm(forms.Form):
    alunos_presentes = forms.ModelMultipleChoiceField(
        queryset=get_aluno_model().objects.none(),
        label="Alunos Presentes",
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, turma=None, **kwargs):
        super().__init__(*args, **kwargs)
        if turma:
            Matricula = get_matricula_model()
            matriculas = Matricula.objects.filter(turma=turma, status='A')
            alunos_ids = matriculas.values_list('aluno_id', flat=True)
            self.fields['alunos_presentes'].queryset = get_aluno_model().objects.filter(
                pk__in=alunos_ids, situacao='ATIVO'
            ).order_by('nome')



## Arquivos views.py:


### Arquivo: presencas\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
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
    # Corrigido o caminho do template:
    return render(request, 'presencas/academicas/listar_presencas_academicas.html', context)

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
    # Corrigido o caminho do template:
    return render(request, 'presencas/ritualisticas/listar_presencas_ritualisticas.html', context)

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
    return render(request, 'presencas/academicas/registrar_presenca_academica.html', context)

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

@login_required
def editar_presenca_academica(request, pk):
    Presenca = get_model_academica()
    presenca = get_object_or_404(Presenca, pk=pk)
    if request.method == 'POST':
        presenca.presente = request.POST.get('presente') == 'on'
        presenca.data = request.POST.get('data')
        presenca.save()
        messages.success(request, 'Presença acadêmica atualizada com sucesso.')
        return redirect('presencas:listar_presencas_academicas')
    return render(request, 'presencas/editar_presenca_academica.html', {'presenca': presenca})

@login_required
def excluir_presenca_academica(request, pk):
    Presenca = get_model_academica()
    presenca = get_object_or_404(Presenca, pk=pk)
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença acadêmica excluída com sucesso.')
        return redirect('presencas:listar_presencas_academicas')
    return render(request, 'presencas/confirmar_exclusao_academica.html', {'presenca': presenca})

@login_required
def detalhar_presenca_academica(request, pk):
    Presenca = get_model_academica()
    presenca = get_object_or_404(Presenca, pk=pk)
    return render(request, 'presencas/detalhar_presenca_academica.html', {'presenca': presenca})

@login_required
def editar_presenca_ritualistica(request, pk):
    Presenca = get_model_ritualistica()
    presenca = get_object_or_404(Presenca, pk=pk)
    if request.method == 'POST':
        presenca.presente = request.POST.get('presente') == 'on'
        presenca.data = request.POST.get('data')
        presenca.save()
        messages.success(request, 'Presença ritualística atualizada com sucesso.')
        return redirect('presencas:listar_presencas_ritualisticas')
    return render(request, 'presencas/editar_presenca_ritualistica.html', {'presenca': presenca})

@login_required
def excluir_presenca_ritualistica(request, pk):
    Presenca = get_model_ritualistica()
    presenca = get_object_or_404(Presenca, pk=pk)
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença ritualística excluída com sucesso.')
        return redirect('presencas:listar_presencas_ritualisticas')
    return render(request, 'presencas/confirmar_exclusao_ritualistica.html', {'presenca': presenca})

@login_required
def detalhar_presenca_ritualistica(request, pk):
    Presenca = get_model_ritualistica()
    presenca = get_object_or_404(Presenca, pk=pk)
    return render(request, 'presencas/detalhar_presenca_ritualistica.html', {'presenca': presenca})

# Exemplo para ObservacaoPresenca:
@login_required
def listar_observacoes_presenca(request):
    ObservacaoPresenca = get_model_observacao()
    observacoes = ObservacaoPresenca.objects.select_related('aluno', 'turma', 'atividade_academica', 'atividade_ritualistica')
    return render(request, 'presencas/listar_observacoes_presenca.html', {'observacoes': observacoes})

@login_required
def exportar_presencas_academicas(request):
    # Exemplo simples: renderiza um template de exportação
    return render(request, 'presencas/academicas/exportar_presencas_academicas.html')

@login_required
def exportar_presencas_ritualisticas(request):
    # Exemplo simples: renderiza um template de exportação
    return render(request, 'presencas/ritualisticas/exportar_presencas_ritualisticas.html')

@login_required
def importar_presencas_academicas(request):
    # Exemplo simples: renderiza um template de importação
    return render(request, 'presencas/academicas/importar_presencas_academicas.html')

@login_required
def importar_presencas_ritualisticas(request):
    # Exemplo simples: renderiza um template de importação
    return render(request, 'presencas/ritualisticas/importar_presencas_ritualisticas.html')

@login_required
def registrar_presenca_totais_atividades(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    curso = turma.curso if turma else None

    atividades = []
    if turma and ano and mes:
        totais_atividades = request.session.get('presenca_totais_atividades', {})
        if totais_atividades:
            atividades_ids = [int(key.replace('qtd_ativ_', '')) for key in totais_atividades.keys() if int(totais_atividades[key]) > 0]
            atividades = AtividadeAcademica.objects.filter(
                id__in=atividades_ids,
                turmas__id=turma.id,
            )
        else:
            # Remova o filtro curso=curso se não for obrigatório
            atividades = AtividadeAcademica.objects.filter(
                turmas__id=turma.id,
                data_inicio__year=ano,
                data_inicio__month=mes
            ).distinct()

    totais_registrados = []
    if turma and ano and mes:
        totais_registrados = TotalAtividadeMes.objects.filter(
            turma=turma, ano=ano, mes=mes
        ).select_related('atividade')

    if request.method == 'POST':
        form = TotaisAtividadesPresencaForm(request.POST, atividades=atividades)
        if form.is_valid():
            request.session['presenca_totais_atividades'] = {
                key: value for key, value in form.cleaned_data.items() if key.startswith('qtd_ativ_')
            }
            return redirect('presencas:registrar_presenca_dias_atividades')
    else:
        form = TotaisAtividadesPresencaForm(atividades=atividades)

    return render(request, 'presencas/registrar_presenca_totais_atividades.html', {
        'form': form,
        'turma': turma,
        'curso': curso,
        'ano': ano,
        'mes': mes,
        'atividades': atividades,
        'totais_registrados': totais_registrados,
    })

@login_required
def registrar_presenca_dias_atividades(request):
    from datetime import date
    from calendar import monthrange
    from atividades.models import AtividadeAcademica
    from turmas.models import Turma
    from presencas.models import ObservacaoPresenca

    if request.method == 'GET':
        turma_id = request.session.get('presenca_turma_id')
        ano = request.session.get('presenca_ano')
        mes = request.session.get('presenca_mes')
        turma = Turma.objects.get(id=turma_id) if turma_id else None

        atividades = []
        if turma and ano and mes:
            totais_atividades = request.session.get('presenca_totais_atividades', {})
            if totais_atividades:
                atividades_ids = [
                    int(key.replace('qtd_ativ_', ''))
                    for key, value in totais_atividades.items()
                    if int(value) > 0
                ]
                atividades = AtividadeAcademica.objects.filter(
                    id__in=atividades_ids,
                    turmas__id=turma.id,
                    data_inicio__year=ano,
                    data_inicio__month=mes
                )
            else:
                atividades = AtividadeAcademica.objects.filter(
                    turmas__id=turma.id,
                    data_inicio__year=ano,
                    data_inicio__month=mes
                ).distinct()

        qtd_dias = monthrange(int(ano), int(mes))[1]
        dias_do_mes = list(range(1, qtd_dias + 1))

        presencas = {}
        presencas_obs = {}
        if turma and ano and mes and atividades:
            observacoes = ObservacaoPresenca.objects.filter(
                turma=turma,
                data__year=ano,
                data__month=mes,
                atividade_academica__in=atividades
            )
            for obs in observacoes:
                aid = obs.atividade_academica_id
                dia = obs.data.day
                presencas.setdefault(aid, []).append(dia)
                presencas_obs.setdefault(aid, {})[dia] = obs.texto

        context = {
            'atividades': atividades,
            'dias_do_mes': dias_do_mes,
            'mes': mes,
            'ano': ano,
            'presencas': presencas,
            'presencas_obs': presencas_obs,
        }
        return render(request, 'presencas/registrar_presenca_dias_atividades.html', context)

    # ...código POST permanece igual...


## Arquivos urls.py:


### Arquivo: presencas\urls.py

python
from django.urls import path
from .views_ext.listagem import listar_presencas
from .views_ext.atividade import registrar_presencas_atividade, editar_presenca
from .views_ext.multiplas import registrar_presencas_multiplas, formulario_presencas_multiplas
from . import views
from importlib import import_module

registro_presenca_views = import_module('presencas.views_ext.registro_presenca')

app_name = "presencas"

urlpatterns = [
    # Presenças acadêmicas
    path("academicas/", views.listar_presencas_academicas, name="listar_presencas_academicas"),
    path("academicas/registrar/", views.registrar_presenca_academica, name="registrar_presenca_academica"),
    path("academicas/editar/<int:pk>/", views.editar_presenca_academica, name="editar_presenca_academica"),
    path("academicas/excluir/<int:pk>/", views.excluir_presenca_academica, name="excluir_presenca_academica"),
    path("academicas/detalhar/<int:pk>/", views.detalhar_presenca_academica, name="detalhar_presenca_academica"),
    path("academicas/exportar/", views.exportar_presencas_academicas, name="exportar_presencas_academicas"),
    path("academicas/importar/", views.importar_presencas_academicas, name="importar_presencas_academicas"),

    # Presenças ritualísticas
    path("ritualisticas/", views.listar_presencas_ritualisticas, name="listar_presencas_ritualisticas"),
    path("ritualisticas/registrar/", views.registrar_presenca_ritualistica, name="registrar_presenca_ritualistica"),
    path("ritualisticas/editar/<int:pk>/", views.editar_presenca_ritualistica, name="editar_presenca_ritualistica"),
    path("ritualisticas/excluir/<int:pk>/", views.excluir_presenca_ritualistica, name="excluir_presenca_ritualistica"),
    path("ritualisticas/detalhar/<int:pk>/", views.detalhar_presenca_ritualistica, name="detalhar_presenca_ritualistica"),
    path("ritualisticas/exportar/", views.exportar_presencas_ritualisticas, name="exportar_presencas_ritualisticas"),
    path("ritualisticas/importar/", views.importar_presencas_ritualisticas, name="importar_presencas_ritualisticas"),

    # Observações de presença
    path("observacoes/", views.listar_observacoes_presenca, name="listar_observacoes_presenca"),

    # Outras rotas dos submódulos, se necessário
    path("multiplas/", registrar_presencas_multiplas, name="registrar_presencas_multiplas"),
    path("multiplas/formulario/", formulario_presencas_multiplas, name="formulario_presencas_multiplas"),

    # Registro de presença - dados básicos
    path('registrar-presenca/dados-basicos/', registro_presenca_views.registrar_presenca_dados_basicos, name='registrar_presenca_dados_basicos'),
    path('registrar-presenca/dados-basicos/ajax/', registro_presenca_views.registrar_presenca_dados_basicos_ajax, name='registrar_presenca_dados_basicos_ajax'),

    # Registro de presença - totais por atividades
    path('registrar-presenca/totais-atividades/', registro_presenca_views.registrar_presenca_totais_atividades, name='registrar_presenca_totais_atividades'),
    path('registrar-presenca/totais-atividades/ajax/', registro_presenca_views.registrar_presenca_totais_atividades_ajax, name='registrar_presenca_totais_atividades_ajax'),

    # Registro de presença - dias/atividades (GET e POST)
    path('registrar-presenca/dias-atividades/', registro_presenca_views.registrar_presenca_dias_atividades, name='registrar_presenca_dias_atividades'),
    path('registrar-presenca/dias-atividades/ajax/', registro_presenca_views.registrar_presenca_dias_atividades_ajax, name='registrar_presenca_dias_atividades_ajax'),

    # Registro de presença - alunos
    path('registrar-presenca/alunos/', registro_presenca_views.registrar_presenca_alunos, name='registrar_presenca_alunos'),
    path('registrar-presenca/alunos/ajax/', registro_presenca_views.registrar_presenca_alunos_ajax, name='registrar_presenca_alunos_ajax'),

    # Confirmação de registro de presença
    path('registrar-presenca/confirmar/', registro_presenca_views.registrar_presenca_confirmar, name='registrar_presenca_confirmar'),
    path('registrar-presenca/confirmar/ajax/', registro_presenca_views.registrar_presenca_confirmar_ajax, name='registrar_presenca_confirmar_ajax'),

    # Turmas por curso - AJAX
    path('registrar-presenca/turmas-por-curso/', registro_presenca_views.turmas_por_curso_ajax, name='turmas_por_curso_ajax'),
    path('registrar-presenca/atividades-por-turma/', registro_presenca_views.atividades_por_turma_ajax, name='atividades_por_turma_ajax'),

    # Limites do calendário - AJAX
    path('registrar-presenca/limites-calendario/', registro_presenca_views.obter_limites_calendario_ajax, name='registrar_presenca_limites_calendario_ajax'),
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

    Armazena informações sobre presença, ausência e justificativas de alunos em atividades acadêmicas ou ritualísticas.
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

class TotalAtividadeMes(models.Model):
    atividade = models.ForeignKey(get_atividade_model(), on_delete=models.CASCADE)
    turma = models.ForeignKey(get_turma_model(), on_delete=models.CASCADE)
    ano = models.IntegerField()
    mes = models.IntegerField()
    qtd_ativ_mes = models.PositiveIntegerField(default=0)
    registrado_por = models.CharField(max_length=100, default="Sistema")
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["atividade", "turma", "ano", "mes"]
        verbose_name = "Total de Atividade no Mês"
        verbose_name_plural = "Totais de Atividades no Mês"

    def __str__(self):
        return f"{self.atividade} - {self.turma} - {self.mes}/{self.ano}: {self.qtd_ativ_mes}"

class ObservacaoPresenca(models.Model):
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Aluno",
        related_name="observacoes_presenca_presencas"
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="observacoes_presenca_presencas"
    )
    data = models.DateField(verbose_name="Data")
    atividade_academica = models.ForeignKey(
        'atividades.AtividadeAcademica',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Atividade Acadêmica",
        related_name="observacoes_presenca_presencas"
    )
    atividade_ritualistica = models.ForeignKey(
        'atividades.AtividadeRitualistica',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Atividade Ritualística",
        related_name="observacoes_presenca_presencas"
    )
    texto = models.TextField(verbose_name="Observação", blank=True, null=True)
    registrado_por = models.CharField(max_length=100, default="Sistema", verbose_name="Registrado por")
    data_registro = models.DateTimeField(default=timezone.now, verbose_name="Data de registro")

    class Meta:
        verbose_name = "Observação de Presença"
        verbose_name_plural = "Observações de Presença"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.data} - {self.atividade_academica or self.atividade_ritualistica} - {self.texto[:30]}"



## Arquivos de Views Modulares:


### Arquivo: presencas\views_ext\__init__.py

python
from .listagem import listar_presencas
from .atividade import registrar_presencas_atividade, editar_presenca
from .multiplas import registrar_presencas_multiplas, formulario_presencas_multiplas

__all__ = [
    'listar_presencas',
    'registrar_presencas_atividade',
    'editar_presenca',
    'registrar_presencas_multiplas',
    'formulario_presencas_multiplas',
]



### Arquivo: presencas\views_ext\academicas.py

python
# ...código existente...
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from alunos.models import Aluno
from presencas.models import Presenca

def listar_presencas_academicas(request):
    cursos = Curso.objects.all()
    turmas = Turma.objects.all()
    atividades = AtividadeAcademica.objects.all()
    alunos = Aluno.objects.all()

    # Filtros
    curso_id = request.GET.get('curso')
    turma_id = request.GET.get('turma')
    atividade_id = request.GET.get('atividade')
    aluno_id = request.GET.get('aluno')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    presencas = Presenca.objects.all()

    if curso_id:
        turmas = Turma.objects.filter(curso_id=curso_id)
        presencas = presencas.filter(turma__curso_id=curso_id)
    if turma_id:
        atividades = Atividade.objects.filter(turma_id=turma_id)
        presencas = presencas.filter(turma_id=turma_id)
    if atividade_id:
        presencas = presencas.filter(atividade_id=atividade_id)
    if aluno_id:
        presencas = presencas.filter(aluno_id=aluno_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    context = {
        'presencas': presencas,
        'cursos': cursos,
        'turmas': turmas,
        'atividades': atividades,
        'alunos': alunos,
    }
    return render(request, 'presencas/academicas/listar_presencas_academicas.html', context)
# ...código existente...



### Arquivo: presencas\views_ext\atividade.py

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



### Arquivo: presencas\views_ext\listagem.py

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



### Arquivo: presencas\views_ext\multiplas.py

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



### Arquivo: presencas\views_ext\registro_presenca.py

python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import date
from presencas.forms import DadosBasicosPresencaForm, TotaisAtividadesPresencaForm, AlunosPresencaForm
from importlib import import_module
from cursos.models import Curso
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from presencas.models import TotalAtividadeMes, ObservacaoPresenca
from calendar import monthrange
from alunos.models import Aluno
import logging
logger = logging.getLogger(__name__)

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

@login_required
def registrar_presenca_dados_basicos(request):
    hoje = date.today()
    ano_corrente = hoje.year
    mes_corrente = hoje.month

    form = DadosBasicosPresencaForm(initial={'ano': ano_corrente, 'mes': mes_corrente})

    return render(request, 'presencas/registrar_presenca_dados_basicos.html', {
        'form': form,
        'ano_corrente': ano_corrente,
        'mes_corrente': mes_corrente,
    })

@login_required
@require_POST
def registrar_presenca_dados_basicos_ajax(request):
    form = DadosBasicosPresencaForm(request.POST)
    if form.is_valid():
        request.session['presenca_turma_id'] = form.cleaned_data['turma'].id
        request.session['presenca_ano'] = form.cleaned_data['ano']
        request.session['presenca_mes'] = form.cleaned_data['mes']
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/totais-atividades/'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def registrar_presenca_totais_atividades(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    curso = turma.curso if turma else None

    atividades = []
    if turma and curso and ano and mes:
        totais_atividades = request.session.get('presenca_totais_atividades', {})
        if totais_atividades:
            atividades_ids = [int(key.replace('qtd_ativ_', '')) for key in totais_atividades.keys() if int(totais_atividades[key]) > 0]
            atividades = AtividadeAcademica.objects.filter(
                id__in=atividades_ids,
                turmas__id=turma.id,
            )
        else:
            atividades = AtividadeAcademica.objects.filter(
                turmas__id=turma.id,
                curso=curso,
                data_inicio__year=ano,
                data_inicio__month=mes
            ).distinct()

    totais_registrados = []
    if turma and ano and mes:
        totais_registrados = TotalAtividadeMes.objects.filter(
            turma=turma, ano=ano, mes=mes
        ).select_related('atividade')

    if request.method == 'POST':
        form = TotaisAtividadesPresencaForm(request.POST, atividades=atividades)
        if form.is_valid():
            request.session['presenca_totais_atividades'] = {
                key: value for key, value in form.cleaned_data.items() if key.startswith('qtd_ativ_')
            }
            # Redireciona para a etapa de designação dos dias
            return redirect('presencas:registrar_presenca_dias_atividades')
    else:
        form = TotaisAtividadesPresencaForm(atividades=atividades)

    return render(request, 'presencas/registrar_presenca_totais_atividades.html', {
        'form': form,
        'turma': turma,
        'curso': curso,
        'ano': ano,
        'mes': mes,
        'atividades': atividades,
        'totais_registrados': totais_registrados,
    })

@login_required
@require_POST
def registrar_presenca_totais_atividades_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    curso = turma.curso if turma else None

    atividades = []
    if turma and curso and ano and mes:
        totais_atividades = request.session.get('presenca_totais_atividades', {})
        atividades_ids = [int(key.replace('qtd_ativ_', '')) for key in totais_atividades.keys() if int(totais_atividades[key]) > 0]
        atividades = AtividadeAcademica.objects.filter(
            id__in=atividades_ids,
            turmas__id=turma.id,
            # ...outros filtros se houver...
        )

    form = TotaisAtividadesPresencaForm(request.POST, atividades=atividades)
    if form.is_valid():
        request.session['presenca_totais_atividades'] = {
            key: value for key, value in form.cleaned_data.items() if key.startswith('qtd_ativ_')
        }
        # Redireciona para a etapa de designação dos dias (AJAX)
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/dias-atividades/'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def registrar_presenca_dias_atividades(request):
    """
    GET: Exibe o formulário para seleção dos dias e observações das atividades.
    POST: Salva no banco os dias e observações selecionados para cada atividade.
    """
    from django.shortcuts import render, redirect
    from datetime import date
    from calendar import monthrange
    from atividades.models import AtividadeAcademica
    from turmas.models import Turma
    from presencas.models import ObservacaoPresenca

    if request.method == 'GET':
        turma_id = request.session.get('presenca_turma_id')
        ano = request.session.get('presenca_ano')
        mes = request.session.get('presenca_mes')
        turma = Turma.objects.get(id=turma_id) if turma_id else None

        atividades = []
        if turma and ano and mes:
            totais_atividades = request.session.get('presenca_totais_atividades', {})
            atividades_ids = [
                int(key.replace('qtd_ativ_', ''))
                for key, value in totais_atividades.items()
                if value not in [None, '', '0', 0]  # Mostra só as atividades informadas
            ]
            logger.debug(f"Totais atividades na sessão: {totais_atividades}")
            atividades_ids = [
                int(key.replace('qtd_ativ_', ''))
                for key, value in totais_atividades.items()
                if int(value) > 0
            ]
            logger.debug(f"IDs filtrados: {atividades_ids}")
            if atividades_ids:
                atividades = AtividadeAcademica.objects.filter(
                    id__in=atividades_ids,
                    turmas__id=turma.id,
                )
            else:
                atividades = []  # Não mostra nenhuma se não houver seleção

        qtd_dias = monthrange(int(ano), int(mes))[1]
        dias_do_mes = list(range(1, qtd_dias + 1))

        # Busca dias já selecionados para cada atividade
        presencas = {}
        presencas_obs = {}
        if turma and ano and mes and atividades:
            observacoes = ObservacaoPresenca.objects.filter(
                turma=turma,
                data__year=ano,
                data__month=mes,
                atividade_academica__in=atividades
            )
            for obs in observacoes:
                aid = obs.atividade_academica_id
                dia = obs.data.day
                presencas.setdefault(aid, []).append(dia)
                presencas_obs.setdefault(aid, {})[dia] = obs.texto

        context = {
            'atividades': atividades,
            'dias_do_mes': dias_do_mes,
            'mes': mes,
            'ano': ano,
            'presencas': presencas,
            'presencas_obs': presencas_obs,
        }
        return render(request, 'presencas/registrar_presenca_dias_atividades.html', context)

    # POST
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    for key in request.POST:
        if key.startswith('presenca_'):
            atividade_id = key.replace('presenca_', '')
            dias = request.POST.getlist(key)
            for dia in dias:
                obs = request.POST.get(f'obs_{atividade_id}_{dia}', '')
                try:
                    atividade = AtividadeAcademica.objects.get(id=atividade_id)
                except AtividadeAcademica.DoesNotExist:
                    continue
                try:
                    data = date(int(ano), int(mes), int(dia))
                except Exception:
                    continue
                ObservacaoPresenca.objects.create(
                    aluno=None,  # ou defina o aluno se necessário
                    turma=turma,
                    data=data,
                    atividade_academica=atividade,
                    texto=obs,
                    registrado_por=request.user.username
                )
    return redirect('presencas:registrar_presenca_alunos')

@login_required
def registrar_presenca_alunos(request):
    turma_id = request.session.get('presenca_turma_id')
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    form = AlunosPresencaForm(turma=turma)

    return render(request, 'presencas/registrar_presenca_alunos.html', {
        'form': form,
        'turma': turma,
    })

@login_required
@require_POST
def registrar_presenca_alunos_ajax(request):
    turma_id = request.session.get('presenca_turma_id')
    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    form = AlunosPresencaForm(request.POST, turma=turma)
    if form.is_valid():
        request.session['presenca_alunos_presentes'] = list(form.cleaned_data['alunos_presentes'].values_list('id', flat=True))
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/confirmar/'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def turmas_por_curso_ajax(request):
    curso_id = request.GET.get('curso_id')
    turmas = Turma.objects.filter(curso_id=curso_id).values('id', 'nome')
    return JsonResponse(list(turmas), safe=False)

@login_required
def atividades_por_turma_ajax(request):
    turma_id = request.GET.get('turma_id')
    atividades = AtividadeAcademica.objects.filter(turmas__id=turma_id).values('id', 'nome')
    return JsonResponse(list(atividades), safe=False)

@login_required
def registrar_presenca_confirmar(request):
    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    atividade_id = request.session.get('presenca_atividade_id')
    alunos_presentes_ids = request.session.get('presenca_alunos_presentes', [])

    Turma = get_turma_model()
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    Atividade = import_module("atividades.models").AtividadeAcademica
    atividade = Atividade.objects.get(id=atividade_id) if atividade_id else None

    alunos_presentes = Aluno.objects.filter(id__in=alunos_presentes_ids)

    return render(request, 'presencas/registrar_presenca_confirmar.html', {
        'turma': turma,
        'ano': ano,
        'mes': mes,
        'atividade': atividade,
        'alunos_presentes': alunos_presentes,
    })

@login_required
@require_POST
@transaction.atomic
def registrar_presenca_confirmar_ajax(request):
    # Exemplo de lógica mínima para não quebrar o fluxo
    # Implemente aqui o salvamento definitivo das presenças, se necessário

    # Limpa sessão (ajuste conforme sua lógica)
    for key in [
        'presenca_turma_id', 'presenca_ano', 'presenca_mes',
        'presenca_atividade_id', 'presenca_alunos_presentes', 'presenca_totais_atividades'
    ]:
        if key in request.session:
            del request.session[key]
    return JsonResponse({'success': True, 'redirect_url': '/presencas/'})

@login_required
def obter_limites_calendario_ajax(request):
    turma_id = request.GET.get('turma_id')
    if not turma_id:
        return JsonResponse({'erro': 'Turma não informada.'}, status=400)
    try:
        turma = Turma.objects.get(id=turma_id)
        data_inicio = turma.data_inicio_ativ
        data_fim = turma.data_termino_atividades

        if not data_inicio or not data_fim:
            return JsonResponse({'erro': 'A turma selecionada não possui datas de início ou término definidas. Por favor, verifique o cadastro da turma.'}, status=400)

        return JsonResponse({
            'data_inicio': data_inicio.strftime('%Y-%m'),
            'data_fim': data_fim.strftime('%Y-%m')
        })
    except Turma.DoesNotExist:
        return JsonResponse({'erro': 'Turma não encontrada.'}, status=404)

@login_required
@require_POST
def registrar_presenca_dias_atividades_ajax(request):
    from datetime import date
    from atividades.models import AtividadeAcademica
    from turmas.models import Turma
    from presencas.models import ObservacaoPresenca

    turma_id = request.session.get('presenca_turma_id')
    ano = request.session.get('presenca_ano')
    mes = request.session.get('presenca_mes')
    turma = Turma.objects.get(id=turma_id) if turma_id else None

    if not turma or not ano or not mes:
        return JsonResponse({'success': False, 'message': 'Dados de sessão ausentes. Refaça o processo.'})

    # Remove observações anteriores para evitar duplicidade
    atividades = AtividadeAcademica.objects.filter(
        turmas__id=turma.id,
        data_inicio__year=ano,
        data_inicio__month=mes
    )
    ObservacaoPresenca.objects.filter(
        turma=turma,
        data__year=ano,
        data__month=mes,
        atividade_academica__in=atividades
    ).delete()

    try:
        for key in request.POST:
            if key.startswith('presenca_'):
                atividade_id = key.replace('presenca_', '')
                dias = request.POST.getlist(key)
                for dia in dias:
                    obs = request.POST.get(f'obs_{atividade_id}_{dia}', '')
                    try:
                        atividade = AtividadeAcademica.objects.get(id=atividade_id)
                        data = date(int(ano), int(mes), int(dia))
                        ObservacaoPresenca.objects.create(
                            aluno=None,
                            turma=turma,
                            data=data,
                            atividade_academica=atividade,
                            texto=obs,
                            registrado_por=request.user.username
                        )
                    except Exception as e:
                        logger.exception(f'Erro ao registrar observação para atividade {atividade_id}, dia {dia}: {e}')
                        continue
        return JsonResponse({'success': True, 'redirect_url': '/presencas/registrar-presenca/alunos/', 'message': 'Presenças salvas com sucesso!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao salvar: {str(e)}'})


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




### Arquivo: presencas\templates\presencas\academicas\exportar_presencas_academicas.html

html
{% extends 'base.html' %}

{% block title %}Exportar Presenças Acadêmicas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h2>Exportação de Presenças Acadêmicas</h2>
    <p>Funcionalidade de exportação de presenças acadêmicas. Implemente aqui a lógica de exportação (CSV, Excel, etc).</p>
    <a href="{% url 'presencas:listar_presencas_academicas' %}" class="btn btn-secondary mt-3">Voltar</a>
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


'''