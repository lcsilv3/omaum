"""
FASE 3C: Configurações de índices para otimização de banco de dados.
"""

from django.db import migrations


class Migration(migrations.Migration):
    """
    Migration para criar índices compostos otimizados para o sistema de presenças.
    """

    dependencies = [
        ("presencas", "0005_alter_presenca_unique_together"),
    ]

    operations = [
        # Índices compostos para PresencaDetalhada
        migrations.RunSQL(
            # Índice principal para consultas por período e turma
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_periodo_turma "
                "ON presencas_presencadetalhada (periodo, turma_id);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_periodo_turma;",
        ),
        migrations.RunSQL(
            # Índice para consultas por aluno e período (mais comum)
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_aluno_periodo "
                "ON presencas_presencadetalhada (aluno_id, periodo DESC);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_aluno_periodo;",
        ),
        migrations.RunSQL(
            # Índice composto para estatísticas por atividade
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_atividade_presente "
                "ON presencas_presencadetalhada (atividade_id, presente, periodo);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_atividade_presente;",
            hints={"check_column_exists": "presente"},  # Adiciona verificação
        ),
        migrations.RunSQL(
            # Índice para consultas por curso e período
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_curso_periodo "
                "ON presencas_presencadetalhada (curso, periodo);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_curso_periodo;",
        ),
        migrations.RunSQL(
            # Índice para ordenação por data de criação (últimas presenças)
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_criado_em "
                "ON presencas_presencadetalhada (criado_em DESC);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_criado_em;",
        ),
        migrations.RunSQL(
            # Índice composto para filtros de exportação avançada
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_export "
                "ON presencas_presencadetalhada (turma_id, curso, periodo, presente);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_export;",
        ),
        # Índices para outras tabelas importantes
        migrations.RunSQL(
            # Índice para consultas de alunos por turma
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_aluno_turma_nome "
                "ON presencas_aluno (turma_id, nome);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_aluno_turma_nome;",
        ),
        migrations.RunSQL(
            # Índice para atividades por curso e data
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_atividade_curso_data "
                "ON presencas_atividade (curso, data_atividade DESC);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_atividade_curso_data;",
        ),
        migrations.RunSQL(
            # Índice para agendamentos ativos
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_agendamento_ativo "
                "ON presencas_agendamentoemail (ativo, proxima_execucao);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_agendamento_ativo;",
        ),
        # Índices parciais para casos específicos
        migrations.RunSQL(
            # Índice apenas para presenças confirmadas (presente=True)
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_confirmada "
                "ON presencas_presencadetalhada (periodo, turma_id) "
                "WHERE presente = true;"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_confirmada;",
        ),
        migrations.RunSQL(
            # Índice para presenças dos últimos 90 dias (mais consultadas)
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_recente "
                "ON presencas_presencadetalhada (aluno_id, periodo) "
                "WHERE periodo >= CURRENT_DATE - INTERVAL '90 days';"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_recente;",
        ),
        # Índices para campos de auditoria
        migrations.RunSQL(
            # Índice para rastreamento de quem registrou presenças
            sql=(
                "CREATE INDEX IF NOT EXISTS idx_presenca_registrado_por "
                "ON presencas_presencadetalhada (registrado_por, criado_em);"
            ),
            reverse_sql="DROP INDEX IF EXISTS idx_presenca_registrado_por;",
        ),
        # Análise de performance - executar ANALYZE após criar índices
        migrations.RunSQL(sql="ANALYZE presencas_presencadetalhada;", reverse_sql=""),
        migrations.RunSQL(sql="ANALYZE presencas_aluno;", reverse_sql=""),
        migrations.RunSQL(sql="ANALYZE presencas_atividade;", reverse_sql=""),
    ]
