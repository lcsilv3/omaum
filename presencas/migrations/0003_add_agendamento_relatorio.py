# Generated manually for exportacao avancada

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("turmas", "0001_initial"),
        ("presencas", "0002_configuracaopresenca_presencadetalhada"),
    ]

    operations = [
        migrations.CreateModel(
            name="AgendamentoRelatorio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(
                        max_length=200, verbose_name="Nome do Agendamento"
                    ),
                ),
                (
                    "formato",
                    models.CharField(
                        choices=[
                            ("excel_basico", "Excel Básico (.xlsx)"),
                            ("excel_avancado", "Excel Profissional (.xlsx)"),
                            ("excel_graficos", "Excel com Gráficos (.xlsx)"),
                            ("csv", "CSV (.csv)"),
                            ("pdf_simples", "PDF Simples (.pdf)"),
                            ("pdf_completo", "PDF Completo (.pdf)"),
                        ],
                        default="excel_avancado",
                        max_length=20,
                        verbose_name="Formato",
                    ),
                ),
                (
                    "template",
                    models.CharField(
                        choices=[
                            ("consolidado_geral", "Consolidado Geral"),
                            ("por_turma", "Relatório por Turma"),
                            ("por_curso", "Relatório por Curso"),
                            ("estatisticas_executivas", "Estatísticas Executivas"),
                            ("carencia_presencas", "Relatório de Carência"),
                            ("comparativo_temporal", "Comparativo Temporal"),
                        ],
                        default="consolidado_geral",
                        max_length=30,
                        verbose_name="Template",
                    ),
                ),
                (
                    "titulo_personalizado",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="Título Personalizado"
                    ),
                ),
                (
                    "periodo",
                    models.CharField(
                        choices=[
                            ("atual", "Período Atual"),
                            ("ultimo_mes", "Último Mês"),
                            ("ultimo_trimestre", "Último Trimestre"),
                            ("ultimo_semestre", "Último Semestre"),
                            ("ano_atual", "Ano Atual"),
                            ("personalizado", "Período Personalizado"),
                        ],
                        default="atual",
                        max_length=20,
                        verbose_name="Período",
                    ),
                ),
                (
                    "data_inicio",
                    models.DateField(blank=True, null=True, verbose_name="Data Início"),
                ),
                (
                    "data_fim",
                    models.DateField(blank=True, null=True, verbose_name="Data Fim"),
                ),
                (
                    "curso",
                    models.CharField(blank=True, max_length=200, verbose_name="Curso"),
                ),
                (
                    "incluir_graficos",
                    models.BooleanField(default=True, verbose_name="Incluir Gráficos"),
                ),
                (
                    "incluir_estatisticas",
                    models.BooleanField(
                        default=True, verbose_name="Incluir Estatísticas"
                    ),
                ),
                (
                    "frequencia",
                    models.CharField(
                        choices=[
                            ("diario", "Diário"),
                            ("semanal", "Semanal"),
                            ("quinzenal", "Quinzenal"),
                            ("mensal", "Mensal"),
                            ("trimestral", "Trimestral"),
                            ("semestral", "Semestral"),
                            ("anual", "Anual"),
                        ],
                        default="mensal",
                        max_length=15,
                        verbose_name="Frequência",
                    ),
                ),
                (
                    "dia_semana",
                    models.IntegerField(
                        blank=True,
                        help_text="0=Segunda, 1=Terça, ..., 6=Domingo",
                        null=True,
                        verbose_name="Dia da Semana (0=Segunda)",
                    ),
                ),
                (
                    "dia_mes",
                    models.IntegerField(
                        blank=True,
                        help_text="Dia do mês para execução (1-31)",
                        null=True,
                        verbose_name="Dia do Mês",
                    ),
                ),
                (
                    "hora_execucao",
                    models.TimeField(default="08:00", verbose_name="Hora de Execução"),
                ),
                (
                    "emails_destino",
                    models.TextField(
                        help_text="Emails separados por vírgula",
                        verbose_name="Emails de Destino",
                    ),
                ),
                ("ativo", models.BooleanField(default=True, verbose_name="Ativo")),
                (
                    "proxima_execucao",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Próxima Execução"
                    ),
                ),
                (
                    "ultima_execucao",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Última Execução"
                    ),
                ),
                (
                    "criado_em",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
                (
                    "atualizado_em",
                    models.DateTimeField(auto_now=True, verbose_name="Atualizado em"),
                ),
                (
                    "turma",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agendamentos_relatorio",
                        to="turmas.turma",
                        verbose_name="Turma",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agendamentos_relatorio",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuário",
                    ),
                ),
            ],
            options={
                "verbose_name": "Agendamento de Relatório",
                "verbose_name_plural": "Agendamentos de Relatórios",
                "ordering": ["-criado_em"],
            },
        ),
    ]
