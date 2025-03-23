from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import AtividadeAcademica, AtividadeRitualistica
from .forms import AtividadeAcademicaForm, AtividadeRitualisticaForm
from turmas.models import Turma

# Views para Atividades Acadêmicas
class AcademicaListaView(ListView):
    model = AtividadeAcademica
    template_name = 'atividades/academica_lista.html'
    context_object_name = 'atividades'
    paginate_by = 10  # Número de itens por página
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        
        # Adicionar lista de turmas para o filtro
        context['turmas'] = Turma.objects.all()
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Busca por nome
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(nome__icontains=search_query)
        
        # Filtro por turma
        turma_id = self.request.GET.get('turma', '')
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        
        # Filtro por data de início
        data_inicio_min = self.request.GET.get('data_inicio_min', '')
        if data_inicio_min:
            queryset = queryset.filter(data_inicio__gte=data_inicio_min)
        
        # Filtro por data de fim
        data_fim_max = self.request.GET.get('data_fim_max', '')
        if data_fim_max:
            queryset = queryset.filter(data_fim__lte=data_fim_max)
        
        # Ordenação
        order_by = self.request.GET.get('order_by', 'nome')
        order_dir = self.request.GET.get('order_dir', 'asc')
        
        if order_dir == 'desc':
            order_by = f'-{order_by}'
            
        return queryset.order_by(order_by)


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
    paginate_by = 10  # Número de itens por página
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        
        # Adicionar lista de turmas para o filtro
        context['turmas'] = Turma.objects.all()
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Busca por nome
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(nome__icontains=search_query)
        
        # Filtro por turma
        turma_id = self.request.GET.get('turma', '')
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        
        # Filtro por data de início
        data_inicio_min = self.request.GET.get('data_inicio_min', '')
        if data_inicio_min:
            queryset = queryset.filter(data_inicio__gte=data_inicio_min)
        
        # Filtro por data de fim
        data_fim_max = self.request.GET.get('data_fim_max', '')
        if data_fim_max:
            queryset = queryset.filter(data_fim__lte=data_fim_max)
        
        # Ordenação
        order_by = self.request.GET.get('order_by', 'nome')
        order_dir = self.request.GET.get('order_dir', 'asc')
        
        if order_dir == 'desc':
            order_by = f'-{order_by}'
            
        return queryset.order_by(order_by)


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


class RitualisticaEditarView(UpdateView):
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
            
        messages.success(self.request, 'Atividade ritualística atualizada com sucesso!')
        return redirect(self.success_url)


class RitualisticaExcluirView(DeleteView):
    model = AtividadeRitualistica
    template_name = 'atividades/ritualistica_confirmar_exclusao.html'
    success_url = reverse_lazy('atividades:ritualistica_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Atividade ritualística excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
