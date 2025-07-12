"""
API Views para o sistema de presenças.
Endpoints AJAX para interface interativa Excel-like.
"""

import json
import logging
from datetime import datetime, date
from decimal import Decimal
from calendar import monthrange

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, Count, Sum, Avg
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from django.core.paginator import Paginator

from rest_framework.decorators import api_view, throttle_scope
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status

from ..models import PresencaDetalhada, ConfiguracaoPresenca, Presenca
from ..serializers import PresencaSerializer
from atividades.models import Atividade
from turmas.models import Turma
from alunos.models import Aluno

logger = logging.getLogger(__name__)


class APIResponseMixin:
    """Mixin para padronizar respostas da API."""
    
    def success_response(self, data=None, message="Operação realizada com sucesso"):
        """Resposta padronizada de sucesso."""
        response = {
            'success': True,
            'message': message,
            'data': data or {}
        }
        return JsonResponse(response)
    
    def error_response(self, message="Erro interno", errors=None, status_code=400):
        """Resposta padronizada de erro."""
        response = {
            'success': False,
            'message': message,
            'errors': errors or []
        }
        return JsonResponse(response, status=status_code)


class CustomThrottle(UserRateThrottle):
    """Throttle customizado para API."""
    scope = 'presencas_api'
    rate = '100/hour'


@method_decorator(login_required, name='dispatch')
class AtualizarPresencasView(APIResponseMixin, View):
    """
    Endpoint para atualização em lote de presenças.
    POST /api/atualizar-presencas/
    """
    
    def post(self, request):
        """Atualiza presenças em lote."""
        try:
            data = json.loads(request.body)
            presencas_data = data.get('presencas', [])
            
            if not presencas_data:
                return self.error_response("Nenhuma presença fornecida para atualização")
            
            # Validar estrutura dos dados
            campos_obrigatorios = ['aluno_id', 'turma_id', 'atividade_id', 'periodo']
            erros_validacao = []
            
            for i, presenca_data in enumerate(presencas_data):
                for campo in campos_obrigatorios:
                    if campo not in presenca_data:
                        erros_validacao.append(f"Presença {i+1}: Campo '{campo}' obrigatório")
            
            if erros_validacao:
                return self.error_response(
                    "Dados inválidos", 
                    erros_validacao
                )
            
            # Processar atualizações em lote
            presencas_atualizadas = []
            presencas_criadas = []
            
            with transaction.atomic():
                for presenca_data in presencas_data:
                    try:
                        # Buscar ou criar presença detalhada
                        presenca, created = PresencaDetalhada.objects.get_or_create(
                            aluno_id=presenca_data['aluno_id'],
                            turma_id=presenca_data['turma_id'],
                            atividade_id=presenca_data['atividade_id'],
                            periodo=datetime.strptime(presenca_data['periodo'], '%Y-%m-%d').date(),
                            defaults={
                                'convocacoes': presenca_data.get('convocacoes', 0),
                                'presencas': presenca_data.get('presencas', 0),
                                'faltas': presenca_data.get('faltas', 0),
                                'voluntario_extra': presenca_data.get('voluntario_extra', 0),
                                'voluntario_simples': presenca_data.get('voluntario_simples', 0),
                                'registrado_por': request.user.username
                            }
                        )
                        
                        if not created:
                            # Atualizar presença existente
                            presenca.convocacoes = presenca_data.get('convocacoes', presenca.convocacoes)
                            presenca.presencas = presenca_data.get('presencas', presenca.presencas)
                            presenca.faltas = presenca_data.get('faltas', presenca.faltas)
                            presenca.voluntario_extra = presenca_data.get('voluntario_extra', presenca.voluntario_extra)
                            presenca.voluntario_simples = presenca_data.get('voluntario_simples', presenca.voluntario_simples)
                            presenca.save()
                            presencas_atualizadas.append(presenca.id)
                        else:
                            presencas_criadas.append(presenca.id)
                            
                    except Exception as e:
                        logger.error(f"Erro ao processar presença {presenca_data}: {str(e)}")
                        return self.error_response(f"Erro ao processar presença: {str(e)}")
            
            # Log da operação
            logger.info(
                f"Atualização em lote realizada por {request.user.username}: "
                f"{len(presencas_atualizadas)} atualizadas, {len(presencas_criadas)} criadas"
            )
            
            return self.success_response({
                'presencas_atualizadas': len(presencas_atualizadas),
                'presencas_criadas': len(presencas_criadas),
                'total_processadas': len(presencas_data)
            })
            
        except json.JSONDecodeError:
            return self.error_response("JSON inválido", status_code=400)
        except Exception as e:
            logger.error(f"Erro na atualização em lote: {str(e)}")
            return self.error_response("Erro interno do servidor", status_code=500)


