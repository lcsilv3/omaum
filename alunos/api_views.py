import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from importlib import import_module
from rest_framework import viewsets

from .models import Aluno
from .serializers import AlunoSerializer

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
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
        if hasattr(aluno, 'pode_ser_instrutor'):
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
            f"Erro ao verificar elegibilidade do aluno {cpf}: {str(e)}",
            exc_info=True
        )
        return JsonResponse(
            {"elegivel": False, "motivo": f"Erro na verificação: {str(e)}"},
            status=500
        )


class AlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que os alunos sejam visualizados ou editados.
    """
    queryset = Aluno.objects.all().order_by('nome')
    serializer_class = AlunoSerializer