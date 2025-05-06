from django.contrib import admin
from .models import Presenca

class PresencaAdmin(admin.ModelAdmin):
    # Atualizando list_display para incluir o campo turma
    list_display = ('aluno', 'turma', 'data', 'presente', 'registrado_por')
    
    # Atualizando list_filter para incluir o campo turma
    list_filter = ('presente', 'turma', 'data')
    search_fields = ('aluno__nome', 'aluno__cpf', 'turma__nome')
    date_hierarchy = 'data'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('aluno', 'turma', 'atividade')

admin.site.register(Presenca, PresencaAdmin)
