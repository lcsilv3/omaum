from django.db import models
from django.contrib.auth.models import User
from alunos.models import Aluno
from turmas.models import Turma


class PresencaAcademica(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        to_field="cpf",  # Especificar que estamos referenciando o campo cpf
    )
    turma = models.ForeignKey(
        Turma, on_delete=models.CASCADE, verbose_name="Turma"
    )
    data = models.DateField(verbose_name="Data")
    presente = models.BooleanField(default=True, verbose_name="Presente")
    justificativa = models.TextField(
        blank=True, null=True, verbose_name="Justificativa"
    )
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Registrado por",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome} - {self.data}"

    class Meta:
        verbose_name = "Presença Acadêmica"
        verbose_name_plural = "Presenças Acadêmicas"
        ordering = ["-data", "aluno__nome"]
        unique_together = ["aluno", "turma", "data"]
