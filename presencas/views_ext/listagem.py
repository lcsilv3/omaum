from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from importlib import import_module

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def listar_presencas(request):
    """Lista todas as presenças registradas."""
    Presenca = get_model_dynamically("presencas", "Presenca")
    
    # Aplicar filtros
    query = request.GET.get('q', '')
    aluno_id = request.GET.get('aluno', '')
    atividade_id = request.GET.get('atividade', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    presente = request.GET.get('presente', '')
    
    presencas = Presenca.objects.all().select_related('aluno', 'atividade')
    
    if query:
        presencas = presencas.filter(
            Q(aluno__nome__icontains=query) |
            Q(atividade__nome__icontains=query)
        )
    
    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    
    if atividade_id:
        presencas = presencas.filter(atividade__id=atividade_id)
    
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)
    
    if presente:
        presencas = presencas.filter(presente=(presente == 'true'))
    
    # Ordenação
    presencas = presencas.order_by('-data', 'aluno__nome')
    
    # Paginação
    paginator = Paginator(presencas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obter modelos para filtros
    Aluno = get_model_dynamically("alunos", "Aluno")
    AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
    
    alunos = Aluno.objects.all()
    atividades = AtividadeAcademica.objects.all()
    
    context = {
        'presencas': page_obj,
        'page_obj': page_obj,
        'query': query,
        'alunos': alunos,
        'atividades': atividades,
        'filtros': {
            'aluno': aluno_id,
            'atividade': atividade_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'presente': presente
        }
    }
    
    return render(request, 'presencas/listar_presencas.html', context)