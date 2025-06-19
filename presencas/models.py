from django.db import models
from django.utils import timezone
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

def get_atividade_model():
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")

class Presenca(models.Model):
    """
    Modelo para registro de presença de alunos em atividades.

    Armazena informações sobre presença, ausência e justificativas de alunos em atividades acadêmicas ou ritualísticas.
    """
    
    aluno = models.ForeignKey(
        get_aluno_model(),
        on_delete=models.CASCADE,
        verbose_name="Aluno"
    )
    
    atividade = models.ForeignKey(
        get_atividade_model(),
        on_delete=models.CASCADE,
        verbose_name="Atividade",
        null=True,
        blank=True
    )
    
    turma = models.ForeignKey(
        get_turma_model(), 
        on_delete=models.CASCADE,
        verbose_name="Turma",
        null=True,
        blank=True
    )
    
    data = models.DateField(verbose_name="Data")
    
    presente = models.BooleanField(default=True, verbose_name="Presente")
    
    justificativa = models.TextField(blank=True, null=True, verbose_name="Justificativa")
    
    registrado_por = models.CharField(max_length=100, default="Sistema", verbose_name="Registrado por")
    
    data_registro = models.DateTimeField(default=timezone.now, verbose_name="Data de registro")
    
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
        
        Raises:
            ValidationError: Se a data for futura ou se a justificativa estiver
                            ausente quando o aluno estiver marcado como ausente.
        """
        super().clean()
        
        # Verificar se a data não é futura
        if self.data and self.data > timezone.now().date():
            raise ValidationError({"data": "A data não pode ser futura."})
        
        # Verificar se há justificativa quando o aluno está ausente
        if not self.presente and not self.justificativa:
            raise ValidationError(
                {"justificativa": "É necessário fornecer uma justificativa para a ausência."}
            )

class TotalAtividadeMes(models.Model):
    atividade = models.ForeignKey(get_atividade_model(), on_delete=models.CASCADE)
    turma = models.ForeignKey(get_turma_model(), on_delete=models.CASCADE)
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
    atividade_academica = models.ForeignKey(
        'atividades.AtividadeAcademica',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Atividade Acadêmica",
        related_name="observacoes_presenca_presencas"
    )
    atividade_ritualistica = models.ForeignKey(
        'atividades.AtividadeRitualistica',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Atividade Ritualística",
        related_name="observacoes_presenca_presencas"
    )
    texto = models.TextField(verbose_name="Observação", blank=True, null=True)
    registrado_por = models.CharField(max_length=100, default="Sistema", verbose_name="Registrado por")
    data_registro = models.DateTimeField(default=timezone.now, verbose_name="Data de registro")

    class Meta:
        verbose_name = "Observação de Presença"
        verbose_name_plural = "Observações de Presença"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.data} - {self.atividade_academica or self.atividade_ritualistica} - {self.texto[:30]}"
