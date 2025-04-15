# Generated by Django 5.1.7 on 2025-04-14 17:50

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alunos", "0002_aluno_situacao"),
        ("cursos", "0001_initial"),
        (
            "turmas",
            "0004_alter_turma_unique_together_turma_alerta_instrutor_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="turma",
            name="alerta_instrutor",
        ),
        migrations.RemoveField(
            model_name="turma",
            name="alerta_mensagem",
        ),
        migrations.AddField(
            model_name="turma",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Criado em"
            ),
        ),
        migrations.AddField(
            model_name="turma",
            name="dias_semana",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name="Dias da Semana",
            ),
        ),
        migrations.AddField(
            model_name="turma",
            name="horario",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Horário"
            ),
        ),
        migrations.AddField(
            model_name="turma",
            name="local",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Local"
            ),
        ),
        migrations.AddField(
            model_name="turma",
            name="updated_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Atualizado em"
            ),
        ),
        migrations.AlterField(
            model_name="turma",
            name="curso",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="turmas",
                to="cursos.curso",
                verbose_name="Curso",
            ),
        ),
        migrations.AlterField(
            model_name="turma",
            name="instrutor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="turmas_como_instrutor",
                to="alunos.aluno",
                verbose_name="Instrutor Principal",
            ),
        ),
        migrations.AlterField(
            model_name="turma",
            name="vagas",
            field=models.PositiveIntegerField(
                default=20,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Número de Vagas",
            ),
        ),
    ]
