"""Views relacionadas a endpoints de API."""

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
import logging
import traceback
from ..utils import get_aluno_model
from alunos.services import InstrutorService

logger = logging.getLogger(__name__)


@require_GET
def search_alunos(request):
    """API para buscar alunos por nome, CPF ou número iniciático."""
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse([], safe=False)

    Aluno = get_aluno_model()
    alunos = Aluno.objects.filter(nome__icontains=query)[:10]

    results = []
    for aluno in alunos:
        results.append(
            {
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "email": aluno.email or "N/A",
                "foto": aluno.foto.url if aluno.foto else None,
            }
        )

    return JsonResponse(results, safe=False)


@login_required
def search_instrutores(request):
    """API endpoint para buscar alunos elegíveis para serem instrutores."""
    try:
        from importlib import import_module

        Aluno = import_module("alunos.models").Aluno
        query = request.GET.get("q", "")
        alunos = Aluno.objects.filter(situacao="ATIVO")

        if query and len(query) >= 2:
            alunos = alunos.filter(Q(nome__icontains=query) | Q(cpf__icontains=query))

        alunos = alunos[:10]

        results = []
        for aluno in alunos:
            results.append(
                {
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "foto": aluno.foto.url if hasattr(aluno, "foto") and aluno.foto else None,
                    "situacao": aluno.get_situacao_display() if hasattr(aluno, "get_situacao_display") else "",
                    "situacao_codigo": aluno.situacao,
                    "esta_ativo": aluno.esta_ativo if hasattr(aluno, "esta_ativo") else False,
                    "elegivel": aluno.pode_ser_instrutor if hasattr(aluno, "pode_ser_instrutor") else True,
                }
            )

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
@permission_required("alunos.view_aluno", raise_exception=True)
def verificar_elegibilidade_endpoint(request, cpf):
    """API endpoint para verificar se um aluno pode ser instrutor."""
    try:
        logger.info(f"Verificando elegibilidade do instrutor com CPF: {cpf}")
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        resultado = InstrutorService.verificar_elegibilidade_completa(aluno)
        return JsonResponse(resultado)

    except Exception as e:
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        logger.error(f"Erro ao verificar elegibilidade: {error_msg}")
        logger.error(f"Traceback: {stack_trace}")
        return JsonResponse(
            {"elegivel": False, "motivo": f"Erro na busca: {error_msg}"}, status=500
        )


@login_required
def get_aluno_detalhes(request, cpf):
    """API endpoint para obter detalhes específicos de um aluno."""
    try:
        from importlib import import_module

        Aluno = import_module("alunos.models").Aluno
        aluno = Aluno.objects.get(cpf=cpf)

        turmas_como_instrutor = False
        try:
            from django.db.models import Q
            Turma = import_module("turmas.models").Turma
            turmas_como_instrutor = Turma.objects.filter(
                Q(instrutor=aluno)
                | Q(instrutor_auxiliar=aluno)
                | Q(auxiliar_instrucao=aluno)
            ).exists()
        except Exception as e:
            logger.error(f"Erro ao verificar turmas como instrutor: {str(e)}")

        turmas_matriculado = []
        try:
            Matricula = import_module("matriculas.models").Matricula
            matriculas = Matricula.objects.filter(aluno=aluno, status="A")
            turmas_matriculado = [
                {
                    "id": m.turma.id,
                    "nome": m.turma.nome,
                    "curso": m.turma.curso.nome if m.turma.curso else "Sem curso",
                }
                for m in matriculas
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar matrículas: {str(e)}")

        return JsonResponse(
            {
                "success": True,
                "e_instrutor": turmas_como_instrutor,
                "turmas": turmas_matriculado,
                "pode_ser_instrutor": getattr(aluno, "pode_ser_instrutor", False),
            }
        )
    except Aluno.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Aluno não encontrado"}, status=404
        )
    except Exception as e:
        logger.error(f"Erro ao obter detalhes do aluno: {str(e)}", exc_info=True)
        return JsonResponse({"success": False, "error": str(e)}, status=500)