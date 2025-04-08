from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import PresencaAcademica
from .forms import PresencaForm  # Changed from PresencaAcademicaForm to PresencaForm
from alunos.models import Aluno
from turmas.models import Turma
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
import xlsxwriter

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def listar_presencas(request):
    presencas_list = PresencaAcademica.objects.all().select_related('aluno', 'turma')

    # Filtros
    aluno_id = request.GET.get('aluno')
    turma_id = request.GET.get('turma')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if aluno_id:
        presencas_list = presencas_list.filter(aluno_id=aluno_id)
    if turma_id:
        presencas_list = presencas_list.filter(turma_id=turma_id)
    if data_inicio:
        presencas_list = presencas_list.filter(data__gte=data_inicio)
    if data_fim:
        presencas_list = presencas_list.filter(data__lte=data_fim)

    # Paginação
    paginator = Paginator(presencas_list, 10)  # 10 itens por página
    page = request.GET.get('page')

    try:
        presencas = paginator.page(page)
    except PageNotAnInteger:
        presencas = paginator.page(1)
    except EmptyPage:
        presencas = paginator.page(paginator.num_pages)

    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()

    return render(request, 'presencas/listar_presencas.html', {
        'presencas': presencas,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'alunos': alunos,
        'turmas': turmas
    })

@login_required
@permission_required('presencas.add_presencaacademica', raise_exception=True)
def registrar_presenca(request):
    """Registra a presença de um aluno."""
    if request.method == 'POST':
        form = PresencaForm(request.POST)
        if form.is_valid():
            presenca = form.save(commit=False)
            presenca.registrado_por = request.user
            presenca.save()
            messages.success(request, 'Presença registrada com sucesso!')
            return redirect('presencas:listar_presencas')
    else:
        form = PresencaForm()

    return render(request, 'presencas/registrar_presenca.html', {'form': form})

@login_required
@permission_required('presencas.change_presencaacademica', raise_exception=True)
def editar_presenca(request, id):
    """Edita um registro de presença."""
    presenca = get_object_or_404(PresencaAcademica, id=id)
    if request.method == 'POST':
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presença atualizada com sucesso!')
            return redirect('presencas:listar_presencas')
    else:
        form = PresencaForm(instance=presenca)

    return render(request, 'presencas/editar_presenca.html', {'form': form, 'presenca': presenca})

@login_required
@permission_required('presencas.delete_presencaacademica', raise_exception=True)
def excluir_presenca(request, id):
    presenca = get_object_or_404(PresencaAcademica, id=id)
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença excluída com sucesso!')
        return redirect('presencas:listar_presencas')

    return render(request, 'presencas/excluir_presenca.html', {'presenca': presenca})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def detalhar_presenca(request, id):
    """Exibe os detalhes de um registro de presença."""
    presenca = get_object_or_404(PresencaAcademica, id=id)
    return render(request, 'presencas/detalhar_presenca.html', {'presenca': presenca})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas(request):
    """Exibe um relatório de presenças com filtros."""
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Começar com todas as presenças
    presencas = PresencaAcademica.objects.all().select_related('aluno', 'turma')

    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno_id=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma_id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    # Calcular estatísticas
    presencas_count = {
        'presentes': presencas.filter(presente=True).count(),
        'ausentes': presencas.filter(presente=False).count()
    }
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()

    context = {
        'presencas': presencas,
        'alunos': alunos,
        'turmas': turmas,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'presencas_count': presencas_count,
    }
    return render(request, 'presencas/relatorio_presencas.html', context)

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas_pdf(request):
    """Gera um relatório de presenças em formato PDF."""
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Começar com todas as presenças
    presencas = PresencaAcademica.objects.all().select_related('aluno', 'turma')

    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno_id=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma_id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    # Criar um buffer para receber os dados do PDF
    buffer = BytesIO()

    # Criar o objeto PDF
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Container para os objetos 'Flowable'
    elementos = []

    # Definir estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']

    # Adicionar título
    elementos.append(Paragraph("Relatório de Presenças", estilo_titulo))

    # Criar dados da tabela
    data = [['Aluno', 'Turma', 'Data', 'Status', 'Justificativa']]  # Linha de cabeçalho
    for presenca in presencas:
        data.append([
            presenca.aluno.nome,
            presenca.turma.nome if hasattr(presenca, 'turma') and presenca.turma else "N/A",
            presenca.data.strftime('%d/%m/%Y'),
            "Presente" if presenca.presente else "Ausente",
            presenca.justificativa if presenca.justificativa else "-"
        ])

    # Criar tabela
    tabela = Table(data)

    # Adicionar estilo à tabela
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabela.setStyle(estilo)

    # Adicionar tabela aos elementos
    elementos.append(tabela)

    # Construir PDF
    doc.build(elementos)

    # Retornar resposta
    buffer.seek(0)

    # Definir nome do arquivo com data atual
    data_atual = datetime.now().strftime('%d-%m-%Y')
    filename = f"relatorio_presencas_{data_atual}.pdf"

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas_excel(request):
    """Gera um relatório de presenças em formato Excel."""
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    turma_id = request.GET.get('turma', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Começar com todas as presenças
    presencas = PresencaAcademica.objects.all().select_related('aluno', 'turma')

    # Aplicar filtros
    if aluno_id:
        presencas = presencas.filter(aluno_id=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma_id=turma_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    # Criar um buffer para receber os dados do Excel
    buffer = BytesIO()

    # Criar o objeto Excel
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet('Presenças')

    # Definir estilos
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4F81BD',
        'color': 'white',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })

    cell_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })

    # Definir largura das colunas
    worksheet.set_column('A:A', 30)  # Aluno
    worksheet.set_column('B:B', 20)  # Turma
    worksheet.set_column('C:C', 15)  # Data
    worksheet.set_column('D:D', 15)  # Status
    worksheet.set_column('E:E', 40)  # Justificativa

    # Escrever cabeçalho
    headers = ['Aluno', 'Turma', 'Data', 'Status', 'Justificativa']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Escrever dados
    for row, presenca in enumerate(presencas, start=1):
        worksheet.write(row, 0, presenca.aluno.nome, cell_format)
        worksheet.write(row, 1, presenca.turma.nome if hasattr(presenca, 'turma') and presenca.turma else "N/A", cell_format)
        worksheet.write(row, 2, presenca.data.strftime('%d/%m/%Y'), cell_format)
        worksheet.write(row, 3, "Presente" if presenca.presente else "Ausente", cell_format)
        worksheet.write(row, 4, presenca.justificativa if presenca.justificativa else "-", cell_format)

    # Adicionar estatísticas
    row = len(presencas) + 3
    worksheet.write(row, 0, "Estatísticas", workbook.add_format({'bold': True, 'font_size': 14}))

    row += 1
    worksheet.write(row, 0, "Total de Registros:")
    worksheet.write(row, 1, len(presencas))

    row += 1
    presentes = sum(1 for p in presencas if p.presente)
    worksheet.write(row, 0, "Total de Presenças:")
    worksheet.write(row, 1, presentes)

    row += 1
    worksheet.write(row, 0, "Total de Ausências:")
    worksheet.write(row, 1, len(presencas) - presentes)

    # Fechar o workbook
    workbook.close()

    # Retornar resposta
    buffer.seek(0)

    # Definir nome do arquivo com data atual
    data_atual = datetime.now().strftime('%d-%m-%Y')
    filename = f"relatorio_presencas_{data_atual}.xlsx"

    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response