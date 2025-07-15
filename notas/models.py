from django.db import models
from importlib import import_module

def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")

def get_curso_model():
    """Obtém o modelo Curso."""
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")

def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")

class Nota(models.Model):
    TIPO_AVALIACAO_CHOICES = [
        ('prova', 'Prova'),
        ('trabalho', 'Trabalho'),
        ('apresentacao', 'Apresentação'),
        ('participacao', 'Participação'),
        ('atividade', 'Atividade'),
        ('exame', 'Exame Final'),
        ('outro', 'Outro'),
    ]
    
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        related_name='notas'
    )
    curso = models.ForeignKey(
        'cursos.Curso',
        on_delete=models.CASCADE,
        related_name='notas'
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        related_name='notas'
    )
    tipo_avaliacao = models.CharField(
        max_length=20,
        choices=TIPO_AVALIACAO_CHOICES
    )
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    peso = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    data = models.DateField()
    observacao = models.TextField(blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-data', 'aluno__nome']
        # Garantir que não haja notas duplicadas para o mesmo
        # aluno/curso/turma/tipo
        unique_together = ['aluno', 'curso', 'turma', 'tipo_avaliacao', 'data']
    
    def __str__(self):
        tipo_display = self.get_tipo_avaliacao_display()
        return f"Nota de {self.aluno} em {self.curso} " \
               f"({tipo_display}): {self.valor}"
    
    @property
    def valor_ponderado(self):
        """Retorna o valor da nota ponderado pelo peso."""
        return self.valor * self.peso
    
    @property
    def situacao(self):
        """Retorna a situação do aluno com base na nota."""
        if self.valor >= 7:
            return 'Aprovado'
        elif self.valor >= 5:
            return 'Em Recuperação'
        else:
            return 'Reprovado'
