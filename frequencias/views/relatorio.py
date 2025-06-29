from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Case, When, IntegerField
from django.http import HttpResponse
from importlib import import_module
import logging
import csv
import json

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia

def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

@login_required
def relatorio_frequencias(request):
    """Exibe um relatório de frequências."""
    try:
        FrequenciaMensal, Carencia = get_models()
        
        # Estatísticas gerais
        total_frequencias = FrequenciaMensal.objects.count()
        
        # Obter total de alunos com carência
        total_carencias = Carencia.objects.count()
        total_liberados = Carencia.objects.filter(liberado=True).count()
        total_nao_liberados = total_carencias - total_liberados
        
        # Percentuais
        percentual_liberados = (total_liberados / total_carencias * 100) if total_carencias > 0 else 0
        percentual_nao_liberados = (total_nao_liberados / total_carencias * 100) if total_carencias > 0 else 0
        
        # Frequências por mês
        from django.db.models import Count
        from django.db.models.functions import TruncMonth
        
        # Agrupar por mês e ano
        frequencias_por_mes = FrequenciaMensal.objects.values('mes', 'ano').annotate(
            total=Count('id')
        ).order_by('ano', 'mes')
        
        # Formatar dados para gráficos
        meses = []
        dados_frequencias = []
        
        for item in frequencias_por_mes:
            mes_nome = dict(FrequenciaMensal.MES_CHOICES).get(item['mes'])
            meses.append(f"{mes_nome}/{item['ano']}")
            dados_frequencias.append(item['total'])
        
        context = {
            'total_frequencias': total_frequencias,
            'total_carencias': total_carencias,
            'total_liberados': total_liberados,
            'total_nao_liberados': total_nao_liberados,
            'percentual_liberados': percentual_liberados,
            'percentual_nao_liberados': percentual_nao_liberados,
            'meses': meses,
            'dados_frequencias': dados_frequencias
        }
        
        return render(request, 'frequencias/relatorio_frequencias.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao gerar relatório: {str(e)}")
        return redirect('frequencias:listar_frequencias')

@login_required
def exportar_frequencia_csv(request, frequencia_id):
    """Exporta os dados de uma frequência mensal para CSV."""
    try:
        FrequenciaMensal, Carencia = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)
        
        # Obter carências
        carencias = Carencia.objects.filter(frequencia_mensal=frequencia).select_related('aluno')
        
        # Criar resposta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="frequencia_{frequencia.turma.nome}_{frequencia.get_mes_display()}_{frequencia.ano}.csv"'
        
        # Escrever cabeçalho e dados
        writer = csv.writer(response)
        writer.writerow(['CPF', 'Aluno', 'Presenças', 'Total Atividades', 'Percentual', 'Carências', 'Liberado', 'Observações'])
        
        for carencia in carencias:
            writer.writerow([
                carencia.aluno.cpf,
                carencia.aluno.nome,
                carencia.total_presencas,
                carencia.total_atividades,
                f"{carencia.percentual_presenca:.2f}",
                carencia.numero_carencias,
                'Sim' if carencia.liberado else 'Não',
                carencia.observacoes or ''
            ])
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao exportar frequência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar frequência: {str(e)}")
        return redirect('frequencias:detalhar_frequencia_mensal', frequencia_id=frequencia_id)

