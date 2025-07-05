from django.db import transaction
from .models import Curso
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from notas.models import Nota
from matriculas.models import Matricula
from pagamentos.models import Pagamento

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
    # Alunos matriculados em turmas deste curso
    alunos_ids = Matricula.objects.filter(turma__curso=curso).values_list('aluno_id', flat=True)
    dependencias = {
        'turmas': list(Turma.objects.filter(curso=curso)),
        'atividades_academicas': list(AtividadeAcademica.objects.filter(curso=curso)),
        'notas': list(Nota.objects.filter(curso=curso)),
        'matriculas': list(Matricula.objects.filter(turma__curso=curso)),
        'pagamentos': list(Pagamento.objects.filter(aluno_id__in=alunos_ids)),
    }
    return {key: value for key, value in dependencias.items() if value}
