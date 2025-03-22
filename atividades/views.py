from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import AtividadeAcademica, AtividadeRitualistica
from .forms import AtividadeAcademicaForm, AtividadeRitualisticaForm

# Views para Atividades Acadêmicas
class AcademicaListaView(ListView):
    model = AtividadeAcademica
    template_name = 'atividades/academica_lista.html'
    context_object_name = 'atividades'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(nome__icontains=search_query)
        return queryset

class AcademicaCriarView(CreateView):
    model = AtividadeAcademica
    form_class = AtividadeAcademicaForm
    template_name = 'atividades/academica_formulario.html'
    success_url = reverse_lazy('atividades:academica_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Atividade acadêmica criada com sucesso!')
        return super().form_valid(form)

class AcademicaEditarView(UpdateView):
    model = AtividadeAcademica
    form_class = AtividadeAcademicaForm
    template_name = 'atividades/academica_formulario.html'
    success_url = reverse_lazy('atividades:academica_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Atividade acadêmica atualizada com sucesso!')
        return super().form_valid(form)

class AcademicaExcluirView(DeleteView):
    model = AtividadeAcademica
    template_name = 'atividades/academica_confirmar_exclusao.html'
    success_url = reverse_lazy('atividades:academica_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Atividade acadêmica excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views para Atividades Ritualísticas
class RitualisticaListaView(ListView):
    model = AtividadeRitualistica
    template_name = 'atividades/ritualistica_lista.html'
    context_object_name = 'atividades_ritualisticas'

class RitualisticaCriarView(CreateView):
    model = AtividadeRitualistica
    form_class = AtividadeRitualisticaForm
    template_name = 'atividades/atividade_ritualistica_form.html'
    success_url = reverse_lazy('atividades:ritualistica_lista')
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        # Handle the todos_alunos field logic
        if form.cleaned_data.get('todos_alunos'):
            # Logic to get all students from the selected turma
            turma = form.cleaned_data.get('turma')
            if turma:
                # Save first to create the instance
                instance.save()
                # Then add all students from the turma
                from core.models import Aluno
                alunos = Aluno.objects.filter(turma=turma)
                instance.alunos.set(alunos)
        else:
            instance.save()
            # The many-to-many relationship will be saved by the form
        
        messages.success(self.request, 'Atividade ritualística criada com sucesso!')
        return redirect(self.success_url)

# Add these missing views
class RitualisticaEditarView(UpdateView):
    model = AtividadeRitualistica
    form_class = AtividadeRitualisticaForm
    template_name = 'atividades/atividade_ritualistica_form.html'
    success_url = reverse_lazy('atividades:ritualistica_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Atividade ritualística atualizada com sucesso!')
        return super().form_valid(form)

class RitualisticaExcluirView(DeleteView):
    model = AtividadeRitualistica
    template_name = 'atividades/academica_confirmar_exclusao.html'  # Reuse the same template
    success_url = reverse_lazy('atividades:ritualistica_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Atividade ritualística excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
