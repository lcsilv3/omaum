"""
API views para o app Frequencias - REST padronizado
"""
import importlib
import logging
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)


def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    try:
        return importlib.import_module("turmas.models").Turma
    except ImportError:
        return None


def get_models():
    """Obtém os modelos de frequência dinamicamente."""
    try:
        frequencias_models = importlib.import_module("frequencias.models")
        return frequencias_models.FrequenciaMensal, frequencias_models.Configuracao
    except ImportError:
        return None, None


class FrequenciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar frequências
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Importação dinâmica do serializer"""
        try:
            serializers_module = importlib.import_module('frequencias.serializers')
            return getattr(serializers_module, 'FrequenciaSerializer')
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Erro ao importar FrequenciaSerializer: {e}")
    
    def get_service(self):
        """Importação dinâmica do service"""
        try:
            services_module = importlib.import_module('frequencias.services')
            return getattr(services_module, 'FrequenciaService')()
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Erro ao importar FrequenciaService: {e}")
    
    def get_queryset(self):
        """Retorna queryset através do service"""
        service = self.get_service()
        return service.get_all_frequencias()
    
    def list(self, request):
        """Lista todas as frequências"""
        try:
            service = self.get_service()
            frequencias = service.get_all_frequencias()
            serializer = self.get_serializer_class()(frequencias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao listar frequências: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        """Retorna uma frequência específica"""
        try:
            service = self.get_service()
            frequencia = service.get_frequencia_by_id(pk)
            if not frequencia:
                raise Http404("Frequência não encontrada")
            serializer = self.get_serializer_class()(frequencia)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {'error': 'Frequência não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao buscar frequência: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def create(self, request):
        """Cria uma nova frequência"""
        try:
            service = self.get_service()
            serializer = self.get_serializer_class()(data=request.data)
            
            if serializer.is_valid():
                frequencia = service.create_frequencia(serializer.validated_data)
                response_serializer = self.get_serializer_class()(frequencia)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': f'Erro ao criar frequência: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def update(self, request, pk=None):
        """Atualiza uma frequência existente"""
        try:
            service = self.get_service()
            frequencia = service.get_frequencia_by_id(pk)
            if not frequencia:
                raise Http404("Frequência não encontrada")
            
            serializer = self.get_serializer_class()(frequencia, data=request.data)
            if serializer.is_valid():
                frequencia_atualizada = service.update_frequencia(pk, serializer.validated_data)
                response_serializer = self.get_serializer_class()(frequencia_atualizada)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {'error': 'Frequência não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao atualizar frequência: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @transaction.atomic
    def destroy(self, request, pk=None):
        """Remove uma frequência"""
        try:
            service = self.get_service()
            frequencia = service.get_frequencia_by_id(pk)
            if not frequencia:
                raise Http404("Frequência não encontrada")
            
            service.delete_frequencia(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {'error': 'Frequência não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao deletar frequência: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def calcular_frequencia(self, request, pk=None):
        """Calcula a frequência de um aluno em uma turma"""
        try:
            service = self.get_service()
            frequencia = service.get_frequencia_by_id(pk)
            if not frequencia:
                raise Http404("Frequência não encontrada")
            
            resultado = service.calcular_frequencia(pk)
            return Response(resultado, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {'error': 'Frequência não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao calcular frequência: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_turma(self, request):
        """Lista frequências por turma"""
        try:
            turma_id = request.query_params.get('turma_id')
            if not turma_id:
                return Response(
                    {'error': 'Parâmetro turma_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = self.get_service()
            frequencias = service.get_frequencias_by_turma(turma_id)
            serializer = self.get_serializer_class()(frequencias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao buscar frequências por turma: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """Lista frequências por aluno"""
        try:
            aluno_id = request.query_params.get('aluno_id')
            if not aluno_id:
                return Response(
                    {'error': 'Parâmetro aluno_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            service = self.get_service()
            frequencias = service.get_frequencias_by_aluno(aluno_id)
            serializer = self.get_serializer_class()(frequencias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Erro ao buscar frequências por aluno: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def relatorio_frequencia(self, request):
        """Gera relatório de frequência"""
        try:
            service = self.get_service()
            relatorio = service.gerar_relatorio_frequencia(request.query_params.dict())
            return Response(relatorio, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Erro ao obter dados da frequência: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Erro ao gerar relatório: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@login_required
def obter_dados_painel_frequencias(request):
    """API para obter dados para o painel de frequências."""
    try:
        # Obter parâmetros
        turma_id = request.GET.get('turma_id')
        mes_inicio = int(request.GET.get('mes_inicio', 1))
        ano_inicio = int(request.GET.get('ano_inicio', datetime.now().year))
        mes_fim = int(request.GET.get('mes_fim', 12))
        ano_fim = int(request.GET.get('ano_fim', datetime.now().year))
        
        # Validar parâmetros
        if not turma_id:
            return JsonResponse({
                'success': False,
                'message': 'Turma não especificada'
            }, status=400)
        
        # Obter turma
        Turma = get_turma_model()
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Calcular período em meses
        data_inicio = ano_inicio * 12 + mes_inicio
        data_fim = ano_fim * 12 + mes_fim
        
        # Obter frequências no período
        FrequenciaMensal, _ = get_models()
        frequencias = FrequenciaMensal.objects.filter(turma=turma)
        
        # Filtrar pelo período
        frequencias_filtradas = []
        for f in frequencias:
            data_freq = f.ano * 12 + f.mes
            if data_inicio <= data_freq <= data_fim:
                frequencias_filtradas.append(f)
        
        # Ordenar por ano e mês
        frequencias_filtradas.sort(key=lambda x: (x.ano, x.mes))
        
        # Formatar dados para resposta
        frequencias_data = []
        for frequencia in frequencias_filtradas:
            # Calcular estatísticas
            carencias = frequencia.carencia_set.all()
            total_alunos = carencias.count()
            alunos_carencia = carencias.filter(percentual_presenca__lt=frequencia.percentual_minimo).count()
            
            frequencias_data.append({
                'id': frequencia.id,
                'mes': frequencia.mes,
                'mes_nome': frequencia.get_mes_display(),
                'ano': frequencia.ano,
                'percentual_minimo': frequencia.percentual_minimo,
                'total_alunos': total_alunos,
                'alunos_carencia': alunos_carencia,
                'percentual_carencia': (alunos_carencia / total_alunos * 100) if total_alunos > 0 else 0
            })
        
        return JsonResponse({
            'success': True,
            'turma': {
                'id': turma.id,
                'nome': turma.nome,
                'curso': turma.curso.nome if turma.curso else None
            },
            'periodo': {
                'mes_inicio': mes_inicio,
                'ano_inicio': ano_inicio,
                'mes_fim': mes_fim,
                'ano_fim': ano_fim
            },
            'frequencias': frequencias_data
        })
    
    except Exception as e:
        logger.error(f"Erro ao obter dados do painel de frequências: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'Erro ao obter dados do painel: {str(e)}'
        }, status=400)

@login_required
def obter_turmas_por_curso(request, curso_id):
    """API para obter turmas de um curso."""
    try:
        Turma = get_turma_model()
        
        # Obter turmas do curso
        turmas = Turma.objects.filter(curso_id=curso_id, status='A')
        
        # Formatar dados para resposta
        turmas_data = []
        for turma in turmas:
            turmas_data.append({
                'id': turma.id,
                'nome': turma.nome
            })
        
        return JsonResponse({
            'success': True,
            'turmas': turmas_data
        })
    
    except Exception as e:
        logger.error(f"Erro ao obter turmas por curso: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'Erro ao obter turmas: {str(e)}'
        }, status=400)