from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _


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
        related_name="matriculas",  # Relacionamento reverso padrão
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

        # Check if student's course matches the class's course
        if (
            hasattr(self.aluno, "curso")
            and hasattr(self.turma, "curso")
            and self.aluno.curso != self.turma.curso
        ):
            raise ValidationError(
                {"aluno": _("O aluno deve pertencer ao mesmo curso da turma.")}
            )
