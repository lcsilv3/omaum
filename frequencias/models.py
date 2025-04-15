from django.db import models
from alunos.models import Aluno
from atividades.models import AtividadeAcademica


class Frequencia(models.Model):
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, verbose_name="Aluno"
    )
    atividade = models.ForeignKey(
        AtividadeAcademica, on_delete=models.CASCADE, verbose_name="Atividade"
    )
    data = models.DateField(verbose_name="Data")
    presente = models.BooleanField(default=True, verbose_name="Presente")
    justificativa = models.TextField(
        blank=True, null=True, verbose_name="Justificativa"
    )

    def __str__(self):
        return f"{self.aluno.nome} - {self.atividade.nome} - {self.data}"

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        ordering = ["-data"]

        unique_together = ["aluno", "atividade", "data"]
