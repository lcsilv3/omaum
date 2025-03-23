from django.contrib import admin
from .models import ConfiguracaoSistema, LogAtividade

@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('nome_sistema', 'versao', 'data_atualizacao', 'manutencao_ativa')
    list_editable = ('manutencao_ativa',)
    readonly_fields = ('data_atualizacao',)

@admin.register(LogAtividade)
class LogAtividadeAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'acao', 'usuario', 'data')
    list_filter = ('tipo', 'data', 'usuario')
    search_fields = ('acao', 'usuario', 'detalhes')
    readonly_fields = ('data',)
