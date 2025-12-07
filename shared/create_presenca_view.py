import os
import sys

sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")

import django
from django.db import connection

django.setup()

SQL_DROP = "DROP VIEW IF EXISTS presencas_presencadetalhada"
SQL_CREATE = """
CREATE VIEW presencas_presencadetalhada AS
SELECT
  rp.aluno_id,
  rp.turma_id,
  rp.atividade_id,
  date_trunc('month', rp.data)::date AS periodo,
  SUM(CASE WHEN rp.convocado THEN 1 ELSE 0 END) AS convocacoes,
  SUM(CASE WHEN rp.status = 'P' THEN 1 ELSE 0 END) AS presencas,
  SUM(CASE WHEN rp.status IN ('F','J') THEN 1 ELSE 0 END) AS faltas,
  SUM(CASE WHEN rp.status = 'V1' THEN 1 ELSE 0 END) AS voluntario_extra,
  SUM(CASE WHEN rp.status = 'V2' THEN 1 ELSE 0 END) AS voluntario_simples,
  SUM(CASE WHEN rp.status IN ('F','J') THEN 1 ELSE 0 END) AS carencias
FROM presencas_registropresenca rp
GROUP BY
  rp.aluno_id,
  rp.turma_id,
  rp.atividade_id,
  date_trunc('month', rp.data)::date
"""


def recreate_view() -> tuple[str | None, str | None]:
    """Drop e recria a view de presenças detalhadas (PostgreSQL)."""

    with connection.cursor() as cursor:
        cursor.execute("select version();")
        db_version = cursor.fetchone()[0]
        cursor.execute(SQL_DROP)
        cursor.execute(SQL_CREATE)
        cursor.execute("select to_regclass('presencas_presencadetalhada');")
        regclass = cursor.fetchone()[0]

    return db_version, regclass


if __name__ == "__main__":
    db_version, regclass = recreate_view()
    print("view recreated")
    print(f"database: {db_version}")
    print(f"regclass: {regclass}")
