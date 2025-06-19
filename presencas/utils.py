from importlib import import_module
from datetime import date

def get_presenca_model():
    """Obtém o modelo Presenca dinamicamente."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")

def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_model():
    """Obtém o modelo AtividadeAcademica dinamicamente."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

def get_matricula_model():
    """Obtém o modelo Matricula dinamicamente."""
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")

def gerar_meses_anos(data_inicio, data_fim):
    """Gera lista de (ano, mes) entre duas datas."""
    meses_anos = []
    ano, mes = data_inicio.year, data_inicio.month
    while (ano < data_fim.year) or (ano == data_fim.year and mes <= data_fim.month):
        meses_anos.append((ano, mes))
        if mes == 12:
            ano += 1
            mes = 1
        else:
            mes += 1
    return meses_anos