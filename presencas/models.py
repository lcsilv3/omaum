from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class Presenca(models.Model):
    """
    Modelo para registro de presença de alunos em atividades acadêmicas ou ritualísticas.
    Armazena informações sobre presença, ausência e justificativas.
    """
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        related_name="presencas_detalhadas"
    )
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        verbose_name="Atividade",
        null=True,
        blank=True,
        related_name="presencas_detalhadas"
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma",
        null=True,
        blank=True,
        related_name="presencas_detalhadas"
    )
    data = models.DateField(verbose_name="Data")
    presente = models.BooleanField(default=True, verbose_name="Presente")
    justificativa = models.TextField(
        blank=True,
        null=True,
        verbose_name="Justificativa"
    )
    registrado_por = models.CharField(
        max_length=100,
        default="Sistema",
        verbose_name="Registrado por"
    )
    data_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de registro"
    )

    class Meta:
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        ordering = ["-data", "aluno__nome"]
        unique_together = ["aluno", "turma", "data"]

    def __str__(self):
        """Retorna uma representação em string do objeto."""
        status = "Presente" if self.presente else "Ausente"
        return f"{self.aluno.nome} - {self.data} - {status}"

    def clean(self):
        """
        Valida os dados do modelo antes de salvar.
        - Data não pode ser futura.
        - Justificativa obrigatória se ausente.
        """
        super().clean()
        if self.data and self.data > timezone.now().date():
            logger.warning(f"Data futura informada para presença: {self.data}")
            raise ValidationError({"data": "A data não pode ser futura."})
        if not self.presente and not self.justificativa:
            raise ValidationError({"justificativa": "É necessário fornecer uma justificativa para a ausência."})

class TotalAtividadeMes(models.Model):
    """
    Modelo para totalização de atividades por mês em uma turma.
    """
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        related_name="totais_atividade_mes"
    )
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE)
    ano = models.IntegerField()
    mes = models.IntegerField()
    qtd_ativ_mes = models.PositiveIntegerField(default=0)
    registrado_por = models.CharField(max_length=100, default="Sistema")
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["atividade", "turma", "ano", "mes"]
        verbose_name = "Total de Atividade no Mês"
        verbose_name_plural = "Totais de Atividades no Mês"

    def __str__(self):
        return f"{self.atividade} - {self.turma} - {self.mes}/{self.ano}: {self.qtd_ativ_mes}"

class ObservacaoPresenca(models.Model):
    """
    Observações relacionadas à presença de alunos em atividades.
    """
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Aluno",
        related_name="observacoes_presenca_presencas"
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="observacoes_presenca_presencas"
    )
    data = models.DateField(verbose_name="Data")
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Atividade",
        related_name="observacoes_presenca"
    )
    texto = models.TextField(verbose_name="Observação", blank=True, null=True)
    registrado_por = models.CharField(
        max_length=100, 
        default="Sistema", 
        verbose_name="Registrado por"
    )
    data_registro = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Data de registro"
    )

    class Meta:
        verbose_name = "Observação de Presença"
        verbose_name_plural = "Observações de Presença"
        ordering = ["-data"]

    def __str__(self):
        atividade_str = str(self.atividade) if self.atividade else "Sem atividade"
        texto_trunc = self.texto[:30] if self.texto else "Sem observação"
        return f"{self.data} - {atividade_str} - {texto_trunc}"


# Aliases para compatibilidade após refatoramento
PresencaAcademica = Presenca
PresencaRitualistica = Presenca
