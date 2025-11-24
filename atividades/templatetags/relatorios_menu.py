from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def render_relatorios_menu():
    """Renderiza as entradas do menu de relatórios do app Atividades.

    Usado em `base.html` como `{% render_relatorios_menu %}`.
    """
    items = [
        (
            reverse("atividades:relatorio_atividades"),
            "Relatório de Atividades",
        ),
        (
            reverse("atividades:relatorio_participacao_atividades"),
            "Participação por Atividade",
        ),
        (
            reverse("atividades:relatorio_carga_instrutores"),
            "Carga de Instrutores",
        ),
        (
            reverse("atividades:relatorio_frequencia_turma"),
            "Carências e Frequência",
        ),
        (
            reverse("atividades:relatorio_cronograma_curso_turmas"),
            "Cronograma Curso × Turmas",
        ),
        (
            reverse("atividades:relatorio_historico_aluno"),
            "Histórico do Aluno",
        ),
    ]

    html = []
    for url, label in items:
        html.append(f'<li><a class="dropdown-item" href="{url}">{label}</a></li>')

    return "\n".join(html)
