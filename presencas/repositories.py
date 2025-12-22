"""
Repositórios para o aplicativo presencas.
Camada de acesso a dados.
"""

from django.db.models import Q, Count
from datetime import date, timedelta
from .models import RegistroPresenca


class PresencaRepository:
    """Repositório para operações de consulta do modelo Presenca."""

    @staticmethod
    def listar_todas():
        """Lista todas as presenças com relacionamentos."""
        return RegistroPresenca.objects.select_related("aluno", "turma", "atividade").all()

    @staticmethod
    def buscar_por_id(presenca_id):
        """Busca presença por ID."""
        try:
            return RegistroPresenca.objects.select_related("aluno", "turma", "atividade").get(
                id=presenca_id
            )
        except RegistroPresenca.DoesNotExist:
            return None

    @staticmethod
    def buscar_por_aluno(aluno_cpf, data_inicio=None, data_fim=None):
        """Busca presenças de um aluno."""
        presencas = RegistroPresenca.objects.filter(aluno__cpf=aluno_cpf).select_related(
            "turma", "atividade"
        )

        if data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)

        if data_fim:
            presencas = presencas.filter(data__lte=data_fim)

        return presencas.order_by("-data")

    @staticmethod
    def buscar_por_turma(turma_id, data_inicio=None, data_fim=None):
        """Busca presenças de uma turma."""
        presencas = RegistroPresenca.objects.filter(turma_id=turma_id).select_related(
            "aluno", "atividade"
        )

        if data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)

        if data_fim:
            presencas = presencas.filter(data__lte=data_fim)

        return presencas.order_by("-data", "aluno__nome")

    @staticmethod
    def buscar_por_atividade(atividade_id, data_inicio=None, data_fim=None):
        """Busca presenças de uma atividade."""
        presencas = RegistroPresenca.objects.filter(atividade_id=atividade_id).select_related(
            "aluno", "turma"
        )

        if data_inicio:
            presencas = presencas.filter(data__gte=data_inicio)

        if data_fim:
            presencas = presencas.filter(data__lte=data_fim)

        return presencas.order_by("-data", "aluno__nome")

    @staticmethod
    def buscar_com_filtros(filtros):
        """
        Busca presenças com filtros específicos.

        Args:
            filtros (dict): Dicionário com filtros
        """
        presencas = RegistroPresenca.objects.select_related("aluno", "turma", "atividade").all()

        if filtros.get("aluno_cpf"):
            presencas = presencas.filter(aluno__cpf=filtros["aluno_cpf"])

        if filtros.get("turma_id"):
            presencas = presencas.filter(turma_id=filtros["turma_id"])

        if filtros.get("atividade_id"):
            presencas = presencas.filter(atividade_id=filtros["atividade_id"])

        if filtros.get("data_inicio"):
            presencas = presencas.filter(data__gte=filtros["data_inicio"])

        if filtros.get("data_fim"):
            presencas = presencas.filter(data__lte=filtros["data_fim"])

        if filtros.get("presente") is not None:
            presencas = presencas.filter(status=("P" if filtros["presente"] else "F"))
        if filtros.get("status"):
            presencas = presencas.filter(status=filtros["status"])

        if filtros.get("search"):
            search_term = filtros["search"]
            presencas = presencas.filter(
                Q(aluno__nome__icontains=search_term)
                | Q(aluno__cpf__icontains=search_term)
                | Q(turma__nome__icontains=search_term)
                | Q(atividade__nome__icontains=search_term)
            )

        return presencas.order_by("-data")

    @staticmethod
    def obter_presentes_por_data(data_presenca):
        """Obtém todas as presenças de uma data específica."""
        return RegistroPresenca.objects.filter(
            data=data_presenca, status="P"
        ).select_related("aluno", "turma", "atividade")

    @staticmethod
    def obter_ausentes_por_data(data_presenca):
        """Obtém todas as ausências de uma data específica."""
        return RegistroPresenca.objects.filter(
            data=data_presenca, status="F"
        ).select_related("aluno", "turma", "atividade")

    @staticmethod
    def calcular_frequencia_aluno(
        aluno_cpf, turma_id=None, periodo_inicio=None, periodo_fim=None
    ):
        """Calcula estatísticas de frequência de um aluno."""
        presencas = RegistroPresenca.objects.filter(aluno__cpf=aluno_cpf)

        if turma_id:
            presencas = presencas.filter(turma_id=turma_id)

        if periodo_inicio:
            presencas = presencas.filter(data__gte=periodo_inicio)

        if periodo_fim:
            presencas = presencas.filter(data__lte=periodo_fim)

        total_registros = presencas.count()
        total_presencas = presencas.filter(status="P").count()
        total_faltas = presencas.filter(status="F").count()

        percentual_presenca = (
            (total_presencas / total_registros * 100) if total_registros > 0 else 0
        )

        return {
            "total_registros": total_registros,
            "total_presencas": total_presencas,
            "total_faltas": total_faltas,
            "percentual_presenca": round(percentual_presenca, 2),
        }

    @staticmethod
    def calcular_frequencia_turma(turma_id, periodo_inicio=None, periodo_fim=None):
        """Calcula estatísticas de frequência de uma turma."""
        presencas = RegistroPresenca.objects.filter(turma_id=turma_id)

        if periodo_inicio:
            presencas = presencas.filter(data__gte=periodo_inicio)

        if periodo_fim:
            presencas = presencas.filter(data__lte=periodo_fim)

        # Estatísticas gerais
        total_registros = presencas.count()
        total_presencas = presencas.filter(status="P").count()
        total_faltas = presencas.filter(status="F").count()

        percentual_presenca = (
            (total_presencas / total_registros * 100) if total_registros > 0 else 0
        )

        # Estatísticas por aluno
        por_aluno = (
            presencas.values("aluno__cpf", "aluno__nome")
            .annotate(
                total_registros=Count("id"),
                total_presencas=Count("id", filter=Q(status="P")),
                total_faltas=Count("id", filter=Q(status="F")),
            )
            .order_by("aluno__nome")
        )

        return {
            "geral": {
                "total_registros": total_registros,
                "total_presencas": total_presencas,
                "total_faltas": total_faltas,
                "percentual_presenca": round(percentual_presenca, 2),
            },
            "por_aluno": list(por_aluno),
        }

    @staticmethod
    def obter_frequencia_por_periodo(periodo_inicio, periodo_fim):
        """Obtém estatísticas de frequência por período."""
        presencas = RegistroPresenca.objects.filter(
            data__gte=periodo_inicio, data__lte=periodo_fim
        )

        # Por dia
        por_dia = (
            presencas.values("data")
            .annotate(
                total_registros=Count("id"),
                total_presencas=Count("id", filter=Q(status="P")),
                total_faltas=Count("id", filter=Q(status="F")),
            )
            .order_by("data")
        )

        # Por turma
        por_turma = (
            presencas.values("turma__id", "turma__nome")
            .annotate(
                total_registros=Count("id"),
                total_presencas=Count("id", filter=Q(status="P")),
                total_faltas=Count("id", filter=Q(status="F")),
            )
            .order_by("turma__nome")
        )

        return {"por_dia": list(por_dia), "por_turma": list(por_turma)}

    @staticmethod
    def obter_alunos_faltosos(limite_faltas=3, periodo_dias=30):
        """Obtém alunos com muitas faltas no período."""
        data_limite = date.today() - timedelta(days=periodo_dias)

        return (
            RegistroPresenca.objects.filter(data__gte=data_limite, status="F")
            .values("aluno__cpf", "aluno__nome")
            .annotate(total_faltas=Count("id"))
            .filter(total_faltas__gte=limite_faltas)
            .order_by("-total_faltas")
        )

    @staticmethod
    def verificar_presenca_existente(aluno_cpf, turma_id, data_presenca):
        """Verifica se já existe presença para aluno/turma/data."""
        return RegistroPresenca.objects.filter(
            aluno__cpf=aluno_cpf, turma_id=turma_id, data=data_presenca
        ).exists()

    @staticmethod
    def obter_estatisticas_gerais():
        """Obtém estatísticas gerais das presenças."""
        total = RegistroPresenca.objects.count()
        presentes = RegistroPresenca.objects.filter(status="P").count()
        ausentes = RegistroPresenca.objects.filter(status="F").count()

        # Presenças dos últimos 30 dias
        data_limite = date.today() - timedelta(days=30)
        recentes = RegistroPresenca.objects.filter(data__gte=data_limite)
        total_recentes = recentes.count()
        presentes_recentes = recentes.filter(presente=True).count()

        # Por mês (últimos 6 meses)
        seis_meses_atras = date.today() - timedelta(days=180)
        por_mes = (
            RegistroPresenca.objects.filter(data__gte=seis_meses_atras)
            .extra(
                select={
                    "mes": "EXTRACT(month FROM data)",
                    "ano": "EXTRACT(year FROM data)",
                }
            )
            .values("ano", "mes")
            .annotate(total=Count("id"), presentes=Count("id", filter=Q(status="P")))
            .order_by("ano", "mes")
        )

        return {
            "total": total,
            "presentes": presentes,
            "ausentes": ausentes,
            "percentual_presenca": (presentes / total * 100) if total > 0 else 0,
            "ultimos_30_dias": {
                "total": total_recentes,
                "presentes": presentes_recentes,
                "percentual": (presentes_recentes / total_recentes * 100)
                if total_recentes > 0
                else 0,
            },
            "por_mes": list(por_mes),
        }


