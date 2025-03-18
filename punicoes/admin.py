from django.contrib import admin
from .models import Punicao

@admin.register(Punicao)
class PunicaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_punicao', 'data')
    list_filter = ('tipo_punicao', 'data')
    search_fields = ('aluno__nome', 'descricao')