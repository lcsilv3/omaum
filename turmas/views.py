from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from importlib import import_module
from .models import Turma, Matricula
from .forms import TurmaForm, MatriculaForm

# Função para importar dinamicamente o modelo Aluno
def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')
@login_required
def listar_turmas(request):
    query = request.GET.get('q')
    curso_id = request.GET.get('curso')
    status = request.GET.get('status')

    turmas = Turma.objects.all().select_related('curso')

    if query:
        turmas = turmas.filter(
            Q(nome__icontains=query) | 
            Q(curso__nome__icontains=query)
        )

    if curso_id:
        turmas = turmas.filter(curso_id=curso_id)

    if status:
        turmas = turmas.filter(status=status)

    # Obtém todos os cursos para o filtro dropdown
    Curso = import_module('cursos.models').Curso
    cursos = Curso.objects.all()

    paginator = Paginator(turmas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'turmas': page_obj,
        'query': query,
        'cursos': cursos,
        'curso_selecionado': curso_id,
        'opcoes_status': Turma.OPCOES_STATUS,
        'status_selecionado': status
    }

    return render(request, 'turmas/listar_turmas.html', context)

@login_required
def criar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, 'Turma criada com sucesso!')
            return redirect('turmas:listar_turmas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = TurmaForm()

    return render(request, 'turmas/criar_turma.html', {'form': form})

@login_required
def detalhar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    matriculas = Matricula.objects.filter(turma=turma).select_related('aluno')

    context = {
        'turma': turma,
        'matriculas': matriculas,
        'total_matriculas': matriculas.count(),
        'vagas_disponiveis': turma.capacidade - matriculas.count()
    }

    return render(request, 'turmas/detalhar_turma.html', context)

@login_required
def editar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('turmas:listar_turmas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'turmas/editar_turma.html', {'form': form, 'turma': turma})

@login_required
def excluir_turma(request, id):
    turma = get_object_or_404(Turma, id=id)

    if request.method == 'POST':
        if turma.matriculas.exists():
            messages.error(request, 'Não é possível excluir uma turma com alunos matriculados.')
            return redirect('turmas:detalhar_turma', id=turma.id)

        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
        return redirect('turmas:listar_turmas')

    return render(request, 'turmas/excluir_turma.html', {'turma': turma})

@login_required
def matricular_aluno(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    Aluno = get_aluno_model()

    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            aluno = form.cleaned_data['aluno']
            if Matricula.objects.filter(turma=turma, aluno=aluno).exists():
                messages.error(request, 'Este aluno já está matriculado nesta turma.')
            else:
                Matricula.objects.create(turma=turma, aluno=aluno)
                messages.success(request, 'Aluno matriculado com sucesso!')
            return redirect('turmas:detalhar_turma', id=turma.id)
    else:
        form = MatriculaForm()

    context = {
        'form': form,
        'turma': turma,
    }
    return render(request, 'turmas/matricular_aluno.html', context)

@login_required
def cancelar_matricula(request, turma_id, aluno_id):
    matricula = get_object_or_404(Matricula, turma_id=turma_id, aluno_id=aluno_id)

    if request.method == 'POST':
        matricula.delete()
        messages.success(request, 'Matrícula cancelada com sucesso!')
        return redirect('turmas:detalhar_turma', id=turma_id)

    return render(request, 'turmas/cancelar_matricula.html', {'matricula': matricula})

@login_required
def listar_alunos_matriculados(request, turma_id):
    """Lista todos os alunos matriculados em uma turma"""
    turma = get_object_or_404(Turma, pk=turma_id)
    alunos = turma.alunos.all()
    
    return render(request, 'turmas/listar_alunos_matriculados.html', {
        'turma': turma,
        'alunos': alunos,
        'titulo': f'Alunos Matriculados na Turma: {turma.nome}'
    })

# Views para Cursos (mantidas para compatibilidade)
def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'turmas/listar_cursos.html', {'cursos': cursos})

def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso criado com sucesso!')
            return redirect('turmas:listar_cursos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CursoForm()
    return render(request, 'turmas/criar_curso.html', {'form': form})

def detalhar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    return render(request, 'turmas/detalhar_curso.html', {'curso': curso})

def editar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso atualizado com sucesso!')
            return redirect('turmas:listar_cursos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'turmas/editar_curso.html', {'form': form, 'curso': curso})

def excluir_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso excluído com sucesso!')
        return redirect('turmas:listar_cursos')
    return render(request, 'turmas/excluir_curso.html', {'curso': curso})