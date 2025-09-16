"""Modelos para o aplicativo presencas."""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class RegistroPresenca(models.Model):
    """Modelo unificado para registro de presença."""

    # Relacionamentos
    aluno = models.ForeignKey(
        "alunos.Aluno", on_delete=models.CASCADE, related_name="registros_de_presenca"
    )
    turma = models.ForeignKey(
        "turmas.Turma", on_delete=models.CASCADE, related_name="registros_de_presenca"
    )
    atividade = models.ForeignKey(
        "atividades.Atividade",
        on_delete=models.CASCADE,
        related_name="registros_de_presenca",
    )
    data = models.DateField()

    # Status da presença
    STATUS_CHOICES = [
        ("P", "Presente"),
        ("F", "Falta"),
        ("J", "Falta Justificada"),
        ("V1", "Voluntário Extra"),
        ("V2", "Voluntário Simples"),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="P")

    # Informações adicionais
    justificativa = models.TextField(blank=True, null=True)
    convocado = models.BooleanField(default=True)

    # Campos de controle
    registrado_por = models.CharField(max_length=100, default="Sistema")
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["aluno", "turma", "atividade", "data"]
        verbose_name = "Registro de Presença"
        verbose_name_plural = "Registros de Presença"
        ordering = ["-data", "aluno__nome"]

    def __str__(self):
        return f"{self.aluno.nome} - {self.data} - {self.get_status_display()}"
