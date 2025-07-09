"""
API Views para o app Atividades.
Este módulo contém as views da API REST para atividades acadêmicas
e ritualísticas, seguindo os padrões do Django REST Framework.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from importlib import import_module

from .serializers import (
    AtividadeAcademicaSerializer,
    AtividadeRitualisticaSerializer
)
from .services import (
    AtividadeAcademicaService,
    AtividadeRitualisticaService
)


def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    try:
        module = import_module(f"{app_name}.models")
        return getattr(module, model_name)
    except (ImportError, AttributeError):
        return None


class AtividadeAcademicaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de atividades acadêmicas.
    
    Provê operações CRUD completas para atividades acadêmicas.
    """
    serializer_class = AtividadeAcademicaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo_atividade', 'status', 'curso', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['data_inicio', 'nome']
    ordering = ['-data_inicio']

    def get_queryset(self):
        """Retorna o queryset de atividades acadêmicas."""
        return AtividadeAcademicaService.listar_atividades()

    def create(self, request):
        """Cria uma nova atividade acadêmica."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                atividade = AtividadeAcademicaService.criar_atividade(
                    serializer.validated_data
                )
                response_serializer = self.get_serializer(atividade)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Atualiza uma atividade acadêmica."""
        atividade = self.get_object()
        serializer = self.get_serializer(atividade, data=request.data)
        if serializer.is_valid():
            try:
                atividade_atualizada = (
                    AtividadeAcademicaService.atualizar_atividade(
                        pk, serializer.validated_data
                    )
                )
                if atividade_atualizada:
                    response_serializer = self.get_serializer(
                        atividade_atualizada
                    )
                    return Response(response_serializer.data)
                return Response(
                    {'error': 'Atividade não encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Remove uma atividade acadêmica."""
        try:
            if AtividadeAcademicaService.deletar_atividade(pk):
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Atividade não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Lista apenas as atividades acadêmicas ativas."""
        atividades = AtividadeAcademicaService.listar_atividades_ativas()
        serializer = self.get_serializer(atividades, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_turma(self, request):
        """Lista atividades acadêmicas por turma."""
        turma_id = request.query_params.get('turma_id')
        if not turma_id:
            return Response(
                {'error': 'turma_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        atividades = AtividadeAcademicaService.listar_atividades_por_turma(
            turma_id
        )
        serializer = self.get_serializer(atividades, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_curso(self, request):
        """Lista atividades acadêmicas por curso."""
        curso_id = request.query_params.get('curso_id')
        if not curso_id:
            return Response(
                {'error': 'curso_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        atividades = AtividadeAcademicaService.listar_atividades_por_curso(
            curso_id
        )
        serializer = self.get_serializer(atividades, many=True)
        return Response(serializer.data)


class AtividadeRitualisticaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de atividades ritualísticas.
    
    Provê operações CRUD completas para atividades ritualísticas.
    """
    serializer_class = AtividadeRitualisticaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'turma', 'ativo']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['data', 'nome']
    ordering = ['-data']

    def get_queryset(self):
        """Retorna o queryset de atividades ritualísticas."""
        return AtividadeRitualisticaService.listar_atividades()

    def create(self, request):
        """Cria uma nova atividade ritualística."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                atividade = AtividadeRitualisticaService.criar_atividade(
                    serializer.validated_data
                )
                response_serializer = self.get_serializer(atividade)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """Lista apenas as atividades ritualísticas ativas."""
        atividades = AtividadeRitualisticaService.listar_atividades_ativas()
        serializer = self.get_serializer(atividades, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_turma(self, request):
        """Lista atividades ritualísticas por turma."""
        turma_id = request.query_params.get('turma_id')
        if not turma_id:
            return Response(
                {'error': 'turma_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        atividades = AtividadeRitualisticaService.listar_atividades_por_turma(
            turma_id
        )
        serializer = self.get_serializer(atividades, many=True)
        return Response(serializer.data)