@method_decorator(login_required, name='dispatch')
class CalcularEstatisticasView(APIResponseMixin, View):
    """
    Endpoint para recalcular estatísticas em tempo real.
    GET /api/calcular-estatisticas/
    """
    
    def get(self, request):
        """Calcula estatísticas de presenças."""
        try:
            # Parâmetros opcionais
            turma_id = request.GET.get('turma_id')
            atividade_id = request.GET.get('atividade_id')
            periodo = request.GET.get('periodo')
            
            # Filtros base
            queryset = PresencaDetalhada.objects.all()
            
            if turma_id:
                queryset = queryset.filter(turma_id=turma_id)
            if atividade_id:
                queryset = queryset.filter(atividade_id=atividade_id)
            if periodo:
                periodo_date = datetime.strptime(periodo, '%Y-%m-%d').date()
                queryset = queryset.filter(periodo=periodo_date)
            
            # Calcular estatísticas
            stats = queryset.aggregate(
                total_presencas=Count('id'),
                total_convocacoes=Sum('convocacoes'),
                total_presencas_efetivas=Sum('presencas'),
                total_faltas=Sum('faltas'),
                total_voluntarios=Sum('total_voluntarios'),
                total_carencias=Sum('carencias'),
                percentual_medio=Avg('percentual_presenca')
            )
            
            # Estatísticas por aluno
            stats_por_aluno = queryset.values(
                'aluno__nome',
                'aluno__id'
            ).annotate(
                total_convocacoes=Sum('convocacoes'),
                total_presencas=Sum('presencas'),
                total_faltas=Sum('faltas'),
                percentual_presenca=Avg('percentual_presenca'),
                total_carencias=Sum('carencias')
            ).order_by('aluno__nome')
            
            # Estatísticas por turma (se não filtrada)
            stats_por_turma = []
            if not turma_id:
                stats_por_turma = queryset.values(
                    'turma__nome',
                    'turma__id'
                ).annotate(
                    total_convocacoes=Sum('convocacoes'),
                    total_presencas=Sum('presencas'),
                    total_faltas=Sum('faltas'),
                    percentual_medio=Avg('percentual_presenca')
                ).order_by('turma__nome')
            
            # Estatísticas por atividade (se não filtrada)
            stats_por_atividade = []
            if not atividade_id:
                stats_por_atividade = queryset.values(
                    'atividade__nome',
                    'atividade__id'
                ).annotate(
                    total_convocacoes=Sum('convocacoes'),
                    total_presencas=Sum('presencas'),
                    total_faltas=Sum('faltas'),
                    percentual_medio=Avg('percentual_presenca')
                ).order_by('atividade__nome')
            
            # Preparar resposta
            response_data = {
                'estatisticas_gerais': {
                    'total_registros': stats['total_presencas'] or 0,
                    'total_convocacoes': stats['total_convocacoes'] or 0,
                    'total_presencas_efetivas': stats['total_presencas_efetivas'] or 0,
                    'total_faltas': stats['total_faltas'] or 0,
                    'total_voluntarios': stats['total_voluntarios'] or 0,
                    'total_carencias': stats['total_carencias'] or 0,
                    'percentual_medio': float(stats['percentual_medio'] or 0),
                    'data_calculo': timezone.now().isoformat()
                },
                'por_aluno': list(stats_por_aluno),
                'por_turma': list(stats_por_turma),
                'por_atividade': list(stats_por_atividade)
            }
            
            return self.success_response(response_data)
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {str(e)}")
            return self.error_response("Erro ao calcular estatísticas", status_code=500)


@method_decorator(login_required, name='dispatch')
class BuscarAlunosView(APIResponseMixin, View):
    """
    Endpoint para busca rápida de alunos.
    GET /api/buscar-alunos/
    """
    
    def get(self, request):
        """Busca alunos por nome ou CPF."""
        try:
            termo = request.GET.get('q', '').strip()
            turma_id = request.GET.get('turma_id')
            limit = min(int(request.GET.get('limit', 20)), 100)  # Máximo 100 resultados
            
            if not termo:
                return self.error_response("Termo de busca obrigatório")
            
            # Buscar alunos
            queryset = Aluno.objects.filter(
                Q(nome__icontains=termo) | 
                Q(cpf__icontains=termo) |
                Q(email__icontains=termo)
            )
            
            # Filtrar por turma se especificada
            if turma_id:
                queryset = queryset.filter(turma_id=turma_id)
            
            # Limitar resultados
            alunos = queryset.select_related('turma')[:limit]
            
            # Preparar dados
            alunos_data = []
            for aluno in alunos:
                alunos_data.append({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'cpf': aluno.cpf,
                    'email': aluno.email,
                    'turma': {
                        'id': aluno.turma.id if aluno.turma else None,
                        'nome': aluno.turma.nome if aluno.turma else None
                    }
                })
            
            return self.success_response({
                'alunos': alunos_data,
                'total_encontrados': len(alunos_data),
                'termo_busca': termo
            })
            
        except Exception as e:
            logger.error(f"Erro na busca de alunos: {str(e)}")
            return self.error_response("Erro na busca de alunos", status_code=500)


