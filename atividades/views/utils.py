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


def get_form_class(form_name, app_name="atividades"):
    """Obtém uma classe de formulário dinamicamente."""
    try:
        forms_module = import_module(f"{app_name}.forms")
        return getattr(forms_module, form_name)
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter formulário %s: %s", form_name, str(e))
        raise


def get_model_class(model_name, app_name="atividades"):
    """Obtém uma classe de modelo dinamicamente."""
    try:
        models_module = import_module(f"{app_name}.models")
        return getattr(models_module, model_name)
    except (ImportError, AttributeError) as e:
        logger.error("Erro ao obter modelo %s: %s", model_name, str(e))
        raise
def get_messages():
    """Importa o módulo messages do Django."""
    from django.contrib import messages
    return messages

def get_models():
    """Obtém os modelos AtividadeAcademica e AtividadeRitualistica."""
    atividades_module = import_module("atividades.models")
    AtividadeAcademica = getattr(atividades_module, "AtividadeAcademica")
    AtividadeRitualistica = getattr(atividades_module, "AtividadeRitualistica")
    return AtividadeAcademica, AtividadeRitualistica


def get_forms():
    """Obtém os formulários AtividadeAcademicaForm e AtividadeRitualisticaForm."""
    atividades_forms = import_module("atividades.forms")
    AtividadeAcademicaForm = getattr(atividades_forms, "AtividadeAcademicaForm")
    AtividadeRitualisticaForm = getattr(atividades_forms, "AtividadeRitualisticaForm")
    return AtividadeAcademicaForm, AtividadeRitualisticaForm


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

from importlib import import_module

def get_cursos():
    Curso = import_module("cursos.models").Curso
    return Curso.objects.all()

def get_turmas(curso_id=None):
    Turma = import_module("turmas.models").Turma
    if curso_id:
        return Turma.objects.filter(curso_id=curso_id)
    return Turma.objects.all()

def get_atividades_academicas(curso_id=None, turma_id=None, query=None):
    from ..models import AtividadeAcademica
    atividades = AtividadeAcademica.objects.all()
    if curso_id:
        atividades = atividades.filter(turma__curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    if query:
        from django.db.models import Q
        atividades = atividades.filter(
            Q(nome__icontains=query) | Q(descricao__icontains=query)
        )
    return atividades.select_related("turma__curso").distinct()