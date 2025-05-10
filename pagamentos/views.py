from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum, Count
from .models import Pagamento
from alunos.models import Aluno
import csv
import datetime

@login_required
def listar_pagamentos(request):
    """Lista todos os pagamentos cadastrados."""
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    status = request.GET.get('status', '')
    periodo = request.GET.get('periodo', '')
    
    # Iniciar queryset
    pagamentos = Pagamento.objects.all().select_related('aluno')
    
    # Aplicar filtros
    if aluno_id:
        pagamentos = pagamentos.filter(aluno__cpf=aluno_id)
    
    if status:
        pagamentos = pagamentos.filter(status=status)
    
    if periodo:
        hoje = datetime.datetime.now().date()
        
        if periodo == 'atual':
            # Mês atual
            pagamentos = pagamentos.filter(data_pagamento__month=hoje.month, data_pagamento__year=hoje.year)
        elif periodo == 'ultimo_mes':
            # Último mês
            um_mes_atras = hoje - datetime.timedelta(days=30)
            pagamentos = pagamentos.filter(data_pagamento__gte=um_mes_atras)
        elif periodo == 'ultimo_trimestre':
            # Último trimestre
            tres_meses_atras = hoje - datetime.timedelta(days=90)
            pagamentos = pagamentos.filter(data_pagamento__gte=tres_meses_atras)
        elif periodo == 'ultimo_semestre':
            # Último semestre
            seis_meses_atras = hoje - datetime.timedelta(days=180)
            pagamentos = pagamentos.filter(data_pagamento__gte=seis_meses_atras)
    
    # Calcular estatísticas
    estatisticas = {
        'total_pagamentos': pagamentos.count(),
        'valor_total': pagamentos.aggregate(Sum('valor'))['valor__sum'] or 0,
        'pagamentos_pendentes': pagamentos.filter(status='pendente').count(),
        'valor_pendente': pagamentos.filter(status='pendente').aggregate(Sum('valor'))['valor__sum'] or 0,
    }
    
    # Obter alunos para os filtros
    alunos = Aluno.objects.filter(situacao='ATIVO')
    
    context = {
        'pagamentos': pagamentos,
        'estatisticas': estatisticas,
        'alunos': alunos,
        'filtros': {
            'aluno': aluno_id,
            'status': status,
            'periodo': periodo
        }
    }
    
    return render(request, "pagamentos/listar_pagamentos.html", context)


@login_required
def detalhar_pagamento(request, pagamento_id):
    """Exibe os detalhes de um pagamento."""
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    return render(request, "pagamentos/detalhar_pagamento.html", {"pagamento": pagamento})


@login_required
def criar_pagamento(request):
    """Cria um novo pagamento."""
    if request.method == "POST":
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, "Pagamento cadastrado com sucesso!")
            return redirect("pagamentos:detalhar_pagamento", pagamento_id=pagamento.id)
    else:
        form = PagamentoForm()
    
    return render(request, "pagamentos/formulario_pagamento.html", {"form": form})


@login_required
def editar_pagamento(request, pagamento_id):
    """Edita um pagamento existente."""
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    
    if request.method == "POST":
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, "Pagamento atualizado com sucesso!")
            return redirect("pagamentos:detalhar_pagamento", pagamento_id=pagamento.id)
    else:
        form = PagamentoForm(instance=pagamento)
    
    return render(request, "pagamentos/formulario_pagamento.html", {"form": form, "pagamento": pagamento})


@login_required
def excluir_pagamento(request, pagamento_id):
    """Exclui um pagamento."""
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    
    if request.method == "POST":
        pagamento.delete()
        messages.success(request, "Pagamento excluído com sucesso!")
        return redirect("pagamentos:listar_pagamentos")
    
    return render(request, "pagamentos/excluir_pagamento.html", {"pagamento": pagamento})


