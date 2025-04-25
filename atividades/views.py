import importlib
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse

# Set up logger
logger = logging.getLogger(__name__)

print(
    "ARQUIVO VIEWS.PY CARREGADO:",
    importlib.import_module("django.conf").settings.BASE_DIR,
)


def get_return_url(request, default_url):
    """Obtém a URL de retorno do request ou usa o valor padrão."""
    return_url = request.GET.get("return_url", "")
    # Verificação básica de segurança
    if not return_url or not return_url.startswith("/"):
        return default_url
    return return_url


def get_form_class(form_name):
    """Importa dinamicamente uma classe de formulário para evitar importações circulares."""
    forms_module = importlib.import_module("atividades.forms")
    return getattr(forms_module, form_name)


def get_model_class(model_name, module_name="atividades.models"):
    """Importa dinamicamente uma classe de modelo para evitar importações circulares."""
    models_module = importlib.import_module(module_name)
    return getattr(models_module, model_name)
