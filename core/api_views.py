"""
API Views para o app core.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ConfiguracaoSistema, LogAtividade
from .serializers import (
    ConfiguracaoSistemaSerializer,
    ConfiguracaoCreateSerializer,
    ConfiguracaoUpdateSerializer,
    LogAtividadeSerializer,
    LogAtividadeCreateSerializer
)
from .services import ConfiguracaoService, LogAtividadeService


class ConfiguracaoSistemaViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de ConfiguracaoSistema."""
    
    queryset = ConfiguracaoSistema.objects.all()
    permission_classes = [IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ConfiguracaoService()
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado baseado na action."""
        if self.action == 'create':
            return ConfiguracaoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ConfiguracaoUpdateSerializer
        return ConfiguracaoSistemaSerializer
    
    def list(self, request):
        """Lista todas as configurações."""
        try:
            configuracoes = self.service.listar_configuracoes()
            serializer = self.get_serializer(configuracoes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request):
        """Cria uma nova configuração."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                configuracao = self.service.definir_configuracao(
                    chave=serializer.validated_data['chave'],
                    valor=serializer.validated_data['valor'],
                    descricao=serializer.validated_data.get('descricao')
                )
                response_serializer = ConfiguracaoSistemaSerializer(
                    configuracao
                )
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def como_dict(self, request):
        """Retorna todas as configurações como dicionário."""
        try:
            configuracoes = self.service.obter_configuracoes_como_dict()
            return Response(configuracoes)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def obter_por_chave(self, request):
        """Obtém uma configuração por chave."""
        try:
            chave = request.query_params.get('chave')
            if not chave:
                return Response(
                    {'error': 'Parâmetro chave é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            valor = self.service.obter_configuracao(chave)
            if valor is None:
                return Response(
                    {'error': 'Configuração não encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response({'chave': chave, 'valor': valor})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogAtividadeViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de LogAtividade."""
    
    queryset = LogAtividade.objects.all()
    permission_classes = [IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = LogAtividadeService()
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado baseado na action."""
        if self.action == 'create':
            return LogAtividadeCreateSerializer
        return LogAtividadeSerializer
    
    def list(self, request):
        """Lista logs de atividade."""
        try:
            logs = self.service.obter_logs_recentes()
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request):
        """Cria um novo log de atividade."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                log = self.service.registrar_atividade(
                    usuario_id=serializer.validated_data['usuario'].id,
                    acao=serializer.validated_data['acao'],
                    detalhes=serializer.validated_data.get('detalhes')
                )
                response_serializer = LogAtividadeSerializer(log)
                return Response(
                    response_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_usuario(self, request):
        """Obtém logs por usuário."""
        try:
            usuario_id = request.query_params.get('usuario_id')
            if not usuario_id:
                return Response(
                    {'error': 'Parâmetro usuario_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            logs = self.service.obter_logs_do_usuario(int(usuario_id))
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'error': 'usuario_id deve ser um número'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def por_acao(self, request):
        """Obtém logs por ação."""
        try:
            acao = request.query_params.get('acao')
            if not acao:
                return Response(
                    {'error': 'Parâmetro acao é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            logs = self.service.obter_logs_por_acao(acao)
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Busca logs por termo."""
        try:
            termo = request.query_params.get('termo', '')
            logs = self.service.buscar_logs(termo)
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas dos logs."""
        try:
            stats = self.service.obter_estatisticas()
            stats_serializer = {
                'total_logs': stats['total_logs'],
                'logs_hoje': stats['logs_hoje'],
                'logs_recentes': LogAtividadeSerializer(
                    stats['logs_recentes'],
                    many=True
                ).data
            }
            return Response(stats_serializer)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['delete'])
    def limpar_antigos(self, request):
        """Remove logs antigos."""
        try:
            dias = int(request.query_params.get('dias', 30))
            removidos = self.service.limpar_logs_antigos(dias)
            return Response({
                'removidos': removidos,
                'dias': dias
            })
        except ValueError:
            return Response(
                {'error': 'dias deve ser um número'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
