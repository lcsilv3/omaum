from django.db import models
from alunos.models import Aluno


class Pagamento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pendente", "Pendente"),
            ("pago", "Pago"),
            ("cancelado", "Cancelado"),
        ],
    )

    def __str__(self):
        return f"Pagamento de {self.aluno} - {self.valor} em {self.data_pagamento}"
