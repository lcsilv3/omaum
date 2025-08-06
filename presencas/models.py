
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import logging
from django.contrib.auth.models import User

# NOVO MODELO: ConvocacaoPresenca
class ConvocacaoPresenca(models.Model):
    """
    Representa a convocação individual de um aluno para uma atividade em um dia específico.
    """
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        related_name='convocacoes_presenca',
        verbose_name='Aluno'
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        related_name='convocacoes_presenca',
        verbose_name='Turma'
    )
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        related_name='convocacoes_presenca',
        verbose_name='Atividade'
    )
    data = models.DateField(verbose_name='Data da Atividade')
    convocado = models.BooleanField(default=True, verbose_name='Convocado')
    registrado_por = models.CharField(max_length=100, default='Sistema', verbose_name='Registrado por')
    data_registro = models.DateTimeField(default=timezone.now, verbose_name='Data de registro')

    class Meta:
        verbose_name = 'Convocação de Presença'
        verbose_name_plural = 'Convocações de Presença'
        unique_together = ['aluno', 'turma', 'atividade', 'data']
        ordering = ['-data', 'aluno__nome']

    def __str__(self):
        status = 'Convocado' if self.convocado else 'Não Convocado'
        return f"{self.aluno} - {self.atividade} - {self.data} - {status}"

logger = logging.getLogger(__name__)

class Presenca(models.Model):
    """
    Modelo para registro de presença de alunos em atividades acadêmicas ou ritualísticas.
    Armazena informações sobre presença, ausência e justificativas.
    """
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        related_name="presencas_detalhadas"
    )
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        verbose_name="Atividade",
        null=True,
        blank=True,
        related_name="presencas_detalhadas"
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma",
        null=True,
        blank=True,
        related_name="presencas_detalhadas"
    )
    data = models.DateField(verbose_name="Data")
    presente = models.BooleanField(default=True, verbose_name="Presente")
    justificativa = models.TextField(
        blank=True,
        null=True,
        verbose_name="Justificativa"
    )
    registrado_por = models.CharField(
        max_length=100,
        default="Sistema",
        verbose_name="Registrado por"
    )
    data_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de registro"
    )

    class Meta:
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        ordering = ["-data", "aluno__nome"]
        unique_together = ["aluno", "turma", "data", "atividade"]

    def __str__(self):
        """Retorna uma representação em string do objeto."""
        status = "Presente" if self.presente else "Ausente"
        return f"{self.aluno.nome} - {self.data} - {status}"

    def clean(self):
        """
        Valida os dados do modelo antes de salvar.
        - Data não pode ser futura.
        - Justificativa é opcional para ausências.
        """
        super().clean()
        if self.data and self.data > timezone.now().date():
            logger.warning(f"Data futura informada para presença: {self.data}")
            raise ValidationError({"data": "A data não pode ser futura."})

class TotalAtividadeMes(models.Model):
    """
    Modelo para totalização de atividades por mês em uma turma.
    """
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        related_name="totais_atividade_mes"
    )
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE)
    ano = models.IntegerField()
    mes = models.IntegerField()
    qtd_ativ_mes = models.PositiveIntegerField(default=0)
    registrado_por = models.CharField(max_length=100, default="Sistema")
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["atividade", "turma", "ano", "mes"]
        verbose_name = "Total de Atividade no Mês"
        verbose_name_plural = "Totais de Atividades no Mês"

    def __str__(self):
        return f"{self.atividade} - {self.turma} - {self.mes}/{self.ano}: {self.qtd_ativ_mes}"

