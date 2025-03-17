from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import AtividadeAcademica, AtividadeRitualistica
from .forms import AtividadeAcademicaForm, AtividadeRitualisticaForm

class AtividadeAcademicaListView(ListView):
    model = AtividadeAcademica
    template_name = 'atividades/atividade_academica_list.html'
    context_object_name = 'atividades_academicas'
    paginate_by = 10

class AtividadeRitualisticaListView(ListView):
    model = AtividadeRitualistica
    template_name = 'atividades/atividade_ritualistica_list.html'
    context_object_name = 'atividades_ritualisticas'
    paginate_by = 10

@login_required
def atividade_academica_create(request):
    if request.method == 'POST':
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('atividades:atividade_academica_list')
    else:
        form = AtividadeAcademicaForm()
    return render(request, 'atividades/atividade_academica_form.html', {'form': form})

@login_required
def atividade_ritualistica_create(request):
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('atividades:atividade_ritualistica_list')
    else:
        form = AtividadeRitualisticaForm()
    return render(request, 'atividades/atividade_ritualistica_form.html', {'form': form})

# Adicione outras views conforme necessário (update, delete, detail)
