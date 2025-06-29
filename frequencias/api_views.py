from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from importlib import import_module
import logging
from datetime import datetime

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
        
        # Formatar dados para resposta
        carencias_data = []
        for carencia in carencias:
            carencias_data.append({
                'id': carencia.id,
                'aluno': {
                    'cpf': carencia.aluno.cpf,
                    'nome': carencia.aluno.nome
                },
                'percentual_presenca': float(carencia.percentual_presenca),
                'numero_carencias': carencia.numero_carencias,
                'liberado': carencia.liberado,
                'status': carencia.status if hasattr(carencia, 'status') else None
            })
        
        return JsonResponse({
            'success': True,
            'frequencia': {
                'id': frequencia.id,
                'turma': {
                    'id': frequencia.turma.id,
                    'nome': frequencia.turma.nome
                },
                'mes': frequencia.mes,
                'mes_nome': frequencia.get_mes_display(),
                'ano': frequencia.ano,
                'percentual_minimo': frequencia.percentual_minimo
            },
            'carencias': carencias_data
        })
    
    except Exception as e:
        logger.error(f"Erro ao obter dados da frequência: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'Erro ao obter dados da frequência: {str(e)}'
        }, status=400)

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