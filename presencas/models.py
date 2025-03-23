from django.db import models
from django.contrib.auth.models import User
from turmas.models import Turma
from alunos.models import Aluno

class PresencaAcademica(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField(default=False)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno} - {self.turma} - {self.data}"

    class Meta:
        verbose_name = "Presença Acadêmica"
        verbose_name_plural = "Presenças Acadêmicas"
        permissions = [
            ("gerar_relatorio_presenca", "Pode gerar relatório de presenças"),
        ]