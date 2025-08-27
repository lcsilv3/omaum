from django.db import models
from importlib import import_module
from decimal import Decimal


def get_turma_model():
    """Obtém o modelo Turma."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_aluno_model():
    """Obtém o modelo Aluno."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_presenca_model():
    """Obtém o modelo Presenca."""
    presencas_module = import_module("presencas.models")
    return getattr(presencas_module, "Presenca")


def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


class FrequenciaMensal(models.Model):
    """Modelo para controle de frequência mensal de uma turma."""

    MES_CHOICES = [
        (1, "Janeiro"),
        (2, "Fevereiro"),
        (3, "Março"),
        (4, "Abril"),
        (5, "Maio"),
        (6, "Junho"),
        (7, "Julho"),
        (8, "Agosto"),
        (9, "Setembro"),
        (10, "Outubro"),
        (11, "Novembro"),
        (12, "Dezembro"),
    ]

    turma = models.ForeignKey(
        get_turma_model(), on_delete=models.CASCADE, verbose_name="Turma"
    )

    mes = models.IntegerField(choices=MES_CHOICES, verbose_name="Mês")

    ano = models.IntegerField(verbose_name="Ano")

    percentual_minimo = models.IntegerField(
        default=75, verbose_name="Percentual Mínimo (%)"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Frequência Mensal"
        verbose_name_plural = "Frequências Mensais"
        ordering = ["-ano", "-mes", "turma__nome"]
        unique_together = ["turma", "mes", "ano"]

    def __str__(self):
        return f"{self.turma.nome} - {self.get_mes_display()}/{self.ano}"

    @property
    def total_alunos(self):
        """Retorna o total de alunos com carência nesta frequência."""
        return self.carencia_set.count()

    @property
    def alunos_liberados(self):
        """Retorna o total de alunos liberados."""
        return self.carencia_set.filter(liberado=True).count()

    @property
    def alunos_com_carencia(self):
        """Retorna o total de alunos com carência."""
        return self.carencia_set.filter(liberado=False).count()

    def calcular_carencias(self):
        """Calcula as carências para todos os alunos da turma."""
        from django.db import transaction
        import calendar
        from datetime import date

        # Obter modelos
        Matricula = get_model_dynamically("matriculas", "Matricula")
        Presenca = get_model_dynamically("presencas", "Presenca")
        get_model_dynamically("alunos", "Aluno")
        Carencia = get_model_dynamically("frequencias", "Carencia")

        # Obter matrículas ativas na turma
        matriculas = Matricula.objects.filter(turma=self.turma, status="A")

        # Determinar o primeiro e último dia do mês
        ultimo_dia = calendar.monthrange(self.ano, self.mes)[1]
        data_inicio = date(self.ano, self.mes, 1)
        data_fim = date(self.ano, self.mes, ultimo_dia)

        # Obter atividades do mês
        Atividade = get_model_dynamically("atividades", "AtividadeAcademica")
        atividades = Atividade.objects.filter(
            turmas=self.turma,
            data_inicio__date__gte=data_inicio,
            data_inicio__date__lte=data_fim,
        )

        total_atividades = atividades.count()

        # Se não houver atividades, não há como calcular carências
        if total_atividades == 0:
            return

        with transaction.atomic():
            # Limpar carências existentes
            Carencia.objects.filter(frequencia_mensal=self).delete()

            # Calcular carências para cada aluno
            for matricula in matriculas:
                aluno = matricula.aluno

                # Contar presenças do aluno nas atividades do mês
                presencas = Presenca.objects.filter(
                    aluno=aluno,
                    atividade__in=atividades,
                    data__gte=data_inicio,
                    data__lte=data_fim,
                    presente=True,
                ).count()

                # Calcular percentual de presença
                percentual_presenca = (
                    (presencas / total_atividades) * 100 if total_atividades > 0 else 0
                )

                # Determinar se o aluno está liberado
                liberado = percentual_presenca >= self.percentual_minimo

                # Calcular número de carências (aulas que faltou)
                numero_carencias = total_atividades - presencas

                # Criar registro de carência
                Carencia.objects.create(
                    frequencia_mensal=self,
                    aluno=aluno,
                    total_presencas=presencas,
                    total_atividades=total_atividades,
                    percentual_presenca=percentual_presenca,
                    numero_carencias=numero_carencias,
                    liberado=liberado,
                    data_identificacao=date.today(),
                    status="PENDENTE" if not liberado else None,
                )


class Carencia(models.Model):
    """Modelo para registro de carências de alunos em uma frequência mensal."""

    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("EM_ACOMPANHAMENTO", "Em Acompanhamento"),
        ("RESOLVIDO", "Resolvido"),
    ]

    frequencia_mensal = models.ForeignKey(
        FrequenciaMensal, on_delete=models.CASCADE, verbose_name="Frequência Mensal"
    )

    aluno = models.ForeignKey(
        get_aluno_model(), on_delete=models.CASCADE, verbose_name="Aluno"
    )

    total_presencas = models.IntegerField(default=0, verbose_name="Total de Presenças")

    total_atividades = models.IntegerField(
        default=0, verbose_name="Total de Atividades"
    )

    percentual_presenca = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Percentual de Presença",
    )

    numero_carencias = models.IntegerField(
        default=0, verbose_name="Número de Carências"
    )

    liberado = models.BooleanField(default=False, verbose_name="Liberado")

    # Adicionando o campo status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDENTE",
        verbose_name="Status",
        null=True,
        blank=True,
    )

    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Carência"
        verbose_name_plural = "Carências"
        ordering = ["frequencia_mensal", "aluno__nome"]
        unique_together = ["frequencia_mensal", "aluno"]

    def __str__(self):
        return f"{self.aluno.nome} - {self.frequencia_mensal}"
