from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Iniciacao
from .forms import IniciacaoForm
from alunos.models import Aluno
from django.contrib.auth.decorators import login_required


@login_required
def listar_iniciacoes(request):
    # Parâmetros de filtro
    aluno_id = request.GET.get('aluno')
    nome_curso = request.GET.get('curso')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Query base
    iniciacoes = Iniciacao.objects.all()
    
    # Aplicar filtros
    if aluno_id:
        iniciacoes = iniciacoes.filter(aluno_id=aluno_id)
    
    if nome_curso:
        iniciacoes = iniciacoes.filter(nome_curso__icontains=nome_curso)
    
    if data_inicio:
        iniciacoes = iniciacoes.filter(data_iniciacao__gte=data_inicio)
    
    if data_fim:
        iniciacoes = iniciacoes.filter(data_iniciacao__lte=data_fim)
    
    # Busca geral
    search_query = request.GET.get('search', '')
    if search_query:
        iniciacoes = iniciacoes.filter(
            Q(aluno__nome__icontains=search_query) |
            Q(nome_curso__icontains=search_query)
        )
    
    # Paginação
    paginator = Paginator(iniciacoes, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Lista de alunos para o filtro
    alunos = Aluno.objects.all()
    
    context = {
        'page_obj': page_obj,
        'alunos': alunos,
        'filtros': {
            'aluno_id': aluno_id,
            'nome_curso': nome_curso,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'search': search_query
        }
    }
    
    return render(request, 'iniciacoes/listar_iniciacoes.html', context)


@login_required
def criar_iniciacao(request):
    if request.method == 'POST':
        form = IniciacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação criada com sucesso.')
            return redirect('iniciacoes:listar_iniciacoes')
    else:
        form = IniciacaoForm()
    return render(request, 'iniciacoes/criar_iniciacao.html', {'form': form})


@login_required
def detalhe_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    return render(request, 'iniciacoes/detalhe_iniciacao.html', {'iniciacao': iniciacao})


@login_required
def editar_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == 'POST':
        form = IniciacaoForm(request.POST, instance=iniciacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação atualizada com sucesso.')
            return redirect('iniciacoes:listar_iniciacoes')
    else:
        form = IniciacaoForm(instance=iniciacao)
    return render(request, 'iniciacoes/editar_iniciacao.html', {'form': form, 'iniciacao': iniciacao})


@login_required
def excluir_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == 'POST':
        iniciacao.delete()
        messages.success(request, 'Iniciação excluída com sucesso.')
        return redirect('iniciacoes:listar_iniciacoes')
    return render(request, 'iniciacoes/excluir_iniciacao.html', {'iniciacao': iniciacao})

import csv
from django.http import HttpResponse

@login_required
def exportar_iniciacoes_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iniciacoes.csv"'
    
    # Aplicar os mesmos filtros da listagem
    aluno_id = request.GET.get('aluno')
    nome_curso = request.GET.get('curso')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    search_query = request.GET.get('search', '')
    
    # Query base
    iniciacoes = Iniciacao.objects.all()
    
    # Aplicar filtros (mesmo código da view listar_iniciacoes)
    if aluno_id:
        iniciacoes = iniciacoes.filter(aluno_id=aluno_id)
    
    if nome_curso:
        iniciacoes = iniciacoes.filter(nome_curso__icontains=nome_curso)
    
    if data_inicio:
        iniciacoes = iniciacoes.filter(data_iniciacao__gte=data_inicio)
    
    if data_fim:
        iniciacoes = iniciacoes.filter(data_iniciacao__lte=data_fim)
    
    if search_query:
        iniciacoes = iniciacoes.filter(
            Q(aluno__nome__icontains=search_query) |
            Q(nome_curso__icontains=search_query)
        )
    
    writer = csv.writer(response)
    writer.writerow(['Aluno', 'Curso', 'Data de Iniciação', 'Observações'])
    
    for iniciacao in iniciacoes:
        writer.writerow([
            iniciacao.aluno.nome,
            iniciacao.nome_curso,
            iniciacao.data_iniciacao.strftime('%d/%m/%Y'),
            iniciacao.observacoes or ''
        ])
    
    # Adicionar mensagem de sucesso
    messages.success(request, f'Arquivo CSV com {iniciacoes.count()} iniciações exportado com sucesso.')
    
    return response
