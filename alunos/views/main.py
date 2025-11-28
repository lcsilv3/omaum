"""
Views relacionadas ao gerenciamento de alunos no sistema.
"""

import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db import transaction
from django import forms
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

from alunos.forms import AlunoForm, RegistroHistoricoFormSet, RegistroHistoricoForm
from alunos.models import Aluno, RegistroHistorico
from alunos.services import listar_alunos, buscar_aluno_por_id

logger = logging.getLogger(__name__)


@login_required
def listar_alunos_view(request):
    """Lista todos os alunos, com suporte a busca dinâmica (AJAX)."""
    try:
        logger.info(
            f"[DEBUG] listar_alunos_view chamada - User: {request.user}, Auth: {request.user.is_authenticated}"
        )
        query = request.GET.get("q", "")
        curso_id = request.GET.get("curso", "")
        page_number = request.GET.get("page")

        alunos_list = listar_alunos(query=query, curso_id=curso_id)
        total_alunos = alunos_list.count()

        paginator = Paginator(alunos_list, 10)
        page_obj = paginator.get_page(page_number)

        from alunos.utils import get_curso_model

        Curso = get_curso_model()
        cursos_para_filtro = Curso.objects.all().order_by("nome") if Curso else []

        context = {
            "alunos": page_obj,
            "page_obj": page_obj,
            "query": query,
            "cursos": cursos_para_filtro,
            "curso_selecionado": curso_id,
            "total_alunos": total_alunos,
        }

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            tabela_html = render_to_string(
                "alunos/_tabela_alunos_parcial.html", context, request=request
            )
            paginacao_html = render_to_string(
                "alunos/_paginacao_parcial.html", context, request=request
            )
            return JsonResponse(
                {"tabela_html": tabela_html, "paginacao_html": paginacao_html}
            )

        return render(
            request,
            "alunos/listar_alunos.html",
            context,
        )
    except Exception as exc:
        logger.error("Erro ao listar alunos: %s", exc)
        context = {
            "alunos": [],
            "page_obj": None,
            "query": "",
            "cursos": [],
            "curso_selecionado": "",
            "total_alunos": 0,
            "error_message": f"Erro ao listar alunos: {exc}",
        }
        return render(
            request,
            "alunos/listar_alunos.html",
            context,
        )


@login_required
@permission_required("alunos.add_aluno", raise_exception=True)
def criar_aluno(request):
    """
    Cria um novo aluno e gerencia seu histórico de registros.
    """
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES)
        historico_formset = RegistroHistoricoFormSet(request.POST, prefix="historico")
        # Garante pelo menos 1 formulário extra
        if historico_formset.total_form_count() == 0:
            historico_formset.extra_forms.append(historico_formset.empty_form)

        if form.is_valid() and historico_formset.is_valid():
            try:
                with transaction.atomic():
                    aluno = form.save(commit=False)
                    aluno.cpf = "".join(filter(str.isdigit, str(aluno.cpf)))
                    
                    # Se não houver foto no upload mas houver foto encontrada automaticamente
                    if not request.FILES.get('foto') and request.POST.get('foto_encontrada_path'):
                        from django.conf import settings
                        from pathlib import Path
                        foto_path = request.POST.get('foto_encontrada_path')
                        # Salva o caminho relativo da foto encontrada
                        aluno.foto = foto_path
                    
                    aluno.save()

                    historico_formset.instance = aluno
                    historico_formset.save()

                messages.success(request, "Aluno criado com sucesso!")
                return redirect("alunos:detalhar_aluno", aluno_id=aluno.id)
            except Exception as exc:
                logger.error("Erro ao criar aluno: %s", exc)
                messages.error(request, f"Ocorreu um erro ao salvar o aluno: {exc}")
        else:
            # Adiciona logs para depurar erros de formulário
            logger.warning("Formulário de aluno inválido: %s", form.errors)
            logger.warning(
                "Formset de histórico inválido: %s", historico_formset.errors
            )
            messages.error(request, "Por favor, corrija os erros abaixo.")

        # Se não for válido, sempre garante pelo menos 1 extra
        if historico_formset.total_form_count() == 0:
            historico_formset.extra_forms.append(historico_formset.empty_form)
    else:
        form = AlunoForm()
        historico_formset = RegistroHistoricoFormSet(prefix="historico")
        # Garante pelo menos 1 formulário extra
        if historico_formset.total_form_count() == 0:
            historico_formset.extra_forms.append(historico_formset.empty_form)

    context = {
        "form": form,
        "historico_formset": historico_formset,
        "aluno": None,
        "debug": True,  # Habilitar debug temporariamente
    }

    # DEBUG: Verificar se o management form está sendo duplicado
    mgmt_form_html = str(historico_formset.management_form)
    mgmt_count = mgmt_form_html.count('name="historico-TOTAL_FORMS"')
    print(f"[DEBUG] View criar_aluno: Management forms no formset: {mgmt_count}")

    return render(request, "alunos/formulario_aluno.html", context)


