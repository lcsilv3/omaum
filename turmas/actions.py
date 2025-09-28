from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from core.utils import get_model_dynamically


def desativar_turmas_action(modeladmin, request, queryset):
    """
    Inicia o processo de desativação, redirecionando para a página de impacto.
    """
    request.session["turmas_para_desativar"] = list(
        queryset.values_list("pk", flat=True)
    )
    return redirect("admin:desativar_turmas_impacto")


desativar_turmas_action.short_description = _(
    "Desativar turmas selecionadas (com análise de impacto)"
)


def get_desativar_turmas_impacto_view(modeladmin):
    """
    Gera a view que mostra o impacto da desativação e processa a confirmação.
    """

    def view(request):
        turma_ids = request.session.get("turmas_para_desativar")
        if not turma_ids:
            messages.error(request, _("Nenhuma turma selecionada."))
            return redirect("admin:turmas_turma_changelist")

        queryset = modeladmin.model.objects.filter(pk__in=turma_ids)

        if request.method == "POST":
            turmas_a_desativar = queryset.filter(ativo=True)

            if not turmas_a_desativar.exists():
                messages.warning(
                    request, _("As turmas selecionadas já estão inativas.")
                )
                return redirect("admin:turmas_turma_changelist")

            num_mat, num_ativ = 0, 0
            Matricula = get_model_dynamically("matriculas", "Matricula")
            Atividade = get_model_dynamically("atividades", "Atividade")

            for turma in turmas_a_desativar:
                mat = Matricula.objects.filter(turma=turma, ativa=True)
                num_mat += mat.update(ativa=False)

                ativ = Atividade.objects.filter(turmas=turma, ativo=True)
                num_ativ += ativ.update(ativo=False)

            num_turmas = turmas_a_desativar.update(ativo=False)

            msg = _(
                "Operação concluída: %(count_turmas)d turmas, "
                "%(count_matriculas)d matrículas e %(count_atividades)d "
                "atividades foram desativadas."
            ) % {
                "count_turmas": num_turmas,
                "count_matriculas": num_mat,
                "count_atividades": num_ativ,
            }
            messages.success(request, msg)

            if "turmas_para_desativar" in request.session:
                del request.session["turmas_para_desativar"]

            return redirect("admin:turmas_turma_changelist")

        Matricula = get_model_dynamically("matriculas", "Matricula")
        Atividade = get_model_dynamically("atividades", "Atividade")

        mat_afetadas = Matricula.objects.filter(turma__in=queryset, ativa=True)
        atividades_afetadas = Atividade.objects.filter(turmas__in=queryset, ativo=True)

        impacto = {
            "turmas": queryset,
            "matriculas": mat_afetadas,
            "atividades": atividades_afetadas,
        }

        context = {
            **modeladmin.admin_site.each_context(request),
            "title": _("Análise de Impacto da Desativação"),
            "queryset": queryset,
            "opts": modeladmin.model._meta,
            "impacto": impacto,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
        }
        return render(request, "admin/turmas/desativar_impacto.html", context)

    return view