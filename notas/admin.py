from django.contrib import admin
from importlib import import_module


# Função para obter o modelo Nota dinamicamente
def get_nota_model():
    notas_module = import_module("notas.models")
    return getattr(notas_module, "Nota")


# Registrar o modelo Nota no admin
Nota = get_nota_model()


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "curso", "valor", "data")
    search_fields = ("aluno__nome", "curso__nome")
    list_filter = ("curso", "data")
    ordering = ("-data",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("aluno", "curso", "turma")
