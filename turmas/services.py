from django.core.exceptions import ValidationError
from core.utils import get_model_dynamically
from .models import Turma


def criar_turma(dados_turma: dict) -> Turma:
    """
    Cria uma nova turma com base nos dados fornecidos em um dicionário.
    Valida a existência do curso e a unicidade do nome da turma para o curso.
    """
    Curso = get_model_dynamically("cursos", "Curso")
    curso_id = dados_turma.get("curso_id")
    if not curso_id:
        raise ValidationError("O ID do curso é obrigatório.")

    try:
        curso = Curso.objects.get(pk=curso_id)
    except Curso.DoesNotExist:
        raise ValidationError(f"O curso com ID {curso_id} não existe.")

    nome_turma = dados_turma.get("nome")
    if Turma.objects.filter(curso=curso, nome=nome_turma).exists():
        raise ValidationError(
            f"Já existe uma turma com o nome '{nome_turma}' para este curso."
        )

    nova_turma = Turma(
        curso=curso,
        nome=nome_turma,
        descricao=dados_turma.get("descricao"),
        num_livro=dados_turma.get("num_livro"),
        perc_presenca_minima=dados_turma.get("perc_presenca_minima")
        or dados_turma.get("perc_carencia"),
        data_iniciacao=dados_turma.get("data_iniciacao"),
        data_inicio_ativ=dados_turma.get("data_inicio_ativ"),
        data_prim_aula=dados_turma.get("data_prim_aula"),
        data_termino_atividades=dados_turma.get("data_termino_atividades"),
        dias_semana=dados_turma.get("dias_semana"),
        horario=dados_turma.get("horario"),
        local=dados_turma.get("local"),
        vagas=dados_turma.get("vagas", 20),
        status=dados_turma.get("status", "A"),
    )
    nova_turma.full_clean()
    nova_turma.save()
    return nova_turma


def matricular_aluno_em_turma(aluno_id: int, turma_id: int):
    """
    Matricula um aluno em uma turma, realizando todas as validações necessárias.
    """
    Aluno = get_model_dynamically("alunos", "Aluno")
    Matricula = get_model_dynamically("matriculas", "Matricula")

    try:
        aluno = Aluno.objects.get(pk=aluno_id)
        turma = Turma.objects.get(pk=turma_id)
    except (Aluno.DoesNotExist, Turma.DoesNotExist) as e:
        raise ValidationError(f"Aluno ou Turma não encontrado(a). Detalhe: {e}")

    # 1. Validar se a turma está ativa para novas matrículas
    if turma.status not in ["A"]:
        raise ValidationError(f"A turma '{turma.nome}' não está ativa para matrículas.")

    # 2. Validar se há vagas
    if turma.matriculas.count() >= turma.vagas:
        raise ValidationError("A turma não possui mais vagas disponíveis.")

    # 3. Validar se o aluno já está matriculado
    if Matricula.objects.filter(aluno=aluno, turma=turma).exists():
        raise ValidationError(f"O aluno {aluno.nome} já está matriculado nesta turma.")

    nova_matricula = Matricula.objects.create(aluno=aluno, turma=turma)
    return nova_matricula


def listar_turmas_ativas():
    """
    Retorna um QuerySet com todas as turmas que estão com status 'Ativa'.
    """
    return Turma.objects.filter(status="A").select_related("curso")