class ObservacaoPresenca(models.Model):
    """
    Observações relacionadas à presença de alunos em atividades.
    """
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Aluno",
        related_name="observacoes_presenca_presencas"
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="observacoes_presenca_presencas"
    )
    data = models.DateField(verbose_name="Data")
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Atividade",
        related_name="observacoes_presenca"
    )
    texto = models.TextField(verbose_name="Observação", blank=True, null=True)
    registrado_por = models.CharField(
        max_length=100, 
        default="Sistema", 
        verbose_name="Registrado por"
    )
    data_registro = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Data de registro"
    )

    class Meta:
        verbose_name = "Observação de Presença"
        verbose_name_plural = "Observações de Presença"
        ordering = ["-data"]

    def __str__(self):
        atividade_str = str(self.atividade) if self.atividade else "Sem atividade"
        texto_trunc = self.texto[:30] if self.texto else "Sem observação"
        return f"{self.data} - {atividade_str} - {texto_trunc}"


class PresencaDetalhada(models.Model):
    """
    Modelo expandido para registro detalhado de presenças mensal.
    Replica funcionalidade Excel com campos: C (Convocação), P (Presença), 
    F (Falta), V1 (Voluntário Extra), V2 (Voluntário Simples).
    """
    
    aluno = models.ForeignKey(
        'alunos.Aluno',
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        related_name="presencas_detalhadas_expandidas"
    )
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="presencas_detalhadas_expandidas"
    )
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        verbose_name="Atividade",
        related_name="presencas_detalhadas_expandidas"
    )
    periodo = models.DateField(
        verbose_name="Período (Mês/Ano)",
        help_text="Data representando o mês/ano (usar primeiro dia do mês)"
    )
    
    # Campos Excel: C, P, F, V1, V2
    convocacoes = models.PositiveIntegerField(
        default=0,
        verbose_name="Convocações (C)",
        help_text="Número de convocações no período"
    )
    presencas = models.PositiveIntegerField(
        default=0,
        verbose_name="Presenças (P)",
        help_text="Número de presenças no período"
    )
    faltas = models.PositiveIntegerField(
        default=0,
        verbose_name="Faltas (F)",
        help_text="Número de faltas no período"
    )
    voluntario_extra = models.PositiveIntegerField(
        default=0,
        verbose_name="Voluntário Extra (V1)",
        help_text="Atividades voluntárias extras"
    )
    voluntario_simples = models.PositiveIntegerField(
        default=0,
        verbose_name="Voluntário Simples (V2)",
        help_text="Atividades voluntárias simples"
    )
    
    # Campos calculados
    percentual_presenca = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Percentual de Presença (%)",
        help_text="Calculado automaticamente"
    )
    total_voluntarios = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de Voluntários",
        help_text="V1 + V2"
    )
    carencias = models.PositiveIntegerField(
        default=0,
        verbose_name="Carências",
        help_text="Número de carências baseado no percentual da turma"
    )
    
    # Campos de controle
    registrado_por = models.CharField(
        max_length=100,
        default="Sistema",
        verbose_name="Registrado por"
    )
    data_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de registro"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de atualização"
    )
    
    class Meta:
        verbose_name = "Presença Detalhada"
        verbose_name_plural = "Presenças Detalhadas"
        ordering = ["-periodo", "aluno__nome"]
        unique_together = ["aluno", "turma", "atividade", "periodo"]
        
    def __str__(self):
        return f"{self.aluno.nome} - {self.periodo.strftime('%m/%Y')} - {self.atividade}"
    
    def calcular_percentual(self):
        """Calcula o percentual de presença baseado em convocações."""
        if self.convocacoes == 0:
            return Decimal('0.00')
        
        percentual = (Decimal(self.presencas) / Decimal(self.convocacoes)) * Decimal('100')
        return round(percentual, 2)
    
    def calcular_voluntarios(self):
        """Calcula o total de voluntários (V1 + V2)."""
        return self.voluntario_extra + self.voluntario_simples
    
    def calcular_carencias(self):
        """Calcula carências baseado na configuração específica da turma/atividade."""
        if not self.turma or not self.atividade:
            return 0
            
        # Verifica se existe configuração específica para esta turma/atividade
        try:
            configuracao = ConfiguracaoPresenca.objects.get(
                turma=self.turma,
                atividade=self.atividade,
                ativo=True
            )
            
            # Usa configuração específica
            percentual_atual = self.calcular_percentual()
            limite_carencia = configuracao.get_limite_carencia_por_percentual(percentual_atual)
            
            # Aplica peso no cálculo
            carencia_permitida = int(limite_carencia * float(configuracao.peso_calculo))
            
            # Calcula carências necessárias
            if self.convocacoes > 0:
                presencas_necessarias = self.convocacoes - carencia_permitida
                carencias = max(0, presencas_necessarias - self.presencas)
                return carencias
            
            return 0
            
        except ConfiguracaoPresenca.DoesNotExist:
            # Fallback para lógica original usando percentual da turma
            if not self.turma.perc_carencia:
                return 0
                
            percentual_atual = self.calcular_percentual()
            percentual_minimo = self.turma.perc_carencia
            
            if percentual_atual < percentual_minimo:
                # Calcula quantas presenças faltam para atingir o mínimo
                presencas_necessarias = (percentual_minimo * self.convocacoes) / 100
                carencias = int(presencas_necessarias - self.presencas)
                return max(0, carencias)
            
            return 0
    
    def clean(self):
        """Validações do modelo."""
        super().clean()
        
        # Validação: P + F deve ser <= C
        if self.presencas + self.faltas > self.convocacoes:
            raise ValidationError(
                "A soma de presenças e faltas não pode ser maior que convocações."
            )
        
        # Validação: período deve ser primeiro dia do mês
        if self.periodo and self.periodo.day != 1:
            raise ValidationError({
                "periodo": "O período deve ser o primeiro dia do mês."
            })
        
        # Validação: não pode ter valores negativos
        campos_positivos = ['convocacoes', 'presencas', 'faltas', 
                           'voluntario_extra', 'voluntario_simples']
        for campo in campos_positivos:
            valor = getattr(self, campo, 0)
            if valor < 0:
                raise ValidationError({
                    campo: f"O campo {campo} não pode ser negativo."
                })
    
    def save(self, *args, **kwargs):
        """Sobrescreve save para calcular campos automaticamente."""
        # Calcula campos automáticos
        self.percentual_presenca = self.calcular_percentual()
        self.total_voluntarios = self.calcular_voluntarios()
        self.carencias = self.calcular_carencias()
        
        # Executa validações
        self.clean()
        
        super().save(*args, **kwargs)
        
        logger.info(
            f"Presença detalhada salva: {self.aluno.nome} - "
            f"{self.periodo.strftime('%m/%Y')} - "
            f"Percentual: {self.percentual_presenca}%"
        )


