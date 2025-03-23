from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Curso
from .forms import CursoForm

def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/listar_cursos.html', {'cursos': cursos})

def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso criado com sucesso!')
            return redirect('listar_cursos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CursoForm()
    return render(request, 'cursos/criar_curso.html', {'form': form})

def editar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso atualizado com sucesso!')
            return redirect('listar_cursos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'cursos/editar_curso.html', {'form': form, 'curso': curso})

def excluir_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso excluído com sucesso!')
        return redirect('listar_cursos')
    return render(request, 'cursos/excluir_curso.html', {'curso': curso})

def detalhes_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    return render(request, 'cursos/detalhes_curso.html', {'curso': curso})