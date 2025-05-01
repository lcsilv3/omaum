import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

from .utils import get_model_class

# Set up logger
logger = logging.getLogger(__name__)

@login_required
def dashboard_atividades(request):
    """Exibe o dashboard de atividades com estatísticas e gráficos."""
    import json
    
    # Obter modelos
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    # Estatísticas gerais
    total_academicas = AtividadeAcademica.objects.count()
    total_ritualisticas = AtividadeRitualistica.objects.count()
    total_atividades = total_academicas + total_ritualisticas
    
    # Estatísticas de status (apenas para atividades acadêmicas)
    status_counts = dict(AtividadeAcademica.objects.values('status').annotate(count=Count('status')).values_list('status', 'count'))
    total_agendadas = status_counts.get('agendada', 0)
    
    # Atividades por mês (últimos 6 meses)
    hoje = datetime.now().date()
    seis_meses_atras = hoje - timedelta(days=180)
    
    # Preparar dados para o gráfico de atividades por mês
    academicas_por_mes = AtividadeAcademica.objects.filter(
        data_inicio__gte=seis_meses_atras
    ).annotate(
        mes=TruncMonth('data_inicio')
    ).values('mes').annotate(
        count=Count('id')
    ).order_by('mes')
    
    ritualisticas_por_mes = AtividadeRitualistica.objects.filter(
        data__gte=seis_meses_atras
    ).annotate(
        mes=TruncMonth('data')
    ).values('mes').annotate(
        count=Count('id')
    ).order_by('mes')
    
    # Converter para dicionários para facilitar o acesso
    academicas_dict = {item['mes'].strftime('%Y-%m'): item['count'] for item in academicas_por_mes}
    ritualisticas_dict = {item['mes'].strftime('%Y-%m'): item['count'] for item in ritualisticas_por_mes}
    
    # Gerar lista de meses (últimos 6 meses)
    meses = []
    academicas_counts = []
    ritualisticas_counts = []
    
    for i in range(5, -1, -1):
        mes_data = hoje.replace(day=1) - timedelta(days=i*30)
        mes_str = mes_data.strftime('%Y-%m')
        mes_nome = mes_data.strftime('%b/%Y')
        
        meses.append(mes_nome)
        academicas_counts.append(academicas_dict.get(mes_str, 0))
        ritualisticas_counts.append(ritualisticas_dict.get(mes_str, 0))
    
    # Próximas atividades
    proximas_academicas = AtividadeAcademica.objects.filter(
        data_inicio__gte=hoje
    ).exclude(
        status='cancelada'
    ).order_by('data_inicio')[:5]
    
    proximas_ritualisticas = AtividadeRitualistica.objects.filter(
        data__gte=hoje
    ).order_by('data', 'hora_inicio')[:5]
    
    # Adicionar tipo para facilitar o template
    for atividade in proximas_academicas:
        atividade.tipo = 'academica'
    
    for atividade in proximas_ritualisticas:
        atividade.tipo = 'ritualistica'
    
    # Combinar e ordenar por data
    proximas_atividades = sorted(
        list(proximas_academicas) + list(proximas_ritualisticas),
        key=lambda x: x.data_inicio if hasattr(x, 'data_inicio') else x.data
    )[:5]
    
    # Atividades recentes
    recentes_academicas = AtividadeAcademica.objects.filter(
        data_inicio__lt=hoje
    ).order_by('-data_inicio')[:5]
    
    recentes_ritualisticas = AtividadeRitualistica.objects.filter(
        data__lt=hoje
    ).order_by('-data')[:5]
    
    # Adicionar tipo para facilitar o template
    for atividade in recentes_academicas:
        atividade.tipo = 'academica'
    
    for atividade in recentes_ritualisticas:
        atividade.tipo = 'ritualistica'
    
    # Combinar e ordenar por data (decrescente)
    atividades_recentes = sorted(
        list(recentes_academicas) + list(recentes_ritualisticas),
        key=lambda x: x.data_inicio if hasattr(x, 'data_inicio') else x.data,
        reverse=True
    )[:5]
    
    return render(
        request,
        "atividades/dashboard_atividades.html",
        {
            "total_atividades": total_atividades,
            "total_academicas": total_academicas,
            "total_ritualisticas": total_ritualisticas,
            "total_agendadas": total_agendadas,
            "meses": json.dumps(meses),
            "academicas_counts": json.dumps(academicas_counts),
            "ritualisticas_counts": json.dumps(ritualisticas_counts),
            "proximas_atividades": proximas_atividades,
            "atividades_recentes": atividades_recentes,
        },
    )