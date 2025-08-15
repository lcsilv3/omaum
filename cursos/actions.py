# cursos/actions.py

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from turmas.models import Turma
from .models import Curso


def desativar_cursos_action(modeladmin, request, queryset):
    selected = queryset.values_list("pk", flat=True)
    url = reverse("admin:desativar_cursos_impacto")
    return HttpResponseRedirect(f"{url}?ids={', '.join(map(str, selected))}")


desativar_cursos_action.short_description = "Desativar Cursos Selecionados"


def get_desativar_cursos_impacto_view(modeladmin):
    def desativar_cursos_impacto_view(request):
        curso_ids_str = request.GET.get("ids", "")
        if not curso_ids_str:
            messages.error(request, "Nenhum curso selecionado.")
            return HttpResponseRedirect(reverse("admin:cursos_curso_changelist"))

        curso_ids = [int(pk) for pk in curso_ids_str.split(",")]
        cursos = Curso.objects.filter(pk__in=curso_ids)
        turmas_afetadas = Turma.objects.filter(curso__in=cursos, ativo=True)

        if request.method == "POST":
            turmas_count = turmas_afetadas.count()
            cursos_count = cursos.count()

            turmas_afetadas.update(ativo=False)
            cursos.update(ativo=False)

            msg = (
                f"{cursos_count} curso(s) e "
                f"{turmas_count} turma(s) foram desativados."
            )
            messages.success(request, msg)
            changelist_url = reverse("admin:cursos_curso_changelist")
            return HttpResponseRedirect(changelist_url)

        context = {
            "title": "Análise de Impacto da Desativação",
            "cursos": cursos,
            "turmas_afetadas": turmas_afetadas,
            "opts": modeladmin.model._meta,
            "action_checkbox_name": "select_across",
            "media": modeladmin.media,
            "ids": curso_ids_str,
        }
        return render(request, "admin/cursos/desativar_impacto.html", context)

    return desativar_cursos_impacto_view
