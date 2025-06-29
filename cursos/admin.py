from django.contrib import admin
from .models import Curso


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
    ]
    search_fields = ["nome"]
    list_filter = []
