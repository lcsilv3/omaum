from datetime import date
from presencas.models import Presenca
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from matriculas.models import Matricula


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