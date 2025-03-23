from django.db import models
from django.contrib.auth.models import User
from alunos.models import Aluno
from turmas.models import Turma

class Frequencia(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField(default=False)
    justificativa = models.TextField(blank=True, null=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno} - {self.turma} - {self.data}"

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        permissions = [
            ("gerar_relatorio_frequencia", "Pode gerar relatório de frequências"),
        ]
        # Garantir que não tenhamos entradas duplicadas para o mesmo aluno, turma e data
        unique_together = ['aluno', 'turma', 'data']
