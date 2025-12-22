"""Modelos para o aplicativo presencas."""

from django.db import models
from django.utils import timezone


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

    # Propriedades de compatibilidade com código legado que usa booleano "presente"
    @property
    def presente(self) -> bool:
        """Retorna True se status é 'P' (Presente), False caso contrário."""
        return self.status == "P"

    @presente.setter
    def presente(self, value: bool):
        """Define status para 'P' se True, 'F' se False."""
        self.status = "P" if value else "F"


class PresencaDetalhada(models.Model):
    """Representa a visão agregada utilizada pelos relatórios legados."""

    aluno = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.DO_NOTHING,
        db_column="aluno_id",
        related_name="+",
    )
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.DO_NOTHING,
        db_column="turma_id",
        related_name="+",
    )
    atividade = models.ForeignKey(
        "atividades.Atividade",
        on_delete=models.DO_NOTHING,
        db_column="atividade_id",
        related_name="+",
    )
    periodo = models.DateField()
    convocacoes = models.PositiveIntegerField(default=0)
    presencas = models.PositiveIntegerField(default=0)
    faltas = models.PositiveIntegerField(default=0)
    voluntario_extra = models.PositiveIntegerField(default=0)
    voluntario_simples = models.PositiveIntegerField(default=0)
    carencias = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
        db_table = "presencas_presencadetalhada"
        verbose_name = "Presença Detalhada (legado)"
        verbose_name_plural = "Presenças Detalhadas (legado)"
        ordering = ["-periodo", "aluno__nome"]

    def __str__(self):
        return f"{self.aluno} - {self.periodo:%m/%Y}"

    # Métodos utilitários mantêm compatibilidade com scripts e serviços legados
    def calcular_percentual(self) -> float:
        """Retorna o percentual de presença considerando convocações."""
        total_convocacoes = self.convocacoes or 0
        total_presencas = self.presencas or 0
        if total_convocacoes <= 0:
            return 0.0
        return round((total_presencas / total_convocacoes) * 100, 2)

    def calcular_voluntarios(self) -> int:
        """Soma os voluntariados extra e simples."""
        return (self.voluntario_extra or 0) + (self.voluntario_simples or 0)

    def calcular_carencias(self) -> int:
        """Retorna a quantidade de carências registradas."""
        return self.carencias or 0


class ConfiguracaoPresenca(models.Model):
    """Placeholder legado para compatibilidade com cálculos estatísticos."""

    class Meta:
        managed = False
        verbose_name = "Configuração de Presença (legado)"
        verbose_name_plural = "Configurações de Presença (legado)"
