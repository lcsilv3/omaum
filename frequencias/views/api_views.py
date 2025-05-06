"""
API views para o aplicativo de frequências.
"""

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from importlib import import_module
import logging
import json

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

@login_required
def obter_dados_frequencia(request, frequencia_id):
    """API para obter dados de uma frequência mensal."""
    try:
        FrequenciaMensal, Carencia = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Obter carências
        carencias = Carencia.objects.filter(frequencia_mensal=frequencia).select_related('aluno')
        
        # Preparar dados
        dados = {
            'frequencia': {
                'id': frequencia.id,
                'turma': frequencia.turma.nome,
                'mes': frequencia.get_mes_display(),
                'ano': frequencia.ano,
                'percentual_minimo': frequencia.percentual_minimo
            },
            'carencias': []
        }
        
        for carencia in carencias:
            dados['carencias'].append({
                'id': carencia.id,
                'aluno': {
                    'cpf': carencia.aluno.cpf,
                    'nome': carencia.aluno.nome,
                    'email': carencia.aluno.email
                },
                'percentual_presenca': float(carencia.percentual_presenca),
                'total_presencas': carencia.total_presencas,
                'total_atividades': carencia.total_atividades,
                'liberado': carencia.liberado,
                'observacoes': carencia.observacoes or ''
            })
        
        return JsonResponse({'success': True, 'dados': dados})
    
    except Exception as e:
        logger.error(f"Erro ao obter dados da frequência: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def obter_dados_painel_frequencias(request):
    """API para obter dados para o painel de frequências."""
    try:
        # Obter parâmetros
        turma_id = request.GET.get('turma')
        mes_inicio = request.GET.get('mes_inicio')
        ano_inicio = request.GET.get('ano_inicio')
        mes_fim = request.GET.get('mes_fim')
        ano_fim = request.GET.get('ano_fim')
        
        if not all([turma_id, mes_inicio, ano_inicio, mes_fim, ano_fim]):
            return JsonResponse({'success': False, 'error': 'Parâmetros incompletos'}, status=400)
        
        FrequenciaMensal, Carencia = get_models()
        Turma = get_turma_model()
        
        # Obter turma
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Converter parâmetros para inteiros
        mes_inicio = int(mes_inicio)
        ano_inicio = int(ano_inicio)
        mes_fim = int(mes_fim)
        ano_fim = int(ano_fim)
        
        # Calcular período em meses
        data_inicio = ano_inicio * 12 + mes_inicio
        data_fim = ano_fim * 12 + mes_fim
        
        # Obter frequências no período
        frequencias = FrequenciaMensal.objects.filter(
            turma=turma
        ).select_related('turma')
        
        # Filtrar pelo período
        frequencias_filtradas = [
            f for f in frequencias
            if data_inicio <= (f.ano * 12 + f.mes) <= data_fim
        ]
        
        # Ordenar por ano e mês
        frequencias_filtradas.sort(key=lambda x: (x.ano, x.mes))
        
        # Preparar dados
        dados = {
            'turma': {
                'id': turma.id,
                'nome': turma.nome,
                'curso': turma.curso.nome if turma.curso else 'Sem curso'
            },
            'periodo': {
                'mes_inicio': mes_inicio,
                'ano_inicio': ano_inicio,
                'mes_fim': mes_fim,
                'ano_fim': ano_fim
            },
            'frequencias': []
        }
        
        for frequencia in frequencias_filtradas:
            # Obter carências
            carencias = Carencia.objects.filter(frequencia_mensal=frequencia)
            
            # Calcular estatísticas
            total_alunos = carencias.count()
            alunos_carencia = carencias.filter(percentual_presenca__lt=frequencia.percentual_minimo).count()
            
            # Adicionar dados da frequência
            dados['frequencias'].append({
                'id': frequencia.id,
                'mes': frequencia.get_mes_display(),
                'ano': frequencia.ano,
                'percentual_minimo': frequencia.percentual_minimo,
                'total_alunos': total_alunos,
                'alunos_carencia': alunos_carencia,
                'percentual_carencia': (alunos_carencia / total_alunos * 100) if total_alunos > 0 else 0
            })
        
        return JsonResponse({'success': True, 'dados': dados})
    
    except Exception as e:
        logger.error(f"Erro ao obter dados do painel: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)