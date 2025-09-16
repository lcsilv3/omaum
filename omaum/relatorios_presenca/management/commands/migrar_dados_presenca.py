"""
Comando Django para migrar dados dos modelos antigos para o novo RegistroPresenca.

Este comando realiza a migração segura dos dados existentes,
mantendo a integridade e rastreabilidade do processo.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from importlib import import_module
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Comando para migrar dados de presença para o novo modelo unificado.

    Uso:
        python manage.py migrar_dados_presenca [--dry-run] [--verbose]
    """

    help = "Migra dados dos modelos antigos de presença para o novo RegistroPresenca"

    def add_arguments(self, parser):
        """Adiciona argumentos do comando."""
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Executa simulação sem alterar dados",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Exibe informações detalhadas",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Tamanho do lote para processamento (padrão: 1000)",
        )

    def handle(self, *args, **options):
        """Executa a migração de dados."""
        self.dry_run = options["dry_run"]
        self.verbose = options["verbose"]
        self.batch_size = options["batch_size"]

        if self.dry_run:
            self.stdout.write(
                self.style.WARNING("MODO SIMULAÇÃO - Nenhum dado será alterado")
            )

        try:
            # Carregar modelos
            self._carregar_modelos()

            # Executar migração
            with transaction.atomic():
                self._executar_migracao()

                if self.dry_run:
                    # Rollback em modo simulação
                    transaction.set_rollback(True)
                    self.stdout.write(
                        self.style.SUCCESS("Simulação concluída com sucesso")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS("Migração concluída com sucesso")
                    )

        except Exception as e:
            logger.error(f"Erro na migração: {e}")
            raise CommandError(f"Erro na migração: {e}")

    def _carregar_modelos(self):
        """Carrega modelos necessários."""
        try:
            # Modelos antigos
            presencas_module = import_module("presencas.models")
            self.Presenca = getattr(presencas_module, "Presenca", None)
            self.PresencaDetalhada = getattr(
                presencas_module, "PresencaDetalhada", None
            )
            self.ConvocacaoPresenca = getattr(
                presencas_module, "ConvocacaoPresenca", None
            )

            # Novo modelo
            self.RegistroPresenca = getattr(presencas_module, "RegistroPresenca", None)
            self.HistoricoMigracao = getattr(
                presencas_module, "HistoricoMigracao", None
            )

            if not self.RegistroPresenca:
                raise CommandError("Modelo RegistroPresenca não encontrado")

        except ImportError as e:
            raise CommandError(f"Erro ao carregar modelos: {e}")

    def _executar_migracao(self):
        """Executa a migração completa."""
        estatisticas = {
            "presencas_migradas": 0,
            "presencas_detalhadas_migradas": 0,
            "convocacoes_migradas": 0,
            "erros": 0,
        }

        # Migrar modelo Presenca
        if self.Presenca:
            estatisticas["presencas_migradas"] = self._migrar_presencas()

        # Migrar modelo PresencaDetalhada
        if self.PresencaDetalhada:
            estatisticas["presencas_detalhadas_migradas"] = (
                self._migrar_presencas_detalhadas()
            )

        # Migrar modelo ConvocacaoPresenca
        if self.ConvocacaoPresenca:
            estatisticas["convocacoes_migradas"] = self._migrar_convocacoes()

        # Exibir estatísticas
        self._exibir_estatisticas(estatisticas)

    def _migrar_presencas(self):
        """Migra dados do modelo Presenca."""
        self.stdout.write("Migrando dados do modelo Presenca...")

        total_registros = self.Presenca.objects.count()
        migrados = 0

        if self.verbose:
            self.stdout.write(f"Total de registros a migrar: {total_registros}")

        # Processar em lotes
        for offset in range(0, total_registros, self.batch_size):
            presencas = self.Presenca.objects.all()[offset : offset + self.batch_size]

            for presenca in presencas:
                try:
                    # Verificar se já foi migrado
                    if (
                        self.HistoricoMigracao
                        and self.HistoricoMigracao.objects.filter(
                            tipo_origem="presenca", id_origem=presenca.id
                        ).exists()
                    ):
                        continue

                    # Criar registro unificado
                    registro = self._criar_registro_presenca(presenca, "presenca")

                    if not self.dry_run:
                        registro.save()

                        # Criar histórico de migração
                        if self.HistoricoMigracao:
                            self.HistoricoMigracao.objects.create(
                                tipo_origem="presenca",
                                id_origem=presenca.id,
                                registro_presenca=registro,
                                observacoes=f"Migrado de Presenca #{presenca.id}",
                            )

                    migrados += 1

                    if self.verbose and migrados % 100 == 0:
                        self.stdout.write(f"Migrados: {migrados}/{total_registros}")

                except Exception as e:
                    logger.error(f"Erro ao migrar presença {presenca.id}: {e}")
                    if self.verbose:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Erro ao migrar presença {presenca.id}: {e}"
                            )
                        )

        return migrados

    def _migrar_presencas_detalhadas(self):
        """Migra dados do modelo PresencaDetalhada."""
        self.stdout.write("Migrando dados do modelo PresencaDetalhada...")

        total_registros = self.PresencaDetalhada.objects.count()
        migrados = 0

        # Processar em lotes
        for offset in range(0, total_registros, self.batch_size):
            presencas = self.PresencaDetalhada.objects.all()[
                offset : offset + self.batch_size
            ]

            for presenca in presencas:
                try:
                    # Verificar se já foi migrado
                    if (
                        self.HistoricoMigracao
                        and self.HistoricoMigracao.objects.filter(
                            tipo_origem="presenca_detalhada", id_origem=presenca.id
                        ).exists()
                    ):
                        continue

                    # Criar registro unificado
                    registro = self._criar_registro_presenca(
                        presenca, "presenca_detalhada"
                    )

                    if not self.dry_run:
                        registro.save()

                        # Criar histórico de migração
                        if self.HistoricoMigracao:
                            self.HistoricoMigracao.objects.create(
                                tipo_origem="presenca_detalhada",
                                id_origem=presenca.id,
                                registro_presenca=registro,
                                observacoes=f"Migrado de PresencaDetalhada #{presenca.id}",
                            )

                    migrados += 1

                except Exception as e:
                    logger.error(
                        f"Erro ao migrar presença detalhada {presenca.id}: {e}"
                    )

        return migrados

    def _migrar_convocacoes(self):
        """Migra dados do modelo ConvocacaoPresenca."""
        self.stdout.write("Migrando dados do modelo ConvocacaoPresenca...")

        total_registros = self.ConvocacaoPresenca.objects.count()
        migrados = 0

        # Processar em lotes
        for offset in range(0, total_registros, self.batch_size):
            convocacoes = self.ConvocacaoPresenca.objects.all()[
                offset : offset + self.batch_size
            ]

            for convocacao in convocacoes:
                try:
                    # Verificar se já foi migrado
                    if (
                        self.HistoricoMigracao
                        and self.HistoricoMigracao.objects.filter(
                            tipo_origem="convocacao", id_origem=convocacao.id
                        ).exists()
                    ):
                        continue

                    # Criar registro unificado
                    registro = self._criar_registro_presenca(convocacao, "convocacao")

                    if not self.dry_run:
                        registro.save()

                        # Criar histórico de migração
                        if self.HistoricoMigracao:
                            self.HistoricoMigracao.objects.create(
                                tipo_origem="convocacao",
                                id_origem=convocacao.id,
                                registro_presenca=registro,
                                observacoes=f"Migrado de ConvocacaoPresenca #{convocacao.id}",
                            )

                    migrados += 1

                except Exception as e:
                    logger.error(f"Erro ao migrar convocação {convocacao.id}: {e}")

        return migrados

    def _criar_registro_presenca(self, objeto_origem, tipo_origem):
        """Cria registro RegistroPresenca a partir do objeto origem."""
        # Mapear campos comuns
        dados = {
            "aluno": objeto_origem.aluno,
            "turma": objeto_origem.turma,
            "atividade": objeto_origem.atividade,
            "data": objeto_origem.data,
            "registrado_por": getattr(objeto_origem, "registrado_por", "Sistema"),
            "data_registro": getattr(objeto_origem, "data_registro", timezone.now()),
        }

        # Mapear campos específicos por tipo
        if tipo_origem == "presenca":
            dados["status"] = "P" if objeto_origem.presente else "F"
            dados["justificativa"] = getattr(objeto_origem, "justificativa", "")
            dados["convocado"] = True  # Assumir convocado por padrão

        elif tipo_origem == "presenca_detalhada":
            # Mapear status detalhado se disponível
            status_map = {
                "presente": "P",
                "falta": "F",
                "justificada": "J",
                "voluntario_extra": "V1",
                "voluntario_simples": "V2",
            }
            dados["status"] = status_map.get(
                getattr(objeto_origem, "status", "presente").lower(), "P"
            )
            dados["justificativa"] = getattr(objeto_origem, "justificativa", "")
            dados["convocado"] = getattr(objeto_origem, "convocado", True)

        elif tipo_origem == "convocacao":
            # Para convocações, assumir presença se convocado
            dados["status"] = "P" if objeto_origem.convocado else "F"
            dados["convocado"] = objeto_origem.convocado
            dados["justificativa"] = ""

        # Calcular período mensal
        dados["periodo_mes"] = dados["data"].replace(day=1)

        return self.RegistroPresenca(**dados)

    def _exibir_estatisticas(self, estatisticas):
        """Exibe estatísticas da migração."""
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("ESTATÍSTICAS DA MIGRAÇÃO")
        self.stdout.write("=" * 50)

        for chave, valor in estatisticas.items():
            label = chave.replace("_", " ").title()
            self.stdout.write(f"{label}: {valor}")

        total_migrados = sum(v for k, v in estatisticas.items() if "migradas" in k)
        self.stdout.write(f"\nTotal de registros migrados: {total_migrados}")

        if estatisticas["erros"] > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"Atenção: {estatisticas['erros']} erros encontrados"
                )
            )

        self.stdout.write("=" * 50)
