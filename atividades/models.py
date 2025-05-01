# Adicione o seguinte código temporário para diagnóstico no início do arquivo:

print("CARREGANDO MODELS.PY")
# Imprimir os campos do modelo para diagnóstico
try:
    from django.db import models
    import inspect

    # Carregar o módulo atual
    import sys

    current_module = sys.modules[__name__]

    # Encontrar todas as classes de modelo no módulo
    for name, obj in inspect.getmembers(current_module):
        if (
            inspect.isclass(obj)
            and issubclass(obj, models.Model)
            and obj != models.Model
        ):
            print(f"Modelo: {name}")
            for field in obj._meta.fields:
                print(f"  - {field.name} ({field.__class__.__name__})")
except Exception as e:
    print(f"Erro ao inspecionar modelos: {e}")

from django.db import models
from django.utils import timezone
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


class AtividadeAcademica(models.Model):
    TIPO_CHOICES = (
        ("aula", "Aula"),
        ("palestra", "Palestra"),
        ("workshop", "Workshop"),
        ("seminario", "Seminário"),
        ("outro", "Outro"),
    )

    STATUS_CHOICES = (
        ("agendada", "Agendada"),
        ("em_andamento", "Em Andamento"),
        ("concluida", "Concluída"),
        ("cancelada", "Cancelada"),
    )

    nome = models.CharField(max_length=100)

    @property
    def titulo(self):
        return self.nome

    @titulo.setter
    def titulo(self, value):
        self.nome = value

    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )
    data_inicio = models.DateTimeField(
        default=timezone.now, verbose_name="Data de Início"
    )
    data_fim = models.DateTimeField(
        blank=True, null=True, verbose_name="Data de Término"
    )
    responsavel = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Responsável"
    )
    local = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Local"
    )
    tipo_atividade = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="aula",
        verbose_name="Tipo de Atividade",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="agendada",
        verbose_name="Status",
    )
    
    # Novo campo para múltiplas turmas
    turmas = models.ManyToManyField(
        "turmas.Turma",
        related_name="atividades_academicas",
        verbose_name="Turmas"
    )

    def __str__(self):
        return self.titulo or self.nome

    class Meta:
        verbose_name = "Atividade Acadêmica"
        verbose_name_plural = "Atividades Acadêmicas"


class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )
    data = models.DateField(verbose_name="Data")
    hora_inicio = models.TimeField(verbose_name="Hora de Início")
    hora_fim = models.TimeField(verbose_name="Hora de Término")
    local = models.CharField(max_length=100, verbose_name="Local")
    turma = models.ForeignKey(
        get_turma_model(), on_delete=models.CASCADE, verbose_name="Turma"
    )
    participantes = models.ManyToManyField(
        get_aluno_model(),
        blank=True,
        verbose_name="Participantes",
        related_name="atividades_ritualisticas",
    )

    def __str__(self):
        return f"{self.nome} - {self.data}"

    class Meta:
        verbose_name = "Atividade Ritualística"
        verbose_name_plural = "Atividades Ritualísticas"
        ordering = ["-data", "hora_inicio"]
