# Generated by Django 5.1.7 on 2025-04-14 14:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alunos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aluno",
            name="situacao",
            field=models.CharField(
                choices=[
                    ("ATIVO", "Ativo"),
                    ("AFASTADO", "Afastado"),
                    ("ESPECIAIS", "Especiais"),
                    ("EXCLUIDO", "Excluído"),
                    ("FALECIDO", "Falecido"),
                    ("LOI", "LOI"),
                ],
                default="ATIVO",
                max_length=10,
                verbose_name="Situação",
            ),
        ),
    ]
