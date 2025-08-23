"""Migration de otimização de índices (revisada).

Esta versão remove SQL bruto inválido/incompatível e cria apenas índices
realistas baseados nos campos existentes de `PresencaDetalhada`.

Compatível com SQLite (dev/test) e outros backends.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("presencas", "0005_alter_presenca_unique_together"),
    ]

    operations = [
        # Índice para buscas por aluno no período
        migrations.AddIndex(
            model_name="presencadetalhada",
            index=models.Index(
                fields=["aluno", "-periodo"], name="pd_aluno_periodo"
            ),
        ),
        # Índice por turma e período
        migrations.AddIndex(
            model_name="presencadetalhada",
            index=models.Index(
                fields=["turma", "periodo"], name="pd_turma_periodo"
            ),
        ),
        # Índice por atividade e período
        migrations.AddIndex(
            model_name="presencadetalhada",
            index=models.Index(
                fields=["atividade", "periodo"], name="pd_ativ_periodo"
            ),
        ),
        # Índice composto mais seletivo para relatórios específicos
        migrations.AddIndex(
            model_name="presencadetalhada",
            index=models.Index(
                fields=["aluno", "atividade", "periodo"], name="pd_aln_ativ_per"
            ),
        ),
    ]
