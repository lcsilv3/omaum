from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Curso, Turma
from .forms import CursoForm, TurmaForm

# Views para Curso
class CursoListView(ListView):
    model = Curso
    template_name = 'turmas/curso_list.html'

class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'turmas/curso_form.html'
    success_url = reverse_lazy('curso_list')

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'turmas/curso_form.html'
    success_url = reverse_lazy('curso_list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'turmas/curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')

# Views para Turma
class TurmaListView(ListView):
    model = Turma
    template_name = 'turmas/turma_list.html'

class TurmaCreateView(CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'turmas/turma_form.html'
    success_url = reverse_lazy('turma_list')

class TurmaUpdateView(UpdateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'turmas/turma_form.html'
    success_url = reverse_lazy('turma_list')

class TurmaDeleteView(DeleteView):
    model = Turma
    template_name = 'turmas/turma_confirm_delete.html'
    success_url = reverse_lazy('turma_list')