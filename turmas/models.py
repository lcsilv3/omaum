from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Turma(models.Model):
    """
    Modelo para representar uma turma no sistema OMAUM.
    """

    STATUS_CHOICES = [
        ("A", "Ativa"),
        ("I", "Inativa"),
        ("C", "Concluída"),
    ]

    # Informações básicas
    nome = models.CharField(max_length=100, verbose_name="Nome da Turma")
    curso = models.ForeignKey(
        "cursos.Curso",
        on_delete=models.CASCADE,
        verbose_name="Curso",
        related_name="turmas",
    )
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )

    # Datas
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Término")

    # Informações de agendamento
    dias_semana = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Dias da Semana"
    )
    local = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Local"
    )
    horario = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Horário"
    )

    # Capacidade e status
    vagas = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(1)],
        verbose_name="Número de Vagas",
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="A",
        verbose_name="Status",
    )

    # Instrutores
    instrutor = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_instrutor",
        verbose_name="Instrutor Principal",
    )
    instrutor_auxiliar = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_instrutor_auxiliar",
        verbose_name="Instrutor Auxiliar",
    )
    auxiliar_instrucao = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_auxiliar_instrucao",
        verbose_name="Auxiliar de Instrução",
    )

    # Metadados
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        default=timezone.now, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ["-data_inicio"]

    def __str__(self):
        return f"{self.nome} - {self.curso.nome}"

    @property
    def vagas_disponiveis(self):
        """Retorna o número de vagas disponíveis na turma."""
        vagas_ocupadas = self.matriculas.filter(status="A").count()
        return self.vagas - vagas_ocupadas

    @property
    def esta_ativa(self):
        """Verifica se a turma está ativa."""
        return self.status == "A"

    @property
    def esta_em_andamento(self):
        """Verifica se a turma está em andamento (começou mas não terminou)."""
        hoje = timezone.now().date()
        return self.data_inicio <= hoje <= self.data_fim and self.status == "A"

    def clean(self):
        super().clean()

        # Verificar se já existe uma turma com o mesmo nome (ignorando case)
        if self.nome:
            turmas_existentes = Turma.objects.filter(nome__iexact=self.nome)

            # Excluir a própria instância se estiver editando
            if self.pk:
                turmas_existentes = turmas_existentes.exclude(pk=self.pk)

            if turmas_existentes.exists():
                raise ValidationError(
                    {
                        "nome": "Já existe uma turma com este nome. Por favor, escolha um nome diferente."
                    }
                )
