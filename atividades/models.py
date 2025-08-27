from django.db import models
from django.utils import timezone
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


class Presenca(models.Model):
    """
    Modelo para presenças em atividades.
    """

    aluno = models.ForeignKey(
        "alunos.Aluno", on_delete=models.CASCADE, verbose_name="Aluno"
    )
    turma = models.ForeignKey(
        "turmas.Turma", on_delete=models.CASCADE, verbose_name="Turma"
    )
    atividade = models.ForeignKey(
        "Atividade", on_delete=models.CASCADE, verbose_name="Atividade"
    )
    data = models.DateField(verbose_name="Data")
    presente = models.BooleanField(default=True, verbose_name="Presente")
    registrado_por = models.CharField(
        max_length=100, default="Sistema", verbose_name="Registrado por"
    )
    data_registro = models.DateTimeField(
        default=timezone.now, verbose_name="Data de registro"
    )

    class Meta:
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        ordering = ["-data", "aluno__nome"]
        unique_together = ["aluno", "turma", "atividade", "data"]

    def __str__(self):
        return f"{self.aluno} - {self.atividade} - {self.data}"


class Atividade(models.Model):
    """
    Modelo para atividades como aulas, palestras, workshops, etc.
    """

    TIPO_CHOICES = [
        ("AULA", "Aula"),
        ("PALESTRA", "Palestra"),
        ("WORKSHOP", "Workshop"),
        ("SEMINARIO", "Seminário"),
        ("OUTRO", "Outro"),
    ]

    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("CONFIRMADA", "Confirmada"),
        ("REALIZADA", "Realizada"),
        ("CANCELADA", "Cancelada"),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    tipo_atividade = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default="AULA"
    )
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField(blank=True, null=True)
    local = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDENTE")
    ativo = models.BooleanField(default=True, verbose_name="Ativa")
    convocacao = models.BooleanField(default=False, verbose_name="Convocação")

    # Relacionamentos
    curso = models.ForeignKey(
        "cursos.Curso",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="atividades",
    )
    turmas = models.ManyToManyField(
        "turmas.Turma", blank=True, related_name="atividades"
    )

    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"
        ordering = ["-data_inicio", "hora_inicio"]


# Alias para compatibilidade após refatoramento
AtividadeAcademica = Atividade
