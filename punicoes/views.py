from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Punicao
from .forms import PunicaoForm
from alunos.models import Aluno

@login_required
@permission_required('punicoes.add_punicao', raise_exception=True)
def criar_punicao(request):
    if request.method == 'POST':
        form = PunicaoForm(request.POST)
        if form.is_valid():
            punicao = form.save(commit=False)
            punicao.registrado_por = request.user
            punicao.save()
            messages.success(request, 'Punição criada com sucesso!')
            return redirect('listar_punicoes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PunicaoForm()
    return render(request, 'punicoes/criar_punicao.html', {'form': form})

@login_required
@permission_required('punicoes.change_punicao', raise_exception=True)
def editar_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    if request.method == 'POST':
        form = PunicaoForm(request.POST, instance=punicao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punição atualizada com sucesso!')
            return redirect('listar_punicoes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PunicaoForm(instance=punicao)
    return render(request, 'punicoes/editar_punicao.html', {'form': form, 'punicao': punicao})

@login_required
@permission_required('punicoes.view_punicao', raise_exception=True)
def listar_punicoes(request):
    punicoes_list = Punicao.objects.all().select_related('aluno')
    
    # Filtros
    aluno_id = request.GET.get('aluno')
    tipo_punicao = request.GET.get('tipo_punicao')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if aluno_id:
        punicoes_list = punicoes_list.filter(aluno_id=aluno_id)
    if tipo_punicao:
        punicoes_list = punicoes_list.filter(tipo_punicao=tipo_punicao)
    if data_inicio:
        punicoes_list = punicoes_list.filter(data__gte=data_inicio)
    if data_fim:
        punicoes_list = punicoes_list.filter(data__lte=data_fim)
    
    # Paginação
    paginator = Paginator(punicoes_list, 10)  # 10 itens por página
    page = request.GET.get('page')
    
    try:
        punicoes = paginator.page(page)
    except PageNotAnInteger:
        punicoes = paginator.page(1)
    except EmptyPage:
        punicoes = paginator.page(paginator.num_pages)
    
    # Obter tipos de punição únicos para o filtro
    tipos_punicao = Punicao.objects.values_list('tipo_punicao', flat=True).distinct()
    alunos = Aluno.objects.all()
    
    return render(request, 'punicoes/listar_punicoes.html', {
        'punicoes': punicoes,
        'aluno_id': aluno_id,
        'tipo_punicao': tipo_punicao,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'tipos_punicao': tipos_punicao,
        'alunos': alunos
    })

@login_required
@permission_required('punicoes.view_punicao', raise_exception=True)
def detalhe_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    return render(request, 'punicoes/detalhe_punicao.html', {'punicao': punicao})

@login_required
@permission_required('punicoes.delete_punicao', raise_exception=True)
def excluir_punicao(request, id):
    punicao = get_object_or_404(Punicao, id=id)
    if request.method == 'POST':
        punicao.delete()
        messages.success(request, 'Punição excluída com sucesso.')
        return redirect('listar_punicoes')
    return render(request, 'punicoes/excluir_punicao.html', {'punicao': punicao})