@login_required
def detalhar_aluno(request, aluno_id):
    """Exibe os detalhes de um aluno e seu histórico de registros."""
    aluno = buscar_aluno_por_id(aluno_id)
    if not aluno:
        messages.error(request, "Aluno não encontrado.")
        return redirect("alunos:listar_alunos")

    historico_list = aluno.historico.all()
    form_historico = RegistroHistoricoForm()

    context = {
        "aluno": aluno,
        "historico_list": historico_list,
        "form_historico": form_historico,
    }
    return render(request, "alunos/detalhar_aluno.html", context)


@login_required
@permission_required("alunos.change_aluno", raise_exception=True)
def editar_aluno(request, aluno_id):
    """
    Edita um aluno existente e seu histórico de registros.
    """

    def build_context(form=None, historico_formset=None, aluno=None):
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
        if form is None:
            form = AlunoForm()
        # Nunca permite historico_formset ser None ou string vazia
        if historico_formset is None or historico_formset == "":
            historico_formset = CustomFormSet(prefix="historico")
        try:
            _ = historico_formset.management_form
        except Exception:
            historico_formset = CustomFormSet(prefix="historico")
        # Garante pelo menos um formulário extra
        if historico_formset.total_form_count() == 0:
            historico_formset.extra_forms.append(historico_formset.empty_form)
        return {
            "form": form,
            "historico_formset": historico_formset,
            "aluno": aluno,
            "debug": True,
        }

    aluno = buscar_aluno_por_id(aluno_id)
    form = None
    historico_formset = None
    try:
        if aluno:
            if request.method == "POST":
                form = AlunoForm(request.POST, request.FILES, instance=aluno)
                historico_formset = RegistroHistoricoFormSet(
                    request.POST, instance=aluno, prefix="historico"
                )
                if (
                    historico_formset is None
                    or historico_formset.total_form_count() == 0
                ):
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
                    historico_formset = CustomFormSet(
                        request.POST, instance=aluno, prefix="historico"
                    )
                # Garante pelo menos um formulário extra
                if historico_formset.total_form_count() == 0:
                    historico_formset.extra_forms.append(historico_formset.empty_form)
                if form.is_valid() and historico_formset.is_valid():
                    try:
                        with transaction.atomic():
                            aluno_editado = form.save(commit=False)
                            
                            # Se não houver foto no upload mas houver foto encontrada automaticamente
                            if not request.FILES.get('foto') and request.POST.get('foto_encontrada_path'):
                                from django.conf import settings
                                from pathlib import Path
                                foto_path = request.POST.get('foto_encontrada_path')
                                # Salva o caminho relativo da foto encontrada
                                aluno_editado.foto = foto_path
                            
                            aluno_editado.save()
                            historico_formset.save()
                        messages.success(request, "Aluno atualizado com sucesso!")
                        return redirect("alunos:detalhar_aluno", aluno_id=aluno.id)
                    except Exception as exc:
                        logger.error("Erro ao editar aluno %s: %s", aluno_id, exc)
                        messages.error(
                            request, f"Ocorreu um erro ao atualizar o aluno: {exc}"
                        )
                else:
                    # Adiciona logs para depurar erros de formulário
                    logger.warning("Formulário de aluno inválido: %s", form.errors)
                    logger.warning(
                        "Formset de histórico inválido: %s", historico_formset.errors
                    )
                    messages.error(request, "Por favor, corrija os erros abaixo.")
                # Sempre retorna contexto robusto
                return render(
                    request,
                    "alunos/formulario_aluno.html",
                    build_context(form, historico_formset, aluno),
                )
            else:
                form = AlunoForm(instance=aluno)
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
                # Garante pelo menos um formulário extra
                if historico_formset.total_form_count() == 0:
                    historico_formset.extra_forms.append(historico_formset.empty_form)
                return render(
                    request,
                    "alunos/formulario_aluno.html",
                    build_context(form, historico_formset, aluno),
                )
        else:
            messages.error(request, "Aluno não encontrado.")
            form = AlunoForm()
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
            historico_formset = CustomFormSet(prefix="historico")
            # Garante pelo menos um formulário extra
            if historico_formset.total_form_count() == 0:
                historico_formset.extra_forms.append(historico_formset.empty_form)
            return render(
                request,
                "alunos/formulario_aluno.html",
                build_context(form, historico_formset, None),
            )
    except Exception as exc:
        logger.error(f"Erro ao inicializar formset de histórico: {exc}")
        if not form:
            form = AlunoForm()
        if not historico_formset:
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
            historico_formset = CustomFormSet(prefix="historico")
        # Garante pelo menos um formulário extra
        if historico_formset.total_form_count() == 0:
            historico_formset.extra_forms.append(historico_formset.empty_form)
        messages.error(request, f"Erro ao carregar formulário de histórico: {exc}")
        # Sempre retorna contexto robusto
        return render(
            request,
            "alunos/formulario_aluno.html",
            build_context(form, historico_formset, aluno),
        )


