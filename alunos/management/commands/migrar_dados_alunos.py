"""
Comando de gerenciamento para migrar dados legados de Alunos para campos normalizados.
"""

import logging
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from alunos.models import Aluno, Pais, Cidade, Bairro

# Configuração do logger para este comando
logger = logging.getLogger("migracao_alunos")
logger.setLevel(logging.INFO)
# Evita adicionar handlers duplicados se o comando for chamado múltiplas vezes
if not logger.handlers:
    handler = logging.FileHandler("migracao_alunos.log", mode="w")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class Command(BaseCommand):
    """
    Comando Django para migrar dados de endereço e nacionalidade de campos de texto
    para campos de ForeignKey no modelo Aluno.
    """

    help = "Migra dados legados de Alunos para campos normalizados."

    def add_arguments(self, parser):
        """Adiciona argumentos ao comando."""
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Executa o comando em modo de simulação, sem salvar alterações no banco de dados.",
        )

    def _migrar_nacionalidade(self, aluno):
        if aluno.nacionalidade and not aluno.pais_nacionalidade:
            try:
                pais = Pais.objects.get(
                    nacionalidade__iexact=aluno.nacionalidade.strip()
                )
                aluno.pais_nacionalidade = pais
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  [Nacionalidade] OK: "{aluno.nacionalidade}" -> {pais.nome}'
                    )
                )
                return True
            except Pais.DoesNotExist:
                logger.warning(
                    f'CPF {aluno.cpf}: País com nacionalidade "{aluno.nacionalidade}" não encontrado.'
                )
            except Pais.MultipleObjectsReturned:
                logger.error(
                    f'CPF {aluno.cpf}: Múltiplos países para a nacionalidade "{aluno.nacionalidade}".'
                )
        else:
            if not aluno.nacionalidade:
                logger.info(
                    f'CPF {aluno.cpf}: [Nacionalidade] Ignorado - campo de texto "nacionalidade" vazio.'
                )
            elif aluno.pais_nacionalidade:
                logger.info(
                    f'CPF {aluno.cpf}: [Nacionalidade] Ignorado - campo "pais_nacionalidade" já preenchido: {aluno.pais_nacionalidade}.'
                )
        return False

    def _migrar_endereco(self, aluno):
        if aluno.cidade and aluno.estado and not aluno.cidade_ref:
            try:
                cidade_nome = aluno.cidade.strip()
                estado_sigla = aluno.estado.strip().upper()

                cidade_obj = Cidade.objects.select_related("estado").get(
                    nome__iexact=cidade_nome, estado__codigo__iexact=estado_sigla
                )
                aluno.cidade_ref = cidade_obj
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  [Endereço] OK: "{cidade_nome}-{estado_sigla}" -> {cidade_obj}'
                    )
                )

                if aluno.bairro and not aluno.bairro_ref:
                    bairro_nome = aluno.bairro.strip()
                    bairro_obj, created = Bairro.objects.get_or_create(
                        nome__iexact=bairro_nome,
                        cidade=cidade_obj,
                        defaults={"nome": bairro_nome},
                    )
                    aluno.bairro_ref = bairro_obj
                    msg = "criado" if created else "encontrado"
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'    [Bairro] OK: "{bairro_nome}" {msg} -> {bairro_obj}'
                        )
                    )

                return True
            except Cidade.DoesNotExist:
                logger.warning(
                    f'CPF {aluno.cpf}: Cidade de endereço "{aluno.cidade}/{aluno.estado}" não encontrada.'
                )
            except Exception as e:
                logger.error(
                    f"CPF {aluno.cpf}: Erro inesperado ao migrar endereço: {e}"
                )
        else:
            if not aluno.cidade or not aluno.estado:
                logger.info(
                    f'CPF {aluno.cpf}: [Endereço] Ignorado - campos de texto "cidade" ou "estado" vazios.'
                )
            elif aluno.cidade_ref:
                logger.info(
                    f'CPF {aluno.cpf}: [Endereço] Ignorado - campo "cidade_ref" já preenchido: {aluno.cidade_ref}.'
                )
        return False

    def _migrar_naturalidade(self, aluno):
        if aluno.naturalidade and not aluno.cidade_naturalidade:
            try:
                # Tenta extrair "Cidade - UF" ou "Cidade/UF"
                parts = re.split(r"\s*-\s*|\s*/\s*", aluno.naturalidade.strip())
                if len(parts) == 2:
                    cidade_nome, estado_sigla = [p.strip() for p in parts]
                    cidade_obj = Cidade.objects.select_related("estado").get(
                        nome__iexact=cidade_nome,
                        estado__codigo__iexact=estado_sigla.upper(),
                    )
                    aluno.cidade_naturalidade = cidade_obj
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  [Naturalidade] OK: "{aluno.naturalidade}" -> {cidade_obj}'
                        )
                    )
                    return True
                else:
                    logger.warning(
                        f'CPF {aluno.cpf}: Formato de naturalidade "{aluno.naturalidade}" não reconhecido.'
                    )
            except Cidade.DoesNotExist:
                logger.warning(
                    f'CPF {aluno.cpf}: Cidade de naturalidade "{aluno.naturalidade}" não encontrada.'
                )
            except Exception as e:
                logger.error(
                    f"CPF {aluno.cpf}: Erro inesperado ao migrar naturalidade: {e}"
                )
        else:
            if not aluno.naturalidade:
                logger.info(
                    f'CPF {aluno.cpf}: [Naturalidade] Ignorado - campo de texto "naturalidade" vazio.'
                )
            elif aluno.cidade_naturalidade:
                logger.info(
                    f'CPF {aluno.cpf}: [Naturalidade] Ignorado - campo "cidade_naturalidade" já preenchido: {aluno.cidade_naturalidade}.'
                )
        return False

    @transaction.atomic
    def handle(self, *args, **options):
        """Lógica principal do comando de migração."""
        dry_run = options["dry_run"]
        self.stdout.write(
            self.style.SUCCESS("Iniciando a migração de dados de Alunos...")
        )
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "Executando em modo --dry-run. Nenhuma alteração será salva."
                )
            )

        logger.info("--- INÍCIO DA MIGRAÇÃO ---")
        logger.info(f"Modo Dry Run: {dry_run}")

        contadores = {
            "nacionalidade": 0,
            "naturalidade": 0,
            "endereco": 0,
            "falhas": 0,
            "sem_alteracao": 0,
            "total": 0,
        }

        alunos_a_processar = Aluno.objects.all()
        total_alunos = alunos_a_processar.count()
        contadores["total"] = total_alunos

        for i, aluno in enumerate(alunos_a_processar):
            self.stdout.write(
                f"\n({i + 1}/{total_alunos}) Processando: {aluno.nome} ({aluno.cpf})"
            )

            alterado_nacionalidade = self._migrar_nacionalidade(aluno)
            alterado_naturalidade = self._migrar_naturalidade(aluno)
            alterado_endereco = self._migrar_endereco(aluno)

            if alterado_nacionalidade:
                contadores["nacionalidade"] += 1
            if alterado_naturalidade:
                contadores["naturalidade"] += 1
            if alterado_endereco:
                contadores["endereco"] += 1

            if any([alterado_nacionalidade, alterado_naturalidade, alterado_endereco]):
                if not dry_run:
                    try:
                        aluno.save()
                    except Exception as e:
                        logger.critical(
                            f"CPF {aluno.cpf}: FALHA CRÍTICA AO SALVAR. Erro: {e}"
                        )
                        contadores["falhas"] += 1
            else:
                self.stdout.write(self.style.NOTICE("  Nenhuma alteração necessária."))
                contadores["sem_alteracao"] += 1

        # Relatório final
        self.stdout.write(self.style.SUCCESS("\n--- Relatório de Migração ---"))
        self.stdout.write(f"Total de Alunos processados: {contadores['total']}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Nacionalidades migradas: {contadores['nacionalidade']}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f"Naturalidades migradas: {contadores['naturalidade']}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Endereços migrados: {contadores['endereco']}")
        )
        self.stdout.write(
            self.style.WARNING(
                f"Alunos com falhas (ver migracao_alunos.log): {contadores['falhas']}"
            )
        )
        self.stdout.write(
            f"Alunos que não necessitaram de alteração: {contadores['sem_alteracao']}"
        )

        logger.info("--- FIM DA MIGRAÇÃO ---")

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "\nLembre-se: Nenhuma alteração foi salva. Execute sem --dry-run para aplicar."
                )
            )
            transaction.set_rollback(
                True
            )  # Garante que nada seja commitado no modo dry-run
        else:
            self.stdout.write(
                self.style.SUCCESS("\nMigração concluída e salva no banco de dados.")
            )
