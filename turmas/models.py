from django.db import models
from cursos.models import Curso

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return f"{self.nome} - {self.curso}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"