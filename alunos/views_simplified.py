"""
Views simplificadas para gerenciamento de alunos - Sistema Dados Iniciáticos v2.0
"""

import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json

from .forms import AlunoForm, RegistroHistoricoFormSet, RegistroHistoricoForm
from .models import Aluno, RegistroHistorico

logger = logging.getLogger(__name__)


@login_required
def listar_alunos_simple(request):
    """Lista todos os alunos com paginação e filtros."""
    alunos = Aluno.objects.filter(ativo=True).order_by("nome")
    
    # Filtros
    if request.GET.get("q"):
        query = request.GET.get("q")
        alunos = alunos.filter(
            Q(nome__icontains=query) |
            Q(cpf__icontains=query) |
            Q(nome_iniciatico__icontains=query) |
            Q(numero_iniciatico__icontains=query)
        )
    
    # Paginação
    paginator = Paginator(alunos, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "query": request.GET.get("q", ""),
        "total_alunos": alunos.count(),
    }
    
    return render(request, "alunos/listar_alunos_simple.html", context)


@login_required
def criar_aluno_simple(request):
    """Cria um novo aluno com interface simplificada."""
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    aluno = form.save()
                    messages.success(
                        request,
                        f"Aluno '{aluno.nome}' criado com sucesso!"
                    )
                    return redirect("alunos:detalhar_aluno_simple", aluno_id=aluno.cpf)
            except Exception as e:
                messages.error(request, f"Erro ao criar aluno: {str(e)}")
        else:
            messages.error(request, "Erro no formulário. Verifique os dados.")
    else:
        form = AlunoForm()
    
    context = {
        "form": form,
        "titulo": "Criar Aluno",
        "action": "criar",
    }
    
    return render(request, "alunos/formulario_aluno_simple.html", context)


@login_required
def editar_aluno_simple(request, aluno_id):
    """Edita um aluno com interface simplificada."""
    aluno = get_object_or_404(Aluno, cpf=aluno_id, ativo=True)
    
    if request.method == "POST":
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            try:
                with transaction.atomic():
                    aluno = form.save()
                    messages.success(
                        request,
                        f"Aluno '{aluno.nome}' atualizado com sucesso!"
                    )
                    return redirect("alunos:detalhar_aluno_simple", aluno_id=aluno.cpf)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar aluno: {str(e)}")
        else:
            messages.error(request, "Erro no formulário. Verifique os dados.")
    else:
        form = AlunoForm(instance=aluno)
    
    context = {
        "form": form,
        "aluno": aluno,
        "titulo": f"Editar {aluno.nome}",
        "action": "editar",
    }
    
    return render(request, "alunos/formulario_aluno_simple.html", context)


@login_required
def detalhar_aluno_simple(request, aluno_id):
    """Exibe detalhes completos do aluno com histórico simplificado."""
    aluno = get_object_or_404(Aluno, cpf=aluno_id, ativo=True)
    
    # Adicionar novo evento ao histórico via POST
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        descricao = request.POST.get("descricao")
        data = request.POST.get("data")
        observacoes = request.POST.get("observacoes", "")
        
        if tipo and descricao and data:
            try:
                from datetime import datetime
                data_obj = datetime.strptime(data, "%Y-%m-%d").date()
                aluno.adicionar_evento_historico(
                    tipo=tipo,
                    descricao=descricao,
                    data=data_obj,
                    observacoes=observacoes
                )
                messages.success(request, "Evento adicionado ao histórico!")
                return redirect("alunos:detalhar_aluno_simple", aluno_id=aluno.cpf)
            except Exception as e:
                messages.error(request, f"Erro ao adicionar evento: {str(e)}")
        else:
            messages.error(request, "Tipo, descrição e data são obrigatórios.")
    
    # Obter histórico ordenado
    historico = aluno.obter_historico_ordenado()
    
    # Buscar último curso
    ultimo_curso = None
    try:
        from importlib import import_module
        Matricula = import_module("matriculas.models").Matricula
        ultima_matricula = Matricula.objects.filter(
            aluno=aluno, 
            ativa=True
        ).select_related('turma__curso').order_by('-data_matricula').first()
        if ultima_matricula:
            ultimo_curso = ultima_matricula.turma.curso.nome
    except:
        pass
    
    context = {
        "aluno": aluno,
        "historico": historico,
        "total_eventos": len(historico),
        "ultimo_evento": aluno.obter_ultimo_evento(),
        "ultimo_curso": ultimo_curso,
    }
    
    return render(request, "alunos/detalhar_aluno_simple.html", context)


@login_required
@require_http_methods(["POST"])
def adicionar_evento_historico_ajax(request, aluno_id):
    """Adiciona um evento ao histórico via AJAX."""
    aluno = get_object_or_404(Aluno, cpf=aluno_id, ativo=True)
    
    try:
        data = json.loads(request.body)
        tipo = data.get("tipo")
        descricao = data.get("descricao")
        data_evento = data.get("data")
        observacoes = data.get("observacoes", "")
        
        if not all([tipo, descricao, data_evento]):
            return JsonResponse({
                "success": False,
                "error": "Tipo, descrição e data são obrigatórios."
            }, status=400)
        
        from datetime import datetime
        data_obj = datetime.strptime(data_evento, "%Y-%m-%d").date()
        
        aluno.adicionar_evento_historico(
            tipo=tipo,
            descricao=descricao,
            data=data_obj,
            observacoes=observacoes
        )
        
        return JsonResponse({
            "success": True,
            "message": "Evento adicionado com sucesso!",
            "total_eventos": len(aluno.obter_historico_ordenado())
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


@login_required
def obter_historico_aluno_ajax(request, aluno_id):
    """Retorna o histórico do aluno em formato JSON."""
    aluno = get_object_or_404(Aluno, cpf=aluno_id, ativo=True)
    historico = aluno.obter_historico_ordenado()
    
    return JsonResponse({
        "historico": historico,
        "total": len(historico),
        "ultimo_evento": aluno.obter_ultimo_evento()
    })


@login_required
def excluir_aluno_simple(request, aluno_id):
    """Exclui um aluno (soft delete)."""
    aluno = get_object_or_404(Aluno, cpf=aluno_id, ativo=True)
    
    if request.method == "POST":
        aluno.ativo = False
        aluno.save()
        messages.success(request, f"Aluno '{aluno.nome}' excluído com sucesso!")
        return redirect("alunos:listar_alunos_simple")
    
    context = {
        "aluno": aluno,
        "titulo": f"Excluir {aluno.nome}",
    }
    
    return render(request, "alunos/excluir_aluno_simple.html", context)
