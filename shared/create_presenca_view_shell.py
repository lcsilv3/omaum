from django.db import connection

cursor = connection.cursor()
cursor.execute("DROP VIEW IF EXISTS presencas_presencadetalhada;")
cursor.execute(
    """
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
)
cursor.execute("select to_regclass('presencas_presencadetalhada');")
print(cursor.fetchone())
