# Revisão da Funcionalidade: presencas

## Arquivos forms.py:


### Arquivo: presencas\forms.py

python
from django import forms
from django.utils import timezone
from importlib import import_module

def get_models():
    """Obtém o modelo Presenca."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

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
    """Formulário para registro de presença."""
    
    class Meta:
        model = get_models()
        fields = ['aluno', 'atividade', 'data', 'situacao', 'justificativa']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'justificativa': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar campos
        self.fields['aluno'].queryset = get_aluno_model().objects.filter(situacao='ATIVO')
        self.fields['aluno'].widget.attrs.update({'class': 'form-control select2'})
        
        self.fields['atividade'].queryset = get_atividade_model().objects.all().order_by('-data_inicio')
        self.fields['atividade'].widget.attrs.update({'class': 'form-control select2'})
        
        self.fields['situacao'].widget.attrs.update({'class': 'form-control'})
        
        # Definir data padrão como hoje
        if not self.instance.pk:
            self.fields['data'].initial = timezone.now().date()
    
    def clean(self):
        cleaned_data = super().clean()
        situacao = cleaned_data.get('situacao')
        justificativa = cleaned_data.get('justificativa')
        
        # Validar justificativa quando a situação for JUSTIFICADO
        if situacao == 'JUSTIFICADO' and not justificativa:
            self.add_error('justificativa', 'A justificativa é obrigatória quando a situação é "Justificado".')
        
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
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
import csv
import logging
from importlib import import_module
from datetime import datetime

logger = logging.getLogger(__name__)

def get_models():
    """Obtém o modelo Presenca."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

def get_forms():
    """Obtém os formulários relacionados a presenças."""
    presencas_forms = import_module("presencas.forms")
    return (
        getattr(presencas_forms, "PresencaForm"),
        getattr(presencas_forms, "PresencaMultiplaForm"),
        getattr(presencas_forms, "FiltroPresencaForm")
    )

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

