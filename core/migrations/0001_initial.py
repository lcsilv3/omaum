# Generated by Django 5.1.7 on 2025-03-23 21:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_sistema', models.CharField(default='OMAUM', max_length=100)),
                ('versao', models.CharField(default='1.0.0', max_length=20)),
                ('data_atualizacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('manutencao_ativa', models.BooleanField(default=False)),
                ('mensagem_manutencao', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Configuração do Sistema',
                'verbose_name_plural': 'Configurações do Sistema',
            },
        ),
        migrations.CreateModel(
            name='LogAtividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('acao', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('INFO', 'Informação'), ('AVISO', 'Aviso'), ('ERRO', 'Erro'), ('DEBUG', 'Depuração')], default='INFO', max_length=10)),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('detalhes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Log de Atividade',
                'verbose_name_plural': 'Logs de Atividades',
                'ordering': ['-data'],
            },
        ),
    ]
