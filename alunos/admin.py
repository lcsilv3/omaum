"""
Admin configuration for the Alunos app.

This module contains the admin interface customizations for the Alunos app.
"""

from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Aluno,
    TipoCodigo,
    Codigo,
    RegistroHistorico,
)
from .forms import AlunoForm


class RegistroHistoricoInline(admin.TabularInline):
    """
    Permite editar o histórico diretamente na página do Aluno.
    Usa um layout de tabela para uma visualização compacta.
    """

    model = RegistroHistorico
    extra = 1  # Exibe um formulário extra para adicionar novo registro.
    autocomplete_fields = ["codigo"]

    # Campos a serem exibidos no inline
    fields = ("codigo", "data_os", "ordem_servico", "observacoes", "ativo")

    # Ordena os registros pela data mais recente
    ordering = ("-data_os",)

    verbose_name = "Registro de Histórico"
    verbose_name_plural = "Dados Iniciáticos e Histórico (Cargos, Punições, etc.)"


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    """
    Configuração simplificada do Admin para o modelo Aluno.
    """

    form = AlunoForm
    list_display = ["nome", "email", "cpf", "grau_atual", "situacao_iniciatica", "situacao", "ativo"]
    list_filter = ["ativo", "situacao", "grau_atual", "situacao_iniciatica", "sexo", "cidade", "estado"]
    search_fields = ["nome", "email", "cpf", "numero_iniciatico", "nome_iniciatico"]
    readonly_fields = ["created_at", "updated_at", "historico_display"]

    fieldsets = (
        ("Dados Pessoais", {
            "fields": (
                "nome", "email", "cpf", "data_nascimento", "hora_nascimento", "sexo", "foto"
            )
        }),
        ("Dados Iniciáticos", {
            "fields": (
                "numero_iniciatico", "nome_iniciatico", "data_iniciacao",
                "grau_atual", "situacao_iniciatica"
            )
        }),
        ("Histórico Iniciático", {
            "fields": ("historico_display",),
            "description": "Histórico de eventos, cargos e registros iniciáticos"
        }),
        ("Nacionalidade e Naturalidade", {
            "fields": ("pais_nacionalidade", "cidade_naturalidade", "nacionalidade", "naturalidade"),
            "classes": ("collapse",)
        }),
        ("Endereço", {
            "fields": ("rua", "numero_imovel", "complemento", "bairro", "cidade", "estado", "cep"),
            "classes": ("collapse",)
        }),
        ("Contatos", {
            "fields": (
                "celular_primeiro_contato", "tipo_relacionamento_primeiro_contato",
                "celular_segundo_contato", "tipo_relacionamento_segundo_contato"
            ),
            "classes": ("collapse",)
        }),
        ("Dados Médicos", {
            "fields": (
                "tipo_sanguineo", "fator_rh", "alergias", "condicoes_medicas_gerais",
                "convenio_medico", "hospital"
            ),
            "classes": ("collapse",)
        }),
        ("Outros", {
            "fields": ("estado_civil", "profissao", "situacao", "ativo"),
            "classes": ("collapse",)
        }),
        ("Metadados", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def historico_display(self, obj):
        """Mostra o histórico de forma organizada no admin."""
        if not obj.historico_iniciatico or not isinstance(obj.historico_iniciatico, list):
            return mark_safe("<em>Nenhum evento registrado</em>")
        
        html = "<table style='width: 100%; border-collapse: collapse;'>"
        html += "<tr style='background-color: #f0f0f0;'>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Data</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Tipo</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Descrição</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Observações</th>"
        html += "</tr>"
        
        for evento in obj.obter_historico_ordenado():
            data = evento.get('data', '')
            tipo = evento.get('tipo', '')
            descricao = evento.get('descricao', '')
            observacoes = evento.get('observacoes', '')
            
            html += "<tr>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{data}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{tipo}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{descricao}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{observacoes}</td>"
            html += "</tr>"
        
        html += "</table>"
        return mark_safe(html)
    
    historico_display.short_description = "Histórico de Eventos"

    def adicionar_evento_cargo(self, request, queryset):
        """Action para adicionar evento de cargo em massa."""
        from django.utils import timezone
        
        count = 0
        for aluno in queryset:
            aluno.adicionar_evento_historico(
                tipo="CARGO",
                descricao="Evento adicionado via admin",
                data=timezone.now().date(),
                observacoes="Adicionado em massa pelo administrador"
            )
            count += 1
        
        self.message_user(request, f"Evento de cargo adicionado para {count} aluno(s).")
    
    adicionar_evento_cargo.short_description = "Adicionar evento de cargo"
    
    actions = ["adicionar_evento_cargo"]

    # Fieldsets corrigidos para refletir os campos atuais do modelo Aluno
    fieldsets = [
        (
            "Informações Pessoais",
            {
                "fields": [
                    "nome",
                    "foto",
                    "data_nascimento",
                    "hora_nascimento",
                    "sexo",
                    "cpf",
                    "email",
                    "situacao",
                    "ativo",
                ]
            },
        ),
        (
            "Endereço",
            {
                "fields": [
                    "rua",
                    "numero_imovel",
                    "complemento",
                    "bairro",
                    "cidade",
                    "estado",
                    "cep",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Contatos de Emergência",
            {
                "fields": [
                    "nome_primeiro_contato",
                    "celular_primeiro_contato",
                    "tipo_relacionamento_primeiro_contato",
                    "nome_segundo_contato",
                    "celular_segundo_contato",
                    "tipo_relacionamento_segundo_contato",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Informações Médicas",
            {
                "fields": [
                    "tipo_sanguineo",
                    "fator_rh",
                    "alergias",
                    "condicoes_medicas_gerais",
                    "convenio_medico",
                    "hospital",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Outras Informações",
            {
                "fields": [
                    "nacionalidade",
                    "naturalidade",
                    "estado_civil",
                    "profissao",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Datas de Controle",
            {
                "fields": ["created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]


# --- INTERFACES ADMIN PARA CÓDIGOS E HISTÓRICO ---


@admin.register(TipoCodigo)
class TipoCodigoAdmin(admin.ModelAdmin):
    """
    Interface Admin para o modelo TipoCodigo.
    """

    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Codigo)
class CodigoAdmin(admin.ModelAdmin):
    """
    Interface Admin para o modelo Codigo.
    """

    list_display = ("nome", "get_tipo_nome", "descricao")
    search_fields = ("nome", "descricao", "tipo_codigo__nome")
    list_filter = ("tipo_codigo",)
    autocomplete_fields = ("tipo_codigo",)  # Melhora a seleção do tipo

    @admin.display(description="Tipo", ordering="tipo_codigo__nome")
    def get_tipo_nome(self, obj):
        return obj.tipo_codigo.nome


@admin.register(RegistroHistorico)
class RegistroHistoricoAdmin(admin.ModelAdmin):
    """
    Interface Admin para o modelo RegistroHistorico.
    """

    list_display = ("aluno", "codigo", "data_os", "ordem_servico", "ativo")
    search_fields = ("aluno__nome", "codigo__nome", "ordem_servico")
    list_filter = ("codigo__tipo_codigo", "data_os", "ativo")
    autocomplete_fields = ("aluno", "codigo")
