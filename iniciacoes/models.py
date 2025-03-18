from django.db import models
from alunos.models import Aluno

class Iniciacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='iniciacoes')
    nome_curso = models.CharField(max_length=100)
    data_iniciacao = models.DateField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Iniciação - {self.aluno.nome} - {self.nome_curso}"

    class Meta:
        ordering = ['-data_iniciacao']
