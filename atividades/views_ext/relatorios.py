import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime, timedelta
from django.views.decorators.http import require_GET

from .utils import get_model_class

# Set up logger
logger = logging.getLogger(__name__)

@login_required
def relatorio_atividades(request):
    """Gera um relatório de atividades com base nos filtros aplicados."""
    Atividade = get_model_class("Atividade")
    
    # Obter parâmetros de filtro
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Filtrar atividades
    atividades = Atividade.objects.all()
    
    if status:
        atividades = atividades.filter(status=status)
    
    if data_inicio:
        atividades = atividades.filter(data_inicio__gte=data_inicio)
    
    if data_fim:
        atividades = atividades.filter(data_inicio__lte=data_fim)
    
    # Calcular totais
    total_atividades = atividades.count()
    
    return render(
        request,
        "atividades/relatorio_atividades.html",
        {
            "atividades": atividades,
            "total_atividades": total_atividades,
            "status": status,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        },
    )

@login_required
def exportar_atividades(request, formato):
    """Exporta as atividades filtradas para o formato especificado."""
    # Obter os mesmos filtros que no relatório
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Obter atividades filtradas
    Atividade = get_model_class("Atividade")
    
    atividades = Atividade.objects.all()
    if status:
        atividades = atividades.filter(status=status)
    if data_inicio:
        atividades = atividades.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades = atividades.filter(data_inicio__lte=data_fim)
    
    # Exportar para o formato solicitado
    if formato == 'csv':
        return exportar_atividades_csv(atividades)
    elif formato == 'excel':
        return exportar_atividades_excel(atividades)
    elif formato == 'pdf':
        return exportar_atividades_pdf(atividades)
    else:
        messages.error(request, f"Formato de exportação '{formato}' não suportado.")
        return redirect('atividades:relatorio_atividades')

def exportar_atividades_csv(atividades):
    """Exporta as atividades para CSV."""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="atividades.csv"'
    
    writer = csv.writer(response)
    
    # Cabeçalho
    writer.writerow(['Nome', 'Descrição', 'Data de Início', 'Data de Término', 
                     'Responsável', 'Local', 'Status', 'Tipo de Atividade'])
    
    # Dados das atividades
    for atividade in atividades:
        writer.writerow([
            atividade.nome,
            atividade.descricao or '',
            atividade.data_inicio.strftime('%d/%m/%Y') if atividade.data_inicio else '',
            atividade.data_fim.strftime('%d/%m/%Y') if atividade.data_fim else '',
            atividade.responsavel or '',
            atividade.local or '',
            atividade.get_status_display() if hasattr(atividade, 'get_status_display') else atividade.status,
            atividade.get_tipo_atividade_display() if hasattr(atividade, 'get_tipo_atividade_display') else getattr(atividade, 'tipo_atividade', ''),
        ])
    
    return response

def exportar_atividades_excel(atividades):
    """Exporta as atividades para Excel."""
    # Implementação básica usando pandas
    try:
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        # Criar DataFrame para as atividades
        dados_atividades = []
        for atividade in atividades:
            dados_atividades.append({
                'Nome': atividade.nome,
                'Descrição': atividade.descricao or '',
                'Data de Início': atividade.data_inicio,
                'Data de Término': atividade.data_fim,
                'Responsável': atividade.responsavel or '',
                'Local': atividade.local or '',
                'Status': atividade.get_status_display() if hasattr(atividade, 'get_status_display') else atividade.status,
                'Tipo de Atividade': atividade.get_tipo_atividade_display() if hasattr(atividade, 'get_tipo_atividade_display') else getattr(atividade, 'tipo_atividade', ''),
            })
        
        # Criar arquivo Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            if dados_atividades:
                df_atividades = pd.DataFrame(dados_atividades)
                df_atividades.to_excel(writer, sheet_name='Atividades', index=False)
        
        # Configurar resposta HTTP
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="atividades.xlsx"'
        
        return response
    except ImportError:
        # Fallback para CSV se pandas não estiver disponível
        return exportar_atividades_csv(atividades)

