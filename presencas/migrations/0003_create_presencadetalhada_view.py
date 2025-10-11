# Generated manually to recreate the legacy view for development environments.
from django.db import migrations


SQLITE_DROP_VIEW = "DROP VIEW IF EXISTS presencas_presencadetalhada"

SQLITE_CREATE_VIEW = """
CREATE VIEW presencas_presencadetalhada AS
SELECT
    rp.aluno_id,
    rp.turma_id,
    rp.atividade_id,
    DATE(rp.data, 'start of month') AS periodo,
    SUM(CASE WHEN rp.convocado = 1 THEN 1 ELSE 0 END) AS convocacoes,
    SUM(CASE WHEN rp.status = 'P' THEN 1 ELSE 0 END) AS presencas,
    SUM(CASE WHEN rp.status IN ('F', 'J') THEN 1 ELSE 0 END) AS faltas,
    SUM(CASE WHEN rp.status = 'V1' THEN 1 ELSE 0 END) AS voluntario_extra,
    SUM(CASE WHEN rp.status = 'V2' THEN 1 ELSE 0 END) AS voluntario_simples,
    SUM(CASE WHEN rp.status IN ('F', 'J') THEN 1 ELSE 0 END) AS carencias
FROM presencas_registropresenca AS rp
GROUP BY
    rp.aluno_id,
    rp.turma_id,
    rp.atividade_id,
    DATE(rp.data, 'start of month');
"""


def create_view(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS presencas_presencadetalhada")
        cursor.execute(SQLITE_DROP_VIEW)
        cursor.execute(SQLITE_CREATE_VIEW)


def drop_view(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(SQLITE_DROP_VIEW)


class Migration(migrations.Migration):
    dependencies = [
        ("presencas", "0002_alter_configuracaopresenca_unique_together_and_more"),
    ]

    operations = [
        migrations.RunPython(create_view, drop_view),
    ]
