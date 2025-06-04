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
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    # Obter parâmetros de filtro
    tipo = request.GET.get('tipo', 'todas')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Filtrar atividades acadêmicas
    atividades_academicas = AtividadeAcademica.objects.all()
    
    if status:
        atividades_academicas = atividades_academicas.filter(status=status)
    
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(data_inicio__gte=data_inicio)
    
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)
    
    # Filtrar atividades ritualísticas
    atividades_ritualisticas = AtividadeRitualistica.objects.all()
    
    if data_inicio:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=data_inicio)
    
    if data_fim:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)
    
    # Aplicar filtro por tipo
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Calcular totais
    total_academicas = atividades_academicas.count()
    total_ritualisticas = atividades_ritualisticas.count()
    total_atividades = total_academicas + total_ritualisticas
    
    return render(
        request,
        "atividades/relatorio_atividades.html",
        {
            "atividades_academicas": atividades_academicas,
            "atividades_ritualisticas": atividades_ritualisticas,
            "total_academicas": total_academicas,
            "total_ritualisticas": total_ritualisticas,
            "total_atividades": total_atividades,
            "tipo": tipo,
            "status": status,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        },
    )

@login_required
def exportar_atividades(request, formato):
    """Exporta as atividades filtradas para o formato especificado."""
    # Obter os mesmos filtros que no relatório
    tipo = request.GET.get('tipo', 'todas')
    status = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    
    # Obter atividades filtradas (mesmo código do relatório)
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    
    atividades_academicas = AtividadeAcademica.objects.all()
    if status:
        atividades_academicas = atividades_academicas.filter(status=status)
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)
    
    atividades_ritualisticas = AtividadeRitualistica.objects.all()
    if data_inicio:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__gte=data_inicio)
    if data_fim:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)
    
    if tipo == 'academicas':
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == 'ritualisticas':
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Exportar para o formato solicitado
    if formato == 'csv':
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)
    elif formato == 'excel':
        return exportar_atividades_excel(atividades_academicas, atividades_ritualisticas)
    elif formato == 'pdf':
        return exportar_atividades_pdf(atividades_academicas, atividades_ritualisticas)
    else:
        messages.error(request, f"Formato de exportação '{formato}' não suportado.")
        return redirect('atividades:relatorio_atividades')

def exportar_atividades_csv(atividades_academicas, atividades_ritualisticas):
    """Exporta as atividades para CSV."""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="atividades.csv"'
    
    writer = csv.writer(response)
    
    # Cabeçalho para atividades acadêmicas
    writer.writerow(['Tipo', 'Nome', 'Descrição', 'Data de Início', 'Data de Término', 
                     'Responsável', 'Local', 'Status', 'Tipo de Atividade'])
    
    # Dados das atividades acadêmicas
    for atividade in atividades_academicas:
        writer.writerow([
            'Acadêmica',
            atividade.nome,
            atividade.descricao or '',
            atividade.data_inicio.strftime('%d/%m/%Y'),
            atividade.data_fim.strftime('%d/%m/%Y') if atividade.data_fim else '',
            atividade.responsavel or '',
            atividade.local or '',
            atividade.get_status_display(),
            atividade.get_tipo_atividade_display(),
        ])
    
    # Dados das atividades ritualísticas
    for atividade in atividades_ritualisticas:
        writer.writerow([
            'Ritualística',
            atividade.nome,
            atividade.descricao or '',
            atividade.data.strftime('%d/%m/%Y'),
            '',  # Não tem data_fim
            '',  # Não tem responsável
            atividade.local,
            '',  # Não tem status
            '',  # Não tem tipo_atividade
        ])
    
    return response

