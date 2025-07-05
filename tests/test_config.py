import pytest
from django.conf import settings

def test_debug_setting():
    """Verifica se o DEBUG está desativado em ambiente de teste."""
    assert settings.DEBUG is False, "DEBUG deve estar desativado em ambiente de teste"

def test_installed_apps():
    """Verifica se todas as aplicações necessárias estão instaladas."""
    required_apps = [
        'alunos',
        'atividades',
        'core',
        'cursos',
        'frequencias',
        'matriculas',
        'notas',
        'pagamentos',
        'presencas',
        'turmas',
    ]
    
    for app in required_apps:
        assert app in settings.INSTALLED_APPS, (
            f"A aplicação {app} não está instalada"
        )