from django.db import models


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField("Descrição", blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["id"]