class ConfiguracaoPresenca(models.Model):
    """
    Configurações específicas de presença por turma/atividade.
    Define limites de carência e parâmetros de cálculo conforme lógica do Excel.
    """
    
    # Relacionamentos
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="configuracoes_presenca"
    )
    atividade = models.ForeignKey(
        'atividades.Atividade',
        on_delete=models.CASCADE,
        verbose_name="Atividade",
        related_name="configuracoes_presenca"
    )
    
    # Campos de limites de carência (faixas percentuais)
    limite_carencia_0_25 = models.PositiveIntegerField(
        default=0,
        verbose_name="Limite Carência 0-25%",
        help_text="Número máximo de carências para presença entre 0-25%"
    )
    limite_carencia_26_50 = models.PositiveIntegerField(
        default=0,
        verbose_name="Limite Carência 26-50%",
        help_text="Número máximo de carências para presença entre 26-50%"
    )
    limite_carencia_51_75 = models.PositiveIntegerField(
        default=0,
        verbose_name="Limite Carência 51-75%",
        help_text="Número máximo de carências para presença entre 51-75%"
    )
    limite_carencia_76_100 = models.PositiveIntegerField(
        default=0,
        verbose_name="Limite Carência 76-100%",
        help_text="Número máximo de carências para presença entre 76-100%"
    )
    
    # Campos de configuração
    obrigatoria = models.BooleanField(
        default=True,
        verbose_name="Obrigatória",
        help_text="Define se a atividade é obrigatória para a turma"
    )
    peso_calculo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('1.00'),
        verbose_name="Peso no Cálculo",
        help_text="Peso da atividade no cálculo geral de carências"
    )
    
    # Campos de controle
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    registrado_por = models.CharField(
        max_length=100,
        default="Sistema",
        verbose_name="Registrado por"
    )
    data_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de registro"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de atualização"
    )
    
    class Meta:
        verbose_name = "Configuração de Presença"
        verbose_name_plural = "Configurações de Presença"
        ordering = ["turma__nome", "atividade__nome"]
        unique_together = ["turma", "atividade"]
    
    def __str__(self):
        return f"{self.turma} - {self.atividade}"
    
    def get_limite_carencia_por_percentual(self, percentual):
        """
        Retorna o limite de carência baseado no percentual de presença.
        
        Args:
            percentual (Decimal): Percentual de presença (0-100)
            
        Returns:
            int: Limite de carência para o percentual informado
        """
        if percentual <= 25:
            return self.limite_carencia_0_25
        elif percentual <= 50:
            return self.limite_carencia_26_50
        elif percentual <= 75:
            return self.limite_carencia_51_75
        else:
            return self.limite_carencia_76_100
    
    def calcular_carencia_permitida(self, presenca_detalhada):
        """
        Calcula a carência permitida para uma presença detalhada específica.
        
        Args:
            presenca_detalhada (PresencaDetalhada): Instância de presença detalhada
            
        Returns:
            int: Número de carências permitidas
        """
        if not presenca_detalhada:
            return 0
        
        percentual = presenca_detalhada.percentual_presenca
        limite_base = self.get_limite_carencia_por_percentual(percentual)
        
        # Aplica peso no cálculo
        carencia_permitida = int(limite_base * float(self.peso_calculo))
        
        return carencia_permitida
    
    def clean(self):
        """Validações do modelo."""
        super().clean()
        
        # Validação: peso deve ser positivo
        if self.peso_calculo <= 0:
            raise ValidationError({
                "peso_calculo": "O peso no cálculo deve ser maior que zero."
            })
        
        # Validação: limites não podem ser negativos
        limites = [
            ('limite_carencia_0_25', self.limite_carencia_0_25),
            ('limite_carencia_26_50', self.limite_carencia_26_50),
            ('limite_carencia_51_75', self.limite_carencia_51_75),
            ('limite_carencia_76_100', self.limite_carencia_76_100),
        ]
        
        for nome_campo, valor in limites:
            if valor < 0:
                raise ValidationError({
                    nome_campo: "O limite de carência não pode ser negativo."
                })
    
    def save(self, *args, **kwargs):
        """Sobrescreve save para executar validações."""
        self.clean()
        super().save(*args, **kwargs)
        
        logger.info(
            f"Configuração de presença salva: {self.turma} - {self.atividade}"
        )


