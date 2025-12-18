from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Turma(models.Model):
    """
    Modelo para representar uma turma no sistema OMAUM.
    """

    DIA_SEMANA_CHOICES = [
        ("SEG", "Segunda-feira"),
        ("TER", "Terça-feira"),
        ("QUA", "Quarta-feira"),
        ("QUI", "Quinta-feira"),
        ("SEX", "Sexta-feira"),
        ("SAB", "Sábado"),
        ("DOM", "Domingo"),
    ]

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

    # Novos campos solicitados
    num_livro = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Nº do Livro de Presenças"
    )
    perc_presenca_minima = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        default=70,
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
        max_length=20,
        choices=DIA_SEMANA_CHOICES,
        blank=True,
        null=True,
        verbose_name="Dia da Semana",
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
        return (
            self.data_inicio_ativ
            and self.data_termino_atividades
            and self.data_inicio_ativ <= hoje <= self.data_termino_atividades
            and self.status == "A"
        )

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
                        "nome": "Já existe uma turma com este nome. "
                        "Por favor, escolha um nome diferente."
                    }
                )
        # Validação das datas
        if self.data_inicio_ativ and self.data_termino_atividades:
            if self.data_termino_atividades < self.data_inicio_ativ:
                raise ValidationError(
                    _(
                        "A data de término das atividades não pode ser anterior à data de início das atividades."
                    )
                )
        
        # NOVA VALIDAÇÃO: Impedir instrutor em múltiplas turmas ativas simultaneamente
        from django.db.models import Q
        
        campos_instrutor = [
            (self.instrutor, 'instrutor', 'Instrutor Principal'),
            (self.instrutor_auxiliar, 'instrutor_auxiliar', 'Instrutor Auxiliar'),
            (self.auxiliar_instrucao, 'auxiliar_instrucao', 'Auxiliar de Instrução')
        ]

        for instrutor, campo_nome, _ in campos_instrutor:  # _ ignora o label não utilizado
            if instrutor:
                # Buscar turmas ativas onde este aluno já é instrutor
                turmas_ativas = Turma.objects.filter(
                    Q(instrutor=instrutor) |
                    Q(instrutor_auxiliar=instrutor) |
                    Q(auxiliar_instrucao=instrutor)
                ).filter(status="A")

                # Excluir a própria turma se estiver editando
                if self.pk:
                    turmas_ativas = turmas_ativas.exclude(pk=self.pk)

                # Se encontrou turmas ativas, lançar erro
                if turmas_ativas.exists():
                    turma_existente = turmas_ativas.first()
                    papel_atual = "Instrutor Principal" if turma_existente.instrutor == instrutor else (
                        "Instrutor Auxiliar" if turma_existente.instrutor_auxiliar == instrutor else
                        "Auxiliar de Instrução"
                    )
                    raise ValidationError({
                        campo_nome: (
                            f"ATENÇÃO: {instrutor.nome} já está atuando como {papel_atual} "
                            f"na turma '{turma_existente.nome}' (Status: Ativa). "
                            f"Um aluno não pode ser instrutor em múltiplas turmas ativas simultaneamente."
                        )
                    })
        
        # NOVA VALIDAÇÃO: Status só pode mudar se data_termino_atividades estiver preenchida
        if self.pk:  # Turma já existe (não é criação)
            try:
                original = Turma.objects.get(pk=self.pk)
                if original.status != self.status:  # Status está mudando
                    if not self.data_termino_atividades:
                        raise ValidationError({
                            'status': 'Não é possível alterar o status da turma sem definir '
                                      'a Data de Término das Atividades.',
                            'data_termino_atividades': 'Preencha este campo para alterar o status.'
                        })
            except Turma.DoesNotExist:
                pass  # Turma não existe ainda, ignore
        
        # NOVA VALIDAÇÃO: Warning se turma ativa tem data de término no passado
        if self.status == "A" and self.data_termino_atividades:
            hoje = timezone.now().date()
            if self.data_termino_atividades < hoje:
                from django.core.exceptions import NON_FIELD_ERRORS
                raise ValidationError({
                    NON_FIELD_ERRORS: [
                        f'ATENÇÃO: A data de término ({self.data_termino_atividades.strftime("%d/%m/%Y")}) '
                        f'já passou. Considere alterar o status da turma para "Finalizada" ou "Inativa".'
                    ]
                })

    @classmethod
    def get_by_codigo(cls, codigo_turma):
        """Método auxiliar para buscar turma por código."""
        try:
            # Use o campo id em vez de codigo
            return Turma.objects.get(id=codigo_turma)

            # Ou use o campo nome
            # return Turma.objects.get(nome=codigo_turma)
        except Turma.DoesNotExist:
            return None
