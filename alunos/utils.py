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

def verificar_elegibilidade_instrutor(aluno):
    """
    Verifica se um aluno é elegível para ser instrutor.
    
    Args:
        aluno: Objeto Aluno a ser verificado
        
    Returns:
        Tupla (elegivel, motivo) onde elegivel é um booleano e motivo é uma string
    """
    # Verificar se o aluno está ativo
    if aluno.situacao != 'ATIVO':
        return False, "Aluno não está ativo"
    
    # Verificar se o aluno tem número iniciático
    if not aluno.numero_iniciatico:
        return False, "Aluno não possui número iniciático"
    
    # Verificar se o aluno tem email (para contato)
    if not aluno.email:
        return False, "Aluno não possui email cadastrado"
    
    # Verificar se o aluno tem telefone (para contato)
    if not aluno.celular_primeiro_contato:
        return False, "Aluno não possui telefone cadastrado"
    
    # Se passou por todas as verificações, é elegível
    return True, "Elegível para ser instrutor"