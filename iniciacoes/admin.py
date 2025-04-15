from django.contrib import admin
from .models import Iniciacao


@admin.register(Iniciacao)
class IniciacaoAdmin(admin.ModelAdmin):
    # Adjust list_display and list_filter to use fields that actually exist
    # Remove 'data' since it doesn't exist in the model
    list_display = ["aluno"]  # Keep only fields that exist
    list_filter = []  # Remove 'data' since it doesn't exist
    search_fields = ("aluno__nome", "nome_curso")
    date_hierarchy = "data_iniciacao"
    ordering = ("-data_iniciacao",)
    raw_id_fields = ("aluno",)
