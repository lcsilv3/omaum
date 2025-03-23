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
    """Matricula um aluno na turma"""
    turma = get_object_or_404(Turma, pk=turma_id)
    
    # Verificar se há vagas disponíveis
    if turma.vagas_disponiveis <= 0:
        adicionar_mensagem(request, 'erro', 'Não há vagas disponíveis nesta turma.')
        return redirect('turmas:detalhes_turma', turma_id=turma.id)
    
    if request.method == 'POST':
        form = AlunoTurmaForm(request.POST, turma=turma)
        if form.is_valid():
            aluno = form.cleaned_data['aluno']
            
            # Verificar se o aluno já está matriculado
            if turma.alunos.filter(id=aluno.id).exists():
                adicionar_mensagem(request, 'erro', f'O aluno {aluno.nome} já está matriculado nesta turma.')
            else:
                turma.alunos.add(aluno)
                registrar_log(request, f'Aluno {aluno.nome} matriculado na turma {turma.nome}')
                adicionar_mensagem(request, 'sucesso', f'Aluno {aluno.nome} matriculado com sucesso!')
            
            return redirect('turmas:detalhes_turma', turma_id=turma.id)
    else:
        form = AlunoTurmaForm(turma=turma)
    
    return render(request, 'turmas/matricular_aluno.html', {
        'form': form,
        'turma': turma,
        'titulo': f'Matricular Aluno na Turma: {turma.nome}'
    })

@login_required
def cancelar_matricula(request, turma_id, aluno_id):
    """Cancela a matrícula de um aluno na turma"""
    turma = get_object_or_404(Turma, pk=turma_id)
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    
    if request.method == 'POST':
        if turma.alunos.filter(id=aluno.id).exists():
            turma.alunos.remove(aluno)
            registrar_log(request, f'Matrícula do aluno {aluno.nome} na turma {turma.nome} foi cancelada')
            adicionar_mensagem(request, 'sucesso', f'Matrícula do aluno {aluno.nome} cancelada com sucesso!')
        else:
            adicionar_mensagem(request, 'erro', f'O aluno {aluno.nome} não está matriculado nesta turma.')
        
        return redirect('turmas:detalhes_turma', turma_id=turma.id)
    
    return render(request, 'turmas/confirmar_cancelamento_matricula.html', {
        'turma': turma,
        'aluno': aluno,
        'titulo': 'Confirmar Cancelamento de Matrícula'
    })

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