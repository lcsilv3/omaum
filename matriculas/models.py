from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from importlib import import_module


def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


class Matricula(models.Model):
    OPCOES_STATUS = [
        ("A", "Ativa"),
        ("C", "Cancelada"),
        ("F", "Finalizada"),
    ]

    aluno = models.ForeignKey(
        "alunos.Aluno", on_delete=models.CASCADE, verbose_name="Aluno"
    )
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="matriculas",
    )
    data_matricula = models.DateField(verbose_name="Data da Matrícula")
    ativa = models.BooleanField(default=True, verbose_name="Matrícula Ativa")
    status = models.CharField(
        "Status", max_length=1, choices=OPCOES_STATUS, default="A"
    )

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        ordering = ["-data_matricula"]
        unique_together = ["aluno", "turma"]

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome}"

    def clean(self):
        # Check if class is active
        if self.turma.status != "A":
            raise ValidationError(
                {
                    "turma": _(
                        "Não é possível matricular em uma turma inativa ou concluída."
                    )
                }
            )

        # Check if there are available spots
        if (
            not self.pk and self.turma.vagas_disponiveis <= 0
        ):  # Only for new enrollments
            raise ValidationError({"turma": _("Não há vagas disponíveis nesta turma.")})
