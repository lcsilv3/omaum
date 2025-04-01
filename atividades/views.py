import importlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Função para obter modelos usando importlib
def get_models():
    AtividadeAcademica = importlib.import_module('atividades.models').AtividadeAcademica
    AtividadeRitualistica = importlib.import_module('atividades.models').AtividadeRitualistica
    return AtividadeAcademica, AtividadeRitualistica

# Função para obter formulários usando importlib
def get_forms():
    AtividadeAcademicaForm = importlib.import_module('atividades.forms').AtividadeAcademicaForm
    AtividadeRitualisticaForm = importlib.import_module('atividades.forms').AtividadeRitualisticaForm
    AtividadeBuscaForm = importlib.import_module('atividades.forms').AtividadeBuscaForm
    return AtividadeAcademicaForm, AtividadeRitualisticaForm, AtividadeBuscaForm

@login_required
def listar_atividades_academicas(request):
    """Lista todas as atividades acadêmicas com opções de filtragem."""
    AtividadeAcademica, _ = get_models()
    _, _, AtividadeBuscaForm = get_forms()
    
    form_busca = AtividadeBuscaForm(request.GET)
    atividades = AtividadeAcademica.objects.all()
    
    # Aplicar filtros se o formulário for válido
    if form_busca.is_valid():
        termo = form_busca.cleaned_data.get('termo')
        data_inicio = form_busca.cleaned_data.get('data_inicio')
        data_fim = form_busca.cleaned_data.get('data_fim')
        
        if termo:
            atividades = atividades.filter(
                Q(nome__icontains=termo) | 
                Q(descricao__icontains=termo)
            )
        
        if data_inicio:
            atividades = atividades.filter(data_inicio__gte=data_inicio)
        
        if data_fim:
            atividades = atividades.filter(data_fim__lte=data_fim)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 atividades por página
    page = request.GET.get('page')
    
    try:
        atividades_paginadas = paginator.page(page)
    except PageNotAnInteger:
        atividades_paginadas = paginator.page(1)
    except EmptyPage:
        atividades_paginadas = paginator.page(paginator.num_pages)
    
    context = {
        'atividades': atividades_paginadas,
        'form_busca': form_busca,
        'total_atividades': atividades.count(),
    }
    
    return render(request, 'atividades/listar_atividades_academicas.html', context)

@login_required
def criar_atividade_academica(request):
    """Cria uma nova atividade acadêmica."""
    AtividadeAcademicaForm, _, _ = get_forms()
    
    if request.method == 'POST':
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            atividade = form.save()
            messages.success(request, 'Atividade acadêmica criada com sucesso!')
            return redirect('atividades:detalhar_atividade_academica', pk=atividade.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AtividadeAcademicaForm()
    
    return render(request, 'atividades/criar_atividade_academica.html', {'form': form})

@login_required
def detalhar_atividade_academica(request, pk):
    """Exibe os detalhes de uma atividade acadêmica."""
    AtividadeAcademica, _ = get_models()
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return render(request, 'atividades/detalhar_atividade_academica.html', {'atividade': atividade})

@login_required
def editar_atividade_academica(request, pk):
    """Edita uma atividade acadêmica existente."""
    AtividadeAcademica, _ = get_models()
    AtividadeAcademicaForm, _, _ = get_forms()
    
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    if request.method == 'POST':
        form = AtividadeAcademicaForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade acadêmica atualizada com sucesso!')
            return redirect('atividades:detalhar_atividade_academica', pk=atividade.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AtividadeAcademicaForm(instance=atividade)
    
    return render(request, 'atividades/editar_atividade_academica.html', {'form': form, 'atividade': atividade})

@login_required
def excluir_atividade_academica(request, pk):
    """Exclui uma atividade acadêmica."""
    AtividadeAcademica, _ = get_models()
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade acadêmica excluída com sucesso!')
        return redirect('atividades:listar_atividades_academicas')
    
    return render(request, 'atividades/excluir_atividade_academica.html', {'atividade': atividade})

@login_required
def listar_atividades_ritualisticas(request):
    """Lista todas as atividades ritualísticas com opções de filtragem."""
    _, AtividadeRitualistica = get_models()
    _, _, AtividadeBuscaForm = get_forms()
    
    form_busca = AtividadeBuscaForm(request.GET)
    atividades = AtividadeRitualistica.objects.all()
    
    # Aplicar filtros se o formulário for válido
    if form_busca.is_valid():
        termo = form_busca.cleaned_data.get('termo')
        data_inicio = form_busca.cleaned_data.get('data_inicio')
        data_fim = form_busca.cleaned_data.get('data_fim')
        
        if termo:
            atividades = atividades.filter(
                Q(nome__icontains=termo) | 
                Q(descricao__icontains=termo)
            )
        
        if data_inicio:
            atividades = atividades.filter(data_inicio__gte=data_inicio)
        
        if data_fim:
            atividades = atividades.filter(data_fim__lte=data_fim)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 atividades por página
    page = request.GET.get('page')
    
    try:
        atividades_paginadas = paginator.page(page)
    except PageNotAnInteger:
        atividades_paginadas = paginator.page(1)
    except EmptyPage:
        atividades_paginadas = paginator.page(paginator.num_pages)
    
    context = {
        'atividades': atividades_paginadas,
        'form_busca': form_busca,
        'total_atividades': atividades.count(),
    }
    
    return render(request, 'atividades/listar_atividades_ritualisticas.html', context)

@login_required
def criar_atividade_ritualistica(request):
    """Cria uma nova atividade ritualística."""
    _, AtividadeRitualisticaForm, _ = get_forms()
    
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST)
        if form.is_valid():
            atividade = form.save()
            messages.success(request, 'Atividade ritualística criada com sucesso!')
            return redirect('atividades:detalhar_atividade_ritualistica', pk=atividade.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AtividadeRitualisticaForm()
    
    return render(request, 'atividades/criar_atividade_ritualistica.html', {'form': form})

@login_required
def detalhar_atividade_ritualistica(request, pk):
    """Exibe os detalhes de uma atividade ritualística."""
    _, AtividadeRitualistica = get_models()
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return render(request, 'atividades/detalhar_atividade_ritualistica.html', {'atividade': atividade})

@login_required
def editar_atividade_ritualistica(request, pk):
    """Edita uma atividade ritualística existente."""
    _, AtividadeRitualistica = get_models()
    _, AtividadeRitualisticaForm, _ = get_forms()
    
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade ritualística atualizada com sucesso!')
            return redirect('atividades:detalhar_atividade_ritualistica', pk=atividade.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AtividadeRitualisticaForm(instance=atividade)
    
    return render(request, 'atividades/editar_atividade_ritualistica.html', {'form': form, 'atividade': atividade})

@login_required
def excluir_atividade_ritualistica(request, pk):
    """Exclui uma atividade ritualística."""
    _, AtividadeRitualistica = get_models()
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade ritualística excluída com sucesso!')
        return redirect('atividades:listar_atividades_ritualisticas')
    
    return render(request, 'atividades/excluir_atividade_ritualistica.html', {'atividade': atividade})
