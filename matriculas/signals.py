"""
Signals para o módulo de matrículas.

Este módulo contém os signals que são disparados quando ocorrem
eventos relacionados a matrículas, como criação, atualização ou exclusão.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Matricula
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Matricula)
def atualizar_grau_atual_aluno(sender, instance, created, **kwargs):
    """
    Atualiza o campo grau_atual do aluno quando uma matrícula é criada ou ativada.

    Args:
        sender: O modelo que enviou o signal (Matricula)
        instance: A instância da matrícula que foi salva
        created: Boolean indicando se é uma nova matrícula
        **kwargs: Argumentos adicionais
    """
    # Só atualiza se a matrícula está ativa
    if instance.ativa and instance.status == "A":
        try:
            aluno = instance.aluno
            turma = instance.turma

            # Verifica se a turma tem curso vinculado
            if hasattr(turma, "curso") and turma.curso:
                # Atualiza o grau_atual com o nome do curso
                aluno.grau_atual = turma.curso.nome
                aluno.save(update_fields=["grau_atual"])

                logger.info(
                    f"Grau atual do aluno {aluno.nome} atualizado para: {turma.curso.nome}"
                )
            else:
                logger.warning(
                    f"Turma {turma.nome} não possui curso vinculado. "
                    f"Grau atual do aluno {aluno.nome} não foi atualizado."
                )
        except Exception as e:
            logger.error(
                f"Erro ao atualizar grau atual do aluno {instance.aluno.nome}: {str(e)}"
            )


@receiver(post_delete, sender=Matricula)
def atualizar_grau_apos_exclusao(sender, instance, **kwargs):
    """
    Atualiza o grau_atual do aluno para o curso da matrícula ativa mais recente
    após a exclusão de uma matrícula.

    Args:
        sender: O modelo que enviou o signal (Matricula)
        instance: A instância da matrícula que foi excluída
        **kwargs: Argumentos adicionais
    """
    try:
        aluno = instance.aluno

        # Busca a matrícula ativa mais recente do aluno
        matricula_mais_recente = (
            Matricula.objects.filter(aluno=aluno, ativa=True, status="A")
            .order_by("-data_matricula")
            .first()
        )

        if matricula_mais_recente and matricula_mais_recente.turma.curso:
            # Atualiza para o curso da matrícula mais recente
            aluno.grau_atual = matricula_mais_recente.turma.curso.nome
            aluno.save(update_fields=["grau_atual"])

            logger.info(
                f"Grau atual do aluno {aluno.nome} atualizado para: "
                f"{matricula_mais_recente.turma.curso.nome} após exclusão de matrícula"
            )
        else:
            # Se não há mais matrículas ativas, limpa o campo
            aluno.grau_atual = ""
            aluno.save(update_fields=["grau_atual"])

            logger.info(
                f"Grau atual do aluno {aluno.nome} limpo (sem matrículas ativas)"
            )
    except Exception as e:
        logger.error(f"Erro ao atualizar grau após exclusão de matrícula: {str(e)}")
