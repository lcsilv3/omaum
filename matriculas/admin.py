from django.contrib import admin
from importlib import import_module


# Função para obter o modelo Matricula dinamicamente
def get_matricula_model():
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")


# Registrar o modelo Matricula no admin
Matricula = get_matricula_model()


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "turma", "data_matricula", "status")
    search_fields = ("aluno__nome", "turma__nome")
    list_filter = ("status", "data_matricula")
    ordering = ("-data_matricula",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("aluno", "turma")
