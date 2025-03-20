from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'codigo', 'descricao']  # Add or remove fields as needed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Curso
from .forms import CursoForm

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