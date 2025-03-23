from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Professor
from .forms import ProfessorForm
from core.utils import registrar_log, adicionar_mensagem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO

@login_required
def listar_professores(request):
    """Exibe a lista de professores cadastrados com paginação e filtros"""
    professores_list = Professor.objects.all()
    
    # Lista de especialidades para o filtro
    especialidades = Professor.objects.values_list('especialidade', flat=True).distinct()
    
    # Parâmetros de busca e filtros
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    especialidade = request.GET.get('especialidade', '')
    
    # Aplicar filtros
    if query:
        professores_list = professores_list.filter(
            nome__icontains=query
        ) | professores_list.filter(
            email__icontains=query
        ) | professores_list.filter(
            especialidade__icontains=query
        )
    
    if status == 'ativo':
        professores_list = professores_list.filter(ativo=True)
    elif status == 'inativo':
        professores_list = professores_list.filter(ativo=False)
    
    if especialidade:
        professores_list = professores_list.filter(especialidade=especialidade)
    
    # Paginação
    paginator = Paginator(professores_list, 10)  # 10 professores por página
    page = request.GET.get('page')
    
    try:
        professores = paginator.page(page)
    except PageNotAnInteger:
        professores = paginator.page(1)
    except EmptyPage:
        professores = paginator.page(paginator.num_pages)
    
    return render(request, 'professores/listar_professores.html', {
        'professores': professores,
        'titulo': 'Lista de Professores',
        'query': query,
        'status': status,
        'especialidade': especialidade,
        'especialidades': especialidades
    })

@login_required
def cadastrar_professor(request):
    """Cadastra um novo professor"""
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save()
            registrar_log(request, f'Professor {professor.nome} cadastrado com sucesso')
            adicionar_mensagem(request, 'sucesso', 'Professor cadastrado com sucesso!')
            return redirect('professores:listar_professores')
    else:
        form = ProfessorForm()
    
    return render(request, 'professores/cadastrar_professor.html', {
        'form': form,
        'titulo': 'Cadastrar Professor',
        'botao': 'Cadastrar'
    })

@login_required
def detalhes_professor(request, professor_id):
    """Exibe os detalhes de um professor específico"""
    professor = get_object_or_404(Professor, pk=professor_id)
    return render(request, 'professores/detalhes_professor.html', {
        'professor': professor,
        'titulo': f'Detalhes do Professor: {professor.nome}'
    })

@login_required
def editar_professor(request, professor_id):
    """Edita as informações de um professor e registra alterações"""
    professor = get_object_or_404(Professor, pk=professor_id)
    
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            # Registrar alterações antes de salvar
            for campo in form.changed_data:
                valor_antigo = getattr(professor, campo)
                valor_novo = form.cleaned_data[campo]
                
                # Não registrar se os valores forem iguais
                if valor_antigo != valor_novo:
                    HistoricoAlteracaoProfessor.objects.create(
                        professor=professor,
                        campo=campo,
                        valor_antigo=str(valor_antigo),
                        valor_novo=str(valor_novo),
                        usuario=request.user.username
                    )
            
            form.save()
            registrar_log(request, f'Professor {professor.nome} atualizado')
            adicionar_mensagem(request, 'sucesso', 'Professor atualizado com sucesso!')
            return redirect('professores:detalhes_professor', professor_id=professor.id)
    else:
        form = ProfessorForm(instance=professor)
    
    return render(request, 'professores/cadastrar_professor.html', {
        'form': form,
        'titulo': f'Editar Professor: {professor.nome}',
        'botao': 'Atualizar',
        'professor': professor
    })

@login_required
def excluir_professor(request, professor_id):
    """Exclui um professor do sistema"""
    professor = get_object_or_404(Professor, pk=professor_id)
    
    if request.method == 'POST':
        nome_professor = professor.nome
        professor.delete()
        registrar_log(request, f'Professor {nome_professor} excluído', tipo='AVISO')
        adicionar_mensagem(request, 'aviso', f'Professor {nome_professor} excluído com sucesso!')
        return redirect('professores:listar_professores')
    
    return render(request, 'professores/confirmar_exclusao.html', {
        'professor': professor,
        'titulo': f'Confirmar Exclusão: {professor.nome}'
    })

@login_required
def exportar_professores_csv(request):
    """Exporta a lista de professores em formato CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="professores.csv"'
    
    # Aplicar filtros se existirem
    professores = Professor.objects.all()
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    especialidade = request.GET.get('especialidade', '')
    
    if query:
        professores = professores.filter(
            nome__icontains=query
        ) | professores.filter(
            email__icontains=query
        ) | professores.filter(
            especialidade__icontains=query
        )
    
    if status == 'ativo':
        professores = professores.filter(ativo=True)
    elif status == 'inativo':
        professores = professores.filter(ativo=False)
    
    if especialidade:
        professores = professores.filter(especialidade=especialidade)
    
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Email', 'Telefone', 'Especialidade', 'Status', 'Data de Cadastro'])
    
    for professor in professores:
        writer.writerow([
            professor.nome,
            professor.email,
            professor.telefone or 'Não informado',
            professor.especialidade,
            'Ativo' if professor.ativo else 'Inativo',
            professor.data_cadastro.strftime('%d/%m/%Y %H:%M')
        ])
    
    registrar_log(request, f'Exportou lista de professores em CSV')
    return response

@login_required
def exportar_professores_pdf(request):
    """Exporta a lista de professores em formato PDF"""
    # Aplicar filtros se existirem
    professores = Professor.objects.all()
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    especialidade = request.GET.get('especialidade', '')
    
    if query:
        professores = professores.filter(
            nome__icontains=query
        ) | professores.filter(
            email__icontains=query
        ) | professores.filter(
            especialidade__icontains=query
        )
    
    if status == 'ativo':
        professores = professores.filter(ativo=True)
    elif status == 'inativo':
        professores = professores.filter(ativo=False)
    
    if especialidade:
        professores = professores.filter(especialidade=especialidade)
    
    # Criar PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Dados da tabela
    data = [['Nome', 'Email', 'Especialidade', 'Status']]
    for professor in professores:
        data.append([
            professor.nome,
            professor.email,
            professor.especialidade,
            'Ativo' if professor.ativo else 'Inativo'
        ])
    
    # Criar tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    # Retornar o PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="professores.pdf"'
    
    registrar_log(request, f'Exportou lista de professores em PDF')
    return response

@login_required
def estatisticas_professores(request):
    """Exibe estatísticas sobre os professores cadastrados"""
    total_professores = Professor.objects.count()
    professores_ativos = Professor.objects.filter(ativo=True).count()
    professores_inativos = Professor.objects.filter(ativo=False).count()
    
    # Contagem por especialidade
    especialidades = Professor.objects.values('especialidade').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Professores mais recentes
    professores_recentes = Professor.objects.order_by('-data_cadastro')[:5]
    
    return render(request, 'professores/estatisticas_professores.html', {
        'total_professores': total_professores,
        'professores_ativos': professores_ativos,
        'professores_inativos': professores_inativos,
        'especialidades': especialidades,
        'professores_recentes': professores_recentes,
        'titulo': 'Estatísticas de Professores'
    })
