"""
Admin configuration for the Alunos app.

This module contains the admin interface customizations for the Alunos app.
"""

from django.contrib import admin
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
    Configuração do Admin para o modelo Aluno, com o histórico embutido.
    """

    form = AlunoForm
    inlines = [RegistroHistoricoInline]
    list_display = ["nome", "email", "cpf", "situacao", "ativo"]
    list_filter = ["ativo", "situacao", "sexo", "cidade", "estado"]
    search_fields = ["nome", "email", "cpf"]
    readonly_fields = ["created_at", "updated_at"]

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
