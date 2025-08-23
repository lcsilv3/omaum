from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("alunos", "0009_add_historico_checksum_field"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bairro",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100, verbose_name="Nome do Bairro")),
                (
                    "codigo_externo",
                    models.CharField(
                        blank=True,
                        max_length=30,
                        null=True,
                        verbose_name="Código Externo",
                    ),
                ),
                (
                    "cidade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bairros",
                        to="alunos.cidade",
                        verbose_name="Cidade",
                    ),
                ),
            ],
            options={
                "verbose_name": "Bairro",
                "verbose_name_plural": "Bairros",
                "ordering": ["nome"],
                "unique_together": {("nome", "cidade")},
            },
        ),
        migrations.AddIndex(
            model_name="bairro",
            index=models.Index(fields=["nome"], name="alunos_bairr_nome_idx"),
        ),
        migrations.AddIndex(
            model_name="bairro",
            index=models.Index(fields=["cidade"], name="alunos_bairr_cidade_idx"),
        ),
    ]
