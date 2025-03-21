from django.db import models
from turmas.models import Turma
from alunos.models import Aluno

class AtividadeAcademica(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    descricao = models.TextField(verbose_name="Descrição")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Fim")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Atividade Acadêmica"
        verbose_name_plural = "Atividades Acadêmicas"
from django.db import models
from turmas.models import Turma
from alunos.models import Aluno
class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    descricao = models.TextField(verbose_name="Descrição")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Fim")
    alunos = models.ManyToManyField(Aluno, blank=True, verbose_name="Alunos")
    todos_alunos = models.BooleanField(default=False, verbose_name="Todos os Alunos")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Atividade Ritualística"
        verbose_name_plural = "Atividades Ritualísticas"
