from django.db import models

class Curso(models.Model):
    codigo_curso = models.CharField(max_length=20, primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
