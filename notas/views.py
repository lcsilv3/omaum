from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Avg, Max, Min
from .models import Nota
from alunos.models import Aluno
from cursos.models import Curso
from .forms import NotaForm
import csv
import datetime


@login_required
def listar_notas(request):
    """Lista todas as notas cadastradas."""
    # Obter parâmetros de filtro
    aluno_id = request.GET.get('aluno', '')
    curso_id = request.GET.get('curso', '')
    periodo = request.GET.get('periodo', '')
    
    # Iniciar queryset
    notas = Nota.objects.all().select_related('aluno', 'curso')
    
    # Aplicar filtros
    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)
    
    if curso_id:
        notas = notas.filter(curso__id=curso_id)
    
    if periodo:
        hoje = datetime.datetime.now().date()
        
        if periodo == 'atual':
            # Mês atual
            notas = notas.filter(data__month=hoje.month, data__year=hoje.year)
        elif periodo == 'ultimo_mes':
            # Último mês
            um_mes_atras = hoje - datetime.timedelta(days=30)
            notas = notas.filter(data__gte=um_mes_atras)
        elif periodo == 'ultimo_trimestre':
            # Último trimestre
            tres_meses_atras = hoje - datetime.timedelta(days=90)
            notas = notas.filter(data__gte=tres_meses_atras)
        elif periodo == 'ultimo_semestre':
            # Último semestre
            seis_meses_atras = hoje - datetime.timedelta(days=180)
            notas = notas.filter(data__gte=seis_meses_atras)
    
    # Calcular estatísticas
    estatisticas = {
        'media_geral': notas.aggregate(Avg('valor'))['valor__avg'] or 0,
        'nota_maxima': notas.aggregate(Max('valor'))['valor__max'] or 0,
        'nota_minima': notas.aggregate(Min('valor'))['valor__min'] or 0,
        'total_notas': notas.count(),
    }
    
    # Obter alunos e cursos para os filtros
    alunos = Aluno.objects.filter(situacao='ATIVO')
    cursos = Curso.objects.filter(ativo=True)
    
    context = {
        'notas': notas,
        'estatisticas': estatisticas,
        'alunos': alunos,
        'cursos': cursos,
        'filtros': {
            'aluno': aluno_id,
            'curso': curso_id,
            'periodo': periodo
        }
    }
    
    return render(request, "notas/listar_notas.html", context)


@login_required
def detalhar_nota(request, nota_id):
    """Exibe os detalhes de uma nota."""
    nota = get_object_or_404(Nota, id=nota_id)
    return render(request, "notas/detalhar_nota.html", {"nota": nota})


@login_required
def criar_nota(request):
    """Cria uma nova nota."""
    if request.method == "POST":
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save()
            messages.success(request, "Nota cadastrada com sucesso!")
            return redirect("notas:detalhar_nota", nota_id=nota.id)
    else:
        form = NotaForm()
    
    return render(request, "notas/formulario_nota.html", {"form": form})


@login_required
def editar_nota(request, nota_id):
    """Edita uma nota existente."""
    nota = get_object_or_404(Nota, id=nota_id)
    
    if request.method == "POST":
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            nota = form.save()
            messages.success(request, "Nota atualizada com sucesso!")
            return redirect("notas:detalhar_nota", nota_id=nota.id)
    else:
        form = NotaForm(instance=nota)
    
    return render(request, "notas/formulario_nota.html", {"form": form, "nota": nota})


@login_required
def excluir_nota(request, nota_id):
    """Exclui uma nota."""
    nota = get_object_or_404(Nota, id=nota_id)
    
    if request.method == "POST":
        nota.delete()
        messages.success(request, "Nota excluída com sucesso!")
        return redirect("notas:listar_notas")
    
    return render(request, "notas/excluir_nota.html", {"nota": nota})


