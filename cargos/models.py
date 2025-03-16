from django.db import models

class CargoAdministrativo(models.Model):
    """
    Represents an administrative cargo in the system. The administrative cargo has a unique code, a name, and an optional description.
    """
    codigo_cargo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
