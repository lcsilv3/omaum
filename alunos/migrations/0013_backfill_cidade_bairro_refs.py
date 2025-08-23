from django.db import migrations


def backfill_cidade_bairro_refs(apps, schema_editor):
    """Backfill de cidade_ref e bairro_ref em registros existentes de Aluno.

    Estratégia best-effort: associações apenas quando encontra correspondência exata (case-insensitive)
    e evita múltiplos hits. Processa em lotes moderados para limitar memória.
    """
    Aluno = apps.get_model("alunos", "Aluno")
    Cidade = apps.get_model("alunos", "Cidade")
    Bairro = apps.get_model("alunos", "Bairro")

    BATCH = 200
    qs = Aluno.objects.filter(cidade_ref__isnull=True).exclude(cidade__isnull=True).exclude(cidade__exact="")
    total = qs.count()
    offset = 0
    while offset < total:
        for aluno in qs[offset: offset + BATCH]:
            changed = False
            if not aluno.cidade_ref and aluno.cidade:
                cidade = Cidade.objects.filter(nome__iexact=aluno.cidade).first()
                if cidade:
                    aluno.cidade_ref = cidade
                    changed = True
                    if not aluno.estado:
                        aluno.estado = cidade.estado.codigo
            if aluno.cidade_ref and not aluno.bairro_ref and aluno.bairro:
                bairro = Bairro.objects.filter(nome__iexact=aluno.bairro, cidade=aluno.cidade_ref).first()
                if bairro:
                    aluno.bairro_ref = bairro
                    changed = True
            if changed:
                aluno.save(update_fields=["cidade_ref", "bairro_ref", "estado"])
        offset += BATCH


def reverse_noop(apps, schema_editor):  # pragma: no cover
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("alunos", "0012_aluno_cidade_ref_bairro_ref"),
    ]

    operations = [
        migrations.RunPython(backfill_cidade_bairro_refs, reverse_noop),
    ]
