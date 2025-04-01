import importlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

# Função para obter modelos usando importlib
def get_models():
    Curso = importlib.import_module('cursos.models').Curso
    return Curso

# Função para obter formulários usando importlib
def get_forms():
    CursoForm = importlib.import_module('cursos.forms').CursoForm
    return CursoForm

@login_required
def listar_cursos(request):
    """Lista todos os cursos."""
    Curso = get_models()
    cursos = Curso.objects.all()
    return render(request, 'cursos/listar_cursos.html', {'cursos': cursos})

@login_required
def criar_curso(request):
    """Cria um novo curso."""
    CursoForm = get_forms()
    
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Curso criado com sucesso!'))
            return redirect('cursos:listar_cursos')
        else:
            messages.error(request, _('Por favor, corrija os erros abaixo.'))
    else:
        form = CursoForm()
    
    return render(request, 'cursos/criar_curso.html', {'form': form})

@login_required
def detalhar_curso(request, id):
    """Exibe os detalhes de um curso."""
    curso = get_object_or_404(Curso, id=id)
    return render(request, 'cursos/detalhar_curso.html', {'curso': curso})

@login_required
def editar_curso(request, id):
    """Edita um curso existente."""
    Curso = get_models()
    CursoForm = get_forms()
    
    curso = get_object_or_404(Curso, id=id)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, _('Curso atualizado com sucesso!'))
            return redirect('cursos:detalhar_curso', id=curso.id)
        else:
            messages.error(request, _('Por favor, corrija os erros abaixo.'))
    else:
        form = CursoForm(instance=curso)
    
    return render(request, 'cursos/editar_curso.html', {
        'form': form, 
        'curso': curso
    })

@login_required
def excluir_curso(request, id):
    """Exclui um curso."""
    Curso = get_models()
    curso = get_object_or_404(Curso, id=id)
    
    if request.method == 'POST':
        curso.delete()
        messages.success(request, _('Curso excluído com sucesso!'))
        return redirect('cursos:listar_cursos')
    
    return render(request, 'cursos/excluir_curso.html', {'curso': curso})