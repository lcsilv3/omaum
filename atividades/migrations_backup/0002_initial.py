# Generated by Django 5.1.7 on 2025-04-01 22:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '0001_initial'),
        ('atividades', '0001_initial'),
        ('turmas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividadeacademica',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividades_academicas', to='turmas.turma'),
        ),
        migrations.AddField(
            model_name='atividaderitualistica',
            name='alunos',
            field=models.ManyToManyField(related_name='atividades_ritualisticas', to='alunos.aluno'),
        ),
        migrations.AddField(
            model_name='atividaderitualistica',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividades_ritualisticas', to='turmas.turma'),
        ),
    ]
