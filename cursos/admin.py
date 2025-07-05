from django.contrib import admin
from django.urls import path
from .models import Curso
from .actions import desativar_cursos_action, get_desativar_cursos_impacto_view


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "ativo",
    ]
    search_fields = ["nome"]
    list_filter = ["ativo"]
    actions = [desativar_cursos_action]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'desativar-impacto/',
                self.admin_site.admin_view(
                    get_desativar_cursos_impacto_view(self)
                ),
                name='desativar_cursos_impacto',
            ),
        ]
        return custom_urls + urls
