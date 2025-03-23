from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from .models import Turma, Matricula
from cursos.models import Curso
from .forms import TurmaForm, MatriculaForm

# Views para Turmas
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
        form = TurmaComAlunoForm(request.POST)
        if form.is_valid():
            # Cria a turma
            turma = Turma(
                nome=form.cleaned_data['nome'],
                curso=form.cleaned_data['curso'],
                data_inicio=form.cleaned_data['data_inicio'],
                data_fim=form.cleaned_data['data_fim'],
                capacidade=form.cleaned_data['capacidade'],
                status=form.cleaned_data['status'],
                descricao=form.cleaned_data['descricao']
            )
            turma.save()
            
            # Cria as matrículas para os alunos selecionados
            alunos = form.cleaned_data['alunos']
            for aluno in alunos:
                Matricula.objects.create(
                    aluno=aluno,
                    turma=turma,
                    status='A'  # Ativa
                )
            
            messages.success(request, 'Turma criada com sucesso com os alunos selecionados!')
            return redirect('turmas:listar_turmas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = TurmaComAlunoForm()
    
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
    
    # Verifica se há matrículas associadas à turma
    matriculas = Matricula.objects.filter(turma=turma)
    
    if request.method == 'POST':
        if matriculas.exists():
            messages.error(request, 'Não é possível excluir uma turma com alunos matriculados.')
            return redirect('turmas:detalhar_turma', id=turma.id)
        
        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
        return redirect('turmas:listar_turmas')
    
    return render(request, 'turmas/excluir_turma.html', {
        'turma': turma,
        'tem_matriculas': matriculas.exists()
    })

# Views para Matrículas
@login_required
def matricular_aluno(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    
    if request.method == 'POST':
        form = MatriculaForm(request.POST, turma=turma)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.turma = turma
            
            try:
                matricula.full_clean()
                matricula.save()
                messages.success(request, f'Aluno matriculado com sucesso na turma {turma.nome}.')
                return redirect('turmas:detalhar_turma', id=turma.id)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
        
    else:
        form = MatriculaForm(turma=turma)
    
    return render(request, 'turmas/matricular_aluno.html', {
        'form': form,
        'turma': turma
    })

@login_required
def cancelar_matricula(request, matricula_id):
    matricula = get_object_or_404(Matricula, id=matricula_id)
    turma = matricula.turma
    turma_id = turma.id
    
    # Verifica se é a última matrícula da turma
    total_matriculas_ativas = Matricula.objects.filter(turma=turma, status='A').count()
    
    if request.method == 'POST':
        if total_matriculas_ativas <= 1 and matricula.status == 'A':
            messages.error(request, 'Não é possível cancelar a matrícula. Uma turma deve ter pelo menos um aluno matriculado.')
            return redirect('turmas:detalhar_turma', id=turma_id)
        
        matricula.status = 'C'  # Cancelada
        matricula.save()
        messages.success(request, 'Matrícula cancelada com sucesso.')
        return redirect('turmas:detalhar_turma', id=turma_id)
    
    return render(request, 'turmas/cancelar_matricula.html', {
        'matricula': matricula,
        'ultima_matricula': total_matriculas_ativas <= 1 and matricula.status == 'A'
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