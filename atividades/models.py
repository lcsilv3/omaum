from django.db import models
from django.utils import timezone

class AtividadeAcademica(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    # Substituir o campo data por data_inicio e data_fim
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(blank=True, null=True)
    # Referência ao app correto
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE, related_name='atividades_academicas')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Acadêmica'
        verbose_name_plural = 'Atividades Acadêmicas'

class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    # Substituir o campo data por data_inicio e data_fim
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(blank=True, null=True)
    # Referência ao app correto
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE, related_name='atividades_ritualisticas')
    # Referência ao app correto
    alunos = models.ManyToManyField('alunos.Aluno', related_name='atividades_ritualisticas')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Ritualística'
        verbose_name_plural = 'Atividades Ritualísticas'
