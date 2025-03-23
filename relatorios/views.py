from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from alunos.models import Aluno
from presencas.models import PresencaAcademica
from punicoes.models import Punicao
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

@login_required
def index(request):
    return render(request, 'relatorios/index.html')

@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
def relatorio_alunos(request):
    # Obter parâmetros de filtro
    nome = request.GET.get('nome', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todos os alunos
    alunos = Aluno.objects.all()
    
    # Aplicar filtros
    if nome:
        alunos = alunos.filter(nome__icontains=nome)
    if data_inicio:
        alunos = alunos.filter(data_nascimento__gte=data_inicio)
    if data_fim:
        alunos = alunos.filter(data_nascimento__lte=data_fim)
    
    context = {
        'alunos': alunos,
        'nome': nome,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'relatorios/relatorio_alunos.html', context)

@login_required
@permission_required('alunos.view_aluno', raise_exception=True)
def relatorio_alunos_pdf(request):
    # Obter parâmetros de filtro
    nome = request.GET.get('nome', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todos os alunos
    alunos = Aluno.objects.all()
    
    # Aplicar filtros
    if nome:
        alunos = alunos.filter(nome__icontains=nome)
    if data_inicio:
        alunos = alunos.filter(data_nascimento__gte=data_inicio)
    if data_fim:
        alunos = alunos.filter(data_nascimento__lte=data_fim)
    
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
    elementos.append(Paragraph("Relatório de Alunos", estilo_titulo))
    
    # Criar dados da tabela
    data = [['Nome', 'CPF', 'Email', 'Data de Nascimento']]  # Linha de cabeçalho
    for aluno in alunos:
        data.append([
            aluno.nome,
            aluno.cpf,
            aluno.email,
            aluno.data_nascimento.strftime('%d/%m/%Y')
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
    filename = f"relatorio_alunos_{data_atual}.pdf"
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas(request):
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
    
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    
    context = {
        'presencas': presencas,
        'alunos': alunos,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'relatorios/relatorio_presencas.html', context)

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas_pdf(request):
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
    data = [['Aluno', 'Turma', 'Data', 'Status']]  # Linha de cabeçalho
    for presenca in presencas:
        data.append([
            presenca.aluno.nome,
            presenca.turma.nome if hasattr(presenca, 'turma') and presenca.turma else "N/A",
            presenca.data.strftime('%d/%m/%Y'),
            "Presente" if presenca.presente else "Ausente"
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
@permission_required('punicoes.view_punicao', raise_exception=True)
def relatorio_punicoes(request):
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    tipo_punicao = request.GET.get('tipo_punicao', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todas as punições
    punicoes = Punicao.objects.all().select_related('aluno')
    
    # Aplicar filtros
    if aluno_id:
        punicoes = punicoes.filter(aluno_id=aluno_id)
    if tipo_punicao:
        punicoes = punicoes.filter(tipo_punicao=tipo_punicao)
    if data_inicio:
        punicoes = punicoes.filter(data__gte=data_inicio)
    if data_fim:
        punicoes = punicoes.filter(data__lte=data_fim)
    
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    tipos_punicao = Punicao.objects.values_list('tipo_punicao', flat=True).distinct()
    
    context = {
        'punicoes': punicoes,
        'alunos': alunos,
        'tipos_punicao': tipos_punicao,
        'aluno_id': aluno_id,
        'tipo_punicao': tipo_punicao,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'relatorios/relatorio_punicoes.html', context)

@login_required
@permission_required('punicoes.view_punicao', raise_exception=True)
def relatorio_punicoes_pdf(request):
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    tipo_punicao = request.GET.get('tipo_punicao', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Começar com todas as punições
    punicoes = Punicao.objects.all().select_related('aluno')
    
    # Aplicar filtros
    if aluno_id:
        punicoes = punicoes.filter(aluno_id=aluno_id)
    if tipo_punicao:
        punicoes = punicoes.filter(tipo_punicao=tipo_punicao)
    if data_inicio:
        punicoes = punicoes.filter(data__gte=data_inicio)
    if data_fim:
        punicoes = punicoes.filter(data__lte=data_fim)
    
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
    elementos.append(Paragraph("Relatório de Punições", estilo_titulo))
    
    # Criar dados da tabela
    data = [['Aluno', 'Tipo de Punição', 'Data', 'Descrição']]  # Linha de cabeçalho
    for punicao in punicoes:
        data.append([
            punicao.aluno.nome,
            punicao.tipo_punicao,
            punicao.data.strftime('%d/%m/%Y'),
            punicao.descricao[:100] + '...' if len(punicao.descricao) > 100 else punicao.descricao
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
    filename = f"relatorio_punicoes_{data_atual}.pdf"
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
