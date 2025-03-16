from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from turmas.models import Turma
from .models import AtividadeAcademica, AtividadeRitualistica
from .forms import AtividadeAcademicaForm, AtividadeRitualisticaForm

class AtividadeAcademicaListView(ListView):
    model = AtividadeAcademica
    template_name = 'atividades/atividade_academica_list.html'
    context_object_name = 'atividades_academicas'

class AtividadeAcademicaCreateView(CreateView):
    model = AtividadeAcademica
    form_class = AtividadeAcademicaForm
    template_name = 'atividades/atividade_academica_form.html'
    success_url = reverse_lazy('atividades:atividade_academica_list')

    def get(self, request, *args, **kwargs):
        if not Turma.objects.exists():
            messages.warning(request, "Atividades só podem ser inseridas se houver Turmas cadastradas, por favor cadastre uma turma")
            # If core has a namespace, use it like this:
            return redirect('atividades:cadastrar_turma')
            # If core doesn't have a namespace, you can try:
            # return redirect('cadastrar_turma')
        return super().get(request, *args, **kwargs)

class AtividadeAcademicaDetailView(DetailView):
    model = AtividadeAcademica
    template_name = 'atividades/atividade_academica_detail.html'
    context_object_name = 'atividade'

class AtividadeAcademicaUpdateView(UpdateView):
    model = AtividadeAcademica
    form_class = AtividadeAcademicaForm
    template_name = 'atividades/atividade_academica_form.html'
    success_url = reverse_lazy('atividades:atividade_academica_list')

class AtividadeAcademicaDeleteView(DeleteView):
    model = AtividadeAcademica
    template_name = 'atividades/atividade_academica_confirm_delete.html'
    success_url = reverse_lazy('atividades:atividade_academica_list')

class AtividadeRitualisticaListView(ListView):
    model = AtividadeRitualistica
    template_name = 'atividades/atividade_ritualistica_list.html'
    context_object_name = 'atividades_ritualisticas'

class AtividadeRitualisticaCreateView(CreateView):
    model = AtividadeRitualistica
    form_class = AtividadeRitualisticaForm
    template_name = 'atividades/atividade_ritualistica_form.html'
    success_url = reverse_lazy('atividades:atividade_ritualistica_list')

    def get(self, request, *args, **kwargs):
        if not Turma.objects.exists():
            messages.warning(request, "Atividades só podem ser inseridas se houver Turmas cadastradas, por favor cadastre uma turma")
            # Use the namespace when redirecting
            return redirect('atividades:cadastrar_turma')
        return super().get(request, *args, **kwargs)

class AtividadeRitualisticaDetailView(DetailView):
    model = AtividadeRitualistica
    template_name = 'atividades/atividade_ritualistica_detail.html'
    context_object_name = 'atividade'

class AtividadeRitualisticaUpdateView(UpdateView):
    model = AtividadeRitualistica
    form_class = AtividadeRitualisticaForm
    template_name = 'atividades/atividade_ritualistica_form.html'
    success_url = reverse_lazy('atividades:atividade_ritualistica_list')

class AtividadeRitualisticaDeleteView(DeleteView):
    model = AtividadeRitualistica
    template_name = 'atividades/atividade_ritualistica_confirm_delete.html'
    success_url = reverse_lazy('atividades:atividade_ritualistica_list')

# Add this to your existing views.py file
def cadastrar_turma_view(request):
    return redirect('turmas:turma_create')  # Adjust to the correct URL pattern
