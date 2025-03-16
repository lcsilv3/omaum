from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class AtividadeAcademica(models.Model):
    codigo_atividade = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data_inicio = models.DateField(_('Data Início'), default=timezone.now)
    data_fim = models.DateField(_('Data Fim'), null=True, blank=True)
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class AtividadeRitualistica(models.Model):
    codigo_atividade = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data_inicio = models.DateField(_('Data Início'), default=timezone.now)
    data_fim = models.DateField(_('Data Fim'), null=True, blank=True)
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
