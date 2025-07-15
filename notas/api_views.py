"""
API views para o app Notas - REST padronizado
"""
import importlib
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import Http404


class NotaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar notas
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Importação dinâmica do serializer"""
        try:
            serializers_module = importlib.import_module('notas.serializers')
            return getattr(serializers_module, 'NotaSerializer')
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Erro ao importar NotaSerializer: {e}")
    
    def get_service(self):
        """Importação dinâmica do service"""
        try:
            services_module = importlib.import_module('notas.services')
            return getattr(services_module, 'NotaService')()
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Erro ao importar NotaService: {e}")
    
    def get_queryset(self):
        """Retorna queryset através do service"""
        service = self.get_service()
        return service.get_all_notas()
    
    def list(self, request):
        """Lista todas as notas"""
        try:
            service = self.get_service()
            notas = service.get_all_notas()
            serializer = self.get_serializer_class()(notas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao listar notas: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Retorna uma nota específica"""
        try:
            service = self.get_service()
            nota = service.get_nota_by_id(pk)
            if not nota:
                raise Http404("Nota não encontrada")
            serializer = self.get_serializer_class()(nota)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {'error': 'Nota não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao buscar nota: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def create(self, request):
        """Cria uma nova nota"""
        try:
            service = self.get_service()
            serializer = self.get_serializer_class()(data=request.data)
            
            if serializer.is_valid():
                nota = service.create_nota(serializer.validated_data)
                response_serializer = self.get_serializer_class()(nota)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f'Erro ao criar nota: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def update(self, request, pk=None):
        """Atualiza uma nota existente"""
        try:
            service = self.get_service()
            nota = service.get_nota_by_id(pk)
            if not nota:
                raise Http404("Nota não encontrada")
            
            serializer = self.get_serializer_class()(nota, data=request.data)
            if serializer.is_valid():
                nota_atualizada = service.update_nota(pk, serializer.validated_data)
                response_serializer = self.get_serializer_class()(nota_atualizada)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {'error': 'Nota não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao atualizar nota: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def destroy(self, request, pk=None):
        """Remove uma nota"""
        try:
            service = self.get_service()
            nota = service.get_nota_by_id(pk)
            if not nota:
                raise Http404("Nota não encontrada")
            
            service.delete_nota(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {'error': 'Nota não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao deletar nota: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """Lista notas por aluno"""
        try:
            aluno_id = request.query_params.get('aluno_id')
            if not aluno_id:
                return Response(
                    {'error': 'Parâmetro aluno_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = self.get_service()
            notas = service.get_notas_by_aluno(aluno_id)
            serializer = self.get_serializer_class()(notas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao buscar notas por aluno: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_turma(self, request):
        """Lista notas por turma"""
        try:
            turma_id = request.query_params.get('turma_id')
            if not turma_id:
                return Response(
                    {'error': 'Parâmetro turma_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = self.get_service()
            notas = service.get_notas_by_turma(turma_id)
            serializer = self.get_serializer_class()(notas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao buscar notas por turma: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_atividade(self, request):
        """Lista notas por atividade"""
        try:
            atividade_id = request.query_params.get('atividade_id')
            if not atividade_id:
                return Response(
                    {'error': 'Parâmetro atividade_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = self.get_service()
            notas = service.get_notas_by_atividade(atividade_id)
            serializer = self.get_serializer_class()(notas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao buscar notas por atividade: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def media_aluno(self, request):
        """Calcula média de um aluno"""
        try:
            aluno_id = request.query_params.get('aluno_id')
            if not aluno_id:
                return Response(
                    {'error': 'Parâmetro aluno_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            turma_id = request.query_params.get('turma_id')
            service = self.get_service()
            media = service.calcular_media_aluno(aluno_id, turma_id)
            return Response(media, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao calcular média do aluno: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def media_turma(self, request):
        """Calcula média de uma turma"""
        try:
            turma_id = request.query_params.get('turma_id')
            if not turma_id:
                return Response(
                    {'error': 'Parâmetro turma_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = self.get_service()
            media = service.calcular_media_turma(turma_id)
            return Response(media, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao calcular média da turma: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def relatorio(self, request):
        """Gera relatório de notas"""
        try:
            service = self.get_service()
            relatorio = service.gerar_relatorio_notas(request.query_params.dict())
            return Response(relatorio, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao gerar relatório: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_periodo(self, request):
        """Lista notas por período"""
        try:
            data_inicio = request.query_params.get('data_inicio')
            data_fim = request.query_params.get('data_fim')
            
            if not data_inicio or not data_fim:
                return Response(
                    {'error': 'Parâmetros data_inicio e data_fim são obrigatórios'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = self.get_service()
            notas = service.get_notas_by_periodo(data_inicio, data_fim)
            serializer = self.get_serializer_class()(notas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao buscar notas por período: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
