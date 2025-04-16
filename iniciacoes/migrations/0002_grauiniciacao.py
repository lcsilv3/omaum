# Generated by Django 5.1.7 on 2025-04-07 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("iniciacoes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GrauIniciacao",
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
                        max_length=100, verbose_name="Nome do Grau"
                    ),
                ),
                (
                    "descricao",
                    models.TextField(
                        blank=True, null=True, verbose_name="Descrição"
                    ),
                ),
                (
                    "ordem",
                    models.PositiveIntegerField(
                        unique=True, verbose_name="Ordem"
                    ),
                ),
            ],
            options={
                "verbose_name": "Grau de Iniciação",
                "verbose_name_plural": "Graus de Iniciação",
                "ordering": ["ordem"],
            },
        ),
    ]
