from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import PresencaAcademica
from .forms import PresencaForm
from alunos.models import Aluno
from turmas.models import Turma

@login_required
def registrar_presenca(request):
    """Registra a presença de um aluno."""
    if request.method == 'POST':
        form = PresencaForm(request.POST)
        if form.is_valid():
            presenca = form.save(commit=False)
            presenca.registrado_por = request.user
            presenca.save()
            messages.success(request, 'Presença registrada com sucesso!')
            return redirect('presencas:listar_presencas')
    else:
        form = PresencaForm()
    
    return render(request, 'presencas/registrar_presenca.html', {'form': form})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def listar_presencas(request):
    presencas_list = PresencaAcademica.objects.all().select_related('aluno', 'turma')
    
    # Filtros
    aluno_id = request.GET.get('aluno')
    turma_id = request.GET.get('turma')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if aluno_id:
        presencas_list = presencas_list.filter(aluno_id=aluno_id)
    if turma_id:
        presencas_list = presencas_list.filter(turma_id=turma_id)
    if data_inicio:
        presencas_list = presencas_list.filter(data__gte=data_inicio)
    if data_fim:
        presencas_list = presencas_list.filter(data__lte=data_fim)
    
    # Paginação
    paginator = Paginator(presencas_list, 10)  # 10 itens por página
    page = request.GET.get('page')
    
    try:
        presencas = paginator.page(page)
    except PageNotAnInteger:
        presencas = paginator.page(1)
    except EmptyPage:
        presencas = paginator.page(paginator.num_pages)
    
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    
    return render(request, 'presencas/lista_presencas.html', {
        'presencas': presencas,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'alunos': alunos,
        'turmas': turmas
    })

@login_required
def editar_presenca(request, id):
    """Edita um registro de presença."""
    presenca = get_object_or_404(PresencaAcademica, id=id)
    
    if request.method == 'POST':
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presença atualizada com sucesso!')
            return redirect('presencas:listar_presencas')
    else:
        form = PresencaForm(instance=presenca)
    
    return render(request, 'presencas/editar_presenca.html', {'form': form, 'presenca': presenca})

@login_required
@permission_required('presencas.delete_presencaacademica', raise_exception=True)
def excluir_presenca(request, id):  # Padronizado para usar 'id'
    presenca = get_object_or_404(PresencaAcademica, id=id)
    
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença excluída com sucesso!')
        return redirect('presencas:listar_presencas')  # Corrigido para usar o namespace
    
    return render(request, 'presencas/excluir_presenca.html', {'presenca': presenca})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas(request):
    # Implementação pendente
    return render(request, 'presencas/relatorio_presencas.html')
