<UPDATED_CODE>"""
Views para o aplicativo de atividades.
Este arquivo agora funciona como um agregador que importa todas as funções
dos módulos separados para manter a compatibilidade com o código existente.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from importlib import import_module
from django.core.exceptions import ValidationError
from django.utils import timezone
import csv
from io import TextIOWrapper
import datetime

# Importar a função utilitária centralizada
from core.utils import get_model_dynamically

logger = logging.getLogger(__name__)

def get_models():
    """Obtém os modelos AtividadeAcademica e AtividadeRitualistica."""
    atividades_module = import_module("atividades.models")
    AtividadeAcademica = getattr(atividades_module, "AtividadeAcademica")
    AtividadeRitualistica = getattr(atividades_module, "AtividadeRitualistica")
    return AtividadeAcademica, AtividadeRitualistica

def get_forms():
    """Obtém os formulários AtividadeAcademicaForm e AtividadeRitualisticaForm."""
    atividades_forms = import_module("atividades.forms")
    AtividadeAcademicaForm = getattr(atividades_forms, "AtividadeAcademicaForm")
    AtividadeRitualisticaForm = getattr(atividades_forms, "AtividadeRitualisticaForm")
    return AtividadeAcademicaForm, AtividadeRitualisticaForm

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

@login_required
def listar_atividades(request):
    """Lista todas as atividades."""
    return render(request, "atividades/listar_atividades.html")

@login_required
def listar_atividades_academicas(request):
    """Lista todas as atividades acadêmicas."""
    AtividadeAcademica, _ = get_models()
    
    # Obter parâmetros de busca
    query = request.GET.get("q", "")
    
    # Filtrar atividades
    atividades = AtividadeAcademica.objects.all().order_by('-data_inicio')
    if query:
        atividades = atividades.filter(
            Q(nome__icontains=query) |
            Q(descricao__icontains=query) |
            Q(responsavel__icontains=query) |
            Q(local__icontains=query)
        )
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 atividades por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "atividades": page_obj,
        "page_obj": page_obj,
        "query": query,
    }
    
    return render(request, "atividades/listar_atividades_academicas.html", context)

@login_required
def criar_atividade_academica(request):
    """Cria uma nova atividade acadêmica."""
    AtividadeAcademicaForm, _ = get_forms()
    
    # Obter URL de retorno
    return_url = request.GET.get('return_url', 'atividades:listar_atividades_academicas')
    
    if request.method == "POST":
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            try:
                atividade = form.save(commit=False)
                
                # Verificar se deve aplicar a todas as turmas
                todas_turmas = form.cleaned_data.get('todas_turmas', False)
                
                # Salvar a atividade
                atividade.save()
                
                # Se marcou para aplicar a todas as turmas, adicionar todas as turmas ativas
                if todas_turmas:
                    Turma = get_turma_model()
                    turmas_ativas = Turma.objects.filter(status='A')
                    atividade.turmas.add(*turmas_ativas)
                else:
                    # Adicionar as turmas selecionadas
                    turmas = form.cleaned_data.get('turmas', [])
                    if turmas:
                        atividade.turmas.add(*turmas)
                
                messages.success(request, "Atividade acadêmica criada com sucesso!")
                return redirect(return_url)
            except Exception as e:
                messages.error(request, f"Erro ao criar atividade: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AtividadeAcademicaForm()
    
    return render(
        request, 
        "atividades/formulario_atividade_academica.html", 
        {
            "form": form, 
            "return_url": return_url
        }
    )

@login_required
def editar_atividade_academica(request, pk):
    """Edita uma atividade acadêmica existente."""
    AtividadeAcademica, _ = get_models()
    AtividadeAcademicaForm, _ = get_forms()
    
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    # Obter URL de retorno
    return_url = request.GET.get('return_url', 'atividades:listar_atividades_academicas')
    
    if request.method == "POST":
        form = AtividadeAcademicaForm(request.POST, instance=atividade)
        if form.is_valid():
            try:
                atividade = form.save(commit=False)
                
                # Verificar se deve aplicar a todas as turmas
                todas_turmas = form.cleaned_data.get('todas_turmas', False)
                
                # Salvar a atividade
                atividade.save()
                
                # Limpar turmas existentes
                atividade.turmas.clear()
                
                # Se marcou para aplicar a todas as turmas, adicionar todas as turmas ativas
                if todas_turmas:
                    Turma = get_turma_model()
                    turmas_ativas = Turma.objects.filter(status='A')
                    atividade.turmas.add(*turmas_ativas)
                else:
                    # Adicionar as turmas selecionadas
                    turmas = form.cleaned_data.get('turmas', [])
                    if turmas:
                        atividade.turmas.add(*turmas)
                
                messages.success(request, "Atividade acadêmica atualizada com sucesso!")
                return redirect(return_url)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar atividade: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AtividadeAcademicaForm(instance=atividade)
    
    return render(
        request, 
        "atividades/formulario_atividade_academica.html", 
        {
            "form": form, 
            "atividade": atividade,
            "return_url": return_url
        }
    )

@login_required
def excluir_atividade_academica(request, pk):
    """Exclui uma atividade acadêmica."""
    AtividadeAcademica, _ = get_models()
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade acadêmica excluída com sucesso!")
            return redirect("atividades:listar_atividades_academicas")
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade: {str(e)}")
            return redirect("atividades:detalhar_atividade_academica", pk=pk)
    
    return render(request, "atividades/excluir_atividade_academica.html", {"atividade": atividade})

@login_required
def detalhar_atividade_academica(request, pk):
    """Exibe os detalhes de uma atividade acadêmica."""
    AtividadeAcademica, _ = get_models()
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return render(request, "atividades/detalhar_atividade_academica.html", {"atividade": atividade})

@login_required
def confirmar_exclusao_academica(request, pk):
    """Confirma a exclusão de uma atividade acadêmica."""
    AtividadeAcademica, _ = get_models()
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    # Obter URL de retorno
    return_url = request.GET.get('return_url', 'atividades:listar_atividades_academicas')
    
    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade acadêmica excluída com sucesso!")
            return redirect(return_url)
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade: {str(e)}")
            return redirect("atividades:detalhar_atividade_academica", pk=pk)
    
    return render(
        request, 
        "atividades/confirmar_exclusao_academica.html", 
        {
            "atividade": atividade,
            "return_url": return_url
        }
    )

@login_required
def copiar_atividade_academica(request, id):
    """Cria uma cópia de uma atividade acadêmica existente."""
    AtividadeAcademica, _ = get_models()
    AtividadeAcademicaForm, _ = get_forms()
    
    atividade_original = get_object_or_404(AtividadeAcademica, id=id)
    
    if request.method == "POST":
        try:
            # Criar uma nova atividade com os mesmos dados
            nova_atividade = AtividadeAcademica.objects.create(
                nome=f"Cópia de {atividade_original.nome}",
                descricao=atividade_original.descricao,
                data_inicio=atividade_original.data_inicio,
                data_fim=atividade_original.data_fim,
                responsavel=atividade_original.responsavel,
                local=atividade_original.local,
                tipo_atividade=atividade_original.tipo_atividade,
                status="agendada"  # Sempre começa como agendada
            )
            
            # Copiar as turmas
            for turma in atividade_original.turmas.all():
                nova_atividade.turmas.add(turma)
            
            messages.success(request, "Atividade acadêmica copiada com sucesso!")
            return redirect("atividades:detalhar_atividade_academica", pk=nova_atividade.id)
        except Exception as e:
            messages.error(request, f"Erro ao copiar atividade: {str(e)}")
            return redirect("atividades:detalhar_atividade_academica", pk=id)
    
    return render(
        request, 
        "atividades/confirmar_copia_academica.html", 
        {"atividade": atividade_original}
    )

@login_required
def listar_atividades_ritualisticas(request):
    """Lista todas as atividades ritualísticas."""
    _, AtividadeRitualistica = get_models()
    
    # Obter parâmetros de busca
    query = request.GET.get("q", "")
    
    # Filtrar atividades
    atividades = AtividadeRitualistica.objects.all().order_by('-data')
    if query:
        atividades = atividades.filter(
            Q(nome__icontains=query) |
            Q(descricao__icontains=query) |
            Q(local__icontains=query)
        )
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 atividades por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "atividades": page_obj,
        "page_obj": page_obj,
        "query": query,
    }
    
    return render(request, "atividades/listar_atividades_ritualisticas.html", context)

@login_required
def criar_atividade_ritualistica(request):
    """Cria uma nova atividade ritualística."""
    _, AtividadeRitualisticaForm = get_forms()
    
    # Obter URL de retorno
    return_url = request.GET.get('return_url', 'atividades:listar_atividades_ritualisticas')
    
    if request.method == "POST":
        form = AtividadeRitualisticaForm(request.POST)
        if form.is_valid():
            try:
                atividade = form.save(commit=False)
                
                # Verificar se deve incluir todos os alunos da turma
                todos_alunos = form.cleaned_data.get('todos_alunos', False)
                
                # Salvar a atividade
                atividade.save()
                
                # Se marcou para incluir todos os alunos, adicionar todos os alunos da turma
                if todos_alunos:
                    # Importar o modelo Matricula dinamicamente
                    Matricula = get_model_dynamically("matriculas", "Matricula")
                    
                    # Buscar alunos matriculados na turma
                    matriculas = Matricula.objects.filter(turma=atividade.turma, status='A')
                    alunos = [matricula.aluno for matricula in matriculas]
                    
                    # Adicionar alunos como participantes
                    atividade.participantes.add(*alunos)
                else:
                    # Adicionar os participantes selecionados
                    participantes = form.cleaned_data.get('participantes', [])
                    if participantes:
                        atividade.participantes.add(*participantes)
                
                messages.success(request, "Atividade ritualística criada com sucesso!")
                return redirect(return_url)
            except Exception as e:
                messages.error(request, f"Erro ao criar atividade: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AtividadeRitualisticaForm()
    
    return render(
        request, 
        "atividades/formulario_atividade_ritualistica.html", 
        {
            "form": form, 
            "return_url": return_url
        }
    )

@login_required
def editar_atividade_ritualistica(request, pk):
    """Edita uma atividade ritualística existente."""
    _, AtividadeRitualistica = get_models()
    _, AtividadeRitualisticaForm = get_forms()
    
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    # Obter URL de retorno
    return_url = request.GET.get('return_url', 'atividades:listar_atividades_ritualisticas')
    
    if request.method == "POST":
        form = AtividadeRitualisticaForm(request.POST, instance=atividade)
        if form.is_valid():
            try:
                atividade = form.save(commit=False)
                
                # Verificar se deve incluir todos os alunos da turma
                todos_alunos = form.cleaned_data.get('todos_alunos', False)
                
                # Salvar a atividade
                atividade.save()
                
                # Limpar participantes existentes
                atividade.participantes.clear()
                
                # Se marcou para incluir todos os alunos, adicionar todos os alunos da turma
                if todos_alunos:
                    # Importar o modelo Matricula dinamicamente
                    Matricula = get_model_dynamically("matriculas", "Matricula")
                    
                    # Buscar alunos matriculados na turma
                    matriculas = Matricula.objects.filter(turma=atividade.turma, status='A')
                    alunos = [matricula.aluno for matricula in matriculas]
                    
                    # Adicionar alunos como participantes
                    atividade.participantes.add(*alunos)
                else:
                    # Adicionar os participantes selecionados
                    participantes = form.cleaned_data.get('participantes', [])
                    if participantes:
                        atividade.participantes.add(*participantes)
                
                messages.success(request, "Atividade ritualística atualizada com sucesso!")
                return redirect(return_url)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar atividade: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AtividadeRitualisticaForm(instance=atividade)
    
    return render(
        request, 
        "atividades/formulario_atividade_ritualistica.html", 
        {
            "form": form, 
            "atividade": atividade,
            "return_url": return_url
        }
    )

@login_required
def excluir_atividade_ritualistica(request, pk):
    """Exclui uma atividade ritualística."""
    _, AtividadeRitualistica = get_models()
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade ritualística excluída com sucesso!")
            return redirect("atividades:listar_atividades_ritualisticas")
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade: {str(e)}")
            return redirect("atividades:detalhar_atividade_ritualistica", pk=pk)
    
    return render(request, "atividades/excluir_atividade_ritualistica.html", {"atividade": atividade})

@login_required
def detalhar_atividade_ritualistica(request, pk):
    """Exibe os detalhes de uma atividade ritualística."""
    _, AtividadeRitualistica = get_models()
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    # Calcular total de participantes
    total_participantes = atividade.participantes.count()
    
    return render(
        request, 
        "atividades/detalhar_atividade_ritualistica.html", 
        {
            "atividade": atividade,
            "total_participantes": total_participantes,
            "return_url": request.META.get('HTTP_REFERER', 'atividades:listar_atividades_ritualisticas')
        }
    )

@login_required
def confirmar_exclusao_ritualistica(request, pk):
    """Confirma a exclusão de uma atividade ritualística."""
    _, AtividadeRitualistica = get_models()
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    # Obter URL de retorno
    return_url = request.GET.get('return_url', 'atividades:listar_atividades_ritualisticas')
    
    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade ritualística excluída com sucesso!")
            return redirect(return_url)
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade: {str(e)}")
            return redirect("atividades:detalhar_atividade_ritualistica", pk=pk)
    
    return render(
        request, 
        "atividades/confirmar_exclusao_ritualistica.html", 
        {
            "atividade": atividade,
            "return_url": return_url
        }
    )

@login_required
def copiar_atividade_ritualistica(request, id):
    """Cria uma cópia de uma atividade ritualística existente."""
    _, AtividadeRitualistica = get_models()
    _, AtividadeRitualisticaForm = get_forms()
    
    atividade_original = get_object_or_404(AtividadeRitualistica, id=id)
    
    if request.method == "POST":
        try:
            # Criar uma nova atividade com os mesmos dados
            nova_atividade = AtividadeRitualistica.objects.create(
                nome=f"Cópia de {atividade_original.nome}",
                descricao=atividade_original.descricao,
                data=atividade_original.data,
                hora_inicio=atividade_original.hora_inicio,
                hora_fim=atividade_original.hora_fim,
                local=atividade_original.local,
                turma=atividade_original.turma
            )
            
            # Copiar os participantes
            for participante in atividade_original.participantes.all():
                nova_atividade.participantes.add(participante)
            
            messages.success(request, "Atividade ritualística copiada com sucesso!")
            return redirect("atividades:detalhar_atividade_ritualistica", pk=nova_atividade.id)
        except Exception as e:
            messages.error(request, f"Erro ao copiar atividade: {str(e)}")
            return redirect("atividades:detalhar_atividade_ritualistica", pk=id)
    
    return render(
        request, 
        "atividades/confirmar_copia_ritualistica.html", 
        {"atividade": atividade_original}
    )

@login_required
def relatorio_atividades(request):
    """Exibe um relatório com estatísticas sobre as atividades."""
    AtividadeAcademica, AtividadeRitualistica = get_models()
    
    # Obter parâmetros de filtro
    tipo = request.GET.get("tipo", "todas")
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")
    
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
    if tipo == "academicas":
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == "ritualisticas":
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Calcular totais
    total_academicas = atividades_academicas.count()
    total_ritualisticas = atividades_ritualisticas.count()
    total_atividades = total_academicas + total_ritualisticas
    
    context = {
        "atividades_academicas": atividades_academicas,
        "atividades_ritualisticas": atividades_ritualisticas,
        "total_academicas": total_academicas,
        "total_ritualisticas": total_ritualisticas,
        "total_atividades": total_atividades,
        "tipo": tipo,
        "status": status,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "filtros": {
            "tipo": tipo,
            "status": status,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        }
    }
    
    return render(request, "atividades/relatorio_atividades.html", context)

@login_required
def exportar_atividades(request, formato):
    """Exporta as atividades para um arquivo no formato especificado."""
    AtividadeAcademica, AtividadeRitualistica = get_models()
    
    # Obter parâmetros de filtro
    tipo = request.GET.get("tipo", "todas")
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")
    
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
    if tipo == "academicas":
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == "ritualisticas":
        atividades_academicas = AtividadeAcademica.objects.none()
    
    # Exportar para CSV
    if formato == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="atividades.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            "Tipo", "Nome", "Descrição", "Data", "Local", "Status", "Turma(s)"
        ])
        
        # Adicionar atividades acadêmicas
        for atividade in atividades_academicas:
            turmas = ", ".join([t.nome for t in atividade.turmas.all()])
            writer.writerow([
                "Acadêmica",
                atividade.nome,
                atividade.descricao,
                atividade.data_inicio.strftime("%d/%m/%Y"),
                atividade.local,
                atividade.get_status_display(),
                turmas
            ])
        
        # Adicionar atividades ritualísticas
        for atividade in atividades_ritualisticas:
            writer.writerow([
                "Ritualística",
                atividade.nome,
                atividade.descricao,
                atividade.data.strftime("%d/%m/%Y"),
                atividade.local,
                "N/A",  # Atividades ritualísticas não têm status
                atividade.turma.nome
            ])
        
        return response
    
    # Exportar para Excel
    elif formato == "excel":
        try:
            import xlwt
            
            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = 'attachment; filename="atividades.xls"'
            
            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Atividades")
            
            # Estilos
            header_style = xlwt.easyxf("font: bold on; align: wrap on, vert centre, horiz center")
            date_style = xlwt.easyxf("align: wrap on, vert centre, horiz left", num_format_str="DD/MM/YYYY")
            
            # Cabeçalho
            row_num = 0
            columns = [
                "Tipo", "Nome", "Descrição", "Data", "Local", "Status", "Turma(s)"
            ]
            
            for col_num, column_title in enumerate(columns):
                ws.write(row_num, col_num, column_title, header_style)
            
            # Adicionar atividades acadêmicas
            for atividade in atividades_academicas:
                row_num += 1
                turmas = ", ".join([t.nome for t in atividade.turmas.all()])
                
                ws.write(row_num, 0, "Acadêmica")
                ws.write(row_num, 1, atividade.nome)
                ws.write(row_num, 2, atividade.descricao)
                ws.write(row_num, 3, atividade.data_inicio, date_style)
                ws.write(row_num, 4, atividade.local)
                ws.write(row_num, 5, atividade.get_status_display())
                ws.write(row_num, 6, turmas)
            
            # Adicionar atividades ritualísticas
            for atividade in atividades_ritualisticas:
                row_num += 1
                
                ws.write(row_num, 0, "Ritualística")
                ws.write(row_num, 1, atividade.nome)
                ws.write(row_num, 2, atividade.descricao)
                ws.write(row_num, 3, atividade.data, date_style)
                ws.write(row_num, 4, atividade.local)
                ws.write(row_num, 5, "N/A")  # Atividades ritualísticas não têm status
                ws.write(row_num, 6, atividade.turma.nome)
            
            wb.save(response)
            return response
        except ImportError:
            messages.error(request, "A biblioteca xlwt não está instalada. Instale-a para exportar para Excel.")
            return redirect("atividades:relatorio_atividades")
    
    # Exportar para PDF
    elif formato == "pdf":
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
            from reportlab.lib.styles import getSampleStyleSheet
            from io import BytesIO
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            title_style = styles["Heading1"]
            
            # Título
            elements.append(Paragraph("Relatório de Atividades", title_style))
            
            # Dados da tabela
            data = [["Tipo", "Nome", "Descrição", "Data", "Local", "Status", "Turma(s)"]]
            
            # Adicionar atividades acadêmicas
            for atividade in atividades_academicas:
                turmas = ", ".join([t.nome for t in atividade.turmas.all()])
                data.append([
                    "Acadêmica",
                    atividade.nome,
                    atividade.descricao,
                    atividade.data_inicio.strftime("%d/%m/%Y"),
                    atividade.local,
                    atividade.get_status_display(),
                    turmas
                ])
            
            # Adicionar atividades ritualísticas
            for atividade in atividades_ritualisticas:
                data.append([
                    "Ritualística",
                    atividade.nome,
                    atividade.descricao,
                    atividade.data.strftime("%d/%m/%Y"),
                    atividade.local,
                    "N/A",  # Atividades ritualísticas não têm status
                    atividade.turma.nome
                ])
            
            # Criar tabela
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(table)
            
            # Gerar PDF
            doc.build(elements)
            
            # Retornar resposta
            buffer.seek(0)
            response = HttpResponse(buffer, content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="atividades.pdf"'
            
            return response
        except ImportError:
            messages.error(request, "As bibliotecas necessárias para gerar PDF não estão instaladas.")
            return redirect("atividades:relatorio_atividades")
    
    # Formato não suportado
    else:
        messages.error(request, f"Formato de exportação '{formato}' não suportado.")
        return redirect("atividades:relatorio_atividades")

@login_required
def calendario_atividades(request):
    """Exibe um calendário com todas as atividades."""
    # Obter todas as turmas para o filtro
    Turma = get_turma_model()
    turmas = Turma.objects.filter(status='A')
    
    return render(request, "atividades/calendario_atividades.html", {"turmas": turmas})

@login_required
def dashboard_atividades(request):
    """Exibe um dashboard com estatísticas sobre as atividades."""
    AtividadeAcademica, AtividadeRitualistica = get_models()
    
    # Estatísticas gerais
    total_academicas = AtividadeAcademica.objects.count()
    total_ritualisticas = AtividadeRitualistica.objects.count()
    
    # Estatísticas por status
    academicas_por_status = {
        'agendada': AtividadeAcademica.objects.filter(status='agendada').count(),
        'em_andamento': AtividadeAcademica.objects.filter(status='em_andamento').count(),
        'concluida': AtividadeAcademica.objects.filter(status='concluida').count(),
        'cancelada': AtividadeAcademica.objects.filter(status='cancelada').count(),
    }
    
    # Estatísticas por tipo
    academicas_por_tipo = {
        'aula': AtividadeAcademica.objects.filter(tipo_atividade='aula').count(),
        'palestra': AtividadeAcademica.objects.filter(tipo_atividade='palestra').count(),
        'workshop': AtividadeAcademica.objects.filter(tipo_atividade='workshop').count(),
        'seminario': AtividadeAcademica.objects.filter(tipo_atividade='seminario').count(),
        'outro': AtividadeAcademica.objects.filter(tipo_atividade='outro').count(),
    }
    
    # Atividades recentes
    atividades_academicas_recentes = AtividadeAcademica.objects.all().order_by('-data_inicio')[:5]
    atividades_ritualisticas_recentes = AtividadeRitualistica.objects.all().order_by('-data')[:5]
    
    #