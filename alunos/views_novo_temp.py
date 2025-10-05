"""Módulo legado mantido apenas para referência histórica.

Todas as views que existiam aqui foram migradas para:
- ``alunos.views.relatorio_views`` (relatórios HTML/exports)
- ``alunos.api_views`` (endpoints do painel de alunos)

Qualquer importação deste arquivo deve ser atualizada para os módulos oficiais
acima. Geramos uma exceção explícita para facilitar a detecção de usos
obsoletos.
"""

from django.core.exceptions import ImproperlyConfigured


raise ImproperlyConfigured(
    "O módulo 'alunos.views_novo_temp' foi descontinuado. Utilize as views "
    "em 'alunos.views.relatorio_views' ou 'alunos.api_views'."
)
