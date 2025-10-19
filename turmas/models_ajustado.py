"""
Ajustes no modelo Turma para atender às premissas estabelecidas.
Renomeia perc_carencia para perc_presenca_minima conforme especificado.
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Turma(models.Model):
    """
    Modelo para representar uma turma no sistema OMAUM.

    AJUSTES REALIZADOS conforme premissas:
    - Campo perc_carencia renomeado para perc_presenca_minima
    - Help text e verbose_name atualizados conforme especificação
    - Mantém compatibilidade com dados existentes
    """

    STATUS_CHOICES = [
        ("A", "Ativa"),
        ("I", "Inativa"),
        ("C", "Cancelada"),
        ("F", "Finalizada"),
    ]

    # Informações básicas
    nome = models.CharField(max_length=100, verbose_name="Nome da Turma")
    curso = models.ForeignKey(
        "cursos.Curso",
        on_delete=models.CASCADE,
        verbose_name="Curso",
        related_name="turmas",
    )
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    # Campos específicos
    num_livro = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Nº do Livro de Presenças"
    )

    # CAMPO RENOMEADO: perc_carencia -> perc_presenca_minima
    perc_presenca_minima = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Percentual Mínimo de Presença (%)",
        help_text="Percentual mínimo de presenças permitido para a turma",
    )

    data_iniciacao = models.DateField(
        blank=True, null=True, verbose_name="Data de Iniciação"
    )
    data_inicio_ativ = models.DateField(
        blank=True, null=True, verbose_name="Data de Início das Atividades"
    )
    data_prim_aula = models.DateField(
        blank=True, null=True, verbose_name="Data da Primeira Aula"
    )
    data_termino_atividades = models.DateField(
        blank=True, null=True, verbose_name="Data de Término das Atividades"
    )

    # Informações de agendamento
    dias_semana = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Dias da Semana"
    )
    horario = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Horário"
    )
    local = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Local"
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

    ativo = models.BooleanField(default=True, verbose_name="Ativo")

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

    # Campos de alerta para instrutores
    alerta_instrutor = models.BooleanField(
        default=False, verbose_name="Alerta de Instrutor"
    )
    alerta_mensagem = models.TextField(
        blank=True, null=True, verbose_name="Mensagem de Alerta"
    )

    # Metadados
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    updated_at = models.DateTimeField(
        default=timezone.now, verbose_name="Atualizado em"
    )

    def __str__(self):
        try:
            return f"{self.nome} - {self.curso.nome}"
        except Exception:
            return f"{self.nome} - [Curso não encontrado]"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ["-data_inicio_ativ"]
        indexes = [
            models.Index(fields=["nome"]),
            models.Index(fields=["status"]),
            models.Index(fields=["ativo"]),
            models.Index(fields=["data_inicio_ativ"]),
        ]

    def clean(self):
        """Validações customizadas."""
        super().clean()

        # Validar percentual de presença
        if self.perc_presenca_minima is not None:
            if self.perc_presenca_minima < 0 or self.perc_presenca_minima > 100:
                raise ValidationError(
                    {"perc_presenca_minima": "O percentual deve estar entre 0 e 100."}
                )

        # Validar datas
        if self.data_inicio_ativ and self.data_termino_atividades:
            if self.data_inicio_ativ > self.data_termino_atividades:
                raise ValidationError(
                    {
                        "data_termino_atividades": "A data de término deve ser posterior à data de início."
                    }
                )

        if self.data_prim_aula and self.data_inicio_ativ:
            if self.data_prim_aula < self.data_inicio_ativ:
                raise ValidationError(
                    {
                        "data_prim_aula": "A data da primeira aula deve ser posterior ou igual à data de início das atividades."
                    }
                )

    @property
    def vagas_disponiveis(self):
        """Retorna o número de vagas disponíveis na turma."""
        # Usar importlib para evitar importação circular
        from importlib import import_module

        matriculas_module = import_module("matriculas.models")

        try:
            vagas_ocupadas = matriculas_module.Matricula.objects.filter(
                turma=self,
                status="A",  # Assumindo que "A" = Ativa
            ).count()
            return self.vagas - vagas_ocupadas
        except:
            return self.vagas

    @property
    def esta_ativa(self):
        """Verifica se a turma está ativa."""
        return self.status == "A" and self.ativo

    @property
    def esta_em_andamento(self):
        """Verifica se a turma está em andamento (começou mas não terminou)."""
        hoje = timezone.now().date()
        return (
            self.data_inicio_ativ
            and self.data_termino_atividades
            and self.data_inicio_ativ <= hoje <= self.data_termino_atividades
            and self.esta_ativa
        )

    @property
    def percentual_ocupacao(self):
        """Calcula o percentual de ocupação da turma."""
        vagas_ocupadas = self.vagas - self.vagas_disponiveis
        if self.vagas > 0:
            return round((vagas_ocupadas / self.vagas) * 100, 2)
        return 0

    def get_alunos_ativos(self):
        """Retorna alunos ativos matriculados na turma."""
        from importlib import import_module

        matriculas_module = import_module("matriculas.models")

        try:
            return matriculas_module.Matricula.objects.filter(
                turma=self, status="A"
            ).select_related("aluno")
        except:
            return []

    def get_percentual_presenca_display(self):
        """Retorna percentual de presença formatado."""
        if self.perc_presenca_minima:
            return f"{self.perc_presenca_minima}%"
        return "Não definido"

    def pode_matricular_aluno(self):
        """Verifica se é possível matricular mais alunos."""
        return self.esta_ativa and self.vagas_disponiveis > 0

    @classmethod
    def obter_ativas(cls):
        """Retorna queryset com turmas ativas."""
        return cls.objects.filter(status="A", ativo=True)

    @classmethod
    def obter_em_andamento(cls):
        """Retorna turmas que estão em andamento."""
        hoje = timezone.now().date()
        return cls.objects.filter(
            status="A",
            ativo=True,
            data_inicio_ativ__lte=hoje,
            data_termino_atividades__gte=hoje,
        )

    # Métodos para compatibilidade com sistema de relatórios
    def get_dados_relatorio_pcg(self):
        """Retorna dados para relatório PCG (Controle Geral)."""
        return {
            "nome": self.nome,
            "curso": self.curso.nome if self.curso else "N/A",
            "descricao": self.descricao or "N/A",
            "num_livro": self.num_livro or "N/A",
            "perc_presenca_minima": self.get_percentual_presenca_display(),
            "data_iniciacao": self.data_iniciacao.strftime("%d/%m/%Y")
            if self.data_iniciacao
            else "N/A",
            "data_inicio_ativ": self.data_inicio_ativ.strftime("%d/%m/%Y")
            if self.data_inicio_ativ
            else "N/A",
            "data_prim_aula": self.data_prim_aula.strftime("%d/%m/%Y")
            if self.data_prim_aula
            else "N/A",
            "data_termino_atividades": self.data_termino_atividades.strftime("%d/%m/%Y")
            if self.data_termino_atividades
            else "N/A",
            "dias_semana": self.dias_semana or "N/A",
            "horario": self.horario or "N/A",
            "local": self.local or "N/A",
            "vagas": self.vagas,
            "status": self.get_status_display(),
            "instrutor": self.instrutor.nome if self.instrutor else "N/A",
            "instrutor_auxiliar": self.instrutor_auxiliar.nome
            if self.instrutor_auxiliar
            else "N/A",
            "auxiliar_instrucao": self.auxiliar_instrucao.nome
            if self.auxiliar_instrucao
            else "N/A",
        }


# Modelo para controlar migração do campo renomeado
class MigracaoPercPresenca(models.Model):
    """
    Modelo temporário para controlar a migração do campo perc_carencia para perc_presenca_minima.
    """

    turma = models.OneToOneField(Turma, on_delete=models.CASCADE, verbose_name="Turma")

    valor_anterior = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor Anterior (perc_carencia)",
    )

    valor_novo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor Novo (perc_presenca_minima)",
    )

    migrado_em = models.DateTimeField(auto_now_add=True, verbose_name="Migrado em")

    class Meta:
        verbose_name = "Migração Percentual Presença"
        verbose_name_plural = "Migrações Percentual Presença"

    def __str__(self):
        return f"{self.turma.nome}: {self.valor_anterior}% -> {self.valor_novo}%"