def exportar_atividades_pdf(atividades):
    """Exporta as atividades para PDF."""
    # Implementação básica usando reportlab
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from django.http import HttpResponse
        import io
        
        # Configurar buffer e documento
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        
        # Título
        elements.append(Paragraph("Relatório de Atividades", title_style))
        elements.append(Spacer(1, 12))
        
        # Atividades
        if atividades:
            # Dados para a tabela
            data = [['Nome', 'Data de Início', 'Data de Término', 'Status', 'Responsável']]
            
            for atividade in atividades:
                data.append([
                    atividade.nome,
                    atividade.data_inicio.strftime('%d/%m/%Y') if atividade.data_inicio else '',
                    atividade.data_fim.strftime('%d/%m/%Y') if atividade.data_fim else '',
                    atividade.get_status_display() if hasattr(atividade, 'get_status_display') else atividade.status,
                    atividade.responsavel or 'Não informado',
                ])
            
            # Criar tabela
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(table)
        
        # Gerar PDF
        doc.build(elements)
        
        # Configurar resposta HTTP
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="atividades.pdf"'
        
        return response
    except ImportError:
        # Fallback para CSV se reportlab não estiver disponível
        return exportar_atividades_csv(atividades)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from importlib import import_module

@login_required
def relatorio_atividades_curso_turma(request):
    """
    Relatório de atividades filtrado por curso e turma.
    Suporta AJAX para atualização parcial da tabela.
    """
    Curso = import_module("cursos.models").Curso
    Turma = import_module("turmas.models").Turma
    Atividade = get_model_class("Atividade")

    cursos = Curso.objects.all()
    turmas = Turma.objects.all()

    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")

    atividades = Atividade.objects.all()

    if curso_id:
        atividades = atividades.filter(turma__curso_id=curso_id)
        turmas = turmas.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)

    atividades = atividades.select_related("curso").prefetch_related("turmas").distinct()

    context = {
        "atividades": atividades,
        "cursos": cursos,
        "turmas": turmas,
        "curso_selecionado": curso_id,
        "turma_selecionada": turma_id,
    }

    # AJAX: retorna apenas o corpo da tabela para atualização dinâmica
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "atividades/_tabela_atividades.html", context)

    return render(request, "atividades/relatorio_atividades_curso_turma.html", context)

@require_GET
@login_required
def ajax_turmas_por_curso_relatorio(request):
    """
    Endpoint AJAX: retorna as turmas de um curso em JSON (para relatório).
    """
    curso_id = request.GET.get("curso_id")
    Turma = import_module("turmas.models").Turma
    turmas = Turma.objects.filter(curso_id=curso_id).values("id", "nome")
    return JsonResponse(list(turmas), safe=False)

@require_GET
@login_required
def ajax_atividades_filtradas_relatorio(request):
    """
    Endpoint AJAX: retorna atividades filtradas por curso/turma para relatório.
    Retorna HTML parcial da tabela.
    """
    return relatorio_atividades_curso_turma(request)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..views_ext.utils import get_model_class

@login_required
def relatorio_atividades_ritualisticas(request):
    """Relatório de atividades (antigas ritualísticas) - mantido para compatibilidade."""
    Turma = get_model_class("Turma", "turmas")
    Atividade = get_model_class("Atividade")
    
    turmas = Turma.objects.filter(status='A')
    turma_id = request.GET.get("turma")
    data = request.GET.get("data")

    atividades = Atividade.objects.all()
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    if data:
        atividades = atividades.filter(data_inicio=data)

    return render(
        request,
        "atividades/ritualisticas/relatorio_ritualisticas.html",
        {
            "atividades": atividades,
            "turmas": turmas,
            "turma_selecionada": turma_id,
            "data_selecionada": data,
        }
    )