@method_decorator(login_required, name='dispatch')
class ValidarDadosView(APIResponseMixin, View):
    """
    Endpoint para validação de dados antes do salvamento.
    POST /api/validar-dados/
    """
    
    def post(self, request):
        """Valida dados de presença antes do salvamento."""
        try:
            data = json.loads(request.body)
            
            # Validações básicas
            erros = []
            warnings = []
            
            # Validar campos obrigatórios
            campos_obrigatorios = ['aluno_id', 'turma_id', 'atividade_id', 'periodo']
            for campo in campos_obrigatorios:
                if campo not in data:
                    erros.append(f"Campo '{campo}' é obrigatório")
            
            if erros:
                return self.error_response("Dados inválidos", erros)
            
            # Validar se objetos existem
            try:
                aluno = Aluno.objects.get(id=data['aluno_id'])
            except Aluno.DoesNotExist:
                erros.append("Aluno não encontrado")
            
            try:
                turma = Turma.objects.get(id=data['turma_id'])
            except Turma.DoesNotExist:
                erros.append("Turma não encontrada")
            
            try:
                atividade = Atividade.objects.get(id=data['atividade_id'])
            except Atividade.DoesNotExist:
                erros.append("Atividade não encontrada")
            
            # Validar período
            try:
                periodo = datetime.strptime(data['periodo'], '%Y-%m-%d').date()
                if periodo.day != 1:
                    erros.append("Período deve ser o primeiro dia do mês")
                if periodo > date.today():
                    warnings.append("Período está no futuro")
            except ValueError:
                erros.append("Formato de período inválido (esperado: YYYY-MM-DD)")
            
            # Validar valores numéricos
            campos_numericos = ['convocacoes', 'presencas', 'faltas', 'voluntario_extra', 'voluntario_simples']
            for campo in campos_numericos:
                if campo in data:
                    try:
                        valor = int(data[campo])
                        if valor < 0:
                            erros.append(f"Campo '{campo}' não pode ser negativo")
                    except (ValueError, TypeError):
                        erros.append(f"Campo '{campo}' deve ser um número inteiro")
            
            # Validar lógica de negócio
            if all(campo in data for campo in ['convocacoes', 'presencas', 'faltas']):
                convocacoes = int(data['convocacoes'])
                presencas = int(data['presencas'])
                faltas = int(data['faltas'])
                
                if presencas + faltas > convocacoes:
                    erros.append("A soma de presenças e faltas não pode ser maior que convocações")
                
                if convocacoes > 0:
                    percentual = (presencas / convocacoes) * 100
                    if percentual < 50:
                        warnings.append(f"Percentual de presença baixo: {percentual:.1f}%")
            
            # Verificar se já existe registro
            if not erros and 'aluno_id' in data:
                existe_registro = PresencaDetalhada.objects.filter(
                    aluno_id=data['aluno_id'],
                    turma_id=data['turma_id'],
                    atividade_id=data['atividade_id'],
                    periodo=periodo
                ).exists()
                
                if existe_registro:
                    warnings.append("Já existe registro para este aluno/turma/atividade/período")
            
            # Resposta
            if erros:
                return self.error_response("Dados inválidos", erros)
            
            return self.success_response({
                'valido': True,
                'warnings': warnings,
                'dados_validados': data
            })
            
        except json.JSONDecodeError:
            return self.error_response("JSON inválido", status_code=400)
        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return self.error_response("Erro na validação", status_code=500)