@login_required
def historico_frequencia(request, aluno_cpf):
    """Exibe o histórico de frequência de um aluno."""
    try:
        FrequenciaMensal, Carencia = get_models()
        Aluno = get_model_dynamically("alunos", "Aluno")
        
        # Obter aluno
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        
        # Obter parâmetros de filtro
        curso_id = request.GET.get('curso')
        turma_id = request.GET.get('turma')
        periodo = request.GET.get('periodo')
        
        # Construir query base
        carencias = Carencia.objects.filter(aluno=aluno).select_related('frequencia_mensal', 'frequencia_mensal__turma')
        
        # Aplicar filtros
        if curso_id:
            carencias = carencias.filter(frequencia_mensal__turma__curso_id=curso_id)
        
        if turma_id:
            carencias = carencias.filter(frequencia_mensal__turma__id=turma_id)
        
        if periodo:
            ano, mes = periodo.split('-')
            carencias = carencias.filter(frequencia_mensal__ano=ano, frequencia_mensal__mes=mes)
        
        # Ordenar por período (mais recente primeiro)
        carencias = carencias.order_by('-frequencia_mensal__ano', '-frequencia_mensal__mes')
        
        # Paginação
        paginator = Paginator(carencias, 10)  # 10 itens por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Calcular média geral de frequência
        from django.db.models import Avg
        media_geral = carencias.aggregate(Avg('percentual_presenca'))['percentual_presenca__avg'] or 0
        
        # Dados para gráfico de evolução
        periodos_labels = []
        percentuais_presenca = []
        
        # Limitar a 12 períodos mais recentes
        for carencia in carencias[:12]:
            periodo_label = f"{carencia.frequencia_mensal.get_mes_display()}/{carencia.frequencia_mensal.ano}"
            periodos_labels.append(periodo_label)
            percentuais_presenca.append(float(carencia.percentual_presenca))
        
        # Inverter para ordem cronológica
        periodos_labels.reverse()
        percentuais_presenca.reverse()
        
        # Obter dados para filtros
        Curso = get_model_dynamically("cursos", "Curso")
        cursos = Curso.objects.all()
        
        Turma = get_turma_model()
        turmas = Turma.objects.filter(matriculas__aluno=aluno).distinct()
        
        anos = FrequenciaMensal.objects.filter(carencia__aluno=aluno).values_list('ano', flat=True).distinct().order_by('-ano')
        meses = FrequenciaMensal.MES_CHOICES
        
        context = {
            'aluno': aluno,
            'registros': page_obj,
            'total_registros': carencias.count(),
            'media_geral': media_geral,
            'carencias': carencias.filter(percentual_presenca__lt=75),
            'periodos_labels': json.dumps(periodos_labels),
            'percentuais_presenca': json.dumps(percentuais_presenca),
            'filtros': {
                'curso': curso_id,
                'turma': turma_id,
                'periodo': periodo
            },
            'cursos': cursos,
            'turmas': turmas,
            'anos': anos,
            'meses': meses
        }
        
        return render(request, 'frequencias/historico_frequencia.html', context)
    
    except Exception as e:
        logger.error(f"Erro ao exibir histórico de frequência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exibir histórico de frequência: {str(e)}")
        return redirect('alunos:detalhar_aluno', cpf=aluno_cpf)

@login_required
def exportar_historico(request, aluno_cpf):
    """Exporta o histórico de frequência de um aluno para CSV."""
    try:
        _, Carencia = get_models()
        Aluno = get_model_dynamically("alunos", "Aluno")
        
        # Obter aluno
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        
        # Obter carências
        carencias = Carencia.objects.filter(aluno=aluno).select_related('frequencia_mensal', 'frequencia_mensal__turma')
        
        # Criar resposta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="historico_frequencia_{aluno.nome}.csv"'
        
        # Escrever cabeçalho e dados
        writer = csv.writer(response)
        writer.writerow(['Curso', 'Turma', 'Período', 'Presenças', 'Faltas', 'Total Aulas', 'Percentual', 'Status'])
        
        for carencia in carencias:
            writer.writerow([
                carencia.frequencia_mensal.turma.curso.nome,
                carencia.frequencia_mensal.turma.nome,
                f"{carencia.frequencia_mensal.get_mes_display()}/{carencia.frequencia_mensal.ano}",
                carencia.total_presencas,
                carencia.total_atividades - carencia.total_presencas,
                carencia.total_atividades,
                f"{carencia.percentual_presenca:.2f}",
                'Regular' if carencia.percentual_presenca >= 75 else 'Carência'
            ])
        
        return response
    
    except Exception as e:
        logger.error(f"Erro ao exportar histórico: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao exportar histórico: {str(e)}")
        return redirect('frequencias:historico_frequencia', aluno_cpf=aluno_cpf)