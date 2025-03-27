from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Frequencia
from .forms import FrequenciaForm
from alunos.models import Aluno
from turmas.models import Turma

def criar_frequencia(request):
    """
    Cria uma nova frequência no sistema.
    """
    if request.method == 'POST':
        form = FrequenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frequência criada com sucesso!')
            return redirect('frequencias:listar_frequencias')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FrequenciaForm()
    return render(request, 'frequencias/criar_frequencia.html', {'form': form})

@login_required
@permission_required('frequencias.add_frequencia', raise_exception=True)
def registrar_frequencia(request):
    if request.method == 'POST':
        form = FrequenciaForm(request.POST)
        if form.is_valid():
            frequencia = form.save(commit=False)
            frequencia.registrado_por = request.user
            frequencia.save()
            messages.success(request, 'Frequência registrada com sucesso!')
            return redirect('listar_frequencias')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = FrequenciaForm()
   
    return render(request, 'frequencias/registrar_frequencia.html', {'form': form})

@login_required
@permission_required('frequencias.add_frequencia', raise_exception=True)
def registrar_frequencia_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    alunos = Aluno.objects.filter(turmas=turma)
    
    if request.method == 'POST':
        data = request.POST.get('data')
        presentes = request.POST.getlist('presentes')
        
        # Create or update attendance records
        for aluno in alunos:
            presente = str(aluno.id) in presentes
            justificativa = request.POST.get(f'justificativa_{aluno.id}', '')
            
            # Check if record exists
            frequencia, created = Frequencia.objects.update_or_create(
                aluno=aluno,
                turma=turma,
                data=data,
                defaults={
                    'presente': presente,
                    'justificativa': justificativa if not presente else '',
                    'registrado_por': request.user
                }
            )
        
        messages.success(request, 'Frequências registradas com sucesso!')
        return redirect('listar_frequencias')
    
    return render(request, 'frequencias/registrar_frequencia_turma.html', {
        'turma': turma,
        'alunos': alunos,
    })

@login_required
@permission_required('frequencias.view_frequencia', raise_exception=True)
def listar_frequencias(request):
    frequencias_list = Frequencia.objects.all().select_related('aluno', 'turma')
   
    # Filtros
    aluno_id = request.GET.get('aluno')
    turma_id = request.GET.get('turma')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')
   
    if aluno_id:
        frequencias_list = frequencias_list.filter(aluno_id=aluno_id)
    if turma_id:
        frequencias_list = frequencias_list.filter(turma_id=turma_id)
    if data_inicio:
        frequencias_list = frequencias_list.filter(data__gte=data_inicio)
    if data_fim:
        frequencias_list = frequencias_list.filter(data__lte=data_fim)
    if status:
        presente = status == 'presente'
        frequencias_list = frequencias_list.filter(presente=presente)
   
    # Paginação
    paginator = Paginator(frequencias_list, 10)  # 10 itens por página
    page = request.GET.get('page')
   
    try:
        frequencias = paginator.page(page)
    except PageNotAnInteger:
        frequencias = paginator.page(1)
    except EmptyPage:
        frequencias = paginator.page(paginator.num_pages)
   
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
   
    return render(request, 'frequencias/listar_frequencias.html', {
        'frequencias': frequencias,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'status': status,
        'alunos': alunos,
        'turmas': turmas
    })

@login_required
@permission_required('frequencias.change_frequencia', raise_exception=True)
def editar_frequencia(request, id):
    frequencia = get_object_or_404(Frequencia, id=id)
   
    if request.method == 'POST':
        form = FrequenciaForm(request.POST, instance=frequencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frequência atualizada com sucesso!')
            return redirect('listar_frequencias')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = FrequenciaForm(instance=frequencia)
   
    return render(request, 'frequencias/editar_frequencia.html', {'form': form, 'frequencia': frequencia})

@login_required
@permission_required('frequencias.view_frequencia', raise_exception=True)
def detalhe_frequencia(request, id):
    frequencia = get_object_or_404(Frequencia, id=id)
    return render(request, 'frequencias/detalhe_frequencia.html', {'frequencia': frequencia})

@login_required
@permission_required('frequencias.delete_frequencia', raise_exception=True)
def excluir_frequencia(request, id):
    frequencia = get_object_or_404(Frequencia, id=id)
   
    if request.method == 'POST':
        frequencia.delete()
        messages.success(request, 'Frequência excluída com sucesso!')
        return redirect('listar_frequencias')
   
    return render(request, 'frequencias/excluir_frequencia.html', {'frequencia': frequencia})

@login_required
@permission_required('frequencias.view_frequencia', raise_exception=True)
def estatisticas_frequencia(request):
    # Get filter parameters
    aluno_id = request.GET.get('aluno')
    turma_id = request.GET.get('turma')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Base queryset
    frequencias = Frequencia.objects.all()
    
    # Apply filters
    if aluno_id:
        frequencias = frequencias.filter(aluno_id=aluno_id)
    if turma_id:
        frequencias = frequencias.filter(turma_id=turma_id)
    if data_inicio:
        frequencias = frequencias.filter(data__gte=data_inicio)
    if data_fim:
        frequencias = frequencias.filter(data__lte=data_fim)
    
    # Calculate statistics
    total = frequencias.count()
    presentes = frequencias.filter(presente=True).count()
    ausentes = total - presentes
    
    taxa_presenca = (presentes / total * 100) if total > 0 else 0
    
    # Get lists for filters
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    
    return render(request, 'frequencias/estatisticas_frequencia.html', {
        'total': total,
        'presentes': presentes,
        'ausentes': ausentes,
        'taxa_presenca': taxa_presenca,
        'alunos': alunos,
        'turmas': turmas,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    })

@login_required
@permission_required('frequencias.change_frequencia', raise_exception=True)
def bulk_actions(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')
        
        if not selected_ids:
            messages.error(request, 'Nenhum registro selecionado.')
            return redirect('listar_frequencias')
            
        if action == 'delete':
            Frequencia.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'{len(selected_ids)} registros excluídos com sucesso!')
        elif action == 'mark_present':
            Frequencia.objects.filter(id__in=selected_ids).update(presente=True, justificativa='')
            messages.success(request, f'{len(selected_ids)} registros marcados como presente!')
        elif action == 'mark_absent':
            Frequencia.objects.filter(id__in=selected_ids).update(presente=False)
            messages.success(request, f'{len(selected_ids)} registros marcados como ausente!')
            
        return redirect('listar_frequencias')
    
    return redirect('listar_frequencias')
