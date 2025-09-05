import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from importlib import import_module
from rest_framework import viewsets
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Aluno
from .serializers import AlunoSerializer
from .services import listar_historico_aluno

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


@login_required
@permission_required("alunos.view_aluno", raise_exception=True)
def verificar_elegibilidade_endpoint(request, cpf):
    """API endpoint para verificar se um aluno pode ser instrutor."""
    try:
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)

        # Verificar se o aluno está ativo
        if aluno.situacao != "ATIVO":
            return JsonResponse(
                {
                    "elegivel": False,
                    "motivo": (
                        f"O aluno não está ativo. "
                        f"Situação atual: {aluno.get_situacao_display()}"
                    ),
                }
            )

        # Verificar se o aluno pode ser instrutor
        if hasattr(aluno, "pode_ser_instrutor"):
            pode_ser_instrutor = aluno.pode_ser_instrutor

            if not pode_ser_instrutor:
                return JsonResponse(
                    {
                        "elegivel": False,
                        "motivo": "O aluno não atende aos requisitos para ser "
                        "instrutor.",
                    }
                )
        else:
            # Se o método não existir, considerar elegível por padrão
            logger.warning(
                f"Método 'pode_ser_instrutor' não encontrado para o aluno {cpf}"
            )
            return JsonResponse({"elegivel": True})

        return JsonResponse({"elegivel": True})
    except Exception as e:
        logger.error(
            f"Erro ao verificar elegibilidade do aluno {cpf}: {str(e)}", exc_info=True
        )
        return JsonResponse(
            {"elegivel": False, "motivo": f"Erro na verificação: {str(e)}"}, status=500
        )


class AlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que os alunos sejam visualizados ou editados.
    """

    queryset = Aluno.objects.all().order_by("nome")
    serializer_class = AlunoSerializer


@login_required
@permission_required("alunos.view_aluno", raise_exception=True)
def listar_historico_aluno_api(request, aluno_id):
    """
    API endpoint para listar o histórico de registros de um aluno, com paginação.
    """
    try:
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        historico_list = listar_historico_aluno(aluno)  # Usa a função de serviço

        page = request.GET.get("page", 1)
        # Garante que page_size seja inteiro
        page_size = int(request.GET.get("page_size", 25))

        paginator = Paginator(historico_list, page_size)
        try:
            historico_page = paginator.page(page)
        except PageNotAnInteger:
            historico_page = paginator.page(1)
        except EmptyPage:
            historico_page = paginator.page(paginator.num_pages)

        results = []
        for item in historico_page:
            results.append(
                {
                    "id": item.id,
                    "tipo_codigo": item.codigo.tipo.nome
                    if item.codigo and item.codigo.tipo
                    else "N/A",
                    "codigo": item.codigo.nome if item.codigo else "N/A",
                    "descricao": item.codigo.descricao if item.codigo else "N/A",
                    "data_os": item.data_os.isoformat() if item.data_os else None,
                    "observacoes": item.observacoes,
                }
            )

        return JsonResponse(
            {
                "status": "success",
                "results": results,
                "page": historico_page.number,
                "total_pages": paginator.num_pages,
                "count": paginator.count,
            }
        )
    except Exception as e:
        logger.error(
            f"Erro ao listar histórico do aluno {aluno_id}: {e}", exc_info=True
        )
        return JsonResponse(
            {"status": "error", "message": "Erro interno do servidor."}, status=500
        )
