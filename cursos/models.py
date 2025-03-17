from django.db import models

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao = models.PositiveIntegerField(verbose_name="Duração (meses)", null=True, blank=True)  # Add this line

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
