from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Turma
from cursos.models import Curso
from .forms import CursoForm, TurmaForm

# Views for Curso
class CursoListView(ListView):
    model = Curso
    template_name = 'turmas/curso_list.html'

class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'turmas/curso_form.html'
    success_url = reverse_lazy('turmas:curso_list')

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'turmas/curso_form.html'
    success_url = reverse_lazy('turmas:curso_list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'turmas/curso_confirm_delete.html'
    success_url = reverse_lazy('turmas:curso_list')

# Views for Turma
class TurmaListView(ListView):
    model = Turma
    template_name = 'turmas/turma_list.html'

class TurmaCreateView(CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'turmas/turma_form.html'
    success_url = reverse_lazy('turmas:turma_list')

class TurmaUpdateView(UpdateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'turmas/turma_form.html'
    success_url = reverse_lazy('turmas:turma_list')

class TurmaDeleteView(DeleteView):
    model = Turma
    template_name = 'turmas/turma_confirm_delete.html'
    success_url = reverse_lazy('turmas:turma_list')