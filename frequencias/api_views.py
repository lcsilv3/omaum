from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    from importlib import import_module
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def obter_dados_frequencia(request, frequencia_id):
    """API para obter dados de uma frequência mensal."""
    try:
        FrequenciaMensal = get_model_dynamically("frequencias", "FrequenciaMensal")
        Carencia = get_model_dynamically("frequencias", "Carencia")
        
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        carencias = Carencia.objects.filter(frequencia_mensal=frequencia).select_related('aluno')
        
        # Preparar dados para o gráfico
        alunos = []
        percentuais = []
        
        for carencia in carencias:
            alunos.append(carencia.aluno.nome)
            percentuais.append(float(carencia.percentual_presenca))
        
        return JsonResponse({
            'success': True,
            'alunos': alunos,
            'percentuais': percentuais,
            'percentual_minimo': frequencia.percentual_minimo,
            'total_alunos': len(alunos),
            'alunos_abaixo_minimo': sum(1 for p in percentuais if p < frequencia.percentual_minimo)
        })
    except Exception as e:
        logger.error(f"Erro ao obter dados de frequência: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def obter_dados_painel_frequencias(request):
    """API para obter dados para o painel de frequências."""
    try:
        turma_id = request.GET.get('turma')
        periodo_inicio = request.GET.get('periodo_inicio')
        periodo_fim = request.GET.get('periodo_fim')
        
        if not turma_id:
            return JsonResponse({'success': False, 'error': 'Turma não especificada'}, status=400)
        
        FrequenciaMensal = get_model_dynamically("frequencias", "FrequenciaMensal")
        Turma = get_model_dynamically("turmas", "Turma")
        
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Obter frequências da turma
        frequencias = FrequenciaMensal.objects.filter(turma=turma).order_by('ano', 'mes')
        
        # Filtrar por período se especificado
        if periodo_inicio and periodo_fim:
            ano_inicio, mes_inicio = map(int, periodo_inicio.split('-'))
            ano_fim, mes_fim = map(int, periodo_fim.split('-'))
            
            # Converter para valor numérico (ano * 12 + mes) para comparação
            inicio_numerico = ano_inicio * 12 + mes_inicio
            fim_numerico = ano_fim * 12 + mes_fim
            
            frequencias = [
                f for f in frequencias
                if inicio_numerico <= (f.ano * 12 + f.mes) <= fim_numerico
            ]
        
        # Preparar dados para o gráfico
        periodos = []
        percentuais_medios = []
        alunos_carencia = []
        
        for freq in frequencias:
            periodo = f"{freq.get_mes_display()}/{freq.ano}"
            periodos.append(periodo)
            
            # Calcular percentual médio de presença
            from django.db.models import Avg
            Carencia = get_model_dynamically("frequencias", "Carencia")
            media = Carencia.objects.filter(frequencia_mensal=freq).aggregate(
                media=Avg('percentual_presenca')
            )['media'] or 0
            
            percentuais_medios.append(float(media))
            
            # Contar alunos em carência
            carencias = Carencia.objects.filter(
                frequencia_mensal=freq,
                percentual_presenca__lt=freq.percentual_minimo
            ).count()
            
            alunos_carencia.append(carencias)
        
        return JsonResponse({
            'success': True,
            'periodos': periodos,
            'percentuais_medios': percentuais_medios,
            'alunos_carencia': alunos_carencia,
            'percentual_minimo': 75  # Valor padrão, pode ser ajustado
        })
    except Exception as e:
        logger.error(f"Erro ao obter dados do painel: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)