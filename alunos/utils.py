"""
Funções utilitárias para o aplicativo alunos.
"""

from importlib import import_module
import logging

logger = logging.getLogger(__name__)


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_aluno_form():
    """Obtém o formulário AlunoForm dinamicamente."""
    alunos_forms = import_module("alunos.forms")
    return getattr(alunos_forms, "AlunoForm")


def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_matricula_model():
    """Obtém o modelo Matricula dinamicamente."""
    try:
        matriculas_module = import_module("matriculas.models")
        return getattr(matriculas_module, "Matricula")
    except (ImportError, AttributeError) as e:
        logger.error(f"Erro ao obter modelo Matricula: {e}")
        return None


def get_atribuicao_cargo_model():
    """Obtém o modelo AtribuicaoCargo dinamicamente."""
    try:
        cargos_module = import_module("cargos.models")
        return getattr(cargos_module, "AtribuicaoCargo")
    except (ImportError, AttributeError) as e:
        logger.error(f"Erro ao obter modelo AtribuicaoCargo: {e}")
        return None


def get_curso_model():
    """Obtém o modelo Curso dinamicamente."""
    try:
        cursos_module = import_module("cursos.models")
        return getattr(cursos_module, "Curso")
    except (ImportError, AttributeError) as e:
        logger.error(f"Erro ao obter modelo Curso: {e}")
        return None


def get_registro_historico_model():
    """Obtém o modelo RegistroHistorico dinamicamente."""
    try:
        models_module = import_module("alunos.models")
        return getattr(models_module, "RegistroHistorico")
    except (ImportError, AttributeError) as e:
        logger.error(f"Erro ao obter modelo RegistroHistorico: {e}")
        return None
