from django.db import models
from alunos.models import Aluno


class Iniciacao(models.Model):
    """
    Modelo para armazenar informações sobre iniciações de alunos em cursos.
    
    Atributos:
        aluno (ForeignKey): Referência ao aluno que recebeu a iniciação
        nome_curso (str): Nome do curso de iniciação
        data_iniciacao (date): Data em que a iniciação ocorreu
        observacoes (str, opcional): Observações adicionais sobre a iniciação
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='iniciacoes')
    nome_curso = models.CharField(max_length=100)
    data_iniciacao = models.DateField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Iniciação - {self.aluno.nome} - {self.nome_curso}"

    class Meta:
        ordering = ['-data_iniciacao']
        verbose_name = 'Iniciação'
        verbose_name_plural = 'Iniciações'
