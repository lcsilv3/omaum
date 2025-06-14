from django.db import models
from django.utils import timezone
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

class PresencaBase(models.Model):
    """
    Modelo abstrato para presenças (campos comuns).
    """
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        verbose_name="Aluno"
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma"
    )
    data = models.DateField(verbose_name="Data")
    presente = models.BooleanField(default=True, verbose_name="Presente")
    registrado_por = models.CharField(max_length=100, default="Sistema", verbose_name="Registrado por")
    data_registro = models.DateTimeField(default=timezone.now, verbose_name="Data de registro")

    class Meta:
        abstract = True
        ordering = ["-data", "aluno__nome"]

class PresencaAcademica(PresencaBase):
    """
    Presença em atividades acadêmicas.
    """
    atividade = models.ForeignKey(
        'AtividadeAcademica',
        on_delete=models.CASCADE,
        verbose_name="Atividade Acadêmica"
    )

    class Meta(PresencaBase.Meta):
        verbose_name = "Presença Acadêmica"
        verbose_name_plural = "Presenças Acadêmicas"
        unique_together = ["aluno", "turma", "atividade", "data"]

class PresencaRitualistica(PresencaBase):
    """
    Presença em atividades ritualísticas.
    """
    atividade = models.ForeignKey(
        'AtividadeRitualistica',
        on_delete=models.CASCADE,
        verbose_name="Atividade Ritualística"
    )

    class Meta(PresencaBase.Meta):
        verbose_name = "Presença Ritualística"
        verbose_name_plural = "Presenças Ritualísticas"
        unique_together = ["aluno", "turma", "atividade", "data"]

class ObservacaoPresenca(models.Model):
    """
    Observação por dia/atividade/aluno.
    """
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        verbose_name="Aluno"
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma"
    )
    data = models.DateField(verbose_name="Data")
    atividade_academica = models.ForeignKey(
        'AtividadeAcademica',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Atividade Acadêmica"
    )
    atividade_ritualistica = models.ForeignKey(
        'AtividadeRitualistica',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Atividade Ritualística"
    )
    texto = models.TextField(verbose_name="Observação", blank=True, null=True)
    registrado_por = models.CharField(max_length=100, default="Sistema", verbose_name="Registrado por")
    data_registro = models.DateTimeField(default=timezone.now, verbose_name="Data de registro")

    class Meta:
        verbose_name = "Observação de Presença"
        verbose_name_plural = "Observações de Presença"
        ordering = ["-data", "aluno__nome"]

class AtividadeBase(models.Model):
    TIPO_CHOICES = (
        ('academica', 'Acadêmica'),
        ('ritualistica', 'Ritualística'),
    )
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='academica')  # <-- Adicione default aqui
    # ...outros campos comuns...

    class Meta:
        abstract = True

class AtividadeAcademica(AtividadeBase):
    """
    Modelo para atividades acadêmicas como aulas, palestras, workshops, etc.
    """
    TIPO_CHOICES = [
        ('AULA', 'Aula'),
        ('PALESTRA', 'Palestra'),
        ('WORKSHOP', 'Workshop'),
        ('SEMINARIO', 'Seminário'),
        ('OUTRO', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    tipo_atividade = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='AULA'
    )
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField(blank=True, null=True)
    local = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    convocacao = models.BooleanField(default=False, verbose_name="Convocação")

    # Relacionamentos
    curso = models.ForeignKey(
        'cursos.Curso',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='atividades'
    )
    turmas = models.ManyToManyField(
        'turmas.Turma',
        blank=True,
        related_name='atividades'
    )

    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Atividade Acadêmica'
        verbose_name_plural = 'Atividades Acadêmicas'
        ordering = ['-data_inicio', 'hora_inicio']


class AtividadeRitualistica(AtividadeBase):
    """
    Modelo para atividades ritualísticas.
    """
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADA', 'Confirmada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField(blank=True, null=True)
    local = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    convocacao = models.BooleanField(default=False, verbose_name="Convocação")

    # Relacionamentos
    participantes = models.ManyToManyField(
        'alunos.Aluno',
        blank=True,
        related_name='atividades_ritualisticas'
    )

    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Atividade Ritualística'
        verbose_name_plural = 'Atividades Ritualísticas'
        ordering = ['-data', 'hora_inicio']