@method_decorator(login_required, name='dispatch')
class AtividadesTurmaView(APIResponseMixin, View):
    """
    Endpoint para listar atividades por turma.
    GET /api/atividades-turma/
    """
    
    def get(self, request):
        """Lista atividades disponíveis para uma turma."""
        try:
            turma_id = request.GET.get('turma_id')
            
            if not turma_id:
                return self.error_response("ID da turma obrigatório")
            
            try:
                turma = Turma.objects.get(id=turma_id)
            except Turma.DoesNotExist:
                return self.error_response("Turma não encontrada")
            
            # Buscar atividades relacionadas à turma
            atividades = Atividade.objects.filter(
                Q(turma=turma) | Q(turma__isnull=True)  # Atividades específicas da turma ou gerais
            ).order_by('nome')
            
            # Preparar dados
            atividades_data = []
            for atividade in atividades:
                # Verificar se há configuração específica
                configuracao = None
                try:
                    configuracao = ConfiguracaoPresenca.objects.get(
                        turma=turma,
                        atividade=atividade,
                        ativo=True
                    )
                except ConfiguracaoPresenca.DoesNotExist:
                    pass
                
                atividades_data.append({
                    'id': atividade.id,
                    'nome': atividade.nome,
                    'tipo': atividade.tipo if hasattr(atividade, 'tipo') else 'Geral',
                    'obrigatoria': configuracao.obrigatoria if configuracao else True,
                    'peso_calculo': float(configuracao.peso_calculo) if configuracao else 1.0,
                    'tem_configuracao': configuracao is not None
                })
            
            return self.success_response({
                'turma': {
                    'id': turma.id,
                    'nome': turma.nome
                },
                'atividades': atividades_data,
                'total_atividades': len(atividades_data)
            })
            
        except Exception as e:
            logger.error(f"Erro ao buscar atividades: {str(e)}")
            return self.error_response("Erro ao buscar atividades", status_code=500)


@method_decorator(login_required, name='dispatch')
class ConfiguracaoPresencaView(APIResponseMixin, View):
    """
    Endpoint para gerenciar configurações de presença.
    GET/POST /api/configuracao-presenca/
    """
    
    def get(self, request):
        """Busca configurações de presença."""
        try:
            turma_id = request.GET.get('turma_id')
            atividade_id = request.GET.get('atividade_id')
            
            queryset = ConfiguracaoPresenca.objects.filter(ativo=True)
            
            if turma_id:
                queryset = queryset.filter(turma_id=turma_id)
            if atividade_id:
                queryset = queryset.filter(atividade_id=atividade_id)
            
            configuracoes = queryset.select_related('turma', 'atividade')
            
            config_data = []
            for config in configuracoes:
                config_data.append({
                    'id': config.id,
                    'turma': {
                        'id': config.turma.id,
                        'nome': config.turma.nome
                    },
                    'atividade': {
                        'id': config.atividade.id,
                        'nome': config.atividade.nome
                    },
                    'obrigatoria': config.obrigatoria,
                    'peso_calculo': float(config.peso_calculo),
                    'limites_carencia': {
                        '0_25': config.limite_carencia_0_25,
                        '26_50': config.limite_carencia_26_50,
                        '51_75': config.limite_carencia_51_75,
                        '76_100': config.limite_carencia_76_100
                    }
                })
            
            return self.success_response({
                'configuracoes': config_data,
                'total': len(config_data)
            })
            
        except Exception as e:
            logger.error(f"Erro ao buscar configurações: {str(e)}")
            return self.error_response("Erro ao buscar configurações", status_code=500)


# Decoradores para endpoints funcionais
@login_required
@require_http_methods(["POST"])
def atualizar_presencas(request):
    """Wrapper funcional para atualização de presenças."""
    view = AtualizarPresencasView()
    return view.post(request)


@login_required
@require_http_methods(["GET"])
def calcular_estatisticas(request):
    """Wrapper funcional para cálculo de estatísticas."""
    view = CalcularEstatisticasView()
    return view.get(request)


@login_required
@require_http_methods(["GET"])
def buscar_alunos(request):
    """Wrapper funcional para busca de alunos."""
    view = BuscarAlunosView()
    return view.get(request)


@login_required
@require_http_methods(["POST"])
def validar_dados(request):
    """Wrapper funcional para validação de dados."""
    view = ValidarDadosView()
    return view.post(request)


@login_required
@require_http_methods(["GET"])
def atividades_turma(request):
    """Wrapper funcional para listagem de atividades por turma."""
    view = AtividadesTurmaView()
    return view.get(request)


@login_required
@require_http_methods(["GET"])
def configuracao_presenca(request):
    """Wrapper funcional para configurações de presença."""
    view = ConfiguracaoPresencaView()
    return view.get(request)


# Endpoints para DRF (se disponível)
try:
    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.permissions import IsAuthenticated
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def presencas_resumo(request):
        """Endpoint DRF para resumo de presenças."""
        try:
            # Últimas presenças
            ultimas_presencas = PresencaDetalhada.objects.select_related(
                'aluno', 'turma', 'atividade'
            ).order_by('-data_atualizacao')[:10]
            
            # Serializar
            serializer = PresencaSerializer(ultimas_presencas, many=True)
            
            return Response({
                'ultimas_presencas': serializer.data,
                'total_registros': PresencaDetalhada.objects.count()
            })
            
        except Exception as e:
            logger.error(f"Erro no resumo de presenças: {str(e)}")
            return Response(
                {'error': 'Erro interno do servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
except ImportError:
    # DRF não disponível
    pass
