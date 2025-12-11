from decimal import Decimal

from django.db import migrations, models


def set_default_perc_presenca(apps, schema_editor):
    Turma = apps.get_model("turmas", "Turma")
    Turma.objects.filter(perc_presenca_minima__isnull=True).update(
        perc_presenca_minima=Decimal("70.00")
    )


class Migration(migrations.Migration):
    dependencies = [
        ("turmas", "0004_remove_turma_data_fim_remove_turma_data_inicio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="turma",
            name="perc_presenca_minima",
            field=models.DecimalField(
                max_digits=5,
                decimal_places=2,
                blank=True,
                null=True,
                default=70,
                verbose_name="Percentual Mínimo de Presença (%)",
                help_text="Percentual mínimo de presenças permitido para a turma",
            ),
        ),
        migrations.RunPython(set_default_perc_presenca, migrations.RunPython.noop),
    ]
