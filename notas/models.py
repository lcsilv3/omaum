from django.db import models
from django.utils import timezone
from alunos.models import Aluno
from cursos.models import Curso
from turmas.models import Turma

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
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='notas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='notas')
    tipo_avaliacao = models.CharField(max_length=20, choices=TIPO_AVALIACAO_CHOICES)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    peso = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    data = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-data', 'aluno__nome']
        # Garantir que não haja notas duplicadas para o mesmo aluno/curso/turma/tipo
        unique_together = ['aluno', 'curso', 'turma', 'tipo_avaliacao', 'data']
    
    def __str__(self):
        return f"Nota de {self.aluno} em {self.curso} ({self.get_tipo_avaliacao_display()}): {self.valor}"
    
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
