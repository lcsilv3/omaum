from django.contrib import admin
from .models import AtividadeAcademica, AtividadeRitualistica

class AtividadeAcademicaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'mostrar_data_inicio', 'data_fim', 'responsavel', 'listar_turmas', 'status']
    list_filter = ['status', 'tipo_atividade']
    search_fields = ['nome', 'responsavel']
    date_hierarchy = 'data_inicio'
    
    def listar_turmas(self, obj):
        """Retorna uma string com os nomes das turmas associadas à atividade."""
        if not obj.turmas.exists():
            return "Nenhuma turma"
        return ", ".join([turma.nome for turma in obj.turmas.all()])
    
    def mostrar_data_inicio(self, obj):
        """Formata a data de início para exibição."""
        if obj.data_inicio:
            return obj.data_inicio.strftime('%d/%m/%Y')
        return "-"
    
    listar_turmas.short_description = "Turmas"
    mostrar_data_inicio.short_description = "Data de Início"

class AtividadeRitualisticaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data', 'hora_inicio', 'hora_fim', 'local', 'turma']
    list_filter = ['turma', 'data']
    search_fields = ['nome', 'local']
    date_hierarchy = 'data'

admin.site.register(AtividadeAcademica, AtividadeAcademicaAdmin)
admin.site.register(AtividadeRitualistica, AtividadeRitualisticaAdmin)
