"""
Service principal para geração de dados de relatórios de presença.

Este service centraliza toda a lógica de negócio para obtenção
e processamento de dados para os diferentes tipos de relatórios.
"""

from datetime import date, timedelta
from django.utils import timezone
from importlib import import_module
import logging

logger = logging.getLogger(__name__)


class RelatorioPresencaService:
    """
    Service centralizado para geração de dados de relatórios de presença.

    Implementa as regras de negócio para cada tipo de relatório
    seguindo as premissas estabelecidas.
    """

    def __init__(self):
        """Inicializa o service com importações dinâmicas."""
        self._carregar_modelos()

    def _carregar_modelos(self):
        """Carrega modelos dinamicamente para evitar importações circulares."""
        try:
            # Usar importlib conforme premissas
            presencas_module = import_module("presencas.models")
            alunos_module = import_module("alunos.models")
            turmas_module = import_module("turmas.models")
            atividades_module = import_module("atividades.models")

            # Tentar usar novo modelo unificado primeiro
            if hasattr(presencas_module, "RegistroPresenca"):
                self.RegistroPresenca = presencas_module.RegistroPresenca
            else:
                # Fallback para modelos antigos
                self.Presenca = presencas_module.Presenca
                self.PresencaDetalhada = getattr(
                    presencas_module, "PresencaDetalhada", None
                )

            self.Aluno = alunos_module.Aluno
            self.Turma = turmas_module.Turma
            self.Atividade = atividades_module.Atividade

        except ImportError as e:
            logger.error(f"Erro ao carregar modelos: {e}")
            raise

    def obter_dados_consolidado_periodo(
        self, turma_id, data_inicio, data_fim, atividade_id=None
    ):
        """
        Obtém dados para o relatório consolidado por período (grau).

        Args:
            turma_id: ID da turma
            data_inicio: Data início do período
            data_fim: Data fim do período
            atividade_id: ID da atividade (opcional)

        Returns:
            dict: Dados organizados para o relatório
        """
        try:
            turma = self.Turma.objects.get(id=turma_id)

            # Construir filtros
            filtros = {"turma_id": turma_id, "data__range": [data_inicio, data_fim]}

            if atividade_id:
                filtros["atividade_id"] = atividade_id

            # Obter registros usando modelo unificado se disponível
            if hasattr(self, "RegistroPresenca"):
                registros = (
                    self.RegistroPresenca.objects.filter(**filtros)
                    .select_related("aluno", "atividade")
                    .order_by("aluno__numero_iniciatico", "data")
                )
            else:
                # Fallback para modelo antigo
                registros = (
                    self.Presenca.objects.filter(**filtros)
                    .select_related("aluno", "atividade")
                    .order_by("aluno__nome", "data")
                )

            # Processar dados por aluno e mês
            dados_alunos = self._processar_dados_consolidado(
                registros, data_inicio, data_fim
            )

            # Obter informações da turma
            dados_turma = self._obter_dados_turma(turma)

            return {
                "turma": dados_turma,
                "periodo": {
                    "inicio": data_inicio,
                    "fim": data_fim,
                    "meses": self._gerar_lista_meses(data_inicio, data_fim),
                },
                "alunos": dados_alunos,
                "estatisticas": self._calcular_estatisticas_consolidado(dados_alunos),
            }

        except Exception as e:
            logger.error(f"Erro ao obter dados consolidado: {e}")
            raise

    def _processar_dados_consolidado(self, registros, data_inicio, data_fim):
        """Processa registros para formato consolidado."""
        dados_alunos = {}

        for registro in registros:
            aluno_id = registro.aluno.id
            mes_ano = f"{registro.data.month:02d}/{registro.data.year}"

            # Inicializar dados do aluno se não existir
            if aluno_id not in dados_alunos:
                dados_alunos[aluno_id] = {
                    "aluno": registro.aluno,
                    "meses": {},
                    "totais": {"P": 0, "F": 0, "J": 0, "V1": 0, "V2": 0},
                    "percentual_presenca": 0,
                }

            # Inicializar dados do mês se não existir
            if mes_ano not in dados_alunos[aluno_id]["meses"]:
                dados_alunos[aluno_id]["meses"][mes_ano] = {
                    "P": 0,
                    "F": 0,
                    "J": 0,
                    "V1": 0,
                    "V2": 0,
                }

            # Determinar status do registro
            if hasattr(self, "RegistroPresenca"):
                status = registro.status
            else:
                # Converter modelo antigo
                status = "P" if registro.presente else "F"

            # Contabilizar por status
            dados_alunos[aluno_id]["meses"][mes_ano][status] += 1
            dados_alunos[aluno_id]["totais"][status] += 1

        # Calcular percentuais
        for aluno_dados in dados_alunos.values():
            total_atividades = sum(aluno_dados["totais"].values())
            total_presencas = (
                aluno_dados["totais"]["P"]
                + aluno_dados["totais"]["V1"]
                + aluno_dados["totais"]["V2"]
            )

            if total_atividades > 0:
                aluno_dados["percentual_presenca"] = round(
                    (total_presencas / total_atividades) * 100, 2
                )

        return list(dados_alunos.values())

    def obter_dados_apuracao_mensal(self, turma_id, ano, mes, atividade_id=None):
        """
        Obtém dados para relatório de apuração mensal (mes01-99).

        Args:
            turma_id: ID da turma
            ano: Ano de referência
            mes: Mês de referência
            atividade_id: ID da atividade (opcional)

        Returns:
            dict: Dados organizados por aluno e dia
        """
        try:
            turma = self.Turma.objects.get(id=turma_id)

            # Definir período do mês
            data_inicio = date(ano, mes, 1)
            if mes == 12:
                data_fim = date(ano + 1, 1, 1) - timedelta(days=1)
            else:
                data_fim = date(ano, mes + 1, 1) - timedelta(days=1)

            # Construir filtros
            filtros = {"turma_id": turma_id, "data__range": [data_inicio, data_fim]}

            if atividade_id:
                filtros["atividade_id"] = atividade_id

            # Obter registros
            if hasattr(self, "RegistroPresenca"):
                registros = (
                    self.RegistroPresenca.objects.filter(**filtros)
                    .select_related("aluno", "atividade")
                    .order_by("aluno__numero_iniciatico", "data")
                )
            else:
                registros = (
                    self.Presenca.objects.filter(**filtros)
                    .select_related("aluno", "atividade")
                    .order_by("aluno__nome", "data")
                )

            # Processar dados por aluno e dia
            dados_alunos = self._processar_dados_mensais(
                registros, data_inicio, data_fim
            )

            return {
                "turma": self._obter_dados_turma(turma),
                "periodo": {
                    "ano": ano,
                    "mes": mes,
                    "nome_mes": self._obter_nome_mes(mes),
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                    "dias_mes": self._gerar_dias_mes(ano, mes),
                },
                "alunos": dados_alunos,
                "atividade": self._obter_dados_atividade(atividade_id)
                if atividade_id
                else None,
            }

        except Exception as e:
            logger.error(f"Erro ao obter dados mensais: {e}")
            raise

    def _processar_dados_mensais(self, registros, data_inicio, data_fim):
        """Processa registros para formato mensal."""
        dados_alunos = {}

        for registro in registros:
            aluno_id = registro.aluno.id
            dia = registro.data.day

            # Inicializar dados do aluno
            if aluno_id not in dados_alunos:
                dados_alunos[aluno_id] = {
                    "aluno": registro.aluno,
                    "dias": {},
                    "totais": {"P": 0, "F": 0, "J": 0, "V1": 0, "V2": 0},
                }

            # Determinar status
            if hasattr(self, "RegistroPresenca"):
                status = registro.status
            else:
                status = "P" if registro.presente else "F"

            # Registrar por dia
            dados_alunos[aluno_id]["dias"][dia] = {
                "status": status,
                "registro": registro,
            }

            # Contabilizar totais
            dados_alunos[aluno_id]["totais"][status] += 1

        return list(dados_alunos.values())

    def obter_dados_formulario_coleta(self, turma_id, ano, mes):
        """
        Obtém dados para formulário de coleta mensal (mod).

        Args:
            turma_id: ID da turma
            ano: Ano de referência
            mes: Mês de referência

        Returns:
            dict: Estrutura para formulário de coleta
        """
        try:
            turma = self.Turma.objects.get(id=turma_id)

            # Obter alunos ativos da turma
            alunos = self._obter_alunos_turma(turma_id)

            # Gerar estrutura de dias do mês
            dias_mes = self._gerar_dias_mes(ano, mes)

            return {
                "turma": self._obter_dados_turma(turma),
                "periodo": {
                    "ano": ano,
                    "mes": mes,
                    "nome_mes": self._obter_nome_mes(mes),
                    "dias_mes": dias_mes,
                },
                "alunos": alunos,
                "estrutura_coleta": self._gerar_estrutura_coleta(alunos, dias_mes),
            }

        except Exception as e:
            logger.error(f"Erro ao obter dados formulário coleta: {e}")
            raise

    def obter_dados_controle_geral(self, turma_id):
        """
        Obtém dados para relatório de controle geral da turma (pcg).

        Args:
            turma_id: ID da turma

        Returns:
            dict: Dados completos da turma
        """
        try:
            turma = self.Turma.objects.get(id=turma_id)

            # Obter dados básicos da turma
            dados_turma = self._obter_dados_turma_completos(turma)

            # Obter estatísticas da turma
            estatisticas = self._calcular_estatisticas_turma(turma_id)

            # Obter alunos matriculados
            alunos = self._obter_alunos_turma_completos(turma_id)

            return {
                "turma": dados_turma,
                "estatisticas": estatisticas,
                "alunos": alunos,
                "data_geracao": timezone.now(),
            }

        except Exception as e:
            logger.error(f"Erro ao obter dados controle geral: {e}")
            raise

    # Métodos auxiliares

    def _obter_dados_turma(self, turma):
        """Obtém dados básicos da turma."""
        return {
            "id": turma.id,
            "nome": turma.nome,
            "curso": turma.curso.nome if turma.curso else "N/A",
            "status": turma.get_status_display(),
            "instrutor": turma.instrutor.nome if turma.instrutor else "N/A",
        }

    def _obter_dados_turma_completos(self, turma):
        """Obtém dados completos da turma para relatório PCG."""
        # Usar método do modelo ajustado se disponível
        if hasattr(turma, "get_dados_relatorio_pcg"):
            return turma.get_dados_relatorio_pcg()

        # Fallback manual
        return {
            "nome": turma.nome,
            "curso": turma.curso.nome if turma.curso else "N/A",
            "descricao": turma.descricao or "N/A",
            "num_livro": getattr(turma, "num_livro", "N/A"),
            "perc_presenca_minima": getattr(
                turma, "perc_presenca_minima", getattr(turma, "perc_carencia", "N/A")
            ),
            "data_iniciacao": turma.data_iniciacao.strftime("%d/%m/%Y")
            if getattr(turma, "data_iniciacao", None)
            else "N/A",
            "data_inicio_ativ": turma.data_inicio_ativ.strftime("%d/%m/%Y")
            if getattr(turma, "data_inicio_ativ", None)
            else "N/A",
            "status": turma.get_status_display(),
            "instrutor": turma.instrutor.nome if turma.instrutor else "N/A",
        }

    def _obter_alunos_turma(self, turma_id):
        """Obtém alunos ativos da turma."""
        try:
            # Tentar usar método da turma
            turma = self.Turma.objects.get(id=turma_id)
            if hasattr(turma, "get_alunos_ativos"):
                matriculas = turma.get_alunos_ativos()
                return [m.aluno for m in matriculas]

            # Fallback: buscar diretamente
            matriculas_module = import_module("matriculas.models")
            matriculas = (
                matriculas_module.Matricula.objects.filter(
                    turma_id=turma_id,
                    status="A",  # Ativa
                )
                .select_related("aluno")
                .order_by("aluno__numero_iniciatico")
            )

            return [m.aluno for m in matriculas]

        except Exception as e:
            logger.warning(f"Erro ao obter alunos da turma: {e}")
            return []

    def _gerar_lista_meses(self, data_inicio, data_fim):
        """Gera lista de meses no período."""
        meses = []
        data_atual = data_inicio.replace(day=1)

        while data_atual <= data_fim:
            meses.append(
                {
                    "mes": data_atual.month,
                    "ano": data_atual.year,
                    "nome": self._obter_nome_mes(data_atual.month),
                    "chave": f"{data_atual.month:02d}/{data_atual.year}",
                }
            )

            if data_atual.month == 12:
                data_atual = data_atual.replace(year=data_atual.year + 1, month=1)
            else:
                data_atual = data_atual.replace(month=data_atual.month + 1)

        return meses

    def _gerar_dias_mes(self, ano, mes):
        """Gera lista de dias do mês."""
        import calendar

        dias = []
        num_dias = calendar.monthrange(ano, mes)[1]

        for dia in range(1, num_dias + 1):
            data = date(ano, mes, dia)
            dias.append(
                {
                    "dia": dia,
                    "data": data,
                    "dia_semana": data.strftime("%A"),
                    "eh_fim_semana": data.weekday() >= 5,
                }
            )

        return dias

    def _obter_nome_mes(self, mes):
        """Retorna nome do mês em português."""
        nomes_meses = [
            "",
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]
        return nomes_meses[mes]

    def _calcular_estatisticas_consolidado(self, dados_alunos):
        """Calcula estatísticas do relatório consolidado."""
        if not dados_alunos:
            return {}

        total_alunos = len(dados_alunos)
        total_presencas = sum(aluno["totais"]["P"] for aluno in dados_alunos)
        total_faltas = sum(aluno["totais"]["F"] for aluno in dados_alunos)
        total_atividades = total_presencas + total_faltas

        percentual_geral = (
            (total_presencas / total_atividades * 100) if total_atividades > 0 else 0
        )

        return {
            "total_alunos": total_alunos,
            "total_presencas": total_presencas,
            "total_faltas": total_faltas,
            "total_atividades": total_atividades,
            "percentual_geral": round(percentual_geral, 2),
        }