def obter_notas_filtradas(request):
    """Obtém as notas com base nos filtros aplicados."""
    aluno_id = request.GET.get('aluno', '')
    curso_id = request.GET.get('curso', '')
    periodo = request.GET.get('periodo', '')
    
    notas = Nota.objects.all().select_related('aluno', 'curso')
    
    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)
    
    if curso_id:
        notas = notas.filter(curso__id=curso_id)
    
    if periodo:
        hoje = datetime.datetime.now().date()
        
        if periodo == 'atual':
            # Mês atual
            notas = notas.filter(data__month=hoje.month, data__year=hoje.year)
        elif periodo == 'ultimo_mes':
            # Último mês
            um_mes_atras = hoje - datetime.timedelta(days=30)
            notas = notas.filter(data__gte=um_mes_atras)
        elif periodo == 'ultimo_trimestre':
            # Último trimestre
            tres_meses_atras = hoje - datetime.timedelta(days=90)
            notas = notas.filter(data__gte=tres_meses_atras)
        elif periodo == 'ultimo_semestre':
            # Último semestre
            seis_meses_atras = hoje - datetime.timedelta(days=180)
            notas = notas.filter(data__gte=seis_meses_atras)
    
    return notas


@login_required
def exportar_notas_csv(request):
    """Exporta os dados das notas para um arquivo CSV."""
    try:
        # Obter notas com os mesmos filtros da listagem
        notas = obter_notas_filtradas(request)
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="notas.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Aluno",
            "Curso",
            "Nota",
            "Data",
            "Tipo de Avaliação",
            "Observações"
        ])
        
        for nota in notas:
            writer.writerow([
                nota.aluno.nome,
                nota.curso.nome,
                nota.valor,
                nota.data.strftime("%d/%m/%Y"),
                nota.get_tipo_avaliacao_display() if hasattr(nota, "get_tipo_avaliacao_display") else "Regular",
                nota.observacoes or ""
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar notas: {str(e)}")
        return redirect("notas:listar_notas")


@login_required
def exportar_notas_excel(request):
    """Exporta os dados das notas para um arquivo Excel."""
    try:
        import xlwt
        
        # Obter notas com os mesmos filtros da listagem
        notas = obter_notas_filtradas(request)
        
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="notas.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Notas')
        
        # Estilos
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        
        # Cabeçalhos
        colunas = ['Aluno', 'Curso', 'Nota', 'Data', 'Tipo de Avaliação', 'Observações']
        for col_num, coluna in enumerate(colunas):
            ws.write(0, col_num, coluna, font_style)
        
        # Dados
        font_style = xlwt.XFStyle()
        for row_num, nota in enumerate(notas, 1):
            ws.write(row_num, 0, nota.aluno.nome, font_style)
            ws.write(row_num, 1, nota.curso.nome, font_style)
            ws.write(row_num, 2, float(nota.valor), font_style)
            ws.write(row_num, 3, nota.data.strftime("%d/%m/%Y"), font_style)
            ws.write(row_num, 4, nota.get_tipo_avaliacao_display() if hasattr(nota, "get_tipo_avaliacao_display") else "Regular", font_style)
            ws.write(row_num, 5, nota.observacoes or "", font_style)
        
        wb.save(response)
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar notas para Excel: {str(e)}")
        return redirect("notas:listar_notas")


@login_required
def dashboard_notas(request):
    """Exibe o dashboard de notas com estatísticas."""
    # Estatísticas gerais
    total_notas = Nota.objects.count()
    media_geral = Nota.objects.aggregate(Avg('valor'))['valor__avg'] or 0
    
    # Notas por curso
    cursos = Curso.objects.filter(ativo=True)
    notas_por_curso = []
    
    for curso in cursos:
        notas_curso = Nota.objects.filter(curso=curso)
        if notas_curso.exists():
            media_curso = notas_curso.aggregate(Avg('valor'))['valor__avg'] or 0
            notas_por_curso.append({
                'curso': curso.nome,
                'media': media_curso,
                'total': notas_curso.count()
            })
    
    # Melhores alunos
    alunos = Aluno.objects.filter(situacao='ATIVO')
    melhores_alunos = []
    
    for aluno in alunos[:10]:  # Limitar a 10 alunos para performance
        notas_aluno = Nota.objects.filter(aluno=aluno)
        if notas_aluno.exists():
            media_aluno = notas_aluno.aggregate(Avg('valor'))['valor__avg'] or 0
            melhores_alunos.append({
                'aluno': aluno,
                'media': media_aluno,
                'total_notas': notas_aluno.count()
            })
    
    # Ordenar por média decrescente
    melhores_alunos.sort(key=lambda x: x['media'], reverse=True)
    melhores_alunos = melhores_alunos[:5]  # Top 5
    
    context = {
        'total_notas': total_notas,
        'media_geral': media_geral,
        'notas_por_curso': notas_por_curso,
        'melhores_alunos': melhores_alunos
    }
    
    return render(request, "notas/dashboard_notas.html", context)


@login_required
def registrar_nota_aluno(request, aluno_cpf):
    """Registra uma nota para um aluno específico."""
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save()
            messages.success(request, 'Nota registrada com sucesso!')
            return redirect('notas:detalhar_nota', nota_id=nota.id)
    else:
        # Pré-preencher o formulário com o aluno selecionado
        form = NotaForm(initial={'aluno': aluno})
    
    return render(request, 'notas/formulario_nota.html', {
        'form': form,
        'aluno': aluno,
        'registro_direto': True
    })


@login_required
def relatorio_notas_aluno(request, aluno_cpf):
    """Exibe um relatório de notas de um aluno específico."""
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    
    # Obter todas as notas do aluno
    notas = Nota.objects.filter(aluno=aluno).select_related('curso', 'turma')
    
    # Agrupar notas por curso
    cursos_info = []
    cursos_ids = notas.values_list('curso', flat=True).distinct()
    
    for curso_id in cursos_ids:
        curso = Curso.objects.get(id=curso_id)
        notas_curso = notas.filter(curso=curso)
        
        # Calcular média ponderada
        total_pesos = sum(nota.peso for nota in notas_curso)
        if total_pesos > 0:
            media = sum(nota.valor * nota.peso for nota in notas_curso) / total_pesos
        else:
            media = 0
        
        # Determinar situação
        if media >= 7:
            situacao = 'Aprovado'
        elif media >= 5:
            situacao = 'Em Recuperação'
        else:
            situacao = 'Reprovado'
        
        cursos_info.append({
            'id': curso.id,
            'nome': curso.nome,
            'notas': notas_curso,
            'media': round(media, 1),
            'situacao': situacao
        })
    
    context = {
        'aluno': aluno,
        'cursos': cursos_info,
        'total_cursos': len(cursos_info),
    }
    
    return render(request, 'notas/relatorio_notas_aluno.html', context)


@login_required
def relatorio_notas_turma(request, turma_id):
    """Exibe um relatório de notas de uma turma específica."""
    turma = get_object_or_404(Turma, id=turma_id)
    
    # Obter todas as notas da turma
    notas = Nota.objects.filter(turma=turma).select_related('aluno')
    
    # Agrupar notas por aluno
    alunos_info = []
    alunos_ids = notas.values_list('aluno', flat=True).distinct()
    
    for aluno_id in alunos_ids:
        aluno = Aluno.objects.get(cpf=aluno_id)
        notas_aluno = notas.filter(aluno=aluno)
        
        # Calcular média ponderada
        total_pesos = sum(nota.peso for nota in notas_aluno)
        if total_pesos > 0:
            media = sum(nota.valor * nota.peso for nota in notas_aluno) / total_pesos
        else:
            media = 0
        
        # Determinar situação
        if media >= 7:
            situacao = 'Aprovado'
        elif media >= 5:
            situacao = 'Em Recuperação'
        else:
            situacao = 'Reprovado'
        
        alunos_info.append({
            'aluno': aluno,
            'notas': notas_aluno,
            'media': round(media, 1),
            'situacao': situacao
        })
    
    # Ordenar por nome do aluno
    alunos_info.sort(key=lambda x: x['aluno'].nome)
    
    context = {
        'turma': turma,
        'alunos': alunos_info,
        'total_alunos': len(alunos_info),
    }
    
    return render(request, 'notas/relatorio_notas_turma.html', context)
from django.http import HttpResponse
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
from django.utils import timezone
import pandas as pd
from io import BytesIO

def exportar_notas_pdf(request):
    """Exporta a lista de notas para PDF."""
    # Obter filtros
    aluno_id = request.GET.get('aluno', '')
    curso_id = request.GET.get('curso', '')
    
    # Filtrar notas
    notas = Nota.objects.all()
    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)
    if curso_id:
        notas = notas.filter(curso__id=curso_id)
    
    # Calcular médias
    alunos_medias = {}
    for nota in notas:
        if nota.aluno.cpf not in alunos_medias:
            alunos_medias[nota.aluno.cpf] = {
                'aluno': nota.aluno,
                'notas': [],
                'soma': 0,
                'count': 0
            }
        alunos_medias[nota.aluno.cpf]['notas'].append(nota)
        alunos_medias[nota.aluno.cpf]['soma'] += nota.valor
        alunos_medias[nota.aluno.cpf]['count'] += 1
    
    for cpf in alunos_medias:
        if alunos_medias[cpf]['count'] > 0:
            alunos_medias[cpf]['media'] = alunos_medias[cpf]['soma'] / alunos_medias[cpf]['count']
        else:
            alunos_medias[cpf]['media'] = 0
    
    # Renderizar o template HTML
    html_string = render_to_string(
        'notas/pdf/notas_pdf.html',
        {
            'notas': notas,
            'alunos_medias': alunos_medias.values(),
            'data_geracao': timezone.now(),
            'filtros': {
                'aluno': aluno_id,
                'curso': curso_id,
            }
        }
    )
    
    # Criar arquivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="notas.pdf"'
    
    # Gerar PDF a partir do HTML
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()
    
    # Retornar o PDF como resposta
    response.write(result)
    return response

def exportar_notas_excel(request):
    """Exporta a lista de notas para Excel."""
    # Obter filtros
    aluno_id = request.GET.get('aluno', '')
    curso_id = request.GET.get('curso', '')
    
    # Filtrar notas
    notas = Nota.objects.all()
    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)
    if curso_id:
        notas = notas.filter(curso__id=curso_id)
    
    # Preparar dados para o Excel
    data = []
    for nota in notas:
        data.append({
            'ID': nota.id,
            'Aluno': nota.aluno.nome,
            'CPF': nota.aluno.cpf,
            'Curso': nota.curso.nome,
            'Turma': nota.turma.nome if hasattr(nota, 'turma') and nota.turma else '',
            'Tipo de Avaliação': nota.get_tipo_avaliacao_display() if hasattr(nota, 'get_tipo_avaliacao_display') else '',
            'Nota': nota.valor,
            'Data': nota.data,
            'Observações': nota.observacoes if hasattr(nota, 'observacoes') else '',
        })
    
    # Criar DataFrame
    df = pd.DataFrame(data)
    
    # Criar arquivo Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Notas', index=False)
    
    # Ajustar largura das colunas
    worksheet = writer.sheets['Notas']
    for i, col in enumerate(df.columns):
        column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, column_width)
    
    # Adicionar formatação condicional para as notas
    formato_nota_alta = writer.book.add_format({'bold': True, 'font_color': 'green'})
    formato_nota_media = writer.book.add_format({'bold': True, 'font_color': 'orange'})
    formato_nota_baixa = writer.book.add_format({'bold': True, 'font_color': 'red'})
    
    # Coluna da nota (índice 6)
    worksheet.conditional_format(1, 6, len(data), 6, {'type': 'cell',
                                                      'criteria': '>=',
                                                      'value': 7,
                                                      'format': formato_nota_alta})
    worksheet.conditional_format(1, 6, len(data), 6, {'type': 'cell',
                                                      'criteria': 'between',
                                                      'minimum': 5,
                                                      'maximum': 6.9,
                                                      'format': formato_nota_media})
    worksheet.conditional_format(1, 6, len(data), 6, {'type': 'cell',
                                                      'criteria': '<',
                                                      'value': 5,
                                                      'format': formato_nota_baixa})
    
    writer.save()
    output.seek(0)
    
    # Retornar o arquivo Excel
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="notas.xlsx"'
    return response