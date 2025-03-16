from django.db import models

class Punicao(models.Model):
    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE)
    descricao = models.TextField()
    data = models.DateField()
    tipo_punicao = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Punição - {self.aluno.nome} - {self.data}"
