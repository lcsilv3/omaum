from datetime import datetime, timedelta, date
from django.db.models import Count, Q, Avg
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Aluno

# Imports necessários para views CRUD e relatórios
import logging
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from .forms import AlunoForm, RegistroHistoricoFormSet, RegistroHistoricoForm
from .models import RegistroHistorico
from .services import listar_alunos, buscar_aluno_por_id
from django import forms

logger = logging.getLogger(__name__)


@login_required
def painel(request):
    """Renderiza o template base do painel de alunos."""
    return render(request, "alunos/painel.html")


# --- API Painel de Alunos ---
@login_required
@require_GET
def painel_kpis_api(request):
    from .models import Aluno

    total_alunos = Aluno.objects.count()
    alunos_ativos = Aluno.objects.filter(situacao="a").count()
    media_idade = Aluno.objects.filter(situacao="a").aggregate(
        m=Avg("data_nascimento")
    )["m"]


@login_required
@require_GET
def painel_tabela_api(request):
    from .models import Aluno

    alunos = Aluno.objects.all().order_by("-id")[:50]
    html = render_to_string("alunos/_tabela_alunos_parcial.html", {"alunos": alunos})
    return HttpResponse(html)


@login_required
def listar_alunos_simple(request):
    alunos = Aluno.objects.all()
    return render(request, "alunos/listar_alunos_simple.html", {"alunos": alunos})


@login_required
def criar_aluno_simple(request):
    if request.method == "POST":
        data = request.POST
        aluno = Aluno.objects.create(
            cpf=data.get("cpf", "99999999999"),
            nome=data.get("nome", "Aluno Teste"),
            data_nascimento=data.get("data_nascimento", date(2000, 1, 1)),
            email=data.get("email", "teste@exemplo.com"),
        )
        return redirect(reverse("alunos:detalhar_aluno_simple", args=[aluno.cpf]))
    return render(request, "alunos/criar_aluno_simple.html")


@login_required
def detalhar_aluno_simple(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    return render(request, "alunos/detalhar_aluno_simple.html", {"aluno": aluno})


@login_required
def editar_aluno_simple(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == "POST":
        aluno.nome = request.POST.get("nome", aluno.nome)
        aluno.save()
        return redirect(reverse("alunos:detalhar_aluno_simple", args=[aluno.cpf]))
    return render(request, "alunos/editar_aluno_simple.html", {"aluno": aluno})


@login_required
def excluir_aluno_simple(request, cpf):
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == "POST":
        aluno.delete()
        return redirect(reverse("alunos:listar_alunos_simple"))
    return render(request, "alunos/excluir_aluno_simple.html", {"aluno": aluno})


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

        from .utils import get_curso_model

        Curso = get_curso_model()
        cursos_para_filtro = Curso.objects.all().order_by("nome") if Curso else []

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            alunos_data = [
                {
                    "id": aluno.id,
                    "nome": aluno.nome,
                    "email": aluno.email,
                    "cpf": aluno.cpf,
                    "foto": aluno.foto.url if aluno.foto else None,
                    "cursos": [
                        matricula.turma.curso.nome
                        for matricula in aluno.matriculas.select_related("turma__curso")
                    ]
                    if aluno.matriculas.exists()
                    else ["Sem curso associado"],
                }
                for aluno in page_obj
            ]
            return JsonResponse(
                {
                    "alunos": alunos_data,
                    "page": page_obj.number,
                    "num_pages": paginator.num_pages,
                }
            )

        from alunos.reports import RELATORIOS

        return render(
            request,
            "alunos/listar_alunos.html",
            {
                "alunos": page_obj,
                "page_obj": page_obj,
                "query": query,
                "cursos": cursos_para_filtro,
                "curso_selecionado": curso_id,
                "total_alunos": total_alunos,
                "relatorios_alunos": RELATORIOS,
            },
        )
    except Exception as exc:
        logger.error("Erro ao listar alunos: %s", exc)
        from alunos.reports import RELATORIOS

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
                "error_message": f"Erro ao listar alunos: {exc}",
                "relatorios_alunos": RELATORIOS,
            },
        )


