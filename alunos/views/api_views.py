"""Módulo legado preservado apenas para compatibilidade temporária.

Todas as views originais foram migradas para ``alunos.api_views``. Este módulo
gera uma exceção explícita para alertar sobre importações obsoletas.
"""

from django.core.exceptions import ImproperlyConfigured


raise ImproperlyConfigured(
    "O módulo 'alunos.views.api_views' foi descontinuado. Utilize as views em "
    "'alunos.api_views'."
)
