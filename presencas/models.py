from django.db import models
from alunos.models import Aluno
from turmas.models import Turma


class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("presente", "Presente"),
            ("ausente", "Ausente"),
            ("justificado", "Justificado"),
        ],
    )

    def __str__(self):
        return f"Presença de {self.aluno} em {self.turma} na data {self.data}"