class TotalAtividadeMesRepository:
    """Repositório compatível: calcula totais via RegistroPresenca (sem persistir)."""

    @staticmethod
    def obter_por_turma_e_periodo(turma_id, ano, mes):
        from django.db.models import Count

        qs = (
            RegistroPresenca.objects.filter(
                turma_id=turma_id, data__year=ano, data__month=mes
            )
            .values("atividade_id")
            .annotate(qtd_ativ_mes=Count("id"))
            .order_by("atividade_id")
        )
        return list(qs)

    @staticmethod
    def obter_por_atividade(atividade_id):
        from django.db.models import Count

        qs = (
            RegistroPresenca.objects.filter(atividade_id=atividade_id)
            .extra(
                select={
                    "mes": "EXTRACT(month FROM data)",
                    "ano": "EXTRACT(year FROM data)",
                }
            )
            .values("ano", "mes", "turma_id")
            .annotate(total=Count("id"))
            .order_by("-ano", "-mes")
        )
        return list(qs)


class ObservacaoPresencaRepository:
    """Repositório compatível: observações via justificativa do RegistroPresenca."""

    @staticmethod
    def listar_por_turma(turma_id, data_inicio=None, data_fim=None):
        observacoes = RegistroPresenca.objects.filter(turma_id=turma_id).exclude(
            justificativa__isnull=True
        ).exclude(justificativa__exact="")

        if data_inicio:
            observacoes = observacoes.filter(data__gte=data_inicio)

        if data_fim:
            observacoes = observacoes.filter(data__lte=data_fim)

        return observacoes.order_by("-data")

    @staticmethod
    def listar_por_aluno(aluno_cpf, data_inicio=None, data_fim=None):
        observacoes = RegistroPresenca.objects.filter(aluno__cpf=aluno_cpf).exclude(
            justificativa__isnull=True
        ).exclude(justificativa__exact="")

        if data_inicio:
            observacoes = observacoes.filter(data__gte=data_inicio)

        if data_fim:
            observacoes = observacoes.filter(data__lte=data_fim)

        return observacoes.order_by("-data")
