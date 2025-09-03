"""
Funções utilitárias para o aplicativo de frequências.
"""

from importlib import import_module
import logging

logger = logging.getLogger(__name__)


def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia


def get_forms():
    """Obtém os formulários relacionados a frequências."""
    frequencias_forms = import_module("frequencias.forms")
    return (
        getattr(frequencias_forms, "FrequenciaMensalForm"),
        getattr(frequencias_forms, "FiltroPainelFrequenciasForm"),
    )


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)
