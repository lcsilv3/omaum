"""
Admin para o aplicativo presencas.
Interface administrativa para gerenciamento de presenças.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import RegistroPresenca, PresencaDetalhada


@admin.register(RegistroPresenca)
class RegistroPresencaAdmin(admin.ModelAdmin):
    """Admin para modelo unificado RegistroPresenca."""

    list_display = [
        "aluno_nome",
        "turma_nome",
        "atividade_nome",
        "data",
        "status_badge",
        "convocado_badge",
        "data_registro",
    ]
    list_filter = [
        "status",
        "convocado",
        "data",
        "turma",
        "atividade",
        "data_registro",
    ]
    search_fields = [
        "aluno__nome",
        "aluno__cpf",
        "turma__nome",
        "atividade__nome",
    ]
    date_hierarchy = "data"
    raw_id_fields = ["aluno", "turma", "atividade"]
    readonly_fields = ["data_registro", "registrado_por"]
    
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("aluno", "turma", "atividade", "data")
        }),
        ("Status da Presença", {
            "fields": ("status", "convocado", "justificativa")
        }),
        ("Auditoria", {
            "fields": ("registrado_por", "data_registro"),
            "classes": ("collapse",),
        }),
    )
    
    list_per_page = 50
    
    def aluno_nome(self, obj):
        """Nome do aluno com CPF."""
        return f"{obj.aluno.nome} ({obj.aluno.cpf})"
    aluno_nome.short_description = "Aluno"
    aluno_nome.admin_order_field = "aluno__nome"
    
    def turma_nome(self, obj):
        """Nome da turma."""
        return obj.turma.nome
    turma_nome.short_description = "Turma"
    turma_nome.admin_order_field = "turma__nome"
    
    def atividade_nome(self, obj):
        """Nome da atividade."""
        return obj.atividade.nome
    atividade_nome.short_description = "Atividade"
    atividade_nome.admin_order_field = "atividade__nome"
    
    def status_badge(self, obj):
        """Badge colorido para status."""
        cores = {
            "P": "success",
            "F": "danger",
            "J": "warning",
            "V1": "info",
            "V2": "primary",
        }
        cor = cores.get(obj.status, "secondary")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            self._get_color(cor),
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = "status"
    
    def convocado_badge(self, obj):
        """Badge para convocado."""
        if obj.convocado:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                'border-radius: 3px;">✓ Convocado</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 8px; '
            'border-radius: 3px;">Voluntário</span>'
        )
    convocado_badge.short_description = "Tipo"
    convocado_badge.admin_order_field = "convocado"
    
    @staticmethod
    def _get_color(badge_type):
        """Retorna cor hexadecimal para badge."""
        colors = {
            "success": "#28a745",
            "danger": "#dc3545",
            "warning": "#ffc107",
            "info": "#17a2b8",
            "primary": "#007bff",
            "secondary": "#6c757d",
        }
        return colors.get(badge_type, "#6c757d")
    
    def get_queryset(self, request):
        """Otimiza queryset com select_related."""
        return super().get_queryset(request).select_related(
            "aluno", "turma", "atividade"
        )


@admin.register(PresencaDetalhada)
class PresencaDetalhadaAdmin(admin.ModelAdmin):
    """Admin read-only para PresencaDetalhada (view de banco)."""

    list_display = [
        "aluno_nome",
        "turma_nome",
        "atividade_nome",
        "periodo",
        "convocacoes",
        "presencas",
        "faltas",
        "percentual_calc",
    ]
    list_filter = [
        "periodo",
        "turma",
        "atividade",
    ]
    search_fields = [
        "aluno__nome",
        "aluno__cpf",
        "turma__nome",
        "atividade__nome",
    ]
    date_hierarchy = "periodo"
    
    # Read-only (managed=False)
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def aluno_nome(self, obj):
        """Nome do aluno."""
        return obj.aluno.nome
    aluno_nome.short_description = "Aluno"
    aluno_nome.admin_order_field = "aluno__nome"
    
    def turma_nome(self, obj):
        """Nome da turma."""
        return obj.turma.nome
    turma_nome.short_description = "Turma"
    turma_nome.admin_order_field = "turma__nome"
    
    def atividade_nome(self, obj):
        """Nome da atividade."""
        return obj.atividade.nome
    atividade_nome.short_description = "Atividade"
    atividade_nome.admin_order_field = "atividade__nome"
    
    def percentual_calc(self, obj):
        """Percentual calculado."""
        return f"{obj.calcular_percentual():.2f}%"
    percentual_calc.short_description = "% Presença"
    
    def get_queryset(self, request):
        """Otimiza queryset com select_related."""
        return super().get_queryset(request).select_related(
            "aluno", "turma", "atividade"
        )
