from django.db import models
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_atividade_model():
    atividades_module = import_module('atividades.models')
    return getattr(atividades_module, 'AtividadeAcademica')

class Frequencia(models.Model):
    aluno = models.ForeignKey(
        get_aluno_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Aluno',
        to_field='cpf'  # Especificar que estamos referenciando o campo cpf
    )
    atividade = models.ForeignKey(
        get_atividade_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Atividade'
    )
    data = models.DateField(verbose_name='Data')
    presente = models.BooleanField(default=True, verbose_name='Presente')
    justificativa = models.TextField(blank=True, null=True, verbose_name='Justificativa')
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.atividade.nome} - {self.data}"
    
    class Meta:
        verbose_name = 'Frequência'
        verbose_name_plural = 'Frequências'
        ordering = ['-data']
        unique_together = ['aluno', 'atividade', 'data']