def exportar_atividades_excel(atividades_academicas, atividades_ritualisticas):
    """Exporta as atividades para Excel."""
    # Implementação básica usando pandas
    try:
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        # Criar DataFrames para cada tipo de atividade
        dados_academicas = []
        for atividade in atividades_academicas:
            dados_academicas.append({
                'Tipo': 'Acadêmica',
                'Nome': atividade.nome,
                'Descrição': atividade.descricao or '',
                'Data de Início': atividade.data_inicio,
                'Data de Término': atividade.data_fim,
                'Responsável': atividade.responsavel or '',
                'Local': atividade.local or '',
                'Status': atividade.get_status_display(),
                'Tipo de Atividade': atividade.get_tipo_atividade_display(),
            })
        
        dados_ritualisticas = []
        for atividade in atividades_ritualisticas:
            dados_ritualisticas.append({
                'Tipo': 'Ritualística',
                'Nome': atividade.nome,
                'Descrição': atividade.descricao or '',
                'Data': atividade.data,
                'Horário': f"{atividade.hora_inicio} - {atividade.hora_fim}",
                'Local': atividade.local,
                'Turma': atividade.turma.nome,
                'Participantes': atividade.participantes.count(),
            })
        
        # Criar arquivo Excel com múltiplas abas
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            if dados_academicas:
                df_academicas = pd.DataFrame(dados_academicas)
                df_academicas.to_excel(writer, sheet_name='Atividades Acadêmicas', index=False)
            
            if dados_ritualisticas:
                df_ritualisticas = pd.DataFrame(dados_ritualisticas)
                df_ritualisticas.to_excel(writer, sheet_name='Atividades Ritualísticas', index=False)
        
        # Configurar resposta HTTP
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="atividades.xlsx"'
        
        return response
    except ImportError:
        # Fallback para CSV se pandas não estiver disponível
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)

def exportar_atividades_pdf(atividades_academicas, atividades_ritualisticas):
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
        subtitle_style = styles['Heading2']
        
        # Título
        elements.append(Paragraph("Relatório de Atividades", title_style))
        elements.append(Spacer(1, 12))
        
        # Atividades Acadêmicas
        if atividades_academicas:
            elements.append(Paragraph("Atividades Acadêmicas", subtitle_style))
            elements.append(Spacer(1, 6))
            
            # Dados para a tabela
            data = [['Nome', 'Tipo', 'Data de Início', 'Status', 'Responsável']]
            
            for atividade in atividades_academicas:
                data.append([
                    atividade.nome,
                    atividade.get_tipo_atividade_display(),
                    atividade.data_inicio.strftime('%d/%m/%Y'),
                    atividade.get_status_display(),
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
            elements.append(Spacer(1, 12))
        
        # Atividades Ritualísticas
        if atividades_ritualisticas:
            elements.append(Paragraph("Atividades Ritualísticas", subtitle_style))
            elements.append(Spacer(1, 6))
            
            # Dados para a tabela
            data = [['Nome', 'Data', 'Horário', 'Local', 'Turma', 'Participantes']]
            
            for atividade in atividades_ritualisticas:
                data.append([
                    atividade.nome,
                    atividade.data.strftime('%d/%m/%Y'),
                    f"{atividade.hora_inicio} - {atividade.hora_fim}",
                    atividade.local,
                    atividade.turma.nome,
                    str(atividade.participantes.count()),
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
        return exportar_atividades_csv(atividades_academicas, atividades_ritualisticas)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from importlib import import_module

from ..models import AtividadeAcademica

@login_required
def relatorio_atividades_curso_turma(request):
    """
    Relatório de atividades acadêmicas filtrado por curso e turma.
    Suporta AJAX para atualização parcial da tabela.
    """
    Curso = import_module("cursos.models").Curso
    Turma = import_module("turmas.models").Turma

    cursos = Curso.objects.all()
    turmas = Turma.objects.all()

    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")

    atividades = AtividadeAcademica.objects.all()

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
from ..models import AtividadeRitualistica
from ..views.utils import get_model_class

@login_required
def relatorio_atividades_ritualisticas(request):
    Turma = get_model_class("Turma", "turmas")
    turmas = Turma.objects.filter(status='A')
    turma_id = request.GET.get("turma")
    data = request.GET.get("data")

    atividades = AtividadeRitualistica.objects.all()
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    if data:
        atividades = atividades.filter(data=data)

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
