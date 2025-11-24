from django.db.models import Q, Count
from presencas.models import RegistroPresenca
from alunos.models import Aluno
from turmas.models import Turma


class RelatorioPresencaService:
    """Serviço centralizado para geração de dados de relatórios."""

    def obter_alunos_mais_carencias(
        self, curso_id=None, turma_id=None, data_inicio=None, data_fim=None
    ):
        """Obtém alunos com mais carências (faltas) no período, filtrando por curso, turma e datas."""
        filtros = Q(status="F")
        if turma_id:
            filtros &= Q(turma_id=turma_id)
        if curso_id:
            filtros &= Q(turma__curso_id=curso_id)
        if data_inicio:
            filtros &= Q(data__gte=data_inicio)
        if data_fim:
            filtros &= Q(data__lte=data_fim)
        qs = RegistroPresenca.objects.filter(filtros)
        qs = (
            qs.values("aluno_id", "turma_id")
            .annotate(faltas=Count("id"))
            .order_by("-faltas")
        )
        alunos = Aluno.objects.in_bulk([x["aluno_id"] for x in qs])
        turmas = Turma.objects.in_bulk([x["turma_id"] for x in qs])
        resultados = []
        for x in qs:
            aluno = alunos.get(x["aluno_id"])
            turma = turmas.get(x["turma_id"])
            resultados.append(
                {
                    "aluno": aluno,
                    "turma": turma,
                    "faltas": x["faltas"],
                }
            )
        return resultados

    def obter_frequencia_por_atividade(
        self, turma_id=None, atividade_id=None, data_inicio=None, data_fim=None
    ):
        """Obtém frequência dos alunos por atividade, filtrando por turma, atividade e período."""
        from atividades.models import Presenca

        filtros = Q()
        if turma_id:
            filtros &= Q(turma_id=turma_id)
        if atividade_id:
            filtros &= Q(atividade_id=atividade_id)
        if data_inicio:
            filtros &= Q(data__gte=data_inicio)
        if data_fim:
            filtros &= Q(data__lte=data_fim)
        presencas = Presenca.objects.filter(filtros).select_related(
            "aluno", "atividade", "turma"
        )
        dados = {}
        for p in presencas:
            key = (p.aluno.id, p.atividade.id)
            if key not in dados:
                dados[key] = {
                    "aluno": p.aluno,
                    "atividade": p.atividade,
                    "turma": p.turma,
                    "presencas": 0,
                    "faltas": 0,
                }
            if p.presente:
                dados[key]["presencas"] += 1
            else:
                dados[key]["faltas"] += 1
        return list(dados.values())

    def obter_dados_consolidado(self, turma_id, data_inicio, data_fim):
        registros = RegistroPresenca.objects.filter(
            turma_id=turma_id, data__range=[data_inicio, data_fim]
        ).select_related("aluno", "atividade")
        dados_processados = self._processar_dados_consolidado(registros)
        return {
            "turma": Turma.objects.get(id=turma_id),
            "periodo": {"inicio": data_inicio, "fim": data_fim},
            "alunos": dados_processados,
        }

    def _processar_dados_consolidado(self, registros):
        dados_alunos = {}
        for registro in registros:
            aluno_id = registro.aluno.id
            mes_ano = f"{registro.data.month:02d}/{registro.data.year}"
            if aluno_id not in dados_alunos:
                dados_alunos[aluno_id] = {
                    "aluno": registro.aluno,
                    "meses": {},
                    "totais": {"P": 0, "F": 0, "J": 0, "V1": 0, "V2": 0},
                }
            if mes_ano not in dados_alunos[aluno_id]["meses"]:
                dados_alunos[aluno_id]["meses"][mes_ano] = {
                    "P": 0,
                    "F": 0,
                    "J": 0,
                    "V1": 0,
                    "V2": 0,
                }
            status = registro.status
            dados_alunos[aluno_id]["meses"][mes_ano][status] += 1
            dados_alunos[aluno_id]["totais"][status] += 1
        return list(dados_alunos.values())

    def obter_boletim_aluno(self, aluno_id, mes, ano, turma_id=None):
        try:
            aluno = Aluno.objects.get(id=aluno_id)
        except Aluno.DoesNotExist:
            return None
        filtros = Q(aluno_id=aluno_id) & Q(data__month=mes) & Q(data__year=ano)
        if turma_id:
            filtros &= Q(turma_id=turma_id)
        registros = RegistroPresenca.objects.filter(filtros)
        totais = {"P": 0, "F": 0, "J": 0, "V1": 0, "V2": 0}
        for reg in registros:
            status = reg.status
            if status in totais:
                totais[status] += 1
        convocacoes = sum([totais[k] for k in ["P", "F", "J"]])
        presencas = totais["P"]
        faltas = totais["F"]
        v1 = totais["V1"]
        v2 = totais["V2"]
        carencias = totais["F"]
        percentual = (
            round((presencas / convocacoes) * 100, 2) if convocacoes > 0 else 0.0
        )
        vol = v1 + v2
        return {
            "aluno": aluno,
            "convocacoes": convocacoes,
            "presencas": presencas,
            "faltas": faltas,
            "percentual": percentual,
            "v1": v1,
            "v2": v2,
            "vol": vol,
            "carencias": carencias,
            "limite_percentual": 70,
        }
