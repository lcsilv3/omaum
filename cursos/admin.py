from django.contrib import admin
from .models import Curso


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    # Adjust list_display to use fields that actually exist in the Curso model
    list_display = [
        "codigo_curso",
        "duracao",
    ]  # Remove 'nome' if it doesn't exist
    search_fields = ["codigo_curso"]
    list_filter = ["duracao"]
