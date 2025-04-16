# Generated by Django 5.1.7 on 2025-04-12 17:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("alunos", "0001_initial"),
        ("turmas", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Matricula",
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
                    "data_matricula",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ATIVA", "Ativa"),
                            ("CANCELADA", "Cancelada"),
                            ("CONCLUIDA", "Concluída"),
                            ("TRANCADA", "Trancada"),
                        ],
                        default="ATIVA",
                        max_length=20,
                    ),
                ),
                (
                    "aluno",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="matriculas",
                        to="alunos.aluno",
                    ),
                ),
                (
                    "turma",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="matriculas",
                        to="turmas.turma",
                    ),
                ),
            ],
            options={
                "verbose_name": "Matrícula",
                "verbose_name_plural": "Matrículas",
                "unique_together": {("aluno", "turma")},
            },
        ),
    ]
