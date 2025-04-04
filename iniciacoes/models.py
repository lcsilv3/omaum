from django.db import models
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_curso_model():
    cursos_module = import_module('cursos.models')
    return getattr(cursos_module, 'Curso')

class Iniciacao(models.Model):
    aluno = models.ForeignKey(
        get_aluno_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Aluno',
        to_field='cpf'  # Especificar que estamos referenciando o campo cpf
    )
    curso = models.ForeignKey(
        get_curso_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Curso'
    )
    data_iniciacao = models.DateField(verbose_name='Data da Iniciação')
    grau = models.CharField(max_length=50, verbose_name='Grau')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.curso.nome} - {self.grau}"
    
    class Meta:
        verbose_name = 'Iniciação'
        verbose_name_plural = 'Iniciações'
        ordering = ['-data_iniciacao']
        unique_together = ['aluno', 'curso', 'grau']
