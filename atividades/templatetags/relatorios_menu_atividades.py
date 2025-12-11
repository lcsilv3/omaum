from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def render_relatorios_menu_atividades():
    """Renderiza as entradas do menu de relatórios do app Atividades.

    Uso recomendado: `{% render_relatorios_menu_atividades %}`.
    """
    items = [
        (reverse("atividades:relatorio_atividades"), "Relatório de Atividades"),
        (
            reverse("atividades:relatorio_participacao_atividades"),
            "Participação por Atividade",
        ),
        (reverse("atividades:relatorio_carga_instrutores"), "Carga de Instrutores"),
        (reverse("atividades:relatorio_frequencia_turma"), "Carências e Frequência"),
        (
            reverse("atividades:relatorio_cronograma_curso_turmas"),
            "Cronograma Curso × Turmas",
        ),
        (reverse("atividades:relatorio_historico_aluno"), "Histórico do Aluno"),
    ]

    html = [f'<li><a class="dropdown-item" href="{url}">{label}</a></li>' for url, label in items]
    return "\n".join(html)
