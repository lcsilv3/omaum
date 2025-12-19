"""Views para o gerenciamento de matrículas usando Django Rest Framework (DRF).

Este módulo contém o ViewSet principal para operações CRUD e ações customizadas
relacionadas ao modelo Matricula.
"""

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from matriculas.models import Matricula
from matriculas.serializers import MatriculaSerializer


class MatriculaViewSet(ModelViewSet):
    """ViewSet para gerenciar matrículas."""

    queryset = Matricula.objects.select_related("aluno", "turma").all()
    serializer_class = MatriculaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="listar")
    def listar_matriculas(self, request):
        """Lista todas as matrículas."""
        return Response(self.serializer_class(self.queryset, many=True).data)

    @action(detail=True, methods=["get"], url_path="detalhar")
    def detalhar_matricula(self, request, pk=None):  # pylint: disable=no-member
        """Exibe os detalhes de uma matrícula."""
        matricula = self.get_object()
        return Response(self.serializer_class(matricula).data)

    @action(detail=False, methods=["post"], url_path="realizar")
    def realizar_matricula(self, request):
        """Realiza uma nova matrícula."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            data_matricula=timezone.now().date(),
            status='A',
            status="A",
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar_matricula(self, request, pk=None):  # pylint: disable=no-member
        """Cancela uma matrícula existente."""
        matricula = self.get_object()
        matricula.status = "C"
        matricula.save()
        return Response(
            {"detail": "Matrícula cancelada com sucesso."},
            status=status.HTTP_200_OK,
        )

    # O argumento `request` é necessário para compatibilidade com DRF,
    # mesmo que não seja usado diretamente.
    # O argumento `pk` é necessário para identificar o recurso em
    # ações detalhadas.
