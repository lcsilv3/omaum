from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_curso_model():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")


class Turma(models.Model):
    OPCOES_STATUS = [
        ("A", "Ativa"),
        ("I", "Inativa"),
        ("C", "Concluída"),
    ]

    nome = models.CharField("Nome", max_length=100)
    curso = models.ForeignKey(
        "cursos.Curso",
        on_delete=models.CASCADE,
        verbose_name="Curso",
        to_field="codigo_curso",  # Especificar que estamos referenciando o campo codigo_curso
    )
    data_inicio = models.DateField("Data de Início")
    data_fim = models.DateField("Data de Fim")
    status = models.CharField(
        "Status", max_length=1, choices=OPCOES_STATUS, default="A"
    )
    capacidade = models.PositiveIntegerField("Capacidade de Alunos", default=30)
    descricao = models.TextField("Descrição", blank=True)

    def __str__(self):
        return f"{self.nome} - {self.curso}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError(
                {"data_fim": "A data de término deve ser posterior à data de início."}
            )
        # Atualiza status automaticamente com base nas datas
        hoje = timezone.now().date()
        if self.status == "A" and self.data_fim < hoje:
            self.status = "C"  # Marca como concluída se a data final já passou

    @property
    def alunos_matriculados(self):
        return self.matriculas.count()

    @property
    def vagas_disponiveis(self):

        return (
            self.capacidade - self.alunos_matriculados
        )  # Use alunos_matriculados for consistency

    @property
    def total_alunos(self):
        """Retorna o número total de alunos matriculados na turma."""
        return self.matriculas.count()

    @property
    def tem_alunos(self):
        """Verifica se a turma tem alunos matriculados."""
        return self.total_alunos > 0

    def save(self, *args, **kwargs):
        # Se for uma turma nova, permitimos salvar sem alunos inicialmente
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            # Para turmas existentes, verificamos se há pelo menos um aluno
            if not self.tem_alunos:  # Corrigido: removidos os parênteses
                raise ValidationError(
                    "Uma turma deve ter pelo menos um aluno matriculado."
                )
            super().save(*args, **kwargs)
