from django.db import models
from alunos.models import Aluno

class CargoAdministrativo(models.Model):
    """
    Representa um cargo administrativo no sistema. O cargo administrativo possui um código único, 
    um nome e uma descrição opcional.
    """
    codigo_cargo = models.CharField(max_length=10, unique=True, verbose_name="Código do Cargo")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cargo Administrativo"
        verbose_name_plural = "Cargos Administrativos"
        ordering = ['nome']

class AtribuicaoCargo(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    cargo = models.ForeignKey(CargoAdministrativo, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Atribuição de Cargo"
        verbose_name_plural = "Atribuições de Cargos"

    def __str__(self):
        return f"{self.aluno.nome} - {self.cargo.nome}"
