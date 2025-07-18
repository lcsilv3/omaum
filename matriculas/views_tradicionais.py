"""
Views tradicionais para o aplicativo de Matrículas.
Seguindo o padrã@login_required
def criar_matricula(request):
    """Cria uma nova matrícula."""
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            try:
                matricula = form.save()
                messages.success(request, 'Matrícula criada com sucesso!')
                return redirect('matriculas:detalhar_matricula', matricula_id=matricula.id)
            except Exception as e:
                messages.error(request, f'Erro ao criar matrícula: {str(e)}')
        else:
            messages.error(request, 'Erro ao criar matrícula. Verifique os dados.')
    else:
        form = MatriculaForm()
    
    context = {
        'form': form,
        'titulo': 'Nova Matrícula',
    }
    
    return render(request, 'matriculas/realizar_matricula.html', context) contrato.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from importlib import import_module
from .models import Matricula
from .forms import MatriculaForm


def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


@login_required
def listar_matriculas(request):
    """Lista todas as matrículas com filtros."""
    matriculas = Matricula.objects.select_related('aluno', 'turma').all()
    
    # Filtros
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    turma_filter = request.GET.get('turma', '')
    
    if search:
        matriculas = matriculas.filter(
            Q(aluno__nome__icontains=search) |
            Q(turma__nome__icontains=search)
        )
    
    if status_filter:
        matriculas = matriculas.filter(status=status_filter)
    
    if turma_filter:
        matriculas = matriculas.filter(turma_id=turma_filter)
    
    # Ordenação
    matriculas = matriculas.order_by('-data_matricula')
    
    # Paginação
    paginator = Paginator(matriculas, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para os filtros
    Turma = get_turma_model()
    turmas = Turma.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'turma_filter': turma_filter,
        'turmas': turmas,
        'status_choices': Matricula.OPCOES_STATUS,
    }
    
    return render(request, 'matriculas/listar_matriculas.html', context)


@login_required
def criar_matricula(request):
    """Cria uma nova matrícula."""
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save()
            messages.success(request, 'Matrícula criada com sucesso!')
            return redirect('matriculas:detalhar_matricula', matricula_id=matricula.id)
        else:
            messages.error(request, 'Erro ao criar matrícula. Verifique os dados.')
    else:
        form = MatriculaForm()
    
    context = {
        'form': form,
        'titulo': 'Nova Matrícula',
    }
    
    return render(request, 'matriculas/realizar_matricula.html', context)


@login_required
def detalhar_matricula(request, matricula_id):
    """Exibe detalhes de uma matrícula."""
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    context = {
        'matricula': matricula,
    }
    
    return render(request, 'matriculas/detalhar_matricula.html', context)


@login_required
def editar_matricula(request, matricula_id):
    """Edita uma matrícula existente."""
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance=matricula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matrícula atualizada com sucesso!')
            return redirect('matriculas:detalhar_matricula', matricula_id=matricula.id)
        else:
            messages.error(request, 'Erro ao atualizar matrícula. Verifique os dados.')
    else:
        form = MatriculaForm(instance=matricula)
    
    context = {
        'form': form,
        'matricula': matricula,
        'titulo': 'Editar Matrícula',
    }
    
    return render(request, 'matriculas/realizar_matricula.html', context)


@login_required
def excluir_matricula(request, matricula_id):
    """Exclui uma matrícula."""
    matricula = get_object_or_404(Matricula, id=matricula_id)
    
    if request.method == 'POST':
        matricula.delete()
        messages.success(request, 'Matrícula excluída com sucesso!')
        return redirect('matriculas:listar_matriculas')
    
    context = {
        'matricula': matricula,
    }
    
    return render(request, 'matriculas/confirmar_exclusao_matricula.html', context)


# Views AJAX para filtros dinâmicos
@login_required
def turmas_por_curso(request):
    """Retorna turmas de um curso específico."""
    curso_id = request.GET.get('curso_id')
    if not curso_id:
        return JsonResponse({'turmas': []})
    
    Turma = get_turma_model()
    turmas = Turma.objects.filter(
        curso_id=curso_id, 
        ativo=True
    ).values('id', 'nome')
    
    return JsonResponse({'turmas': list(turmas)})


@login_required
def alunos_disponiveis(request):
    """Retorna alunos disponíveis para matrícula."""
    turma_id = request.GET.get('turma_id')
    if not turma_id:
        return JsonResponse({'alunos': []})
    
    # Alunos que não estão matriculados na turma
    matriculados = Matricula.objects.filter(
        turma_id=turma_id,
        status='A'
    ).values_list('aluno_id', flat=True)
    
    Aluno = get_aluno_model()
    alunos = Aluno.objects.filter(
        ativo=True
    ).exclude(
        id__in=matriculados
    ).values('id', 'nome', 'cpf')
    
    return JsonResponse({'alunos': list(alunos)})
