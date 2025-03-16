from django.db import models
from cursos.models import Curso
from alunos.models import Aluno
class Turma(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    alunos = models.ManyToManyField(Aluno, blank=True)