from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alunos", "0005_alter_aluno_situacao_iniciatica"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="registrohistorico",
            options={
                "verbose_name": "Registro Histórico",
                "verbose_name_plural": "Registros Históricos",
                "ordering": ["-data_os", "-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="registrohistorico",
            index=models.Index(
                fields=["aluno", "-data_os"], name="rh_aluno_dataos_desc"
            ),
        ),
        migrations.AddIndex(
            model_name="registrohistorico",
            index=models.Index(fields=["codigo"], name="rh_codigo_idx"),
        ),
    ]
