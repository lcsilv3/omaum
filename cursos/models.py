from django.db import models
from django.core.validators import MinValueValidator


class Curso(models.Model):
    codigo_curso = models.IntegerField(
        "Código do Curso",
        primary_key=True,
        validators=[MinValueValidator(1)],
        help_text="Digite um número inteiro positivo",
    )
    nome = models.CharField("Nome do Curso", max_length=100)
    descricao = models.TextField("Descrição", blank=True)
    duracao = models.PositiveIntegerField("Duração (meses)", default=6)

    def __str__(self):
        return f"{self.codigo_curso} - {self.nome}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["codigo_curso"]
