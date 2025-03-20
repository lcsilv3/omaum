from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import AtividadeRitualistica
from .forms import AtividadeRitualisticaForm

def criar_atividade_ritualistica(request):
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            if atividade.todos_alunos:
                atividade.save()
                atividade.alunos.set(atividade.turma.aluno_set.all())
            else:
                atividade.save()
                atividade.alunos.set(form.cleaned_data['alunos'])
            messages.success(request, 'Atividade ritualística criada com sucesso!')
            return redirect('atividades:atividade_ritualistica_list')
    else:
        form = AtividadeRitualisticaForm()
    return render(request, 'atividades/criar_atividade_ritualistica.html', {'form': form})

def editar_atividade_ritualistica(request, pk):
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST, instance=atividade)
        if form.is_valid():
            atividade = form.save(commit=False)
            if atividade.todos_alunos:
                atividade.save()
                atividade.alunos.set(atividade.turma.aluno_set.all())
            else:
                atividade.save()
                atividade.alunos.set(form.cleaned_data['alunos'])
            messages.success(request, 'Atividade ritualística atualizada com sucesso!')
            return redirect('atividades:atividade_ritualistica_list')
    else:
        form = AtividadeRitualisticaForm(instance=atividade)
    return render(request, 'atividades/editar_atividade_ritualistica.html', {'form': form, 'atividade': atividade})
from django.views.generic import ListView
from .models import AtividadeAcademica
from django.db.models import Q

class AtividadeAcademicaListView(ListView):
    model = AtividadeAcademica
    template_name = 'atividades/atividade_academica_list.html'
    context_object_name = 'atividades_academicas'
    paginate_by = 10  # Adjust this number as needed

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(nome__icontains=search_query) |
                Q(descricao__icontains=search_query) |
                Q(turma__nome__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class AtividadeRitualisticaListView(ListView):
    model = AtividadeRitualistica
    template_name = 'atividades/listar_atividades_ritualisticas.html'
    context_object_name = 'object_list'
