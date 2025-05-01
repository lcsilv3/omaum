import logging
from django.shortcuts import get_object_or_404
from importlib import import_module

# Set up logger
logger = logging.getLogger(__name__)

def get_return_url(request, default_url):
    """Obtém a URL de retorno do request ou usa o valor padrão."""
    return_url = request.GET.get("return_url", "")
    # Verificação básica de segurança
    if not return_url or not return_url.startswith("/"):
        return default_url
    return return_url

def get_form_class(form_name):
    """Importa dinamicamente uma classe de formulário para evitar importações circulares."""
    try:
        forms_module = import_module("atividades.forms")
        return getattr(forms_module, form_name)
    except (ImportError, AttributeError) as e:
        logger.error(f"Erro ao importar formulário {form_name}: {str(e)}")
        raise

def get_model_class(model_name, module_name="atividades"):
    """Importa dinamicamente uma classe de modelo para evitar importações circulares."""
    try:
        models_module = import_module(f"{module_name}.models")
        return getattr(models_module, model_name)
    except (ImportError, AttributeError) as e:
        logger.error(f"Erro ao importar modelo {model_name} do módulo {module_name}: {str(e)}")
        raise

def get_messages():
    """Importa o módulo messages do Django."""
    from django.contrib import messages
    return messages