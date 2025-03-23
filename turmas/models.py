from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Turma(models.Model):
    OPCOES_STATUS = [
        ('A', 'Ativa'),
        ('I', 'Inativa'),
        ('C', 'Concluída'),
    ]
    
    nome = models.CharField('Nome', max_length=100)
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE, verbose_name='Curso')
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Fim')
    status = models.CharField('Status', max_length=1, choices=OPCOES_STATUS, default='A')
    capacidade = models.PositiveIntegerField('Capacidade de Alunos', default=30)
    descricao = models.TextField('Descrição', blank=True)
    
    def __str__(self):
        return f"{self.nome} - {self.curso}"
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
    
    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError({'data_fim': 'A data de término deve ser posterior à data de início.'})
        
        # Atualiza status automaticamente com base nas datas
        hoje = timezone.now().date()
        if self.status == 'A' and self.data_fim < hoje:
            self.status = 'C'  # Marca como concluída se a data final já passou
    
    @property
    def alunos_matriculados(self):
        return self.matriculas.count()
    
    @property
    def vagas_disponiveis(self):
        return self.capacidade - self.alunos_matriculados
    
    def tem_alunos(self):
        """Verifica se a turma tem pelo menos um aluno matriculado"""
        return self.alunos_matriculados > 0
    
    def save(self, *args, **kwargs):
        # Se for uma turma nova, permitimos salvar sem alunos inicialmente
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            # Para turmas existentes, verificamos se há pelo menos um aluno
            if not self.tem_alunos():
                raise ValidationError("Uma turma deve ter pelo menos um aluno matriculado.")
            super().save(*args, **kwargs)


class Matricula(models.Model):
    OPCOES_STATUS = [
        ('A', 'Ativa'),
        ('C', 'Cancelada'),
        ('F', 'Finalizada'),
    ]
    
    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE, 
                             related_name='matriculas', verbose_name='Aluno')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, 
                             related_name='matriculas', verbose_name='Turma')
    data_matricula = models.DateField('Data da Matrícula', auto_now_add=True)
    status = models.CharField('Status', max_length=1, choices=OPCOES_STATUS, default='A')
    
    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = ['aluno', 'turma']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome}"
    
    def clean(self):
        # Check if class is active
        if self.turma.status != 'A':
            raise ValidationError({'turma': _('Não é possível matricular em uma turma inativa ou concluída.')})
        
        # Check if there are available spots
        if not self.pk and self.turma.vagas_disponiveis <= 0:  # Only for new enrollments
            raise ValidationError({'turma': _('Não há vagas disponíveis nesta turma.')})
        
        # Check if student's course matches the class's course
        if self.aluno.curso != self.turma.curso:
            raise ValidationError({'aluno': _('O aluno deve pertencer ao mesmo curso da turma.')})