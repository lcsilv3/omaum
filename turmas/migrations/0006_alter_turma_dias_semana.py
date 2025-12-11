from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("turmas", "0005_alter_turma_perc_presenca_minima"),
    ]

    operations = [
        migrations.AlterField(
            model_name="turma",
            name="dias_semana",
            field=models.CharField(
                blank=True,
                choices=[
                    ("SEG", "Segunda-feira"),
                    ("TER", "Terça-feira"),
                    ("QUA", "Quarta-feira"),
                    ("QUI", "Quinta-feira"),
                    ("SEX", "Sexta-feira"),
                    ("SAB", "Sábado"),
                    ("DOM", "Domingo"),
                ],
                max_length=20,
                null=True,
                verbose_name="Dia da Semana",
            ),
        ),
    ]
