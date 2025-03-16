from django.db import models
from turmas.models import Turma
from alunos.models import Aluno

class PresencaAcademica(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.aluno} - {self.turma} - {self.data}"

    class Meta:
        verbose_name = "Presença Acadêmica"
        verbose_name_plural = "Presenças Acadêmicas"