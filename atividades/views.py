from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
import importlib

# Importação dinâmica dos modelos
from .models import AtividadeAcademica, AtividadeRitualistica
from .forms import criar_form_atividade_academica, criar_form_atividade_ritualistica

# Views para Atividades Acadêmicas
def listar_atividades_academicas(request):
    """Exibe a lista de atividades acadêmicas com filtros e paginação"""
    # Importação dinâmica
    turmas_module = importlib.import_module('turmas.models')
    Turma = getattr(turmas_module, 'Turma')
    
    # Obter todas as atividades
    atividades = AtividadeAcademica.objects.all()
    
    # Busca por nome
    search_query = request.GET.get('search', '')
    if search_query:
        atividades = atividades.filter(nome__icontains=search_query)
    
    # Filtro por turma
    turma_id = request.GET.get('turma', '')
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    
    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    order_dir = request.GET.get('order_dir', 'asc')
    
    if order_dir == 'desc':
        order_by = f'-{order_by}'
        
    atividades = atividades.order_by(order_by)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Contexto para o template
    context = {
        'atividades': page_obj,
        'search_query': search_query,
        'turmas': Turma.objects.all(),
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    
    return render(request, 'atividades/academica_lista.html', context)

def criar_atividade_academica(request):
    """Cria uma nova atividade acadêmica"""
    AtividadeAcademicaForm = criar_form_atividade_academica()
   
    if request.method == 'POST':
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            try:
                atividade = form.save()
                messages.success(request, 'Atividade acadêmica criada com sucesso!')
                return redirect('atividades:academica_lista')
            except Exception as e:
                messages.error(request, f'Erro ao criar atividade: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Erro no campo {field}: {error}')
    else:
        form = AtividadeAcademicaForm()
   
    return render(request, 'atividades/academica_formulario.html', {'form': form})

def editar_atividade_academica(request, pk):
    """Edita uma atividade acadêmica existente"""
    AtividadeAcademicaForm = criar_form_atividade_academica()
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    if request.method == 'POST':
        form = AtividadeAcademicaForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade acadêmica atualizada com sucesso!')
            return redirect('atividades:academica_lista')
    else:
        form = AtividadeAcademicaForm(instance=atividade)
    
    return render(request, 'atividades/academica_formulario.html', {'form': form})

def excluir_atividade_academica(request, pk):
    """Exclui uma atividade acadêmica"""
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade acadêmica excluída com sucesso!')
        return redirect('atividades:academica_lista')
    
    return render(request, 'atividades/academica_confirmar_exclusao.html', {'object': atividade})

# Views para Atividades Ritualísticas
def listar_atividades_ritualisticas(request):
    """Exibe a lista de atividades ritualísticas com filtros e paginação"""
    # Importação dinâmica
    turmas_module = importlib.import_module('turmas.models')
    Turma = getattr(turmas_module, 'Turma')
    
    # Obter todas as atividades
    atividades = AtividadeRitualistica.objects.all()
    
    # Busca por nome
    search_query = request.GET.get('search', '')
    if search_query:
        atividades = atividades.filter(nome__icontains=search_query)
    
    # Filtro por turma
    turma_id = request.GET.get('turma', '')
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    
    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    order_dir = request.GET.get('order_dir', 'asc')
    
    if order_dir == 'desc':
        order_by = f'-{order_by}'
        
    atividades = atividades.order_by(order_by)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Contexto para o template
    context = {
        'atividades_ritualisticas': page_obj,
        'search_query': search_query,
        'turmas': Turma.objects.all(),
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    
    return render(request, 'atividades/ritualistica_lista.html', context)

def criar_atividade_ritualistica(request):
    """Cria uma nova atividade ritualística"""
    AtividadeRitualisticaForm = criar_form_atividade_ritualistica()
    
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            
            # Tratar a opção de incluir todos os alunos
            if form.cleaned_data.get('todos_alunos'):
                turma = form.cleaned_data.get('turma')
                if turma:
                    # Importação dinâmica usando importlib
                    alunos_module = importlib.import_module('alunos.models')
                    Aluno = getattr(alunos_module, 'Aluno')
                    
                    # Adicionar todos os alunos da turma
                    alunos = Aluno.objects.filter(turmas=turma)
                    instance.alunos.set(alunos)
            else:
                # Salvar os alunos selecionados no formulário
                form.save_m2m()
            
            messages.success(request, 'Atividade ritualística criada com sucesso!')
            return redirect('atividades:ritualistica_lista')
    else:
        form = AtividadeRitualisticaForm()
    
    return render(request, 'atividades/atividade_ritualistica_form.html', {'form': form})

def editar_atividade_ritualistica(request, pk):
    """Edita uma atividade ritualística existente"""
    AtividadeRitualisticaForm = criar_form_atividade_ritualistica()
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST, instance=atividade)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            
            # Tratar a opção de incluir todos os alunos
            if form.cleaned_data.get('todos_alunos'):
                turma = form.cleaned_data.get('turma')
                if turma:
                    # Importação dinâmica usando importlib
                    alunos_module = importlib.import_module('alunos.models')
                    Aluno = getattr(alunos_module, 'Aluno')
                    
                    # Adicionar todos os alunos da turma
                    alunos = Aluno.objects.filter(turmas=turma)
                    instance.alunos.set(alunos)
            else:
                # Salvar os alunos selecionados no formulário
                form.save_m2m()
            
            messages.success(request, 'Atividade ritualística atualizada com sucesso!')
            return redirect('atividades:ritualistica_lista')
    else:
        form = AtividadeRitualisticaForm(instance=atividade)
    
    return render(request, 'atividades/atividade_ritualistica_form.html', {'form': form})

def excluir_atividade_ritualistica(request, pk):
    """Exclui uma atividade ritualística"""
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade ritualística excluída com sucesso!')
        return redirect('atividades:ritualistica_lista')
    
    return render(request, 'atividades/ritualistica_confirmar_exclusao.html', {'object': atividade})