class AgendamentoRelatorio(models.Model):
    """
    Modelo para agendamento de relatórios automáticos.
    """
    
    FORMATO_CHOICES = [
        ('excel_basico', 'Excel Básico (.xlsx)'),
        ('excel_avancado', 'Excel Profissional (.xlsx)'),
        ('excel_graficos', 'Excel com Gráficos (.xlsx)'),
        ('csv', 'CSV (.csv)'),
        ('pdf_simples', 'PDF Simples (.pdf)'),
        ('pdf_completo', 'PDF Completo (.pdf)'),
    ]
    
    TEMPLATE_CHOICES = [
        ('consolidado_geral', 'Consolidado Geral'),
        ('por_turma', 'Relatório por Turma'),
        ('por_curso', 'Relatório por Curso'),
        ('estatisticas_executivas', 'Estatísticas Executivas'),
        ('carencia_presencas', 'Relatório de Carência'),
        ('comparativo_temporal', 'Comparativo Temporal'),
    ]
    
    PERIODO_CHOICES = [
        ('atual', 'Período Atual'),
        ('ultimo_mes', 'Último Mês'),
        ('ultimo_trimestre', 'Último Trimestre'),
        ('ultimo_semestre', 'Último Semestre'),
        ('ano_atual', 'Ano Atual'),
        ('personalizado', 'Período Personalizado'),
    ]
    
    FREQUENCIA_CHOICES = [
        ('diario', 'Diário'),
        ('semanal', 'Semanal'),
        ('quinzenal', 'Quinzenal'),
        ('mensal', 'Mensal'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]
    
    # Campos básicos
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Agendamento"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name="agendamentos_relatorio"
    )
    
    # Configurações do relatório
    formato = models.CharField(
        max_length=20,
        choices=FORMATO_CHOICES,
        default='excel_avancado',
        verbose_name="Formato"
    )
    
    template = models.CharField(
        max_length=30,
        choices=TEMPLATE_CHOICES,
        default='consolidado_geral',
        verbose_name="Template"
    )
    
    titulo_personalizado = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Título Personalizado"
    )
    
    # Filtros
    periodo = models.CharField(
        max_length=20,
        choices=PERIODO_CHOICES,
        default='atual',
        verbose_name="Período"
    )
    
    data_inicio = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data Início"
    )
    
    data_fim = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data Fim"
    )
    
    turma = models.ForeignKey(
        'turmas.Turma',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Turma",
        related_name="agendamentos_relatorio"
    )
    
    curso = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Curso"
    )
    
    # Opções avançadas
    incluir_graficos = models.BooleanField(
        default=True,
        verbose_name="Incluir Gráficos"
    )
    
    incluir_estatisticas = models.BooleanField(
        default=True,
        verbose_name="Incluir Estatísticas"
    )
    
    # Agendamento
    frequencia = models.CharField(
        max_length=15,
        choices=FREQUENCIA_CHOICES,
        default='mensal',
        verbose_name="Frequência"
    )
    
    dia_semana = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Dia da Semana (0=Segunda)",
        help_text="0=Segunda, 1=Terça, ..., 6=Domingo"
    )
    
    dia_mes = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Dia do Mês",
        help_text="Dia do mês para execução (1-31)"
    )
    
    hora_execucao = models.TimeField(
        default='08:00',
        verbose_name="Hora de Execução"
    )
    
    # Email
    emails_destino = models.TextField(
        verbose_name="Emails de Destino",
        help_text="Emails separados por vírgula"
    )
    
    # Controle
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    proxima_execucao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Próxima Execução"
    )
    
    ultima_execucao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Última Execução"
    )
    
    # Metadados
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Agendamento de Relatório"
        verbose_name_plural = "Agendamentos de Relatórios"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.nome} - {self.get_frequencia_display()}"
    
    def clean(self):
        """Validações customizadas."""
        
        if self.periodo == 'personalizado':
            if not self.data_inicio or not self.data_fim:
                raise ValidationError(
                    "Data início e fim são obrigatórias para período personalizado"
                )
            
            if self.data_inicio > self.data_fim:
                raise ValidationError(
                    "Data início deve ser anterior à data fim"
                )
        
        if self.frequencia == 'semanal' and self.dia_semana is None:
            raise ValidationError(
                "Dia da semana é obrigatório para frequência semanal"
            )
        
        if self.frequencia in ['mensal', 'trimestral', 'semestral', 'anual'] and self.dia_mes is None:
            raise ValidationError(
                f"Dia do mês é obrigatório para frequência {self.frequencia}"
            )
        
        # Validar emails
        if self.emails_destino:
            emails = [email.strip() for email in self.emails_destino.split(',')]
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError as DjangoValidationError
            
            for email in emails:
                try:
                    validate_email(email)
                except DjangoValidationError:
                    raise ValidationError(f"Email inválido: {email}")
    
    def save(self, *args, **kwargs):
        """Sobrescreve save para calcular próxima execução."""
        
        self.clean()
        
        if not self.proxima_execucao:
            self.calcular_proxima_execucao()
        
        super().save(*args, **kwargs)
    
    def calcular_proxima_execucao(self):
        """Calcula a próxima data de execução baseada na frequência."""
        
        from datetime import timedelta
        from django.utils import timezone
        
        agora = timezone.now()
        base_date = agora.replace(
            hour=self.hora_execucao.hour,
            minute=self.hora_execucao.minute,
            second=0,
            microsecond=0
        )
        
        if self.frequencia == 'diario':
            if base_date <= agora:
                base_date += timedelta(days=1)
            self.proxima_execucao = base_date
            
        elif self.frequencia == 'semanal':
            dias_ate_target = (self.dia_semana - agora.weekday()) % 7
            if dias_ate_target == 0 and base_date <= agora:
                dias_ate_target = 7
            self.proxima_execucao = base_date + timedelta(days=dias_ate_target)
            
        elif self.frequencia == 'quinzenal':
            # Próxima quinzena
            if agora.day <= 15:
                if self.dia_mes <= 15:
                    target_day = self.dia_mes
                    target_month = agora.month
                    target_year = agora.year
                else:
                    target_day = self.dia_mes - 15
                    if agora.month == 12:
                        target_month = 1
                        target_year = agora.year + 1
                    else:
                        target_month = agora.month + 1
                        target_year = agora.year
            else:
                target_day = self.dia_mes
                if agora.month == 12:
                    target_month = 1
                    target_year = agora.year + 1
                else:
                    target_month = agora.month + 1
                    target_year = agora.year
            
            self.proxima_execucao = base_date.replace(
                year=target_year,
                month=target_month,
                day=min(target_day, 28)  # Evitar problemas com meses
            )
            
        elif self.frequencia == 'mensal':
            if agora.day < self.dia_mes:
                target_month = agora.month
                target_year = agora.year
            else:
                if agora.month == 12:
                    target_month = 1
                    target_year = agora.year + 1
                else:
                    target_month = agora.month + 1
                    target_year = agora.year
            
            self.proxima_execucao = base_date.replace(
                year=target_year,
                month=target_month,
                day=min(self.dia_mes, 28)
            )
            
        elif self.frequencia == 'trimestral':
            # A cada 3 meses
            meses_adicionar = 3
            target_month = agora.month + meses_adicionar
            target_year = agora.year
            
            while target_month > 12:
                target_month -= 12
                target_year += 1
            
            self.proxima_execucao = base_date.replace(
                year=target_year,
                month=target_month,
                day=min(self.dia_mes, 28)
            )
            
        elif self.frequencia == 'semestral':
            # A cada 6 meses
            meses_adicionar = 6
            target_month = agora.month + meses_adicionar
            target_year = agora.year
            
            while target_month > 12:
                target_month -= 12
                target_year += 1
            
            self.proxima_execucao = base_date.replace(
                year=target_year,
                month=target_month,
                day=min(self.dia_mes, 28)
            )
            
        elif self.frequencia == 'anual':
            target_year = agora.year
            if agora.month > self.dia_mes or (
                agora.month == self.dia_mes and agora.day >= self.dia_mes
            ):
                target_year += 1
            
            self.proxima_execucao = base_date.replace(
                year=target_year,
                month=self.dia_mes,
                day=min(self.dia_mes, 28)
            )
    
    def atualizar_proxima_execucao(self):
        """Atualiza próxima execução após execução atual."""
        
        self.ultima_execucao = timezone.now()
        self.calcular_proxima_execucao()
        self.save()
