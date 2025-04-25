"""Views relacionadas a endpoints de API."""
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
import logging
import traceback
from alunos.utils import get_aluno_model
from ..services import verificar_elegibilidade_instrutor as verificar_elegibilidade_service

logger = logging.getLogger(__name__)

@require_GET
def search_alunos(request):
    """API para buscar alunos por nome, CPF ou número iniciático."""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Buscar alunos que correspondam à consulta
    Aluno = get_aluno_model()
    alunos = Aluno.objects.filter(
        nome__icontains=query
    )[:10]  # Limitar a 10 resultados
    
    # Formatar resultados
    results = []
    for aluno in alunos:
        results.append({
            'cpf': aluno.cpf,
            'nome': aluno.nome,
            'numero_iniciatico': aluno.numero_iniciatico or 'N/A',
            'email': aluno.email or 'N/A',
            'foto': aluno.foto.url if aluno.foto else None,
        })
    
    return JsonResponse(results, safe=False)

@require_GET
def search_instrutores(request):
    """API para buscar alunos que podem ser instrutores."""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Buscar alunos que correspondam à consulta
    Aluno = get_aluno_model()
    alunos = Aluno.objects.filter(
        nome__icontains=query
    )[:10]  # Limitar a 10 resultados
    
    # Formatar resultados
    results = []
    for aluno in alunos:
        results.append({
            'cpf': aluno.cpf,
            'nome': aluno.nome,
            'numero_iniciatico': aluno.numero_iniciatico or 'N/A',
            'situacao': aluno.get_situacao_display(),
            'situacao_codigo': aluno.situacao,
            'foto': aluno.foto.url if aluno.foto else None,
        })
    
    return JsonResponse(results, safe=False)

@login_required
def get_aluno(request, cpf):
    """API endpoint para obter dados de um aluno específico."""
    try:
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        return JsonResponse(
            {
                "success": True,
                "aluno": {
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                    "foto": (
                        aluno.foto.url
                        if hasattr(aluno, "foto") and aluno.foto
                        else None
                    ),
                },
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=404)

@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
def verificar_elegibilidade_instrutor_api(request, cpf):
    """API endpoint para verificar se um aluno pode ser instrutor."""
    try:
        # Configurar logging
        logger.info(f"Verificando elegibilidade do instrutor com CPF: {cpf}")
        
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        
        # Usar o serviço para verificar elegibilidade
        resultado = verificar_elegibilidade_service(aluno)
        return JsonResponse(resultado)
        
    except Exception as e:
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        logger.error(f"Erro ao verificar elegibilidade: {error_msg}")
        logger.error(f"Traceback: {stack_trace}")
        return JsonResponse(
            {"elegivel": False, "motivo": f"Erro na busca: {error_msg}"},
            status=500
        )

@require_GET
def verificar_elegibilidade_endpoint(request, cpf):
    """
    Verifica se um aluno é elegível para ser instrutor.
    
    Args:
        request: O objeto de requisição HTTP
        cpf: O CPF do aluno a ser verificado
        
    Returns:
        JsonResponse com informações sobre a elegibilidade do aluno
    """
    try:
        Aluno = get_aluno_model()
        aluno = Aluno.objects.get(cpf=cpf)
        
        # Verificar critérios de elegibilidade
        # Por exemplo: situação ativa, cursos concluídos, etc.
        elegivel = aluno.situacao == 'A'  # Simplificado - apenas verifica se está ativo
        
        # Motivo da inelegibilidade, se aplicável
        motivo = ""
        if not elegivel:
            motivo = "O aluno precisa estar com situação ATIVA para ser instrutor."
        
        return JsonResponse({
            'elegivel': elegivel,
            'motivo': motivo,
            'nome': aluno.nome,
            'cpf': aluno.cpf,
            'numero_iniciatico': aluno.numero_iniciatico or 'N/A',
            'situacao': aluno.get_situacao_display()
        })
    except Aluno.DoesNotExist:
        return JsonResponse({
            'elegivel': False,
            'motivo': "Aluno não encontrado."
        }, status=404)

@require_GET
def get_aluno_detalhes(request, cpf):
    """Obtém detalhes de um aluno específico."""
    Aluno = get_aluno_model()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    # Verificar se é instrutor (simplificado)
    e_instrutor = False  # Lógica para verificar se é instrutor
    turmas = []  # Lógica para obter turmas do instrutor
    
    return JsonResponse({
        'cpf': aluno.cpf,
        'nome': aluno.nome,
        'numero_iniciatico': aluno.numero_iniciatico or 'N/A',
        'situacao': aluno.get_situacao_display(),
        'e_instrutor': e_instrutor,
        'turmas': turmas,
    })