"""
API Views para o app relatorios.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Relatorio
from .serializers import (
    RelatorioSerializer,
    RelatorioCreateSerializer,
    RelatorioUpdateSerializer,
)
from .services import RelatorioService


class RelatorioViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de Relatório."""

    queryset = Relatorio.objects.all()
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = RelatorioService()

    def get_serializer_class(self):
        """Retorna o serializer apropriado baseado na action."""
        if self.action == "create":
            return RelatorioCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return RelatorioUpdateSerializer
        return RelatorioSerializer

    def list(self, request):
        """Lista todos os relatórios."""
        try:
            relatorios = self.service.obter_relatorios_ordenados()
            serializer = self.get_serializer(relatorios, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        """Retorna um relatório específico."""
        try:
            relatorio = self.service.obter_por_id(pk)
            if not relatorio:
                return Response(
                    {"error": "Relatório não encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = self.get_serializer(relatorio)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request):
        """Cria um novo relatório."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                relatorio = self.service.criar_relatorio(
                    titulo=serializer.validated_data["titulo"],
                    conteudo=serializer.validated_data["conteudo"],
                )
                response_serializer = RelatorioSerializer(relatorio)
                return Response(
                    response_serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):
        """Atualiza um relatório existente."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                relatorio = self.service.atualizar_relatorio(
                    relatorio_id=pk,
                    titulo=serializer.validated_data.get("titulo"),
                    conteudo=serializer.validated_data.get("conteudo"),
                )
                if not relatorio:
                    return Response(
                        {"error": "Relatório não encontrado"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                response_serializer = RelatorioSerializer(relatorio)
                return Response(response_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, pk=None):
        """Atualiza parcialmente um relatório existente."""
        try:
            relatorio = self.service.obter_por_id(pk)
            if not relatorio:
                return Response(
                    {"error": "Relatório não encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = self.get_serializer(relatorio, data=request.data, partial=True)
            if serializer.is_valid():
                relatorio_atualizado = self.service.atualizar_relatorio(
                    relatorio_id=pk,
                    titulo=serializer.validated_data.get("titulo"),
                    conteudo=serializer.validated_data.get("conteudo"),
                )

                response_serializer = RelatorioSerializer(relatorio_atualizado)
                return Response(response_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        """Remove um relatório."""
        try:
            if self.service.excluir_relatorio(pk):
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"error": "Relatório não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def buscar(self, request):
        """Busca relatórios por termo."""
        try:
            termo = request.query_params.get("termo", "")
            relatorios = self.service.buscar_relatorios(termo)
            serializer = self.get_serializer(relatorios, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def estatisticas(self, request):
        """Retorna estatísticas dos relatórios."""
        try:
            stats = self.service.obter_estatisticas()
            stats_serializer = {
                "total_relatorios": stats["total_relatorios"],
                "relatorios_recentes": RelatorioSerializer(
                    stats["relatorios_recentes"], many=True
                ).data,
            }
            return Response(stats_serializer)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
