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
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from alunos.utils import get_aluno_model, get_aluno_form
from alunos.services import InstrutorService

from django import forms
from alunos.models import Aluno, RegistroHistorico
from alunos.forms import RegistroHistoricoForm
from alunos.utils import get_tipo_codigo_model, get_codigo_model

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
                    Matricula.objects.filter(turma__curso__codigo_curso=curso_id)
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
            except Exception:
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
        except Exception:
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
    import time

    logger = logging.getLogger(__name__)
    logger.info("[PERF] View criar_aluno chamada")
    t0 = time.perf_counter()
    AlunoForm = get_aluno_form()
    CustomFormSet = forms.inlineformset_factory(
        Aluno,
        RegistroHistorico,
        form=RegistroHistoricoForm,
        extra=1,
        can_delete=True,
        min_num=0,
        max_num=20,
        validate_min=False,
        validate_max=True,
    )
    if request.method == "POST":
        t3 = time.perf_counter()
        form = AlunoForm(request.POST, request.FILES)
        t4 = time.perf_counter()
        historico_formset = CustomFormSet(request.POST, prefix="historico")
        t5 = time.perf_counter()
        logger.info(
            f"[PERF] Tempo para instanciar AlunoForm: {t4-t3:.4f}s | Formset: {t5-t4:.4f}s"
        )
        if form.is_valid() and historico_formset.is_valid():
            try:
                t6 = time.perf_counter()
                aluno = form.save()
                historico_formset.instance = aluno
                historico_formset.save()
                t7 = time.perf_counter()
                logger.info(f"[PERF] Tempo para salvar aluno e formset: {t7-t6:.4f}s")
                messages.success(request, "Aluno cadastrado com sucesso!")
                return redirect("alunos:detalhar_aluno", cpf=aluno.cpf)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
                messages.error(request, "Por favor, corrija os erros abaixo.")
            except Exception as e:
                messages.error(request, f"Erro ao cadastrar aluno: {str(e)}")
            # Renderiza o formulário novamente após exceção
            t8 = time.perf_counter()
            response = render(
                request,
                "alunos/formulario_aluno.html",
                {"form": form, "aluno": None, "historico_formset": historico_formset},
            )
            t9 = time.perf_counter()
            logger.info(f"[PERF] Tempo para renderizar template (erro): {t9-t8:.4f}s")
            return response
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
        # Renderiza o formulário novamente após erro de validação
        t10 = time.perf_counter()
        response = render(
            request,
            "alunos/formulario_aluno.html",
            {"form": form, "aluno": None, "historico_formset": historico_formset},
        )
        t11 = time.perf_counter()
        logger.info(
            f"[PERF] Tempo para renderizar template (validação): {t11-t10:.4f}s"
        )
        return response
    else:
        try:
            t12 = time.perf_counter()
            form = AlunoForm()
            t13 = time.perf_counter()
            historico_formset = CustomFormSet(
                queryset=RegistroHistorico.objects.none(), prefix="historico"
            )
            t14 = time.perf_counter()
            # Garante que o management_form SEMPRE seja gerado
            _ = historico_formset.management_form
            t15 = time.perf_counter()
            logger.info(
                f"[PERF] Tempo para instanciar AlunoForm: {t13-t12:.4f}s | Formset: {t14-t13:.4f}s | Management form: {t15-t14:.4f}s"
            )
            t16 = time.perf_counter()
            response = render(
                request,
                "alunos/formulario_aluno.html",
                {"form": form, "aluno": None, "historico_formset": historico_formset},
            )
            t17 = time.perf_counter()
            logger.info(
                f"[PERF] Tempo para renderizar template (GET): {t17-t16:.4f}s | Total: {t17-t0:.4f}s"
            )
            return response
        except Exception as e:
            from django.http import HttpResponse

            return HttpResponse(
                f"<h1>Erro ao renderizar o template:</h1><pre>{str(e)}</pre>",
                status=500,
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
        matriculas = Matricula.objects.filter(aluno=aluno).select_related(
            "turma__curso"
        )
    except (ImportError, AttributeError):
        pass

    # Buscar atividades acadêmicas do aluno
    atividades_academicas = []
    try:
        # Importar o modelo Frequencia dinamicamente
        frequencias_module = import_module("frequencias.models")
        Frequencia = getattr(frequencias_module, "Frequencia")
        # Buscar frequências do aluno
        atividades_academicas = (
            Frequencia.objects.filter(aluno=aluno)
            .select_related("atividade")
            .order_by("-data")
        )
    except (ImportError, AttributeError):
        pass

    # Buscar atividades ritualísticas do aluno
    atividades_ritualisticas = []
    try:
        # Importar o modelo AtividadeRitualistica dinamicamente
        atividades_module = import_module("atividades.models")
        AtividadeRitualistica = getattr(atividades_module, "AtividadeRitualistica")
        # Buscar atividades ritualísticas do aluno
        atividades_ritualisticas = AtividadeRitualistica.objects.filter(
            participantes=aluno
        ).order_by("-data")
    except (ImportError, AttributeError):
        pass

    # Buscar registros históricos do aluno
    historico_registros = []
    try:
        from alunos.models import RegistroHistorico

        historico_registros = RegistroHistorico.objects.filter(
            aluno=aluno, ativo=True
        ).order_by("-data_os")[:10]  # Últimos 10 registros
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
            "historico_registros": historico_registros,
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
                    if request.POST.get("confirmar_remocao_instrutoria") != "1":
                        # Redirecionar para a página de confirmação
                        return redirect(
                            "alunos:confirmar_remocao_instrutoria",
                            cpf=aluno.cpf,
                            nova_situacao=nova_situacao,
                        )
                    # Se confirmou, atualizar as turmas
                    resultado = InstrutorService.remover_de_turmas(aluno, nova_situacao)
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

    # Garante que historico_formset está sempre presente
    CustomFormSet = forms.inlineformset_factory(
        Aluno,
        RegistroHistorico,
        form=RegistroHistoricoForm,
        extra=1,
        can_delete=True,
        min_num=0,
        max_num=20,
        validate_min=False,
        validate_max=True,
    )
    historico_formset = CustomFormSet(instance=aluno, prefix="historico")
    # Garante que o management_form SEMPRE será renderizado
    if historico_formset.total_form_count() == 0:
        historico_formset.extra_forms = [historico_formset.empty_form]
    return render(
        request,
        "alunos/formulario_aluno.html",
        {"form": form, "aluno": aluno, "historico_formset": historico_formset},
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


@login_required
@require_http_methods(["GET"])
def listar_tipos_codigos_ajax(request):
    """Retorna lista de tipos de códigos via AJAX."""
    try:
        TipoCodigo = get_tipo_codigo_model()
        if not TipoCodigo:
            return JsonResponse(
                {"status": "error", "message": "Modelo TipoCodigo indisponível"},
                status=500,
            )
        tipos = TipoCodigo.objects.all().values("id", "nome", "descricao")
        return JsonResponse({"status": "success", "tipos": list(tipos)})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def listar_codigos_por_tipo_ajax(request):
    """Retorna códigos filtrados por tipo via AJAX."""
    try:
        Codigo = get_codigo_model()
        if not Codigo:
            return JsonResponse(
                {"status": "error", "message": "Modelo Codigo indisponível"}, status=500
            )
        tipo_id = request.GET.get("tipo_id")
        if not tipo_id:
            return JsonResponse(
                {"status": "error", "message": "Tipo de código não fornecido"},
                status=400,
            )

        codigos = Codigo.objects.filter(tipo_codigo_id=tipo_id).values(
            "id", "nome", "descricao"
        )

        return JsonResponse({"status": "success", "codigos": list(codigos)})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def adicionar_evento_historico_ajax(request):
    """Adiciona evento ao histórico via AJAX."""
    try:
        import json

        data = json.loads(request.body)
        aluno_id = data.get("aluno_id")
        tipo_evento = data.get("tipo_evento")
        codigo_id = data.get("codigo_id")
        ordem_servico = data.get("ordem_servico", "")
        data_os = data.get("data_os")
        data_evento = data.get("data_evento")
        observacoes = data.get("observacoes", "")

        # Validar campos obrigatórios
        if not all([aluno_id, tipo_evento, codigo_id, data_os, data_evento]):
            return JsonResponse(
                {"status": "error", "message": "Campos obrigatórios não preenchidos"},
                status=400,
            )

        # Obter objetos
        aluno = get_object_or_404(Aluno, id=aluno_id)
        Codigo = get_codigo_model()
        if not Codigo:
            return JsonResponse(
                {"status": "error", "message": "Modelo Codigo indisponível"}, status=500
            )
        codigo = get_object_or_404(Codigo, id=codigo_id)

        # Criar evento via serviço centralizado (garante sincronização JSON + relacional)
        try:
            # TODO: Implementar e importar a função 'criar_evento_iniciatico'
            resultado = {"registro": None}  # Valor provisório para evitar erros
            # resultado = criar_evento_iniciatico(
            #     aluno=aluno,
            #     codigo=codigo,
            #     tipo_evento=tipo_evento,
            #     data_os=data_os,
            #     data_evento=data_evento,
            #     ordem_servico=ordem_servico,
            #     observacoes=observacoes,
            # )
        except Exception as exc:  # noqa: BLE001
            return JsonResponse(
                {"status": "error", "message": f"Falha ao criar evento: {exc}"},
                status=500,
            )
        registro = resultado["registro"]

        return JsonResponse(
            {
                "status": "success",
                "message": "Evento adicionado com sucesso",
                "registro": {
                    "id": registro.id,
                    "codigo": codigo.nome,
                    "data_os": registro.data_os.strftime("%d/%m/%Y"),
                    "observacoes": registro.observacoes,
                    "cache_evento": evento_json,
                },
            }
        )

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def historico_iniciatico_paginado_ajax(request, cpf):
    """Retorna histórico iniciático paginado (JSON) para consumo incremental.

    Parâmetros query:
      - page (int, opcional, default=1)
      - page_size (int, opcional, default=20, max=200)
    """
    try:
        Aluno = get_aluno_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 20))
        if page_size > 200:
            page_size = 200

        # TODO: Implementar e importar a função 'listar_eventos_iniciaticos'
        registros = []  # Valor provisório para evitar erros
        # registros = listar_eventos_iniciaticos(aluno)
        total = len(registros)
        start = (page - 1) * page_size
        end = start + page_size
        slice_regs = registros[start:end]

        itens = []
        for r in slice_regs:
            itens.append(
                {
                    "id": r.id,
                    "codigo_id": r.codigo_id,
                    "codigo": r.codigo.nome,
                    "tipo_codigo": r.codigo.tipo_codigo.nome,
                    "descricao": r.codigo.descricao or "",
                    "data_os": r.data_os.isoformat(),
                    "created_at": r.created_at.isoformat(),
                    "ordem_servico": r.ordem_servico or "",
                    "observacoes": r.observacoes or "",
                }
            )

        return JsonResponse(
            {
                "status": "success",
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size if page_size else 1,
                "results": itens,
            }
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Falha ao paginar histórico: %s", exc)
        return JsonResponse(
            {"status": "error", "message": f"Falha ao obter histórico: {exc}"},
            status=500,
        )
