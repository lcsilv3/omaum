from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("alunos", "0011_rename_alunos_bairr_nome_idx_alunos_bair_nome_3317e8_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="aluno",
            name="cidade_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="alunos_cidade",
                to="alunos.cidade",
                verbose_name="Cidade (Ref)",
                help_text="Referência normalizada da cidade (mantém campo texto para compatibilidade)",
            ),
        ),
        migrations.AddField(
            model_name="aluno",
            name="bairro_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="alunos_bairro",
                to="alunos.bairro",
                verbose_name="Bairro (Ref)",
                help_text="Referência normalizada do bairro (mantém campo texto para compatibilidade)",
            ),
        ),
        migrations.AddIndex(
            model_name="aluno",
            index=models.Index(fields=["cidade_ref"], name="aluno_cidade_ref_idx"),
        ),
        migrations.AddIndex(
            model_name="aluno",
            index=models.Index(fields=["bairro_ref"], name="aluno_bairro_ref_idx"),
        ),
    ]