@login_required
def listar_presencas(request):
    """Lista todas as presenças com filtros."""
    try:
        Presenca = get_models()
        _, _, FiltroPresencaForm = get_forms()
        
        # Inicializar formulário de filtro
        filtro_form = FiltroPresencaForm(request.GET)
        
        # Aplicar filtros
        presencas = Presenca.objects.all().select_related('aluno', 'atividade')
        
        if filtro_form.is_valid():
            # Filtrar por aluno
            aluno = filtro_form.cleaned_data.get('aluno')
            if aluno:
                presencas = presencas.filter(aluno=aluno)
            
            # Filtrar por atividade
            atividade = filtro_form.cleaned_data.get('atividade')
            if atividade:
                presencas = presencas.filter(atividade=atividade)
            
            # Filtrar por data
            data_inicio = filtro_form.cleaned_data.get('data_inicio')
            if data_inicio:
                presencas = presencas.filter(data__gte=data_inicio)
            
            data_fim = filtro_form.cleaned_data.get('data_fim')
            if data_fim:
                presencas = presencas.filter(data__lte=data_fim)
            
            # Filtrar por situação
            situacao = filtro_form.cleaned_data.get('situacao')
            if situacao:
                presencas = presencas.filter(situacao=situacao)
        
        # Ordenar
        presencas = presencas.order_by('-data', 'aluno__nome')
        
        # Paginação
        paginator = Paginator(presencas, 20)  # 20 itens por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'presencas': page_obj,
            'page_obj': page_obj,
            'filtro_form': filtro_form
        }
        
        return render(request, 'presencas/listar_presencas.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao listar presenças: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao listar presenças: {str(e)}")
        return redirect('home')

@login_required
def registrar_presenca(request):
    """Registra uma nova presença."""
    try:
        PresencaForm, _, _ = get_forms()
        
        if request.method == 'POST':
            form = PresencaForm(request.POST)
            if form.is_valid():
                presenca = form.save()
                messages.success(request, "Presença registrada com sucesso!")
                
                # Redirecionar para a lista ou para registrar outra presença
                if 'salvar_continuar' in request.POST:
                    return redirect('presencas:registrar_presenca')
                else:
                    return redirect('presencas:listar_presencas')
        else:
            # Pré-preencher com aluno e atividade se fornecidos na URL
            initial = {}
            
            aluno_id = request.GET.get('aluno')
            if aluno_id:
                initial['aluno'] = aluno_id
            
            atividade_id = request.GET.get('atividade')
            if atividade_id:
                initial['atividade'] = atividade_id
            
            form = PresencaForm(initial=initial)
        
        context = {
            'form': form,
            'titulo': 'Registrar Presença'
        }
        
        return render(request, 'presencas/formulario_presenca.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao registrar presença: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao registrar presença: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def editar_presenca(request, presenca_id):
    """Edita uma presença existente."""
    try:
        Presenca = get_models()
        PresencaForm, _, _ = get_forms()
        
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
            'presenca': presenca,
            'titulo': 'Editar Presença'
        }
        
        return render(request, 'presencas/formulario_presenca.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao editar presença: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar presença: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def excluir_presenca(request, presenca_id):
    """Exclui uma presença."""
    try:
        Presenca = get_models()
        presenca = get_object_or_404(Presenca, id=presenca_id)
        
        if request.method == 'POST':
            presenca.delete()
            messages.success(request, "Presença excluída com sucesso!")
            return redirect('presencas:listar_presencas')
        
        context = {
            'presenca': presenca
        }
        
        return render(request, 'presencas/excluir_presenca.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao excluir presença: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao excluir presença: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def registrar_presencas_multiplas(request):
    """Registra múltiplas presenças de uma vez."""
    try:
        _, PresencaMultiplaForm, _ = get_forms()
        
        if request.method == 'POST':
            form = PresencaMultiplaForm(request.POST)
            if form.is_valid():
                # Os dados serão processados via API JavaScript
                messages.success(request, "Formulário válido. Prossiga com o registro de presenças.")
                
                # Redirecionar para a página de seleção de alunos
                return redirect('presencas:selecionar_alunos_presencas', 
                               data=form.cleaned_data['data'].strftime('%Y-%m-%d'),
                               turmas=','.join(str(t.id) for t in form.cleaned_data['turmas']),
                               atividades=','.join(str(a.id) for a in form.cleaned_data['atividades']))
        else:
            form = PresencaMultiplaForm()
        
        # Obter turmas ativas
        Turma = get_turma_model()
        turmas = Turma.objects.filter(status='A')
        
        # Obter atividades
        Atividade = get_atividade_model()
        atividades = Atividade.objects.all()
        
        context = {
            'form': form,
            'turmas': turmas,
            'atividades': atividades
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas_passo1.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao registrar presenças múltiplas: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao registrar presenças múltiplas: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def selecionar_alunos_presencas(request, data, turmas, atividades):
    """Seleciona alunos para registro de presenças múltiplas."""
    try:
        # Converter parâmetros
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        turmas_ids = [int(id) for id in turmas.split(',')]
        atividades_ids = [int(id) for id in atividades.split(',')]
        
        # Obter turmas
        Turma = get_turma_model()
        turmas_objs = Turma.objects.filter(id__in=turmas_ids)
        
        # Obter atividades
        Atividade = get_atividade_model()
        atividades_objs = Atividade.objects.filter(id__in=atividades_ids)
        
        # Obter alunos matriculados nas turmas
        Matricula = import_module("matriculas.models").Matricula
        matriculas = Matricula.objects.filter(turma__in=turmas_objs, status='A').select_related('aluno')
        
        # Obter alunos únicos
        alunos = []
        alunos_ids = set()
        
        for matricula in matriculas:
            if matricula.aluno.cpf not in alunos_ids:
                alunos.append(matricula.aluno)
                alunos_ids.add(matricula.aluno.cpf)
        
        # Verificar presenças existentes
        Presenca = get_models()
        presencas_existentes = Presenca.objects.filter(
            aluno__in=alunos,
            atividade__in=atividades_objs,
            data=data_obj
        )
        
        # Criar dicionário de presenças existentes para fácil acesso
        presencas_dict = {}
        for presenca in presencas_existentes:
            key = f"{presenca.aluno.cpf}_{presenca.atividade.id}"
            presencas_dict[key] = presenca
        
        context = {
            'data': data,
            'data_formatada': data_obj.strftime('%d/%m/%Y'),
            'turmas': turmas_objs,
            'atividades': atividades_objs,
            'alunos': alunos,
            'presencas_dict': presencas_dict
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas_passo2.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao selecionar alunos para presenças: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao selecionar alunos: {str(e)}")
        return redirect('presencas:registrar_presencas_multiplas')

@login_required
def registrar_presencas_multiplas_form(request):
    """Formulário para registrar presenças múltiplas."""
    try:
        # Obter parâmetros da URL
        data_str = request.GET.get('data')
        turmas_ids = request.GET.get('turmas', '').split(',')
        atividades_ids = request.GET.get('atividades', '').split(',')
        
        if not data_str or not turmas_ids or not atividades_ids:
            messages.error(request, "Parâmetros inválidos. Por favor, tente novamente.")
            return redirect('presencas:registrar_presencas_multiplas')
        
        # Converter para data
        try:
            data = timezone.datetime.strptime(data_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de data inválido.")
            return redirect('presencas:registrar_presencas_multiplas')
        
        # Obter modelos
        Turma = get_turma_model()
        Atividade = get_atividade_model()
        
        # Obter turmas e atividades
        turmas = Turma.objects.filter(id__in=turmas_ids)
        atividades = Atividade.objects.filter(id__in=atividades_ids)
        
        if not turmas or not atividades:
            messages.error(request, "Turmas ou atividades não encontradas.")
            return redirect('presencas:registrar_presencas_multiplas')
        
        context = {
            'data': data,
            'turmas': turmas,
            'atividades': atividades,
        }
        
        return render(request, 'presencas/formulario_presencas_multiplas.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao exibir formulário múltiplo: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exibir formulário múltiplo: {str(e)}")
        return redirect('presencas:registrar_presencas_multiplas')

@login_required
def exportar_presencas_csv(request):
    """Exporta presenças para um arquivo CSV."""
    try:
        Presenca = get_models()
        _, _, FiltroPresencaForm = get_forms()
        
        # Aplicar filtros
        filtro_form = FiltroPresencaForm(request.GET)
        presencas = Presenca.objects.all().select_related('aluno', 'atividade')
        
        if filtro_form.is_valid():
            # Aplicar os mesmos filtros da listagem
            aluno = filtro_form.cleaned_data.get('aluno')
            if aluno:
                presencas = presencas.filter(aluno=aluno)
            
            atividade = filtro_form.cleaned_data.get('atividade')
            if atividade:
                presencas = presencas.filter(atividade=atividade)
            
            data_inicio = filtro_form.cleaned_data.get('data_inicio')
            if data_inicio:
                presencas = presencas.filter(data__gte=data_inicio)
            
            data_fim = filtro_form.cleaned_data.get('data_fim')
            if data_fim:
                presencas = presencas.filter(data__lte=data_fim)
            
            situacao = filtro_form.cleaned_data.get('situacao')
            if situacao:
                presencas = presencas.filter(situacao=situacao)
        
        # Ordenar
        presencas = presencas.order_by('-data', 'aluno__nome')
        
        # Criar resposta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="presencas.csv"'
        
        # Escrever cabeçalho e dados
        writer = csv.writer(response)
        writer.writerow(['CPF', 'Aluno', 'Atividade', 'Data', 'Situação', 'Justificativa'])
        
        for presenca in presencas:
            writer.writerow([
                presenca.aluno.cpf,
                presenca.aluno.nome,
                presenca.atividade.titulo,
                presenca.data.strftime('%d/%m/%Y'),
                dict(Presenca.SITUACAO_CHOICES).get(presenca.situacao, presenca.situacao),
                presenca.justificativa or ''
            ])
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao exportar presenças: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar presenças: {str(e)}")
        return redirect('presencas:listar_presencas')

@login_required
def detalhar_presenca(request, presenca_id):
    """
    Exibe os detalhes de um registro de presença.
    """
    Presenca = get_presenca_model()
    presenca = get_object_or_404(Presenca, id=presenca_id)
    
    return render(request, 'presencas/detalhar_presenca.html', {'presenca': presenca})

@login_required
def registrar_presenca_multipla(request):
    """
    Registra presenças para múltiplos alunos em múltiplas atividades.
    """
    RegistroPresencaMultiplaForm = get_registro_presenca_multipla_form()
    Presenca = get_presenca_model()
    Aluno = get_aluno_model()
    
    if request.method == 'POST':
        form = RegistroPresencaMultiplaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            atividades = form.cleaned_data['atividades']
            turmas = form.cleaned_data['turmas']
            
            # Obter alunos das turmas selecionadas
            alunos = Aluno.objects.filter(turmas__in=turmas).distinct()
            
            # Processar os dados de presença
            alunos_presentes = request.POST.getlist('alunos_presentes')
            justificativas = {}
            
            # Coletar justificativas
            for key, value in request.POST.items():
                if key.startswith('justificativa_'):
                    aluno_id = key.replace('justificativa_', '')
                    justificativas[aluno_id] = value
            
            # Registrar presenças
            with transaction.atomic():
                for atividade in atividades:
                    for aluno in alunos:
                        aluno_id_str = str(aluno.cpf)
                        
                        # Determinar situação
                        if aluno_id_str in alunos_presentes:
                            situacao = 'PRESENTE'
                            justificativa = None
                        else:
                            # Verificar se há justificativa
                            if aluno_id_str in justificativas and justificativas[aluno_id_str].strip():
                                situacao = 'JUSTIFICADO'
                                justificativa = justificativas[aluno_id_str]
                            else:
                                situacao = 'AUSENTE'
                                justificativa = None
                        
                        # Criar ou atualizar registro de presença
                        Presenca.objects.update_or_create(
                            aluno=aluno,
                            atividade=atividade,
                            data=data,
                            defaults={
                                'situacao': situacao,
                                'justificativa': justificativa,
                                'registrado_por': request.user,
                            }
                        )
            
            messages.success(request, "Presenças registradas com sucesso!")
            return redirect('presencas:listar_presencas')
        else:
            messages.error(request, "Erro ao registrar presenças. Verifique os dados informados.")
    else:
        form = RegistroPresencaMultiplaForm()
    
    return render(request, 'presencas/registrar_presenca_multipla.html', {'form': form})

@login_required
def obter_alunos_por_turmas(request):
    """
    API para obter alunos das turmas selecionadas.
    """
    if request.method == 'GET':
        turmas_ids = request.GET.getlist('turmas[]')
        data = request.GET.get('data')
        atividades_ids = request.GET.getlist('atividades[]')
        
        if not turmas_ids:
            return JsonResponse({'error': 'Nenhuma turma selecionada'}, status=400)
        
        # Obter alunos das turmas selecionadas
        Aluno = get_aluno_model()
        Turma = get_turma_model()
        Presenca = get_presenca_model()
        
        try:
            turmas = Turma.objects.filter(id__in=turmas_ids)
            alunos = Aluno.objects.filter(turmas__in=turmas).distinct()
            
            # Formatar dados dos alunos
            alunos_data = []
            for aluno in alunos:
                # Verificar se já existem registros de presença para este aluno nas atividades selecionadas
                situacoes = {}
                justificativas = {}
                
                if data and atividades_ids:
                    for atividade_id in atividades_ids:
                        try:
                            presenca = Presenca.objects.get(
                                aluno=aluno,
                                atividade_id=atividade_id,
                                data=data
                            )
                            situacoes[atividade_id] = presenca.situacao
                            justificativas[atividade_id] = presenca.justificativa or ''
                        except Presenca.DoesNotExist:
                            situacoes[atividade_id] = 'PRESENTE'  # Padrão
                            justificativas[atividade_id] = ''
                
                alunos_data.append({
                    'id': aluno.cpf,
                    'nome': aluno.nome,
                    'numero_iniciatico': aluno.numero_iniciatico or 'N/A',
                    'turmas': [t.nome for t in aluno.turmas.all()],
                    'situacoes': situacoes,
                    'justificativas': justificativas,
                })
            
            return JsonResponse({'alunos': alunos_data})
        except Exception as e:
            logger.error(f"Erro ao obter alunos por turmas: {str(e)}")
            return JsonResponse({'error': f"Erro ao obter alunos: {str(e)}"}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def obter_atividades_por_data(request):
    """
    API para obter atividades disponíveis para uma data específica.
    """
    if request.method == 'GET':
        data = request.GET.get('data')
        
        if not data:
            return JsonResponse({'error': 'Data não fornecida'}, status=400)
        
        try:
            data_obj = timezone.datetime.strptime(data, '%Y-%m-%d').date()
            
            # Obter atividades para a data
            Atividade = get_atividade_model()
            atividades = Atividade.objects.filter(data=data_obj)
            
            # Formatar dados das atividades
            atividades_data = []
            for atividade in atividades:
                atividades_data.append({
                    'id': atividade.id,
                    'titulo': atividade.titulo,
                    'tipo': atividade.get_tipo_display() if hasattr(atividade, 'get_tipo_display') else 'Não especificado',
                    'turmas': [t.nome for t in atividade.turmas.all()] if hasattr(atividade, 'turmas') else [],
                })
            
            return JsonResponse({'atividades': atividades_data})
        except Exception as e:
            logger.error(f"Erro ao obter atividades por data: {str(e)}")
            return JsonResponse({'error': f"Erro ao obter atividades: {str(e)}"}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)



## Arquivos urls.py:


### Arquivo: presencas\urls.py

python
from django.urls import path
from . import views
from . import api_views

app_name = 'presencas'

urlpatterns = [
   # Views principais
   path('', views.listar_presencas, name='listar_presencas'),
   path('registrar/', views.registrar_presenca, name='registrar_presenca'),
   path('editar/<int:presenca_id>/', views.editar_presenca, name='editar_presenca'),
   path('excluir/<int:presenca_id>/', views.excluir_presenca, name='excluir_presenca'),
   path('multiplas/', views.registrar_presencas_multiplas, name='registrar_presencas_multiplas'),
   path('multiplas/selecionar/<str:data>/<str:turmas>/<str:atividades>/', 
        views.selecionar_alunos_presencas, name='selecionar_alunos_presencas'),
   path('exportar/', views.exportar_presencas_csv, name='exportar_presencas_csv'),
   path('relatorio/', views.relatorio_presencas, name='relatorio_presencas'),
    
   # APIs
   path('api/obter-alunos-por-turmas/', api_views.obter_alunos_por_turmas, name='api_obter_alunos_por_turmas'),
   path('api/obter-atividades-por-data/', api_views.obter_atividades_por_data, name='api_obter_atividades_por_data'),
   path('api/salvar-presencas-multiplas/', api_views.salvar_presencas_multiplas, name='api_salvar_presencas_multiplas'),
]



## Arquivos models.py:


### Arquivo: presencas\models.py

python
from django.db import models
from django.utils import timezone
from importlib import import_module

def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_atividade_model():
    """Obtém o modelo Atividade."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "Atividade")

class Presenca(models.Model):
    """Modelo para registro de presença de alunos em atividades."""
    
    SITUACAO_CHOICES = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
        ('JUSTIFICADO', 'Justificado'),
    ]
    
    aluno = models.ForeignKey(
        get_aluno_model(),
        on_delete=models.CASCADE,
        verbose_name="Aluno"
    )
    
    atividade = models.ForeignKey(
        get_atividade_model(),
        on_delete=models.CASCADE,
        verbose_name="Atividade"
    )
    
    data = models.DateField(
        verbose_name="Data",
        default=timezone.now
    )
    
    situacao = models.CharField(
        max_length=15,
        choices=SITUACAO_CHOICES,
        default='PRESENTE',
        verbose_name="Situação"
    )
    
    justificativa = models.TextField(
        blank=True,
        null=True,
        verbose_name="Justificativa"
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
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        ordering = ['-data', 'aluno__nome']
        unique_together = ['aluno', 'atividade', 'data']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.atividade.titulo} - {self.data}"
    
    def save(self, *args, **kwargs):
        # Limpar justificativa se a situação não for JUSTIFICADO
        if self.situacao != 'JUSTIFICADO':
            self.justificativa = None
        
        super().save(*args, **kwargs)



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
    <!-- Cabeçalho com título e botões -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Presenças</h1>
        <div class="btn-group">
            <a href="{% url 'presencas:registrar_presenca' %}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Nova Presença
            </a>
            <a href="{% url 'presencas:registrar_presencas_multiplas' %}" class="btn btn-success">
                <i class="fas fa-list-check"></i> Presenças Múltiplas
            </a>
            <a href="{% url 'presencas:exportar_presencas_csv' %}" class="btn btn-info">
                <i class="fas fa-file-export"></i> Exportar CSV
            </a>
            <a href="{% url 'presencas:relatorio_presencas' %}" class="btn btn-warning">
                <i class="fas fa-chart-bar"></i> Relatório
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
                <div class="col-md-3">
                    {{ filtro_form.aluno.label_tag }}
                    {{ filtro_form.aluno }}
                </div>
                <div class="col-md-3">
                    {{ filtro_form.atividade.label_tag }}
                    {{ filtro_form.atividade }}
                </div>
                <div class="col-md-2">
                    {{ filtro_form.data_inicio.label_tag }}
                    {{ filtro_form.data_inicio }}
                </div>
                <div class="col-md-2">
                    {{ filtro_form.data_fim.label_tag }}
                    {{ filtro_form.data_fim }}
                </div>
                <div class="col-md-2">
                    {{ filtro_form.situacao.label_tag }}
                    {{ filtro_form.situacao }}
                </div>
                <div class="col-12 mt-3">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-filter"></i> Filtrar
                    </button>
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
                        <i class="fas fa-broom"></i> Limpar Filtros
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
                    <thead class="table-dark">
                        <tr>
                            <th>Aluno</th>
                            <th>Atividade</th>
                            <th>Data</th>
                            <th>Situação</th>
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
                                                 class="rounded-circle me-2" width="40" height="40">
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
                                <td>{{ presenca.atividade.titulo }}</td>
                                <td>{{ presenca.data|date:"d/m/Y" }}</td>
                                <td>
                                    {% if presenca.situacao == 'PRESENTE' %}
                                        <span class="badge bg-success">Presente</span>
                                    {% elif presenca.situacao == 'AUSENTE' %}
                                        <span class="badge bg-danger">Ausente</span>
                                    {% elif presenca.situacao == 'JUSTIFICADO' %}
                                        <span class="badge bg-warning">Justificado</span>
                                        <div class="small text-muted mt-1">{{ presenca.justificativa|truncatechars:30 }}</div>
                                    {% endif %}
                                </td>
                                <td>
                                    <div class="btn-group">
                                        <a href="{% url 'presencas:editar_presenca' presenca.id %}" 
                                           class="btn btn-sm btn-warning" title="Editar">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                        <a href="{% url 'presencas:excluir_presenca' presenca.id %}" 
                                           class="btn btn-sm btn-danger" title="Excluir">
                                            <i class="fas fa-trash"></i>
                                        </a>
                                    </div>
                                </td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="5" class="text-center py-4">
                                    <div class="alert alert-info mb-0">
                                        Nenhuma presença encontrada com os filtros selecionados.
                                    </div>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <!-- Paginação -->
            {% if page_obj.has_other_pages %}
            <nav aria-label="Paginação" class="mt-4">
                <ul class="pagination justify-content-center">
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                            <i class="fas fa-angle-double-left"></i>
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                            <i class="fas fa-angle-left"></i>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link"><i class="fas fa-angle-double-left"></i></span>
                    </li>
                    <li class="page-item disabled">
                        <span class="page-link"><i class="fas fa-angle-left"></i></span>
                    </li>
                    {% endif %}
                    
                    {% for num in page_obj.paginator.page_range %}
                        {% if page_obj.number == num %}
                        <li class="page-item active">
                            <span class="page-link">{{ num }}</span>
                        </li>
                        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ num }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                                {{ num }}
                            </a>
                        </li>
                        {% endif %}
                    {% endfor %}
                    
                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                            <i class="fas fa-angle-right"></i>
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% for key, value in request.GET.items %}{% if key != 'page' %}&{{ key }}={{ value }}{% endif %}{% endfor %}">
                            <i class="fas fa-angle-double-right"></i>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link"><i class="fas fa-angle-right"></i></span>
                    </li>
                    <li class="page-item disabled">
                        <span class="page-link"><i class="fas fa-angle-double-right"></i></span>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>
        <div class="card-footer">
            <div class="d-flex justify-content-between align-items-center">
                <span>Total: {{ page_obj.paginator.count }} presenças</span>
                <span>Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
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




### Arquivo: presencas\templates\presencas\registrar_presenca_multipla.html

html
{% extends 'base.html' %}

{% block title %}Registro Múltiplo de Presenças{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Registro Múltiplo de Presenças</h1>
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <div class="card">
        <div class="card-header">
            <h5>Selecione os parâmetros</h5>
        </div>
        <div class="card-body">
            <form method="post" id="form-parametros">
                {% csrf_token %}
                
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="{{ form.data.id_for_label }}" class="form-label">{{ form.data.label }}</label>
                        {{ form.data }}
                        {% if form.data.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.data.errors }}
                            </div>
                        {% endif %}
                        {% if form.data.help_text %}
                            <div class="form-text">{{ form.data.help_text }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-8">
                        <label for="{{ form.turmas.id_for_label }}" class="form-label">{{ form.turmas.label }}</label>
                        {{ form.turmas }}
                        {% if form.turmas.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.turmas.errors }}
                            </div>
                        {% endif %}
                        {% if form.turmas.help_text %}
                            <div class="form-text">{{ form.turmas.help_text }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-12">
                        <label for="{{ form.atividades.id_for_label }}" class="form-label">{{ form.atividades.label }}</label>
                        {{ form.atividades }}
                        {% if form.atividades.errors %}
                            <div class="invalid-feedback d-block">
                                {{ form.atividades.errors }}
                            </div>
                        {% endif %}
                        {% if form.atividades.help_text %}
                            <div class="form-text">{{ form.atividades.help_text }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-arrow-right"></i> Próximo
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
        // Inicializar select2 para os campos de seleção múltipla
        if (typeof $.fn.select2 !== 'undefined') {
            $('#id_turmas').select2({
                placeholder: 'Selecione uma ou mais turmas',
                allowClear: true
            });
            
            $('#id_atividades').select2({
                placeholder: 'Selecione uma ou mais atividades',
                allowClear: true
            });
        }
        
        // Carregar atividades disponíveis quando a data mudar
        const dataInput = document.getElementById('id_data');
        const atividadesSelect = document.getElementById('id_atividades');
        
        if (dataInput && atividadesSelect) {
            dataInput.addEventListener('change', function() {
                const data = this.value;
                if (!data) return;
                
                // Limpar atividades atuais
                $(atividadesSelect).empty();
                
                // Carregar atividades para a data selecionada
                fetch(`{% url 'presencas:api_obter_atividades_por_data' %}?data=${data}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            console.error(data.error);
                            return;
                        }
                        
                        // Adicionar atividades ao select
                        data.atividades.forEach(atividade => {
                            const option = new Option(atividade.titulo, atividade.id);
                            $(atividadesSelect).append(option);
                        });
                        
                        // Atualizar select2
                        $(atividadesSelect).trigger('change');
                    })
                    .catch(error => console.error('Erro ao carregar atividades:', error));
            });
        }
    });
</script>
{% endblock %}



### Arquivo: presencas\templates\presencas\relatorio_presencas.html

html
{% extends 'base.html' %}

{% block title %}Relatório de Presenças{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Relatório de Presenças</h1>
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
    </div>
    
    <!-- Resumo em cards -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <h5 class="card-title">Total de Presenças</h5>
                    <p class="card-text display-4">{{ total_presencas }}</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5 class="card-title">Presentes</h5>
                    <p class="card-text display-4">{{ total_presentes }}</p>
                    <p class="card-text">{{ percentual_presentes|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-danger text-white">
                <div class="card-body">
                    <h5 class="card-title">Ausentes</h5>
                    <p class="card-text display-4">{{ total_ausentes }}</p>
                    <p class="card-text">{{ percentual_ausentes|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-dark">
                <div class="card-body">
                    <h5 class="card-title">Justificados</h5>
                    <p class="card-text display-4">{{ total_justificados }}</p>
                    <p class="card-text">{{ percentual_justificados|floatformat:1 }}%</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Gráficos -->
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Distribuição de Presenças</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-distribuicao"></canvas>
                </div>
            </div>
        </div>
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Presenças por Mês</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-mensal"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-12 mb-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Presenças por Atividade</h5>
                </div>
                <div class="card-body">
                    <canvas id="grafico-atividades"></canvas>
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
        // Gráfico de distribuição (pizza)
        const ctxDistribuicao = document.getElementById('grafico-distribuicao').getContext('2d');
        new Chart(ctxDistribuicao, {
            type: 'pie',
            data: {
                labels: ['Presentes', 'Ausentes', 'Justificados'],
                datasets: [{
                    data: [{{ total_presentes }}, {{ total_ausentes }}, {{ total_justificados }}],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.7)',  // Verde
                        'rgba(220, 53, 69, 0.7)',  // Vermelho
                        'rgba(255, 193, 7, 0.7)'   // Amarelo
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(220, 53, 69, 1)',
                        'rgba(255, 193, 7, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        
        // Gráfico mensal (linha)
        const ctxMensal = document.getElementById('grafico-mensal').getContext('2d');
        new Chart(ctxMensal, {
            type: 'line',
            data: {
                labels: {{ meses|safe }},
                datasets: [
                    {
                        label: 'Presentes',
                        data: {{ presentes_por_mes|safe }},
                        borderColor: 'rgba(40, 167, 69, 1)',
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        fill: true
                    },
                    {
                        label: 'Ausentes',
                        data: {{ ausentes_por_mes|safe }},
                        borderColor: 'rgba(220, 53, 69, 1)',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        fill: true
                    },
                    {
                        label: 'Justificados',
                        data: {{ justificados_por_mes|safe }},
                        borderColor: 'rgba(255, 193, 7, 1)',
                        backgroundColor: 'rgba(255, 193, 7, 0.1)',
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        // Gráfico por atividade (barra)
        const ctxAtividades = document.getElementById('grafico-atividades').getContext('2d');
        new Chart(ctxAtividades, {
            type: 'bar',
            data: {
                labels: {{ atividades_labels|safe }},
                datasets: [
                    {
                        label: 'Presentes',
                        data: {{ presentes_por_atividade|safe }},
                        backgroundColor: 'rgba(40, 167, 69, 0.7)'
                    },
                    {
                        label: 'Ausentes',
                        data: {{ ausentes_por_atividade|safe }},
                        backgroundColor: 'rgba(220, 53, 69, 0.7)'
                    },
                    {
                        label: 'Justificados',
                        data: {{ justificados_por_atividade|safe }},
                        backgroundColor: 'rgba(255, 193, 7, 0.7)'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    x: {
                        stacked: false
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
</script>
{% endblock %}