@login_required
@permission_required("alunos.delete_aluno", raise_exception=True)
def excluir_aluno(request, aluno_id):
    """Exclui um aluno utilizando a camada de serviço."""
    aluno = buscar_aluno_por_id(aluno_id)
    if not aluno:
        messages.error(request, "Aluno não encontrado.")
        return redirect("alunos:listar_alunos")

    if request.method == "POST":
        try:
            aluno.delete()
            messages.success(request, "Aluno excluído com sucesso!")
            return redirect("alunos:listar_alunos")
        except Exception as exc:
            messages.error(request, f"Não foi possível excluir o aluno. Erro: {exc}")
            return redirect("alunos:detalhar_aluno", aluno_id=aluno_id)

    context = {
        "aluno": aluno,
    }
    return render(request, "alunos/excluir_aluno.html", context)


from django.contrib.auth.decorators import login_required


@login_required
def search_alunos(request):
    """
    Endpoint para busca dinâmica de alunos.
    Retorna os resultados em formato JSON para requisições AJAX.
    Para requisições normais, renderiza a página de listagem de alunos.
    """
    logger.info(
        f"[DEBUG] search_alunos chamada - User: {request.user}, Auth: {request.user.is_authenticated}, Headers: {dict(request.headers)}"
    )
    # Tratamento especial para AJAX não autenticado (deve ser redundante, mas cobre edge cases de sessão expirada)
    if (
        not request.user.is_authenticated
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        return JsonResponse({"success": False, "error": "Não autenticado"}, status=401)

    query = request.GET.get("q", "").strip()
    curso_id = request.GET.get("curso", None)

    logger.debug(
        "[search_alunos] Requisição recebida. Query: '%s', Curso ID: '%s', Params: %s",
        query,
        curso_id,
        dict(request.GET),
    )

    try:
        alunos_queryset = listar_alunos(query=query, curso_id=curso_id)
        logger.debug(
            "[search_alunos] Query executada. Resultados encontrados: %d",
            alunos_queryset.count(),
        )

        paginator = Paginator(alunos_queryset, 10)
        page_number = request.GET.get("page", 1)
        alunos = paginator.get_page(page_number)

        # Se for uma requisição AJAX, retorna HTML parcial (compatível com JS atual)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            context_partials = {
                "alunos": alunos,  # page object
                "page_obj": alunos,
                "total_alunos": alunos.paginator.count
                if hasattr(alunos, "paginator")
                else 0,
                "query": query,
                "cursos": [],
                "curso_selecionado": curso_id or "",
            }
            logger.debug(
                "[search_alunos] Contexto enviado para templates parciais: %s",
                context_partials,
            )
            try:
                tabela_html = render_to_string(
                    "alunos/_tabela_alunos_parcial.html",
                    context_partials,
                    request=request,
                )
                paginacao_html = render_to_string(
                    "alunos/_paginacao_parcial.html", context_partials, request=request
                )
                logger.debug(
                    "[search_alunos] Templates parciais renderizados com sucesso."
                )
            except Exception as exc:
                import traceback

                logger.error(
                    "Erro ao renderizar templates parciais AJAX: %s\n%s",
                    exc,
                    traceback.format_exc(),
                )
                return JsonResponse(
                    {
                        "success": False,
                        "error": f"Erro ao renderizar templates parciais: {exc}",
                    },
                    status=500,
                )
            return JsonResponse(
                {
                    "success": True,
                    "tabela_html": tabela_html,
                    "paginacao_html": paginacao_html,
                    "page": alunos.number,
                    "num_pages": alunos.paginator.num_pages,
                    "total_alunos": context_partials["total_alunos"],
                }
            )
        # Renderização padrão
        context = {"alunos": alunos}
        logger.debug("[search_alunos] Renderização padrão. Contexto: %s", context)
        return render(request, "alunos/listar_alunos.html", context)
    except ValueError as exc:
        logger.error("[search_alunos] Erro de valor: %s", exc, exc_info=True)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": str(exc)}, status=400)
        else:
            messages.error(request, f"Erro na busca: {str(exc)}")
            return redirect("alunos:listar_alunos")
    except Exception as exc:
        import traceback

        logger.error(
            "[search_alunos] Erro inesperado: %s\n%s", exc, traceback.format_exc()
        )
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {"success": False, "error": "Erro interno do servidor."}, status=500
            )
        else:
            messages.error(request, "Erro interno do servidor.")
            return redirect("alunos:listar_alunos")


# Alias para manter compatibilidade com URLs
listar_alunos_url = listar_alunos_view
