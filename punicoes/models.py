from django.db import models
from alunos.models import Aluno

class Punicao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='punicoes')
    descricao = models.TextField()
    data = models.DateField()
    tipo_punicao = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Punição - {self.aluno.nome} - {self.data}"

    class Meta:
        ordering = ['-data']
