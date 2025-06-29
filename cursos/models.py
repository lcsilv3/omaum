from django.db import models
from django.core.validators import MinValueValidator


class Curso(models.Model):
    # Novo campo id será a chave primária automaticamente
    codigo_curso = models.IntegerField(
        "Código do Curso",
        unique=True,  # Agora é apenas único, não mais PK
        null=True,    # Permitir null temporariamente para migração
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Digite um número inteiro positivo",
    )
    nome = models.CharField(max_length=100)
    descricao = models.TextField("Descrição", blank=True)
    duracao = models.PositiveIntegerField("Duração (meses)", default=6)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["nome"]  # Ordenar por nome agora
