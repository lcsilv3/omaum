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

@login_required
def search_instrutores(request):
    """API endpoint para buscar alunos elegíveis para serem instrutores."""
    try:
        from importlib import import_module
        Aluno = import_module("alunos.models").Aluno
        
        query = request.GET.get("q", "")
        
        # Buscar apenas alunos ativos
        alunos = Aluno.objects.filter(situacao="ATIVO")
        
        # Se houver uma consulta, filtrar por ela
        if query and len(query) >= 2:
            alunos = alunos.filter(
                Q(nome__icontains=query) |
                Q(cpf__icontains=query) |
                Q(numero_iniciatico__icontains=query)
            )
        
        # Limitar a 10 resultados
        alunos = alunos[:10]
        
        # Formatar resultados
        results = []
        for aluno in alunos:
            results.append({
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                "foto": aluno.foto.url if hasattr(aluno, "foto") and aluno.foto else None,
                "situacao": aluno.get_situacao_display() if hasattr(aluno, "get_situacao_display") else "",
                "situacao_codigo": aluno.situacao,
                "esta_ativo": aluno.esta_ativo if hasattr(aluno, "esta_ativo") else False,
                "elegivel": aluno.pode_ser_instrutor if hasattr(aluno, "pode_ser_instrutor") else True
            })
        
        logger.info(f"Busca por '{query}' retornou {len(results)} resultados")
        return JsonResponse(results, safe=False)
    except Exception as e:
        logger.error(f"Error in search_instrutores: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

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

@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
def verificar_elegibilidade_endpoint(request, cpf):
    """API endpoint para verificar se um aluno pode ser instrutor."""
    try:
        from importlib import import_module
        Aluno = import_module("alunos.models").Aluno
        
        aluno = Aluno.objects.get(cpf=cpf)
        
        # Verificar se o aluno está ativo
        if aluno.situacao != "ATIVO":
            return JsonResponse({
                "elegivel": False,
                "motivo": f"O aluno não está ativo. Situação atual: {aluno.get_situacao_display()}"
            })
        
        # Verificar se o aluno pode ser instrutor
        if hasattr(aluno, 'pode_ser_instrutor'):
            pode_ser_instrutor = aluno.pode_ser_instrutor
            
            if not pode_ser_instrutor:
                return JsonResponse({
                    "elegivel": False,
                    "motivo": "O aluno não atende aos requisitos para ser instrutor."
                })
        else:
            # Se o método não existir, considerar elegível por padrão
            return JsonResponse({"elegivel": True})
        
        return JsonResponse({"elegivel": True})
    except Aluno.DoesNotExist:
        return JsonResponse({
            "elegivel": False,
            "motivo": "Aluno não encontrado."
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "elegivel": False,
            "motivo": f"Erro na busca: {str(e)}"
        }, status=500)

@login_required
def get_aluno_detalhes(request, cpf):
    """API endpoint para obter detalhes específicos de um aluno."""
    try:
        from importlib import import_module
        Aluno = import_module("alunos.models").Aluno
        
        aluno = Aluno.objects.get(cpf=cpf)
        
        # Verificar se o aluno é instrutor em alguma turma
        turmas_como_instrutor = False
        try:
            from django.db.models import Q
            Turma = import_module("turmas.models").Turma
            turmas_como_instrutor = Turma.objects.filter(
                Q(instrutor=aluno) |
                Q(instrutor_auxiliar=aluno) |
                Q(auxiliar_instrucao=aluno)
            ).exists()
        except Exception as e:
            logger.error(f"Erro ao verificar turmas como instrutor: {str(e)}")
        
        # Obter turmas em que o aluno está matriculado
        turmas_matriculado = []
        try:
            Matricula = import_module("matriculas.models").Matricula
            matriculas = Matricula.objects.filter(aluno=aluno, status="A")
            turmas_matriculado = [
                {
                    "id": m.turma.id,
                    "nome": m.turma.nome,
                    "curso": m.turma.curso.nome if m.turma.curso else "Sem curso"
                }
                for m in matriculas
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar matrículas: {str(e)}")
        
        return JsonResponse({
            "success": True,
            "e_instrutor": turmas_como_instrutor,
            "turmas": turmas_matriculado,
            "pode_ser_instrutor": getattr(aluno, 'pode_ser_instrutor', False)
        })
    except Aluno.DoesNotExist:
        return JsonResponse({"success": False, "error": "Aluno não encontrado"}, status=404)
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do aluno: {str(e)}", exc_info=True)
        return JsonResponse({"success": False, "error": str(e)}, status=500)