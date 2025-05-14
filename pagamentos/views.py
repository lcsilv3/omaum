from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from .models import Pagamento
from .forms import PagamentoForm  # Adicionando a importação que estava faltando
import csv
import datetime

@login_required
def listar_pagamentos(request):
    """Lista todos os pagamentos cadastrados."""
    # Obter parâmetros de busca e filtro
    query = request.GET.get("q", "")
    aluno_id = request.GET.get("aluno", "")
    status = request.GET.get("status", "")
    
    # Filtrar pagamentos
    pagamentos = Pagamento.objects.all().select_related('aluno')
    
    if query:
        pagamentos = pagamentos.filter(
            Q(aluno__nome__icontains=query) |
            Q(descricao__icontains=query)
        )
    
    if aluno_id:
        pagamentos = pagamentos.filter(aluno__cpf=aluno_id)
    
    if status:
        pagamentos = pagamentos.filter(status=status)
    
    # Ordenar por data mais recente
    pagamentos = pagamentos.order_by('-data_vencimento')
    
    # Paginação
    paginator = Paginator(pagamentos, 10)  # 10 pagamentos por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # Obter alunos para o filtro
    from alunos.models import Aluno
    alunos = Aluno.objects.all().order_by('nome')
    
    context = {
        "pagamentos": page_obj,
        "page_obj": page_obj,
        "query": query,
        "alunos": alunos,
        "aluno_selecionado": aluno_id,
        "status_selecionado": status,
        "total_pagamentos": pagamentos.count(),
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
            try:
                # Garantir que data_vencimento tenha um valor
                pagamento = form.save(commit=False)
                
                # Se o status for PAGO, garantir que data_pagamento e valor_pago estejam preenchidos
                if pagamento.status == 'PAGO':
                    if not pagamento.data_pagamento:
                        from django.utils import timezone
                        pagamento.data_pagamento = timezone.now().date()
                    if not pagamento.valor_pago:
                        pagamento.valor_pago = pagamento.valor
                
                pagamento.save()
                
                messages.success(request, "Pagamento registrado com sucesso!")
                return redirect("pagamentos:detalhar_pagamento", pagamento_id=pagamento.id)
            except Exception as e:
                messages.error(request, f"Erro ao salvar pagamento: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
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
            try:
                # Garantir que data_vencimento tenha um valor
                pagamento = form.save(commit=False)
                
                # Se o status for PAGO, garantir que data_pagamento e valor_pago estejam preenchidos
                if pagamento.status == 'PAGO':
                    if not pagamento.data_pagamento:
                        pagamento.data_pagamento = timezone.now().date()
                    if not pagamento.valor_pago:
                        pagamento.valor_pago = pagamento.valor
                
                pagamento.save()
                
                messages.success(request, "Pagamento atualizado com sucesso!")
                return redirect("pagamentos:detalhar_pagamento", pagamento_id=pagamento.id)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar pagamento: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        # Aqui está a modificação principal
        form = PagamentoForm(instance=pagamento)
        
        # Garantir que as datas estejam no formato correto para o input type="date"
        if pagamento.data_vencimento:
            form.initial['data_vencimento'] = pagamento.data_vencimento.strftime('%Y-%m-%d')
        
        if pagamento.data_pagamento:
            form.initial['data_pagamento'] = pagamento.data_pagamento.strftime('%Y-%m-%d')
    
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

@login_required
def registrar_pagamento(request, pagamento_id):
    """Registra o pagamento de uma fatura."""
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    
    if request.method == "POST":
        data_pagamento = request.POST.get("data_pagamento")
        valor_pago = request.POST.get("valor_pago")
        
        try:
            data_pagamento = datetime.datetime.strptime(data_pagamento, "%Y-%m-%d").date()
            valor_pago = float(valor_pago)
            
            pagamento.data_pagamento = data_pagamento
            pagamento.valor_pago = valor_pago
            pagamento.status = "PAGO"
            pagamento.save()
            
            messages.success(request, "Pagamento registrado com sucesso!")
            return redirect("pagamentos:detalhar_pagamento", pagamento_id=pagamento.id)
        except Exception as e:
            messages.error(request, f"Erro ao registrar pagamento: {str(e)}")
    
    return render(request, "pagamentos/registrar_pagamento.html", {"pagamento": pagamento})

@login_required
def exportar_pagamentos_csv(request):
    """Exporta os pagamentos para um arquivo CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagamentos.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Aluno', 'Descrição', 'Valor', 'Data Vencimento', 'Status', 'Data Pagamento', 'Valor Pago'])
    
    pagamentos = Pagamento.objects.all().select_related('aluno')
    for pagamento in pagamentos:
        writer.writerow([
            pagamento.aluno.nome,
            pagamento.descricao,
            pagamento.valor,
            pagamento.data_vencimento.strftime('%d/%m/%Y'),
            pagamento.get_status_display(),
            pagamento.data_pagamento.strftime('%d/%m/%Y') if pagamento.data_pagamento else 'N/A',
            pagamento.valor_pago if pagamento.valor_pago else 'N/A',
        ])
    
    return response

@login_required
def exportar_pagamentos_excel(request):
    """Exporta os pagamentos para um arquivo Excel."""
    import xlsxwriter
    from io import BytesIO
    
    # Criar um buffer de memória para o arquivo Excel
    output = BytesIO()
    
    # Criar um novo workbook e adicionar uma planilha
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Pagamentos')
    
    # Definir estilos
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    })
    
    # Escrever cabeçalhos
    headers = ['Aluno', 'Descrição', 'Valor', 'Data Vencimento', 'Status', 'Data Pagamento', 'Valor Pago']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)
    
    # Buscar todos os pagamentos
    pagamentos = Pagamento.objects.all().select_related('aluno')
    
    # Escrever dados
    for row_num, pagamento in enumerate(pagamentos, 1):
        worksheet.write(row_num, 0, pagamento.aluno.nome)
        worksheet.write(row_num, 1, pagamento.descricao)
        worksheet.write(row_num, 2, float(pagamento.valor))
        worksheet.write(row_num, 3, pagamento.data_vencimento.strftime('%d/%m/%Y'))
        worksheet.write(row_num, 4, pagamento.get_status_display())
        worksheet.write(row_num, 5, pagamento.data_pagamento.strftime('%d/%m/%Y') if pagamento.data_pagamento else 'N/A')
        worksheet.write(row_num, 6, float(pagamento.valor_pago) if pagamento.valor_pago else 'N/A')
    
    # Fechar o workbook
    workbook.close()
    
    # Configurar a resposta HTTP
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="pagamentos.xlsx"'
    
    return response

@login_required
def dashboard_pagamentos(request):
    """Exibe um dashboard com estatísticas sobre os pagamentos."""
    # Estatísticas gerais
    total_pagamentos = Pagamento.objects.count()
    total_valor = Pagamento.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    total_pago = Pagamento.objects.filter(status='PAGO').aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0
    total_pendente = Pagamento.objects.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
    
    # Pagamentos por status
    pagamentos_por_status = Pagamento.objects.values('status').annotate(
        total=Count('id'),
        valor_total=Sum('valor')
    ).order_by('status')
    
    # Pagamentos recentes
    pagamentos_recentes = Pagamento.objects.all().select_related('aluno').order_by('-data_vencimento')[:5]
    
    # Pagamentos atrasados
    hoje = datetime.date.today()
    pagamentos_atrasados = Pagamento.objects.filter(
        status='PENDENTE',
        data_vencimento__lt=hoje
    ).select_related('aluno').order_by('data_vencimento')
    
    context = {
        'total_pagamentos': total_pagamentos,
        'total_valor': total_valor,
        'total_pago': total_pago,
        'total_pendente': total_pendente,
        'pagamentos_por_status': pagamentos_por_status,
        'pagamentos_recentes': pagamentos_recentes,
        'pagamentos_atrasados': pagamentos_atrasados,
    }
    
    return render(request, "pagamentos/dashboard_pagamentos.html", context)

@login_required
def buscar_alunos(request):
    """API endpoint para buscar alunos."""
    query = request.GET.get("q", "")
    if len(query) < 2:
        return JsonResponse({"results": []})
    
    try:
        from alunos.models import Aluno
        alunos = Aluno.objects.filter(
            Q(nome__icontains=query) |
            Q(cpf__icontains=query)
        )[:10]
        
        results = []
        for aluno in alunos:
            results.append({
                "id": aluno.cpf,
                "text": f"{aluno.nome} (CPF: {aluno.cpf})"
            })
        
        return JsonResponse({"results": results})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
