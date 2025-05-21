"""
Views relacionadas ao dashboard financeiro.
"""
import datetime
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Importação dinâmica para evitar referências circulares
def get_pagamento_model():
    from pagamentos.models import Pagamento
    return Pagamento

def get_aluno_model():
    from alunos.models import Aluno
    return Aluno

@login_required
def dashboard(request):
    """
    Dashboard principal do módulo de pagamentos.
    Exibe estatísticas gerais e links para outras seções.
    """
    Pagamento = get_pagamento_model()
    Aluno = get_aluno_model()
    total_alunos = Aluno.objects.count()
    total_pagamentos = Pagamento.objects.count()
    pagamentos_pagos = Pagamento.objects.filter(status='PAGO').count()
    pagamentos_pendentes = Pagamento.objects.filter(status='PENDENTE').count()
    pagamentos_atrasados = Pagamento.objects.filter(status='ATRASADO').count()
    total_pago = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in Pagamento.objects.filter(status='PAGO')])
    total_pendente = Pagamento.objects.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
    total_atrasado = Pagamento.objects.filter(status='ATRASADO').aggregate(Sum('valor'))['valor__sum'] or 0
    pagamentos_recentes = Pagamento.objects.all().order_by('-data_pagamento')[:5]
    hoje = timezone.now().date()
    data_limite = hoje + datetime.timedelta(days=7)
    pagamentos_proximos = Pagamento.objects.filter(
        status='PENDENTE',
        data_vencimento__gte=hoje,
        data_vencimento__lte=data_limite
    ).order_by('data_vencimento')[:5]
    context = {
        'total_alunos': total_alunos,
        'total_pagamentos': total_pagamentos,
        'pagamentos_pagos': pagamentos_pagos,
        'pagamentos_pendentes': pagamentos_pendentes,
        'pagamentos_atrasados': pagamentos_atrasados,
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'total_atrasado': total_atrasado,
        'pagamentos_recentes': pagamentos_recentes,
        'pagamentos_proximos': pagamentos_proximos,
    }
    return render(request, 'pagamentos/dashboard.html', context)

@login_required
def dashboard_pagamentos(request):
    """
    Dashboard específico para análise de pagamentos.
    Exibe gráficos e estatísticas sobre pagamentos.
    """
    Pagamento = get_pagamento_model()
    hoje = timezone.now().date()
    mes_atual = hoje.replace(day=1)
    if mes_atual.month == 12:
        proximo_mes = mes_atual.replace(year=mes_atual.year + 1, month=1)
    else:
        proximo_mes = mes_atual.replace(month=mes_atual.month + 1)
    pagamentos_mes = Pagamento.objects.filter(
        data_vencimento__gte=mes_atual,
        data_vencimento__lt=proximo_mes
    )
    pagos_mes = pagamentos_mes.filter(status='PAGO').count()
    pendentes_mes = pagamentos_mes.filter(status='PENDENTE').count()
    atrasados_mes = pagamentos_mes.filter(status='ATRASADO').count()
    valor_pago_mes = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in pagamentos_mes.filter(status='PAGO')])
    valor_pendente_mes = pagamentos_mes.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
    valor_atrasado_mes = pagamentos_mes.filter(status='ATRASADO').aggregate(Sum('valor'))['valor__sum'] or 0
    dias = []
    valores_por_dia = []
    for dia in range(1, (proximo_mes - mes_atual).days):
        data = mes_atual + datetime.timedelta(days=dia-1)
        if data > hoje:
            break
        pagamentos_dia = Pagamento.objects.filter(
            data_pagamento=data,
            status='PAGO'
        )
        valor_dia = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in pagamentos_dia])
        dias.append(data.strftime('%d/%m'))
        valores_por_dia.append(float(valor_dia))
    pagamentos_por_metodo = pagamentos_mes.filter(status='PAGO').values('metodo_pagamento').annotate(
        total=Count('id')
    ).order_by('-total')
    metodos = []
    contagens = []
    for item in pagamentos_por_metodo:
        metodo = dict(Pagamento.METODO_PAGAMENTO_CHOICES).get(item['metodo_pagamento'], 'Não informado')
        metodos.append(metodo)
        contagens.append(item['total'])
    hoje = timezone.now().date()
    atrasados_ate_15 = Pagamento.objects.filter(
        status='ATRASADO',
        data_vencimento__gte=hoje - datetime.timedelta(days=15)
    ).count()
    atrasados_15_30 = Pagamento.objects.filter(
        status='ATRASADO',
        data_vencimento__lt=hoje - datetime.timedelta(days=15),
        data_vencimento__gte=hoje - datetime.timedelta(days=30)
    ).count()
    atrasados_mais_30 = Pagamento.objects.filter(
        status='ATRASADO',
        data_vencimento__lt=hoje - datetime.timedelta(days=30)
    ).count()
    context = {
        'pagos_mes': pagos_mes,
        'pendentes_mes': pendentes_mes,
        'atrasados_mes': atrasados_mes,
        'valor_pago_mes': valor_pago_mes,
        'valor_pendente_mes': valor_pendente_mes,
        'valor_atrasado_mes': valor_atrasado_mes,
        'dias': json.dumps(dias),
        'valores_por_dia': json.dumps(valores_por_dia),
        'metodos': json.dumps(metodos),
        'contagens': json.dumps(contagens),
        'atrasados_ate_15': atrasados_ate_15,
        'atrasados_15_30': atrasados_15_30,
        'atrasados_mais_30': atrasados_mais_30,
        'mes_atual': mes_atual.strftime('%B/%Y')
    }
    return render(request, 'pagamentos/dashboard_pagamentos.html', context)

