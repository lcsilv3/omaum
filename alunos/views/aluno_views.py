"""
Views relacionadas ao CRUD básico de alunos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from importlib import import_module
import logging

from alunos.utils import get_aluno_model, get_aluno_form
from alunos.services import remover_instrutor_de_turmas

logger = logging.getLogger(__name__)

@login_required
def listar_alunos(request):
    """Lista todos os alunos cadastrados."""
    try:
        Aluno = get_aluno_model()
        # Obter parâmetros de busca e filtro
        query = request.GET.get("q", "")
        curso_id = request.GET.get("curso", "")
        
        # Filtrar alunos
        alunos = Aluno.objects.all()
        if query:
            alunos = alunos.filter(
                Q(nome__icontains=query)
                | Q(cpf__icontains=query)
                | Q(email__icontains=query)
                | Q(numero_iniciatico__icontains=query)
            )
        
        # Adicionar filtro por curso
        if curso_id:
            try:
                # Importar o modelo Matricula dinamicamente
                Matricula = import_module("matriculas.models").Matricula
                # Filtrar alunos matriculados no curso especificado
                alunos_ids = (
                    Matricula.objects.filter(
                        turma__curso__codigo_curso=curso_id
                    )
                    .values_list("aluno__cpf", flat=True)
                    .distinct()
                )
                alunos = alunos.filter(cpf__in=alunos_ids)
            except (ImportError, AttributeError) as e:
                # Log do erro, mas continuar sem o filtro de curso
                logger.error(f"Erro ao filtrar por curso: {e}")
        
        # Para cada aluno, buscar os cursos em que está matriculado
        alunos_com_cursos = []
        for aluno in alunos:
            try:
                # Importar o modelo Matricula dinamicamente
                Matricula = import_module("matriculas.models").Matricula
                # Buscar matrículas do aluno
                matriculas = Matricula.objects.filter(aluno=aluno)
                # Extrair nomes dos cursos
                cursos = [m.turma.curso.nome for m in matriculas]
                # Adicionar informação de cursos ao aluno
                aluno.cursos = cursos
            except:
                aluno.cursos = []
            alunos_com_cursos.append(aluno)
        
        # Paginação
        paginator = Paginator(alunos_com_cursos, 10)  # 10 alunos por página
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        # Obter cursos para o filtro
        try:
            Curso = import_module("cursos.models").Curso
            cursos = Curso.objects.all()
        except:
            cursos = []
        
        context = {
            "alunos": page_obj,
            "page_obj": page_obj,
            "query": query,
            "cursos": cursos,
            "curso_selecionado": curso_id,
            "total_alunos": alunos.count(),
        }
        return render(request, "alunos/listar_alunos.html", context)
    except Exception as e:
        # Em vez de mostrar a mensagem de erro, apenas retornamos uma lista vazia
        logger.error(f"Erro ao listar alunos: {str(e)}")
        return render(
            request,
            "alunos/listar_alunos.html",
            {
                "alunos": [],
                "page_obj": None,
                "query": "",
                "cursos": [],
                "curso_selecionado": "",
                "total_alunos": 0,
                "error_message": f"Erro ao listar alunos: {str(e)}",
            },
        )

@login_required
def criar_aluno(request):
    """Cria um novo aluno."""
    AlunoForm = get_aluno_form()
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                aluno = form.save()
                messages.success(request, "Aluno cadastrado com sucesso!")
                return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                messages.error(request, f"Erro ao cadastrar aluno: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AlunoForm()
    return render(
        request, "alunos/formulario_aluno.html", {"form": form, "aluno": None}
    )

@login_required
def detalhar_aluno(request, cpf):
    """Exibe os detalhes de um aluno."""
    Aluno = get_aluno_model()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    # Buscar turmas onde o aluno é instrutor
    turmas_como_instrutor = []
    turmas_como_instrutor_auxiliar = []
    turmas_como_auxiliar_instrucao = []
    
    if aluno.esta_ativo:
        from importlib import import_module
        try:
            # Importar o modelo Turma dinamicamente
            turmas_module = import_module("turmas.models")
            Turma = getattr(turmas_module, "Turma")
            # Buscar turmas ativas onde o aluno é instrutor
            turmas_como_instrutor = Turma.objects.filter(
                instrutor=aluno, status="A"
            ).select_related("curso")
            turmas_como_instrutor_auxiliar = Turma.objects.filter(
                instrutor_auxiliar=aluno, status="A"
            ).select_related("curso")
            turmas_como_auxiliar_instrucao = Turma.objects.filter(
                auxiliar_instrucao=aluno, status="A"
            ).select_related("curso")
        except (ImportError, AttributeError):
            pass
    
    # Buscar matrículas do aluno
    matriculas = []
    try:
        # Importar o modelo Matricula dinamicamente
        matriculas_module = import_module("matriculas.models")
        Matricula = getattr(matriculas_module, "Matricula")
        # Buscar matrículas do aluno
        matriculas = Matricula.objects.filter(aluno=aluno).select_related("turma__curso")
    except (ImportError, AttributeError):
        pass
    
    # Buscar atividades acadêmicas do aluno
    atividades_academicas = []
    try:
        # Importar o modelo Frequencia dinamicamente
        frequencias_module = import_module("frequencias.models")
        Frequencia = getattr(frequencias_module, "Frequencia")
        # Buscar frequências do aluno
        atividades_academicas = Frequencia.objects.filter(aluno=aluno).select_related("atividade").order_by("-data")
    except (ImportError, AttributeError):
        pass
    
    # Buscar atividades ritualísticas do aluno
    atividades_ritualisticas = []
    try:
        # Importar o modelo AtividadeRitualistica dinamicamente
        atividades_module = import_module("atividades.models")
        AtividadeRitualistica = getattr(atividades_module, "AtividadeRitualistica")
        # Buscar atividades ritualísticas do aluno
        atividades_ritualisticas = AtividadeRitualistica.objects.filter(participantes=aluno).order_by("-data")
    except (ImportError, AttributeError):
        pass
    
    return render(
        request,
        "alunos/detalhar_aluno.html",
        {
            "aluno": aluno,
            "turmas_como_instrutor": turmas_como_instrutor,
            "turmas_como_instrutor_auxiliar": turmas_como_instrutor_auxiliar,
            "turmas_como_auxiliar_instrucao": turmas_como_auxiliar_instrucao,
            "matriculas": matriculas,
            "atividades_academicas": atividades_academicas,
            "atividades_ritualisticas": atividades_ritualisticas,
        },
    )

@login_required
def editar_aluno(request, cpf):
    """Edita um aluno existente."""
    Aluno = get_aluno_model()
    AlunoForm = get_aluno_form()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    situacao_anterior = aluno.situacao
    
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        # Verificar se o formulário é válido
        if form.is_valid():
            try:
                # Verificar se a situação mudou de "ATIVO" para outra
                nova_situacao = form.cleaned_data.get("situacao")
                # Se a situação mudou e o aluno é instrutor em alguma turma
                if (
                    situacao_anterior == "ATIVO"
                    and nova_situacao != "ATIVO"
                    and hasattr(form, "aluno_e_instrutor")
                ):
                    # Verificar se o usuário confirmou a remoção da instrutoria
                    if (
                        request.POST.get("confirmar_remocao_instrutoria")
                        != "1"
                    ):
                        # Redirecionar para a página de confirmação
                        return redirect(
                            "alunos:confirmar_remocao_instrutoria",
                            cpf=aluno.cpf,
                            nova_situacao=nova_situacao,
                        )
                    # Se confirmou, atualizar as turmas
                    resultado = remover_instrutor_de_turmas(aluno, nova_situacao)
                    if not resultado["sucesso"]:
                        messages.error(request, resultado["mensagem"])
                
                # Salvar o aluno
                form.save()
                messages.success(request, "Aluno atualizado com sucesso!")
                return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                messages.error(request, f"Erro ao atualizar aluno: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = AlunoForm(instance=aluno)
    
    return render(
        request, "alunos/formulario_aluno.html", {"form": form, "aluno": aluno}
    )

@login_required
def excluir_aluno(request, cpf):
    """Exclui um aluno."""
    Aluno = get_aluno_model()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    
    if request.method == "POST":
        try:
            aluno.delete()
            messages.success(request, "Aluno excluído com sucesso!")
            return redirect("alunos:listar_alunos")
        except Exception as e:
            messages.error(request, f"Erro ao excluir aluno: {str(e)}")
            return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
    
    return render(request, "alunos/excluir_aluno.html", {"aluno": aluno})