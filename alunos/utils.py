"""Funções utilitárias para resolução dinâmica de modelos e formulários.

Centraliza importação tardia para evitar dependências cíclicas e permitir
transição de modelos entre apps (ex: extração de dados iniciáticos).
"""

from importlib import import_module
import logging

logger = logging.getLogger(__name__)


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_aluno_form():
    alunos_forms = import_module("alunos.forms")
    return getattr(alunos_forms, "AlunoForm")


def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_matricula_model():
    try:
        matriculas_module = import_module("matriculas.models")
        return getattr(matriculas_module, "Matricula")
    except (ImportError, AttributeError) as exc:
        logger.debug("Matricula model não disponível: %s", exc)
        return None


def get_atribuicao_cargo_model():
    try:
        cargos_module = import_module("cargos.models")
        return getattr(cargos_module, "AtribuicaoCargo")
    except (ImportError, AttributeError) as exc:
        logger.debug("AtribuicaoCargo model não disponível: %s", exc)
        return None


def get_curso_model():
    try:
        cursos_module = import_module("cursos.models")
        return getattr(cursos_module, "Curso")
    except (ImportError, AttributeError) as exc:
        logger.debug("Curso model não disponível: %s", exc)
        return None


def get_registro_historico_model():
    try:
        models_module = import_module("alunos.models")
        return getattr(models_module, "RegistroHistorico")
    except (ImportError, AttributeError) as exc:
        logger.debug("RegistroHistorico model não disponível: %s", exc)
        return None


def get_tipo_codigo_model():
    # Modelos consolidados: retorno direto; manter função para compatibilidade.
    try:  # pragma: no cover - deve sempre existir
        from alunos.models import TipoCodigo  # type: ignore

        return TipoCodigo
    except Exception:  # noqa: BLE001
        return None


def get_codigo_model():
    # Consolidação: sempre em 'alunos'.
    try:  # pragma: no cover
        from alunos.models import Codigo  # type: ignore

        return Codigo
    except Exception:  # noqa: BLE001
        return None


def clean_cpf(cpf):
    """Remove a máscara do CPF, retornando apenas os dígitos."""
    return "".join(filter(str.isdigit, cpf))


def mask_cpf(cpf):
    """Aplica a máscara a um CPF de 11 dígitos."""
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf
