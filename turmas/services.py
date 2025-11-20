# c:/projetos/omaum/turmas/services.py
from __future__ import annotations

import logging
from datetime import time

from django.core.exceptions import ValidationError
from django.db import transaction

from core.utils import get_model_dynamically

logger = logging.getLogger(__name__)


def criar_turma(dados_turma: dict):
    """
    Cria uma nova turma com base nos dados fornecidos em um dicionário.
    Valida a existência do curso e a unicidade do nome da turma para o curso.
    """
    Turma = get_model_dynamically("turmas", "Turma")
    Curso = get_model_dynamically("cursos", "Curso")
    curso_id = dados_turma.get("curso_id")
    if not curso_id:
        raise ValidationError("O ID do curso é obrigatório.")

    try:
        curso = Curso.objects.get(pk=curso_id)
    except Curso.DoesNotExist as exc:
        raise ValidationError(f"O curso com ID {curso_id} não existe.") from exc

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
    Turma = get_model_dynamically("turmas", "Turma")
    Aluno = get_model_dynamically("alunos", "Aluno")
    Matricula = get_model_dynamically("matriculas", "Matricula")

    try:
        aluno = Aluno.objects.get(pk=aluno_id)
        turma = Turma.objects.get(pk=turma_id)
    except (Aluno.DoesNotExist, Turma.DoesNotExist) as exc:
        raise ValidationError(
            f"Aluno ou Turma não encontrado(a). Detalhe: {exc}"
        ) from exc

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
    Turma = get_model_dynamically("turmas", "Turma")
    return Turma.objects.filter(status="A").select_related("curso")


def validar_turma_para_registro(turma):
    """Impede operações quando a turma foi encerrada."""
    if getattr(turma, "esta_encerrada", False):
        raise ValidationError(
            "Esta turma está encerrada e não aceita novos lançamentos."
        )


def criar_atividades_basicas(turma):
    """Gera atividades padrão 'Aula' e 'Plenilúnio' para a turma informada."""
    try:
        Atividade = get_model_dynamically("atividades", "Atividade")
    except (ImportError, AttributeError):
        logger.warning(
            "Modulo atividades indisponível, atividades padrão não foram criadas."
        )
        return

    existentes = Atividade.objects.filter(
        turmas=turma, nome__in=["Aula", "Plenilúnio"]
    ).values_list("nome", flat=True)
    faltantes = [
        {
            "nome": "Aula",
            "tipo": "AULA",
            "hora": time(19, 0),
        },
        {
            "nome": "Plenilúnio",
            "tipo": "PALESTRA",
            "hora": time(20, 0),
        },
    ]

    data_padrao = turma.data_inicio
    for definicao in faltantes:
        if definicao["nome"] in existentes:
            continue
        atividade = Atividade.objects.create(
            nome=definicao["nome"],
            descricao="Atividade gerada automaticamente ao criar a turma.",
            tipo_atividade=definicao["tipo"],
            data_inicio=data_padrao,
            data_fim=data_padrao,
            hora_inicio=definicao["hora"],
            hora_fim=definicao["hora"],
            curso=turma.curso,
            status="PENDENTE",
        )
        atividade.turmas.add(turma)
        logger.info(
            "Atividade padrão %s criada para a turma %s", atividade.nome, turma.id
        )


def encerrar_turma(turma, usuario):
    """Registra auditoria do encerramento."""
    turma.registrar_encerramento(usuario)
    turma.save(update_fields=["encerrada_em", "encerrada_por"])
    logger.info(
        "Turma %s encerrada por %s em %s",
        turma.id,
        getattr(usuario, "username", usuario),
        turma.encerrada_em,
    )


def transferir_matriculas_em_lote(turma_origem, turma_destino, usuario):
    """Transfere todos os alunos ativos de uma turma encerrada."""
    if turma_origem == turma_destino:
        raise ValidationError("Selecione uma turma de destino diferente.")

    validar_turma_para_registro(turma_destino)

    Matricula = get_model_dynamically("matriculas", "Matricula")

    with transaction.atomic():
        matriculas = Matricula.objects.select_for_update().filter(
            turma=turma_origem, status="A"
        )
        transferidos = 0
        for matricula in matriculas:
            matricula.status = "T"
            matricula.ativa = False
            matricula.save(update_fields=["status", "ativa"])
            Matricula.objects.create(
                aluno=matricula.aluno,
                turma=turma_destino,
                data_matricula=turma_destino.data_inicio,
                ativa=True,
                status="A",
            )
            transferidos += 1

    logger.info(
        "Transferência em lote concluída da turma %s para %s por %s. Total: %s",
        turma_origem.id,
        turma_destino.id,
        getattr(usuario, "username", usuario),
        transferidos,
    )
    return transferidos
