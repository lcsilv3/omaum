from django.db import models
from alunos.models import Aluno
from cursos.models import Curso


class Nota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"Nota de {self.aluno} em {self.curso}: {self.valor}"
