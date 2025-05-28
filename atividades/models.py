from django.db import models
from django.utils import timezone

class AtividadeAcademica(models.Model):
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

class AtividadeRitualistica(models.Model):
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
