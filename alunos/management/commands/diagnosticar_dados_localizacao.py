"""
Comando de gerenciamento para diagnosticar dados de localização (nacionalidade, naturalidade)
nos modelos Aluno, Pais e Cidade.
"""

from django.core.management.base import BaseCommand
from alunos.models import Aluno, Pais, Cidade


class Command(BaseCommand):
    help = "Diagnostica a consistência dos dados de nacionalidade e naturalidade."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("--- Iniciando Diagnóstico de Dados de Localização ---")
        )

        # --- Diagnóstico de Nacionalidade ---
        self.stdout.write(self.style.HTTP_INFO("\n1. Análise de Nacionalidade"))

        # Valores únicos de nacionalidade nos Alunos
        nacionalidades_alunos = (
            Aluno.objects.exclude(nacionalidade__isnull=True)
            .exclude(nacionalidade__exact="")
            .values_list("nacionalidade", flat=True)
            .distinct()
        )
        self.stdout.write(
            self.style.WARNING(
                f"  - Nacionalidades distintas encontradas em Alunos: {list(nacionalidades_alunos)}"
            )
        )

        # Valores únicos de nacionalidade nos Países
        nacionalidades_paises = (
            Pais.objects.exclude(nacionalidade__isnull=True)
            .exclude(nacionalidade__exact="")
            .values_list("nacionalidade", flat=True)
            .distinct()
        )
        self.stdout.write(
            self.style.WARNING(
                f"  - Nacionalidades distintas encontradas em Países: {list(nacionalidades_paises)}"
            )
        )

        # Tentativa de correspondência
        self.stdout.write("  - Testando correspondência:")
        if not nacionalidades_alunos:
            self.stdout.write(
                self.style.NOTICE("    Nenhuma nacionalidade para testar em Alunos.")
            )
        else:
            for nac_aluno in nacionalidades_alunos:
                try:
                    pais_encontrado = Pais.objects.get(
                        nacionalidade__iexact=nac_aluno.strip()
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'    [SUCESSO] "{nac_aluno}" -> Encontrado em País: {pais_encontrado.nome} (Nacionalidade: {pais_encontrado.nacionalidade})'
                        )
                    )
                except Pais.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'    [FALHA] "{nac_aluno}" -> Não encontrado na tabela de Países com busca exata.'
                        )
                    )
                except Pais.MultipleObjectsReturned:
                    self.stdout.write(
                        self.style.ERROR(
                            f'    [FALHA] "{nac_aluno}" -> Múltiplos resultados encontrados, dados ambíguos.'
                        )
                    )

        # --- Diagnóstico de Naturalidade ---
        self.stdout.write(self.style.HTTP_INFO("\n2. Análise de Naturalidade"))
        naturalidades_alunos = (
            Aluno.objects.exclude(naturalidade__isnull=True)
            .exclude(naturalidade__exact="")
            .values_list("naturalidade", flat=True)
            .distinct()
        )

        self.stdout.write(
            self.style.WARNING(
                f"  - Primeiras 50 naturalidades distintas encontradas em Alunos: {list(naturalidades_alunos)[:50]}..."
            )
        )

        # Tentativa de correspondência
        self.stdout.write("  - Testando correspondência (primeiras 50):")
        if not naturalidades_alunos:
            self.stdout.write(
                self.style.NOTICE("    Nenhuma naturalidade para testar em Alunos.")
            )
        else:
            for nat_aluno in list(naturalidades_alunos)[:50]:
                nat_aluno_strip = nat_aluno.strip()
                try:
                    # Tentativa 1: Busca exata pelo nome da cidade
                    cidade_encontrada = Cidade.objects.get(nome__iexact=nat_aluno_strip)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'    [SUCESSO] "{nat_aluno}" -> Encontrada cidade: {cidade_encontrada.nome}/{cidade_encontrada.estado.codigo}'
                        )
                    )
                except Cidade.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'    [FALHA] "{nat_aluno}" -> Nenhuma cidade encontrada com este nome.'
                        )
                    )
                except Cidade.MultipleObjectsReturned:
                    cidades = Cidade.objects.filter(nome__iexact=nat_aluno_strip)
                    estados = [c.estado.codigo for c in cidades]
                    self.stdout.write(
                        self.style.ERROR(
                            f'    [FALHA] "{nat_aluno}" -> Nome de cidade ambíguo. Encontrado em múltiplos estados: {estados}'
                        )
                    )

        self.stdout.write(self.style.SUCCESS("\n--- Diagnóstico Concluído ---"))
