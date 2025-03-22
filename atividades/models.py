from django.db import models
from turmas.models import Turma
from django.conf import settings

class AtividadeAcademica(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    data_inicio = models.DateField(verbose_name='Data de Início')
    data_fim = models.DateField(verbose_name='Data de Fim')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Acadêmica'
        verbose_name_plural = 'Atividades Acadêmicas'

class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    data_inicio = models.DateField(verbose_name='Data de Início')
    data_fim = models.DateField(verbose_name='Data de Fim')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    alunos = models.ManyToManyField('core.Aluno', blank=True, related_name='atividades_ritualisticas', verbose_name='Alunos')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Ritualística'
        verbose_name_plural = 'Atividades Ritualísticas'
