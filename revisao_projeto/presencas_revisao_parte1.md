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
from django.http import HttpResponse, JsonResponse
import csv
import logging
from datetime import datetime

# Configurar logger
logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos necessários dinamicamente."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_model():
    """Obtém o modelo AtividadeAcademica dinamicamente."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

@login_required
def listar_presencas(request):
    """Lista todas as presenças registradas."""
    Presenca = get_models()
    
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Iniciar queryset
    presencas = Presenca.objects.all().select_related('aluno', 'turma', 'atividade')
    
    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    # Obter dados para os filtros
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    
    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'filtros': {
            'aluno': aluno_id,
            'turma': turma_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        }
    }
    
    return render(request, 'presencas/listar_presencas.html', context)

@login_required
def registrar_presenca(request):
    """Registra uma nova presença."""
    Presenca = get_models()
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    AtividadeAcademica = get_atividade_model()
    
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        turma_id = request.POST.get('turma')
        atividade_id = request.POST.get('atividade')
        data = request.POST.get('data')
        presente = request.POST.get('presente') == 'on'
        justificativa = request.POST.get('justificativa', '')
        
        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
            turma = Turma.objects.get(id=turma_id)
            atividade = None
            if atividade_id:
                atividade = AtividadeAcademica.objects.get(id=atividade_id)
            
            # Verificar se já existe registro para este aluno/turma/data
            if Presenca.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                messages.warning(request, f'Já existe um registro de presença para {aluno.nome} na turma {turma.nome} na data {data}.')
                return redirect('presencas:listar_presencas')
            
            presenca = Presenca(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                presente=presente,
                justificativa=justificativa if not presente else '',
                registrado_por=request.user.username,
                data_registro=timezone.now()
            )
            presenca.save()
            
            messages.success(request, f'Presença registrada com sucesso para {aluno.nome}.')
            return redirect('presencas:listar_presencas')
        
        except Exception as e:
            messages.error(request, f'Erro ao registrar presença: {str(e)}')
    
    # Para requisições GET, exibir o formulário
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    atividades = AtividadeAcademica.objects.all()
    
    context = {
        'alunos': alunos,
        'turmas': turmas,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    
    return render(request, 'presencas/registrar_presenca.html', context)

@login_required
def editar_presenca(request, presenca_id):
    """Edita um registro de presença existente."""
    Presenca = get_models()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    if request.method == 'POST':
        presente = request.POST.get('presente') == 'on'
        justificativa = request.POST.get('justificativa', '')
        
        presenca.presente = presente
        presenca.justificativa = justificativa if not presente else ''
        presenca.registrado_por = request.user.username
        presenca.data_registro = timezone.now()
        
        try:
            presenca.save()
            messages.success(request, 'Registro de presença atualizado com sucesso.')
            return redirect('presencas:listar_presencas')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar presença: {str(e)}')
    
    context = {
        'presenca': presenca
    }
    
    return render(request, 'presencas/editar_presenca.html', context)

@login_required
def excluir_presenca(request, presenca_id):
    """Exclui um registro de presença."""
    Presenca = get_models()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    if request.method == 'POST':
        try:
            presenca.delete()
            messages.success(request, 'Registro de presença excluído com sucesso.')
            return redirect('presencas:listar_presencas')
        except Exception as e:
            messages.error(request, f'Erro ao excluir presença: {str(e)}')
    
    context = {
        'presenca': presenca
    }
    
    return render(request, 'presencas/excluir_presenca.html', context)

@login_required
def detalhar_presenca(request, presenca_id):
    """Exibe os detalhes de um registro de presença."""
    Presenca = get_models()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    context = {
        'presenca': presenca
    }
    
    return render(request, 'presencas/detalhar_presenca.html', context)

@login_required
def registrar_presenca_turma(request, turma_id):
    """Registra presença para todos os alunos de uma turma."""
    Presenca = get_models()
    Turma = get_turma_model()
    
    turma = get_object_or_404(Turma, id=turma_id)
    
    # Obter todos os alunos matriculados na turma
    try:
        Matricula = import_module("matriculas.models").Matricula
        matriculas = Matricula.objects.filter(turma=turma, status='A')
        alunos = [m.aluno for m in matriculas]
    except Exception as e:
        messages.error(request, f'Erro ao obter alunos da turma: {str(e)}')
        return redirect('turmas:detalhar_turma', turma_id=turma_id)
    
    if request.method == 'POST':
        data = request.POST.get('data')
        atividade_id = request.POST.get('atividade')
        
        try:
            atividade = None
            if atividade_id:
                AtividadeAcademica = get_atividade_model()
                atividade = AtividadeAcademica.objects.get(id=atividade_id)
            
            # Processar presenças para cada aluno
            for aluno in alunos:
                presente = request.POST.get(f'presente_{aluno.cpf}') == 'on'
                justificativa = request.POST.get(f'justificativa_{aluno.cpf}', '')
                
                # Verificar se já existe registro
                if Presenca.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                    # Atualizar registro existente
                    presenca = Presenca.objects.get(aluno=aluno, turma=turma, data=data)
                    presenca.presente = presente
                    presenca.justificativa = justificativa if not presente else ''
                    presenca.atividade = atividade
                    presenca.registrado_por = request.user.username
                    presenca.data_registro = timezone.now()
                    presenca.save()
                else:
                    # Criar novo registro
                    Presenca.objects.create(
                        aluno=aluno,
                        turma=turma,
                        atividade=atividade,
                        data=data,
                        presente=presente,
                        justificativa=justificativa if not presente else '',
                        registrado_por=request.user.username,
                        data_registro=timezone.now()
                    )
            
            messages.success(request, f'Presenças registradas com sucesso para a turma {turma.nome}.')
            return redirect('turmas:detalhar_turma', turma_id=turma_id)
            
        except Exception as e:
            messages.error(request, f'Erro ao registrar presenças: {str(e)}')
    
    # Para requisições GET, exibir o formulário
    AtividadeAcademica = get_atividade_model()
    atividades = AtividadeAcademica.objects.filter(turmas=turma)
    
    context = {
        'turma': turma,
        'alunos': alunos,
        'atividades': atividades,
        'data_hoje': timezone.now().date()
    }
    
    return render(request, 'presencas/registrar_presenca_turma.html', context)

@login_required
def exportar_presencas_csv(request):
    """Exporta os registros de presença para um arquivo CSV."""
    Presenca = get_models()
    
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Iniciar queryset
    presencas = Presenca.objects.all().select_related('aluno', 'turma', 'atividade')
    
    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    # Criar resposta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="presencas.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Aluno', 'CPF', 'Turma', 'Data', 'Presente', 'Justificativa', 'Registrado Por', 'Data de Registro'])
    
    for presenca in presencas:
        writer.writerow([
            presenca.aluno.nome,
            presenca.aluno.cpf,
            presenca.turma.nome,
            presenca.data,
            'Sim' if presenca.presente else 'Não',
            presenca.justificativa,
            presenca.registrado_por,
            presenca.data_registro
        ])
    
    return response

@login_required
def relatorio_presencas(request):
    """Exibe um relatório de presenças."""
    Presenca = get_models()
    
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Iniciar queryset
    presencas = Presenca.objects.all().select_related('aluno', 'turma')
    
    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    # Calcular estatísticas
    total = presencas.count()
    presentes = presencas.filter(presente=True).count()
    ausentes = total - presentes
    taxa_presenca = (presentes / total * 100) if total > 0 else 0
    
    # Obter dados para os filtros
    Aluno = get_aluno_model()
    Turma = get_turma_model()
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    
    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'filtros': {
            'aluno': aluno_id,
            'turma': turma_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        },
        'estatisticas': {
            'total': total,
            'presentes': presentes,
            'ausentes': ausentes,
            'taxa_presenca': taxa_presenca
        }
    }
    
    return render(request, 'presencas/relatorio_presencas.html', context)

@login_required
def registrar_presenca_em_massa(request):
    """Registra presença em massa para uma turma."""
    Turma = get_turma_model()
    Presenca = get_models()
    Aluno = get_aluno_model()
    AtividadeAcademica = get_atividade_model()
    
    # Para requisições POST (quando o formulário é enviado)
    if request.method == "POST":
        turma_id = request.POST.get("turma")
        atividade_id = request.POST.get("atividade")
        data = request.POST.get("data")
        presentes = request.POST.getlist("presentes")
        
        if not turma_id or not atividade_id or not data:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            return redirect("presencas:registrar_presenca_em_massa")
        
        try:
            turma = Turma.objects.get(id=turma_id)
            atividade = AtividadeAcademica.objects.get(id=atividade_id)
            data_obj = datetime.strptime(data, "%Y-%m-%d").date()
            
            # Obter todos os alunos da turma
            Matricula = import_module("matriculas.models").Matricula
            matriculas = Matricula.objects.filter(turma=turma, status="A")
            alunos = [m.aluno for m in matriculas]
            
            # Registrar presenças/ausências
            for aluno in alunos:
                presente = aluno.cpf in presentes
                justificativa = request.POST.get(f"justificativa_{aluno.cpf}", "") if not presente else ""
                
                # Verificar se já existe registro para este aluno/atividade/data
                presenca, created = Presenca.objects.update_or_create(
                    aluno=aluno,
                    atividade=atividade,
                    turma=turma,
                    data=data_obj,
                    defaults={
                        "presente": presente,
                        "justificativa": justificativa,
                        "registrado_por": request.user.username
                    }
                )
            
            messages.success(request, f"Presenças registradas com sucesso para {len(alunos)} alunos.")
            return redirect("presencas:listar_presencas")
            
        except Exception as e:
            messages.error(request, f"Erro ao registrar presenças: {str(e)}")
            return redirect("presencas:registrar_presenca_em_massa")
    
    # Para requisições GET (quando a página é carregada)
    turmas = Turma.objects.filter(status="A")
    data_hoje = timezone.now().date()
    
    return render(
        request, 
        "presencas/registrar_presenca_em_massa.html",
        {
            "turmas": turmas,
            "data_hoje": data_hoje
        }
    )

@login_required
def api_atividades_por_turma(request, turma_id):
    """API para obter atividades de uma turma."""
    try:
        Turma = get_turma_model()
        AtividadeAcademica = get_atividade_model()
        
        turma = Turma.objects.get(id=turma_id)
        atividades = AtividadeAcademica.objects.filter(turmas=turma)
        
        return JsonResponse({
            "success": True,
            "atividades": [
                {
                    "id": atividade.id,
                    "nome": atividade.nome
                }
                for atividade in atividades
            ]
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@login_required
def api_alunos_por_turma(request, turma_id):
    """API para obter alunos de uma turma."""
    try:
        Turma = get_turma_model()
        
        turma = Turma.objects.get(id=turma_id)
        Matricula = import_module("matriculas.models").Matricula
        matriculas = Matricula.objects.filter(turma=turma, status="A")
        
        return JsonResponse({
            "success": True,
            "alunos": [
                {
                    "cpf": m.aluno.cpf,
                    "nome": m.aluno.nome,
                    "foto": m.aluno.foto.url if m.aluno.foto else None
                }
                for m in matriculas
            ]
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


## Arquivos urls.py:


### Arquivo: presencas\urls.py

python
from django.urls import path
from . import views

app_name = "presencas"

urlpatterns = [
   path("", views.listar_presencas, name="listar_presencas"),
   path("registrar-em-massa/", views.registrar_presenca_em_massa, name="registrar_presenca_em_massa"),
   path("registrar/", views.registrar_presenca, name="registrar_presenca"),
   path("editar/<int:presenca_id>/", views.editar_presenca, name="editar_presenca"),
   path("excluir/<int:presenca_id>/", views.excluir_presenca, name="excluir_presenca"),
   path("detalhar/<int:presenca_id>/", views.detalhar_presenca, name="detalhar_presenca"),
   path("turma/<int:turma_id>/registrar/", views.registrar_presenca_turma, name="registrar_presenca_turma"),
   path("exportar/csv/", views.exportar_presencas_csv, name="exportar_presencas_csv"),
   path("relatorio/", views.relatorio_presencas, name="relatorio_presencas"),
   path("api/atividades-por-turma/<int:turma_id>/", views.api_atividades_por_turma, name="api_atividades_por_turma"),
   path("api/alunos-por-turma/<int:turma_id>/", views.api_alunos_por_turma, name="api_alunos_por_turma"),
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



## Arquivos de Template:


### Arquivo: presencas\templates\presencas\detalhar_presenca.html

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
    </div>

    <div class="mt-3">
        <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-warning">Editar</a>
        <a href="{% url 'presencas:excluir_presenca' presenca.id %}" class="btn btn-danger">Excluir</a>
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\editar_presenca.html

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




### Arquivo: presencas\templates\presencas\excluir_presenca.html

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




### Arquivo: presencas\templates\presencas\filtro_presencas.html

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



### Arquivo: presencas\templates\presencas\formulario_presenca.html

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



### Arquivo: presencas\templates\presencas\formulario_presencas_multiplas.html

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



### Arquivo: presencas\templates\presencas\formulario_presencas_multiplas_passo1.html

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



### Arquivo: presencas\templates\presencas\formulario_presencas_multiplas_passo2.html

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



### Arquivo: presencas\templates\presencas\listar_presencas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Presenças{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Presenças</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'presencas:registrar_presenca' %}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Registrar Presença
            </a>
            <a href="{% url 'presencas:registrar_presenca_em_massa' %}" class="btn btn-success">
                <i class="fas fa-users"></i> Registro em Massa
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
                                <div class="btn-group">
                                    <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-sm btn-warning">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <a href="{% url 'presencas:excluir_presenca' presenca.id %}" class="btn btn-sm btn-danger">
                                        <i class="fas fa-trash"></i>
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




### Arquivo: presencas\templates\presencas\registrar_presenca.html

html
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




### Arquivo: presencas\templates\presencas\registrar_presenca_em_massa.html

html
{% extends 'base.html' %}

{% block title %}Registrar Presença em Massa{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registrar Presença em Massa</h1>
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Selecione a Turma e a Data</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <label for="turma" class="form-label">Turma</label>
                        <select name="turma" id="turma" class="form-select" required>
                            <option value="">Selecione uma turma</option>
                            {% for turma in turmas %}
                                <option value="{{ turma.id }}">{{ turma.nome }} - {{ turma.curso.nome }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="col-md-6">
                        <label for="data" class="form-label">Data</label>
                        <input type="date" name="data" id="data" class="form-control" 
                               value="{{ data_hoje|date:'Y-m-d' }}" required>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="atividade" class="form-label">Atividade</label>
                    <select name="atividade" id="atividade" class="form-select" required>
                        <option value="">Selecione uma atividade</option>
                        <!-- As atividades serão carregadas via JavaScript quando uma turma for selecionada -->
                    </select>
                </div>
                
                <div id="lista-alunos" class="mt-4" style="display: none;">
                    <h5>Lista de Alunos</h5>
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="marcar-todos" checked>
                        <label class="form-check-label" for="marcar-todos">Marcar/Desmarcar Todos</label>
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th style="width: 50px;">#</th>
                                    <th>Aluno</th>
                                    <th style="width: 120px;">Presente</th>
                                    <th>Justificativa (se ausente)</th>
                                </tr>
                            </thead>
                            <tbody id="tbody-alunos">
                                <!-- Os alunos serão carregados via JavaScript -->
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div class="d-flex justify-content-between mt-4">
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary" id="btn-registrar" disabled>
                        <i class="fas fa-save"></i> Registrar Presenças
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
        const turmaSelect = document.getElementById('turma');
        const atividadeSelect = document.getElementById('atividade');
        const listaAlunos = document.getElementById('lista-alunos');
        const tbodyAlunos = document.getElementById('tbody-alunos');
        const btnRegistrar = document.getElementById('btn-registrar');
        const marcarTodosCheckbox = document.getElementById('marcar-todos');
        
        // Carregar atividades quando uma turma for selecionada
        turmaSelect.addEventListener('change', function() {
            const turmaId = this.value;
            
            if (!turmaId) {
                atividadeSelect.innerHTML = '<option value="">Selecione uma atividade</option>';
                listaAlunos.style.display = 'none';
                btnRegistrar.disabled = true;
                return;
            }
            
            // Fazer requisição AJAX para buscar atividades da turma
            fetch(`/api/atividades-por-turma/${turmaId}/`)
                .then(response => response.json())
                .then(data => {
                    atividadeSelect.innerHTML = '<option value="">Selecione uma atividade</option>';
                    
                    if (data.atividades && data.atividades.length > 0) {
                        data.atividades.forEach(atividade => {
                            const option = document.createElement('option');
                            option.value = atividade.id;
                            option.textContent = atividade.nome;
                            atividadeSelect.appendChild(option);
                        });
                    } else {
                        const option = document.createElement('option');
                        option.value = "";
                        option.textContent = "Nenhuma atividade encontrada para esta turma";
                        option.disabled = true;
                        atividadeSelect.appendChild(option);
                    }
                })
                .catch(error => console.error('Erro ao buscar atividades:', error));
        });
        
        // Carregar alunos quando uma atividade for selecionada
        atividadeSelect.addEventListener('change', function() {
            const atividadeId = this.value;
            const turmaId = turmaSelect.value;
            
            if (!atividadeId || !turmaId) {
                listaAlunos.style.display = 'none';
                btnRegistrar.disabled = true;
                return;
            }
            
            // Fazer requisição AJAX para buscar alunos da turma
            fetch(`/api/alunos-por-turma/${turmaId}/`)
                .then(response => response.json())
                .then(data => {
                    tbodyAlunos.innerHTML = '';
                    
                    if (data.alunos && data.alunos.length > 0) {
                        data.alunos.forEach((aluno, index) => {
                            const tr = document.createElement('tr');
                            
                            tr.innerHTML = `
                                <td>${index + 1}</td>
                                <td>
                                    <div class="d-flex align-items-center">
                                        ${aluno.foto ? 
                                            `<img src="${aluno.foto}" alt="${aluno.nome}" 
                                                 class="rounded-circle me-2" width="40" height="40" 
                                                 style="object-fit: cover;">` : 
                                            `<div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                 style="width: 40px; height: 40px; color: white;">
                                                ${aluno.nome.charAt(0).toUpperCase()}
                                            </div>`
                                        }
                                        <div>
                                            <div>${aluno.nome}</div>
                                            <small class="text-muted">${aluno.cpf}</small>
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <div class="form-check">
                                        <input class="form-check-input presenca-checkbox" type="checkbox" 
                                               name="presentes" value="${aluno.cpf}" id="presente_${aluno.cpf}" checked>
                                        <label class="form-check-label" for="presente_${aluno.cpf}">
                                            Presente
                                        </label>
                                    </div>
                                </td>
                                <td>
                                    <textarea class="form-control justificativa-field" 
                                              name="justificativa_${aluno.cpf}" rows="1" 
                                              placeholder="Justificativa para ausência" disabled></textarea>
                                </td>
                            `;
                            
                            tbodyAlunos.appendChild(tr);
                        });
                        
                        // Adicionar eventos para os checkboxes de presença
                        const checkboxes = document.querySelectorAll('.presenca-checkbox');
                        checkboxes.forEach(function(checkbox) {
                            checkbox.addEventListener('change', function() {
                                const row = this.closest('tr');
                                const justificativa = row.querySelector('.justificativa-field');
                                
                                if (this.checked) {
                                    justificativa.disabled = true;
                                    justificativa.value = '';
                                } else {
                                    justificativa.disabled = false;
                                }
                            });
                        });
                        
                        // Marcar/Desmarcar todos
                        marcarTodosCheckbox.addEventListener('change', function() {
                            checkboxes.forEach(function(checkbox) {
                                checkbox.checked = marcarTodosCheckbox.checked;
                                const row = checkbox.closest('tr');
                                const justificativa = row.querySelector('.justificativa-field');
                                
                                if (checkbox.checked) {
                                    justificativa.disabled = true;
                                    justificativa.value = '';
                                } else {
                                    justificativa.disabled = false;
                                }
                            });
                        });
                        
                        listaAlunos.style.display = 'block';
                        btnRegistrar.disabled = false;
                    } else {
                        tbodyAlunos.innerHTML = `
                            <tr>
                                <td colspan="4" class="text-center py-3">
                                    <p class="mb-0">Nenhum aluno encontrado para esta turma.</p>
                                </td>
                            </tr>
                        `;
                        
                        listaAlunos.style.display = 'block';
                        btnRegistrar.disabled = true;
                    }
                })
                .catch(error => console.error('Erro ao buscar alunos:', error));
        });
    });
</script>
{% endblock %}


'''