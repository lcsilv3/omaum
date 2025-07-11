from django.db import transaction
from importlib import import_module
from .models import Curso


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_atividade_model():
    """Obtém o modelo Atividade."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "Atividade")


def get_nota_model():
    """Obtém o modelo Nota."""
    notas_module = import_module("notas.models")
    return getattr(notas_module, "Nota")


def get_matricula_model():
    """Obtém o modelo Matricula."""
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")


def get_pagamento_model():
    """Obtém o modelo Pagamento."""
    pagamentos_module = import_module("pagamentos.models")
    return getattr(pagamentos_module, "Pagamento")

# --- Funções de Leitura (Read) ---

def listar_cursos():
    """Retorna uma queryset com todos os cursos, ordenados por id."""
    return Curso.objects.all().order_by('id')

def obter_curso_por_id(curso_id):
    """
    Busca um curso pelo seu ID.
    Retorna o objeto Curso ou None se não for encontrado.
    """
    try:
        return Curso.objects.get(pk=curso_id)
    except Curso.DoesNotExist:
        return None

# --- Funções de Escrita (Create, Update, Delete) ---

@transaction.atomic
def criar_curso(nome, descricao):
    """
    Cria um novo curso no banco de dados.
    Retorna a instância do curso criado.
    """
    if not nome:
        raise ValueError("O nome do curso é obrigatório.")
    
    curso = Curso.objects.create(nome=nome, descricao=descricao)
    return curso

@transaction.atomic
def atualizar_curso(curso_id, nome, descricao):
    """
    Atualiza os dados de um curso existente.
    Retorna a instância do curso atualizado ou None se não for encontrado.
    """
    curso = obter_curso_por_id(curso_id)
    if curso:
        curso.nome = nome
        curso.descricao = descricao
        curso.save()
    return curso

@transaction.atomic
def excluir_curso(curso_id):
    """
    Exclui um curso, desde que não hajam dependências.
    Retorna True se a exclusão for bem-sucedida, False caso contrário.
    Levanta uma exceção ValueError se houver dependências.
    """
    curso = obter_curso_por_id(curso_id)
    if not curso:
        return False # Curso não existe

    dependencias = verificar_dependencias_curso(curso)
    # Verifica se alguma lista de dependência não está vazia
    if any(dependencias.values()):
        raise ValueError("Não é possível excluir o curso pois existem dependências associadas.")

    curso.delete()
    return True

# --- Funções de Lógica de Negócio ---

def verificar_dependencias_curso(curso):
    """
    Verifica e retorna um dicionário com todas as dependências de um curso.
    """
    # Obter modelos dinamicamente
    Turma = get_turma_model()
    Atividade = get_atividade_model()
    Nota = get_nota_model()
    Matricula = get_matricula_model()
    Pagamento = get_pagamento_model()
    
    # Alunos matriculados em turmas deste curso
    alunos_ids = Matricula.objects.filter(
        turma__curso=curso
    ).values_list('aluno_id', flat=True)
    
    dependencias = {
        'turmas': list(Turma.objects.filter(curso=curso)),
        'atividades': list(Atividade.objects.filter(curso=curso)),
        'notas': list(Nota.objects.filter(curso=curso)),
        'matriculas': list(Matricula.objects.filter(turma__curso=curso)),
        'pagamentos': list(Pagamento.objects.filter(
            aluno_id__in=alunos_ids
        )),
    }
    return {key: value for key, value in dependencias.items() if value}