def obter_pagamentos_filtrados(request):
    """Obtém os pagamentos com base nos filtros aplicados."""
    aluno_id = request.GET.get('aluno', '')
    status = request.GET.get('status', '')
    periodo = request.GET.get('periodo', '')
    
    pagamentos = Pagamento.objects.all().select_related('aluno')
    
    if aluno_id:
        pagamentos = pagamentos.filter(aluno__cpf=aluno_id)
    
    if status:
        pagamentos = pagamentos.filter(status=status)
    
    if periodo:
        hoje = datetime.datetime.now().date()
        
        if periodo == 'atual':
            # Mês atual
            pagamentos = pagamentos.filter(data_pagamento__month=hoje.month, data_pagamento__year=hoje.year)
        elif periodo == 'ultimo_mes':
            # Último mês
            um_mes_atras = hoje - datetime.timedelta(days=30)
            pagamentos = pagamentos.filter(data_pagamento__gte=um_mes_atras)
        elif periodo == 'ultimo_trimestre':
            # Último trimestre
            tres_meses_atras = hoje - datetime.timedelta(days=90)
            pagamentos = pagamentos.filter(data_pagamento__gte=tres_meses_atras)
        elif periodo == 'ultimo_semestre':
            # Último semestre
            seis_meses_atras = hoje - datetime.timedelta(days=180)
            pagamentos = pagamentos.filter(data_pagamento__gte=seis_meses_atras)
    
    return pagamentos


@login_required
def exportar_pagamentos_csv(request):
    """Exporta os dados dos pagamentos para um arquivo CSV."""
    try:
        # Obter pagamentos com os mesmos filtros da listagem
        pagamentos = obter_pagamentos_filtrados(request)
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="pagamentos.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Aluno",
            "Valor",
            "Data de Pagamento",
            "Status"
        ])
        
        for pagamento in pagamentos:
            writer.writerow([
                pagamento.aluno.nome,
                pagamento.valor,
                pagamento.data_pagamento.strftime("%d/%m/%Y"),
                pagamento.get_status_display()
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar pagamentos: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")


@login_required
def exportar_pagamentos_excel(request):
    """Exporta os dados dos pagamentos para um arquivo Excel."""
    try:
        import xlwt
        
        # Obter pagamentos com os mesmos filtros da listagem
        pagamentos = obter_pagamentos_filtrados(request)
        
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="pagamentos.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Pagamentos')
        
        # Estilos
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        # Cabeçalhos
        colunas = ['Aluno', 'Valor', 'Data de Pagamento', 'Status']
        for col_num, coluna in enumerate(colunas):
            ws.write(0, col_num, coluna, font_style)
        
        # Dados
        font_style = xlwt.XFStyle()
        for row_num, pagamento in enumerate(pagamentos, 1):
            ws.write(row_num, 0, pagamento.aluno.nome, font_style)
            ws.write(row_num, 1, float(pagamento.valor), font_style)
            ws.write(row_num, 2, pagamento.data_pagamento.strftime("%d/%m/%Y"), font_style)
            ws.write(row_num, 3, pagamento.get_status_display(), font_style)
        
        wb.save(response)
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar pagamentos para Excel: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")


@login_required
def dashboard_pagamentos(request):
    """Exibe o dashboard de pagamentos com estatísticas."""
    # Estatísticas gerais
    total_pagamentos = Pagamento.objects.count()
    valor_total = Pagamento.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    
    # Pagamentos por status
    pagamentos_por_status = Pagamento.objects.values('status').annotate(
        total=Count('id'),
        valor_total=Sum('valor')
    )
    
    # Pagamentos por mês (últimos 6 meses)
    hoje = datetime.datetime.now().date()
    seis_meses_atras = hoje - datetime.timedelta(days=180)
    
    pagamentos_por_mes = []
    for i in range(6):
        mes = hoje.month - i
        ano = hoje.year
        if mes <= 0:
            mes += 12
            ano -= 1
        
        pagamentos_mes = Pagamento.objects.filter(
            data_pagamento__month=mes,
            data_pagamento__year=ano
        )
        
        pagamentos_por_mes.append({
            'mes': datetime.date(ano, mes, 1).strftime('%b/%Y'),
            'total': pagamentos_mes.count(),
            'valor_total': pagamentos_mes.aggregate(Sum('valor'))['valor__sum'] or 0
        })
    
    # Pagamentos por aluno (top 5)
    pagamentos_por_aluno = Pagamento.objects.values('aluno__nome').annotate(
        total=Count('id'),
        valor_total=Sum('valor')
    ).order_by('-valor_total')[:5]
    
    context = {
        'total_pagamentos': total_pagamentos,
        'valor_total': valor_total,
        'pagamentos_por_status': pagamentos_por_status,
        'pagamentos_por_mes': pagamentos_por_mes,
        'pagamentos_por_aluno': pagamentos_por_aluno
    }
    
    return render(request, "pagamentos/dashboard_pagamentos.html", context)