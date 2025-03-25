# Generated by Django 5.1.7 on 2025-03-25 14:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('atividades', '0001_initial'),
    ]

    operations = [
        # For AtividadeAcademica
        migrations.RenameField(
            model_name='atividadeacademica',
            old_name='data',
            new_name='data_inicio',
        ),
        migrations.AddField(
            model_name='atividadeacademica',
            name='data_fim',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # For AtividadeRitualistica
        migrations.RenameField(
            model_name='atividaderitualistica',
            old_name='data',
            new_name='data_inicio',
        ),
        migrations.AddField(
            model_name='atividaderitualistica',
            name='data_fim',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
