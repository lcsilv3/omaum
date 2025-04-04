from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module

def get_models():
    cursos_module = import_module('cursos.models')
    return getattr(cursos_module, 'Curso')

def get_forms():
    cursos_forms = import_module('cursos.forms')
    return getattr(cursos_forms, 'CursoForm')

@login_required
def listar_cursos(request):
    """Lista todos os cursos cadastrados."""
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
            messages.success(request, 'Curso criado com sucesso!')
            return redirect('cursos:listar_cursos')
    else:
        form = CursoForm()
    return render(request, 'cursos/criar_curso.html', {'form': form})

@login_required
def detalhar_curso(request, codigo_curso):
    """Exibe os detalhes de um curso."""
    Curso = get_models()
    curso = get_object_or_404(Curso, codigo_curso=codigo_curso)
    return render(request, 'cursos/detalhar_curso.html', {'curso': curso})

@login_required
def editar_curso(request, codigo_curso):
    """Edita um curso existente."""
    Curso = get_models()
    CursoForm = get_forms()
    curso = get_object_or_404(Curso, codigo_curso=codigo_curso)
    
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso atualizado com sucesso!')
            return redirect('cursos:listar_cursos')
    else:
        form = CursoForm(instance=curso)
    
    return render(request, 'cursos/editar_curso.html', {'form': form, 'curso': curso})

@login_required
def excluir_curso(request, codigo_curso):
    """Exclui um curso."""
    Curso = get_models()
    curso = get_object_or_404(Curso, codigo_curso=codigo_curso)
    
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso excluído com sucesso!')
        return redirect('cursos:listar_cursos')
    
    return render(request, 'cursos/excluir_curso.html', {'curso': curso})