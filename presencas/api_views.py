"""
API Views para o aplicativo presencas.
Views REST organizadas e seguindo padrões do projeto.
"""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q, Prefetch
import json
import logging
from importlib import import_module

from .models import RegistroPresenca
from .serializers import (
    PresencaSerializer,
    PresencaDetalhadaSerializer,
    ConfiguracaoPresencaSerializer,
)
from .services import listar_presencas


def _get_model(app_name: str, model_name: str):
    """Importa modelo dinamicamente para evitar circularidade."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


Aluno = _get_model("alunos", "Aluno")
Turma = _get_model("turmas", "Turma")
Matricula = _get_model("matriculas", "Matricula")
AtividadeAcademica = _get_model("atividades", "AtividadeAcademica")

logger = logging.getLogger(__name__)


# FASE 3B: Paginação customizada para melhor performance
class PresencaPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "page_size": self.page_size,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "results": data,
            }
        )


class PresencaViewSet(ModelViewSet):
    """ViewSet para gerenciar presenças via API REST."""

    # FASE 3B: Queryset otimizado com cache estratégico
    queryset = (
        RegistroPresenca.objects.select_related("aluno", "turma__curso", "atividade")
        .prefetch_related(
            Prefetch("aluno", queryset=Aluno.objects.only("id", "nome", "cpf")),
            Prefetch(
                "turma",
                queryset=Turma.objects.select_related("curso").only(
                    "id", "nome", "curso__nome"
                ),
            ),
        )
        .all()
    )

    serializer_class = PresencaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PresencaPagination

    def get_queryset(self):
        """FASE 3B: Customiza queryset com cache inteligente e filtros otimizados."""
        # Cache baseado nos parâmetros de filtro
        filter_params = self.request.query_params.copy()
        cache_key = f"presencas_api_{hash(str(sorted(filter_params.items())))}"

        cached_ids = cache.get(cache_key)
        if cached_ids:
            # Usar apenas IDs em cache para evitar problemas de serialização
            queryset = self.queryset.filter(id__in=cached_ids)
            logger.debug(f"API Cache hit: {cache_key}")
        else:
            queryset = self.queryset

            # Filtros via query parameters otimizados
            aluno_cpf = filter_params.get("aluno_cpf")
            turma_id = filter_params.get("turma_id")
            atividade_id = filter_params.get("atividade_id")
            data_inicio = filter_params.get("data_inicio")
            data_fim = filter_params.get("data_fim")
            presente = filter_params.get("presente")
            status_param = filter_params.get("status")

            # Construir filtros de forma eficiente
            filters = Q()

            if aluno_cpf:
                filters &= Q(aluno__cpf=aluno_cpf)

            if turma_id:
                filters &= Q(turma_id=turma_id)

            if atividade_id:
                filters &= Q(atividade_id=atividade_id)

            if data_inicio:
                filters &= Q(data__gte=data_inicio)

            if data_fim:
                filters &= Q(data__lte=data_fim)

            if presente is not None:
                filters &= Q(status=("P" if presente.lower() == "true" else "F"))

            if status_param:
                filters &= Q(status=status_param)

            queryset = queryset.filter(filters) if filters else queryset

            # Cache apenas os IDs para reduzir uso de memória
            ids = list(
                queryset.values_list("id", flat=True)[:1000]
            )  # Limite para cache
            cache.set(cache_key, ids, 300)  # 5 minutos
            logger.debug(f"API Cache set: {cache_key} with {len(ids)} items")

        return queryset.order_by("-data", "id")  # ID como desempate

    @action(detail=False, methods=["get"], url_path="listar_presencas")
    def listar_presencas_action(self, request):
        """Lista todas as presenças."""
        try:
            tipo_presenca = request.query_params.get("tipo", "todas")
            presencas = listar_presencas(tipo_presenca)

            # Paginação
            page = self.paginate_queryset(presencas)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(presencas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Erro ao listar presenças: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    


# Mantendo as funções existentes para compatibilidade


@login_required
@require_POST
def obter_alunos_por_turmas(request):
    """
    API para obter alunos de turmas específicas.

    Retorna lista de alunos e atividades, ou mensagem de erro padronizada.
    """
    try:
        # Obter dados do corpo da requisição
        data = json.loads(request.body)
        turmas_ids = data.get("turmas_ids", [])

        if not turmas_ids:
            return JsonResponse({"error": "Nenhuma turma selecionada."}, status=400)

        # Obter turmas
        turmas = Turma.objects.filter(id__in=turmas_ids)

        if not turmas.exists():
            return JsonResponse(
                {"error": "Nenhuma turma encontrada com os IDs fornecidos."}, status=404
            )

        # Obter matrículas ativas nas turmas
        matriculas = Matricula.objects.filter(
            turma__in=turmas, status="A"
        ).select_related("aluno")

        # Obter alunos únicos
        alunos = []
        alunos_ids = set()

        for matricula in matriculas:
            if matricula.aluno.cpf not in alunos_ids:
                alunos.append(
                    {
                        "cpf": matricula.aluno.cpf,
                        "nome": matricula.aluno.nome,
                        "foto": matricula.aluno.foto.url
                        if matricula.aluno.foto
                        else None,
                        "numero_iniciatico": matricula.aluno.numero_iniciatico,
                    }
                )
                alunos_ids.add(matricula.aluno.cpf)

        # Obter atividades
        atividades = AtividadeAcademica.objects.all()

        atividades_data = [
            {
                "id": atividade.id,
                "titulo": atividade.titulo,
                "descricao": atividade.descricao,
            }
            for atividade in atividades
        ]

        return JsonResponse({"alunos": alunos, "atividades": atividades_data})

    except Exception as e:
        logger.error("Erro ao obter alunos por turmas: %s", e, exc_info=True)
        return JsonResponse(
            {
                "error": "Ocorreu um erro inesperado ao buscar alunos. Tente novamente mais tarde."
            },
            status=500,
        )


@login_required
@require_GET
def obter_atividades_por_data(request):
    """API para obter atividades disponíveis em uma data específica."""
    try:
        data = request.GET.get("data")

        if not data:
            return JsonResponse({"error": "Data não fornecida."}, status=400)

        # Obter atividades para a data
        atividades = AtividadeAcademica.objects.filter(data_inicio__date=data)

        atividades_data = [
            {
                "id": atividade.id,
                "titulo": atividade.titulo,
                "descricao": atividade.descricao,
            }
            for atividade in atividades
        ]

        return JsonResponse({"atividades": atividades_data})

    except Exception as e:
        logger.error("Erro ao obter atividades por data: %s", e, exc_info=True)
        return JsonResponse(
            {"error": f"Erro ao obter atividades: {str(e)}"}, status=500
        )


@login_required
@require_POST
def salvar_presencas_multiplas(request):
    """API para salvar múltiplas presenças de uma vez."""
    try:
        # Obter dados do corpo da requisição
        data = json.loads(request.body)
        presencas_data = data.get("presencas", [])

        if not presencas_data:
            return JsonResponse({"error": "Nenhuma presença para salvar."}, status=400)

        # Salvar presenças em uma transação
        with transaction.atomic():
            presencas_salvas = 0

            for presenca_data in presencas_data:
                aluno_id = presenca_data.get("aluno_id")
                atividade_id = presenca_data.get("atividade_id")
                data_presenca = presenca_data.get("data")
                situacao = presenca_data.get("situacao")
                justificativa = presenca_data.get("justificativa", "")

                # Validar dados
                if not all([aluno_id, atividade_id, data_presenca, situacao]):
                    continue

                # Obter aluno e atividade
                try:
                    aluno = Aluno.objects.get(cpf=aluno_id)
                    atividade = AtividadeAcademica.objects.get(id=atividade_id)
                except (Aluno.DoesNotExist, AtividadeAcademica.DoesNotExist):
                    continue

                # Verificar se já existe presença para este aluno/atividade/data
                presenca, created = Presenca.objects.update_or_create(
                    aluno=aluno,
                    atividade=atividade,
                    data=data_presenca,
                    defaults={
                        "situacao": situacao,
                        "justificativa": justificativa
                        if situacao == "JUSTIFICADO"
                        else "",
                    },
                )

                presencas_salvas += 1

            return JsonResponse(
                {
                    "success": True,
                    "message": f"{presencas_salvas} presenças salvas com sucesso.",
                }
            )

    except Exception as e:
        logger.error("Erro ao salvar presenças múltiplas: %s", e, exc_info=True)
        return JsonResponse(
            {"error": f"Erro ao salvar presenças: {str(e)}"}, status=500
        )
