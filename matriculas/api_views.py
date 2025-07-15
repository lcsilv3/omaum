"""
API Views para o aplicativo matriculas.
Views REST organizadas e seguindo padrões do projeto.
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError

from .models import Matricula
from .serializers import MatriculaSerializer
from .services import (
    listar_matriculas,
    obter_matricula_por_id,
    criar_matricula,
    atualizar_matricula,
    cancelar_matricula,
    excluir_matricula,
    obter_matriculas_ativas_por_aluno,
    obter_matriculas_por_turma,
    verificar_dependencias_matricula
)
from .repositories import MatriculaRepository


class MatriculaViewSet(ModelViewSet):
    """ViewSet para gerenciar matrículas via API REST."""
    
    queryset = Matricula.objects.select_related("aluno", "turma").all()
    serializer_class = MatriculaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Customiza o queryset com filtros opcionais."""
        queryset = self.queryset
        
        # Filtros via query parameters
        aluno_cpf = self.request.query_params.get('aluno_cpf')
        turma_id = self.request.query_params.get('turma_id')
        status_filter = self.request.query_params.get('status')
        
        if aluno_cpf:
            queryset = queryset.filter(aluno__cpf=aluno_cpf)
        
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-data_matricula')
    
    def create(self, request, *args, **kwargs):
        """Cria uma nova matrícula usando serviços."""
        try:
            dados_matricula = {
                'aluno_cpf': request.data.get('aluno_cpf'),
                'turma_id': request.data.get('turma_id'),
                'data_matricula': request.data.get('data_matricula'),
                'status': request.data.get('status', 'A')
            }
            
            matricula = criar_matricula(dados_matricula)
            serializer = self.get_serializer(matricula)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Erro interno: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, *args, **kwargs):
        """Atualiza uma matrícula usando serviços."""
        try:
            matricula_id = kwargs.get('pk')
            dados_atualizacao = request.data
            
            matricula = atualizar_matricula(matricula_id, dados_atualizacao)
            serializer = self.get_serializer(matricula)
            return Response(serializer.data)
            
        except ValidationError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Erro interno: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, *args, **kwargs):
        """Exclui uma matrícula usando serviços."""
        try:
            matricula_id = kwargs.get('pk')
            excluir_matricula(matricula_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except ValidationError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Erro interno: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=["get"], url_path="listar_matriculas")
    def listar_matriculas_action(self, request):
        """Lista todas as matrículas."""
        try:
            matriculas = listar_matriculas()
            serializer = self.get_serializer(matriculas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Erro ao listar matrículas: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=["get"], url_path="detalhar_matricula")
    def detalhar_matricula_action(self, request, pk=None):
        """Exibe os detalhes de uma matrícula."""
        try:
            matricula = obter_matricula_por_id(pk)
            if not matricula:
                return Response(
                    {"error": "Matrícula não encontrada"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = self.get_serializer(matricula)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Erro ao detalhar matrícula: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=["post"], url_path="realizar_matricula")
    def realizar_matricula_action(self, request):
        """Realiza uma nova matrícula."""
        return self.create(request)
    
    @action(detail=True, methods=["post"], url_path="cancelar_matricula")
    def cancelar_matricula_action(self, request, pk=None):
        """Cancela uma matrícula existente."""
        try:
            motivo = request.data.get('motivo', '')
            matricula = cancelar_matricula(pk, motivo)
            serializer = self.get_serializer(matricula)
            return Response({
                "detail": "Matrícula cancelada com sucesso.",
                "matricula": serializer.data
            })
        except ValidationError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Erro interno: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=["get"], url_path="por_aluno/(?P<aluno_cpf>[^/.]+)")
    def matriculas_por_aluno(self, request, aluno_cpf=None):
        """Lista matrículas de um aluno específico."""
        try:
            matriculas = obter_matriculas_ativas_por_aluno(aluno_cpf)
            serializer = self.get_serializer(matriculas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar matrículas do aluno: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=["get"], url_path="por_turma/(?P<turma_id>[^/.]+)")
    def matriculas_por_turma(self, request, turma_id=None):
        """Lista matrículas de uma turma específica."""
        try:
            matriculas = obter_matriculas_por_turma(turma_id)
            serializer = self.get_serializer(matriculas, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar matrículas da turma: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=["get"], url_path="dependencias")
    def verificar_dependencias(self, request, pk=None):
        """Verifica dependências de uma matrícula."""
        try:
            dependencias = verificar_dependencias_matricula(pk)
            return Response(dependencias)
        except Exception as e:
            return Response(
                {"error": f"Erro ao verificar dependências: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=["get"], url_path="estatisticas")
    def obter_estatisticas(self, request):
        """Obtém estatísticas das matrículas."""
        try:
            estatisticas = MatriculaRepository.obter_estatisticas_gerais()
            return Response(estatisticas)
        except Exception as e:
            return Response(
                {"error": f"Erro ao obter estatísticas: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=["get"], url_path="filtrar")
    def filtrar_matriculas(self, request):
        """Filtra matrículas com múltiplos critérios."""
        try:
            filtros = {
                'aluno_cpf': request.query_params.get('aluno_cpf'),
                'turma_id': request.query_params.get('turma_id'),
                'status': request.query_params.get('status'),
                'curso_id': request.query_params.get('curso_id'),
                'search': request.query_params.get('search'),
                'data_inicio': request.query_params.get('data_inicio'),
                'data_fim': request.query_params.get('data_fim'),
            }
            
            # Remove filtros vazios
            filtros = {k: v for k, v in filtros.items() if v}
            
            matriculas = MatriculaRepository.buscar_com_filtros(filtros)
            
            # Paginação
            page = self.paginate_queryset(matriculas)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(matriculas, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": f"Erro ao filtrar matrículas: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