@login_required
@permission_required("alunos.add_aluno", raise_exception=True)

                    historico_formset.instance = aluno
    if (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        and request.GET.get("ajax_relatorios") == "1"
    ):
        import json
        from alunos.reports import RELATORIOS
        context_cards = {
            "relatorios_alunos": RELATORIOS,
            "relatorios_alunos_json": json.dumps(RELATORIOS, ensure_ascii=False, indent=2)
        }
        print("DEBUG CONTEXTO CARDS RELATORIOS (REAL):", context_cards)
        cards_relatorios_html = render_to_string(
            "alunos/cards_relatorios_alunos.html",
            context_cards,
            request=request,
        )
        return JsonResponse({"cards_relatorios_html": cards_relatorios_html})
                    historico_formset.save()

                messages.success(request, "Aluno criado com sucesso!")
                return redirect("alunos:listar_alunos")
            except Exception as exc:
                logger.error("Erro ao criar aluno: %s", exc)
                messages.error(request, f"Ocorreu um erro ao salvar o aluno: {exc}")
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

    historico_list = aluno.historico_set.all()

    context = {
        "aluno": aluno,
        "historico_list": historico_list,
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
                            form.save()
                            historico_formset.save()
                        messages.success(request, "Aluno atualizado com sucesso!")
                        return redirect("alunos:listar_alunos")
                    except Exception as exc:
                        logger.error("Erro ao editar aluno %s: %s", aluno_id, exc)
                        messages.error(
                            request, f"Ocorreu um erro ao atualizar o aluno: {exc}"
                        )
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


@login_required
def search_alunos(request):
        if (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            and request.GET.get("ajax_relatorios") == "1"
        ):
            import json
            from alunos.reports import RELATORIOS
            context_cards = {
                "relatorios_alunos": RELATORIOS,
                "relatorios_alunos_json": json.dumps(RELATORIOS, ensure_ascii=False, indent=2)
            }
            print("DEBUG CONTEXTO CARDS RELATORIOS (REAL):", context_cards)
            cards_relatorios_html = render_to_string(
                "alunos/cards_relatorios_alunos.html",
                context_cards,
                request=request,
            )
            return JsonResponse({"cards_relatorios_html": cards_relatorios_html})

    query = request.GET.get("q", "").strip()
    curso_id = request.GET.get("curso", None)

    try:
        alunos_queryset = listar_alunos(query=query, curso_id=curso_id)
        paginator = Paginator(alunos_queryset, 10)
        page_number = request.GET.get("page", 1)
        alunos = paginator.get_page(page_number)

        # Se for requisição AJAX só para os cards de relatórios
        if (
            request.headers.get("x-requested-with") == "XMLHttpRequest"
            and request.GET.get("ajax_relatorios") == "1"
        ):
            from alunos.reports import RELATORIOS

            context_cards = {"relatorios_alunos": RELATORIOS}
            print("DEBUG CONTEXTO CARDS RELATORIOS (REAL):", context_cards)
            cards_relatorios_html = render_to_string(
                "alunos/cards_relatorios_alunos.html",
                context_cards,
                request=request,
            )
            return JsonResponse({"cards_relatorios_html": cards_relatorios_html})

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            from alunos.reports import RELATORIOS

            print("DEBUG RELATORIOS (AJAX):", RELATORIOS)

            tabela_html = render_to_string(
                "alunos/_tabela_alunos_parcial.html",
                {"alunos": alunos, "page_obj": alunos, "relatorios_alunos": RELATORIOS},
                request=request,
            )
            paginacao_html = render_to_string(
                "alunos/_paginacao_parcial.html", {"page_obj": alunos}, request=request
            )
            context_cards = {"relatorios_alunos": RELATORIOS}
            print("DEBUG CONTEXTO CARDS RELATORIOS:", context_cards)
            cards_relatorios_html = render_to_string(
                "alunos/cards_relatorios_alunos.html",
                context_cards,
                request=request,
            )
            return JsonResponse(
                {
                    "success": True,
                    "tabela_html": tabela_html,
                    "paginacao_html": paginacao_html,
                    "cards_relatorios_html": cards_relatorios_html,
                    "total_alunos": paginator.count,
                }
            )

        from .utils import get_curso_model

        Curso = get_curso_model()
        cursos_para_filtro = Curso.objects.all().order_by("nome") if Curso else []
        from alunos.reports import RELATORIOS

        print("DEBUG RELATORIOS (RENDER):", RELATORIOS)
        context = {
            "alunos": alunos,
            "page_obj": alunos,
            "query": query,
            "cursos": cursos_para_filtro,
            "curso_selecionado": curso_id,
            "total_alunos": paginator.count,
            "relatorios_alunos": RELATORIOS,
        }
        return render(request, "alunos/listar_alunos.html", context)
    except Exception as exc:
        logger.error("[search_alunos] Erro inesperado: %s", exc, exc_info=True)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {"success": False, "error": "Erro interno do servidor."},
                status=500,
            )
        else:
            messages.error(request, "Ocorreu um erro inesperado ao buscar alunos.")
            from alunos.reports import RELATORIOS

            return render(
                request,
                "alunos/listar_alunos.html",
                {"alunos": [], "relatorios_alunos": RELATORIOS},
            )


# Alias para manter compatibilidade com URLs
listar_alunos_url = listar_alunos_view
