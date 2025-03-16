from django.db import models
from django.utils import timezone

class Curso(models.Model):
    nome = models.CharField(max_length=255, unique=True, verbose_name="Nome")
    descricao = models.TextField(verbose_name="Descrição")
    duracao = models.PositiveIntegerField(verbose_name="Duração (meses)")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['nome']

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='turmas', verbose_name="Curso")
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(verbose_name="Data de Término")
    vagas = models.PositiveIntegerField(verbose_name="Número de Vagas")

    def __str__(self):
        return f"{self.nome} - {self.curso.nome}"

    class Meta:
        ordering = ['-data_inicio', 'nome']

class AtividadeBase(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    descricao = models.TextField(verbose_name="Descrição")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    data = models.DateTimeField(verbose_name="Data e Hora")
    duracao = models.DurationField(verbose_name="Duração")

    class Meta:
        abstract = True

class AtividadeAcademica(AtividadeBase):
    tipo = models.CharField(max_length=50, choices=[
        ('aula', 'Aula'),
        ('prova', 'Prova'),
        ('seminario', 'Seminário'),
    ], verbose_name="Tipo")

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()}) - {self.turma}"

    class Meta:
        verbose_name = "Atividade Acadêmica"
        verbose_name_plural = "Atividades Acadêmicas"

class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True, blank=True)
    alunos = models.ManyToManyField(Aluno, blank=True)

    def __str__(self):
        return self.nome

class PresencaBase(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    presente = models.BooleanField(default=False, verbose_name="Presente")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

    class Meta:
        abstract = True

class PresencaAcademica(PresencaBase):
    atividade_academica = models.ForeignKey(AtividadeAcademica, on_delete=models.CASCADE, verbose_name="Atividade Acadêmica")

    def __str__(self):
        return f"{self.aluno} - {self.atividade_academica}"

    class Meta:
        verbose_name = "Presença Acadêmica"
        verbose_name_plural = "Presenças Acadêmicas"
        unique_together = ['aluno', 'atividade_academica']

class PresencaRitualistica(PresencaBase):
    atividade_ritualistica = models.ForeignKey(AtividadeRitualistica, on_delete=models.CASCADE, verbose_name="Atividade Ritualística")

    def __str__(self):
        return f"{self.aluno} - {self.atividade_ritualistica}"

    class Meta:
        verbose_name = "Presença Ritualística"
        verbose_name_plural = "Presenças Ritualísticas"
        unique_together = ['aluno', 'atividade_ritualistica']