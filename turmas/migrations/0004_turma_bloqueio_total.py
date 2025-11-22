from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("turmas", "0003_turma_datas_encerramento"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="turma",
            name="bloqueio_total",
            field=models.BooleanField(
                default=False,
                help_text="Indica se a turma está com todos os relacionamentos bloqueados.",
                verbose_name="Bloqueio Total",
            ),
        ),
        migrations.AddField(
            model_name="turma",
            name="bloqueio_ativo_em",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Bloqueio ativado em"
            ),
        ),
        migrations.AddField(
            model_name="turma",
            name="bloqueio_ativo_por",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="turmas_bloqueadas",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Bloqueio ativado por",
            ),
        ),
        migrations.AddField(
            model_name="turma",
            name="justificativa_reabertura",
            field=models.TextField(
                blank=True, null=True, verbose_name="Justificativa de Reabertura"
            ),
        ),
    ]
