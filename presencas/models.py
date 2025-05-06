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
    
    Este modelo armazena informações sobre a presença ou ausência de um aluno
    em uma determinada atividade, incluindo a data, status e justificativa
    em caso de ausência.
    
    Attributes:
        aluno (ForeignKey): Referência ao aluno cuja presença está sendo registrada.
        atividade (ForeignKey): Referência à atividade em que a presença está sendo registrada.
        data (DateField): Data do registro de presença.
        presente (BooleanField): Indica se o aluno estava presente (True) ou ausente (False).
        justificativa (TextField): Justificativa para a ausência, se aplicável.
        registrado_por (ForeignKey): Usuário que registrou a presença.
        data_registro (DateTimeField): Data e hora em que o registro foi criado.
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