@login_required
def dashboard_financeiro(request):
    """Exibe o dashboard financeiro."""
    Pagamento = get_pagamento_model()
    hoje = timezone.now().date()
    pagamentos_pagos = Pagamento.objects.filter(status='PAGO')
    pagamentos_pendentes = Pagamento.objects.filter(status='PENDENTE')
    pagamentos_atrasados = Pagamento.objects.filter(status='ATRASADO')
    total_pago = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in pagamentos_pagos])
    total_pendente = pagamentos_pendentes.aggregate(Sum('valor'))['valor__sum'] or 0
    total_atrasado = pagamentos_atrasados.aggregate(Sum('valor'))['valor__sum'] or 0
    pagamentos_por_mes = []
    meses = []
    valores_pagos = []
    valores_pendentes = []
    for i in range(5, -1, -1):
        mes_data = hoje.replace(day=1)
        if i > 0:
            ano = mes_data.year
            mes = mes_data.month - i
            if mes <= 0:
                mes = 12 + mes
                ano -= 1
            mes_data = mes_data.replace(year=ano, month=mes)
        if mes_data.month == 12:
            ultimo_dia = mes_data.replace(year=mes_data.year + 1, month=1, day=1) - datetime.timedelta(days=1)
        else:
            ultimo_dia = mes_data.replace(month=mes_data.month + 1, day=1) - datetime.timedelta(days=1)
        pagamentos_mes = Pagamento.objects.filter(
            data_vencimento__gte=mes_data,
            data_vencimento__lte=ultimo_dia
        )
        total_pago_mes = sum([p.valor_pago if p.valor_pago is not None else p.valor for p in pagamentos_mes.filter(status='PAGO')])
        total_pendente_mes = pagamentos_mes.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
        meses.append(mes_data.strftime('%b/%Y'))
        valores_pagos.append(float(total_pago_mes))
        valores_pendentes.append(float(total_pendente_mes))
    pagamentos_por_metodo = pagamentos_pagos.values('metodo_pagamento').annotate(
        total=Count('id')
    ).order_by('-total')
    metodos = []
    contagens = []
    for item in pagamentos_por_metodo:
        metodo = dict(Pagamento.METODO_PAGAMENTO_CHOICES).get(item['metodo_pagamento'], 'Não informado')
        metodos.append(metodo)
        contagens.append(item['total'])
    context = {
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'total_atrasado': total_atrasado,
        'meses': json.dumps(meses),
        'valores_pagos': json.dumps(valores_pagos),
        'valores_pendentes': json.dumps(valores_pendentes),
        'metodos': json.dumps(metodos),
        'contagens': json.dumps(contagens)
    }
    return render(request, 'pagamentos/dashboard_financeiro.html', context)