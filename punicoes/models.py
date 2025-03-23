from django.db import models
from django.contrib.auth.models import User
from alunos.models import Aluno

class Punicao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='punicoes')
    descricao = models.TextField()
    data = models.DateField()
    tipo_punicao = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True, null=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Punição - {self.aluno.nome} - {self.data}"

    class Meta:
        ordering = ['-data']
        permissions = [
            ("gerar_relatorio_punicao", "Pode gerar relatório de punições"),
        ]
