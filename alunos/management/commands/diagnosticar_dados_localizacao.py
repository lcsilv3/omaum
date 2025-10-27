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
        alunos_com_pais = Aluno.objects.select_related("pais_nacionalidade").filter(
            pais_nacionalidade__isnull=False
        )
        nacionalidades_alunos = (
            alunos_com_pais.values_list("pais_nacionalidade__nacionalidade", flat=True)
            .exclude(pais_nacionalidade__nacionalidade__isnull=True)
            .exclude(pais_nacionalidade__nacionalidade__exact="")
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
                valor = (nac_aluno or "").strip()
                if not valor:
                    continue
                pais_encontrado = Pais.objects.filter(
                    nacionalidade__iexact=valor
                ).first()
                if pais_encontrado:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'    [SUCESSO] "{valor}" -> Encontrado em País: {pais_encontrado.nome} (Nacionalidade: {pais_encontrado.nacionalidade})'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'    [FALHA] "{valor}" -> Não encontrado na tabela de Países com busca exata.'
                        )
                    )

        # --- Diagnóstico de Naturalidade ---
        self.stdout.write(self.style.HTTP_INFO("\n2. Análise de Naturalidade"))
        alunos_com_cidade = Aluno.objects.select_related(
            "cidade_naturalidade", "cidade_naturalidade__estado"
        ).filter(cidade_naturalidade__isnull=False)
        naturalidades_alunos = alunos_com_cidade.values_list(
            "cidade_naturalidade__nome", "cidade_naturalidade__estado__codigo"
        ).distinct()

        self.stdout.write(
            self.style.WARNING(
                "  - Primeiras 50 naturalidades distintas encontradas em Alunos: "
                f"{[(nome, uf) for nome, uf in list(naturalidades_alunos)[:50]]}..."
            )
        )

        # Tentativa de correspondência
        self.stdout.write("  - Testando correspondência (primeiras 50):")
        if not naturalidades_alunos:
            self.stdout.write(
                self.style.NOTICE("    Nenhuma naturalidade para testar em Alunos.")
            )
        else:
            for nome_cidade, uf in list(naturalidades_alunos)[:50]:
                nome_cidade = (nome_cidade or "").strip()
                uf = (uf or "").strip()
                if not nome_cidade:
                    continue
                qs = Cidade.objects.filter(nome__iexact=nome_cidade)
                if uf:
                    qs = qs.filter(estado__codigo__iexact=uf)
                cidades = list(qs)
                if len(cidades) == 1:
                    cidade = cidades[0]
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'    [SUCESSO] "{nome_cidade}" ({uf or "??"}) -> Encontrada cidade: {cidade.nome}/{cidade.estado.codigo}'
                        )
                    )
                elif len(cidades) > 1:
                    estados = [c.estado.codigo for c in cidades]
                    self.stdout.write(
                        self.style.ERROR(
                            f'    [FALHA] "{nome_cidade}" -> Nome ambiguo. Encontrado em múltiplos estados: {estados}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'    [FALHA] "{nome_cidade}" ({uf or "??"}) -> Nenhuma cidade encontrada com este nome.'
                        )
                    )

        self.stdout.write(self.style.SUCCESS("\n--- Diagnóstico Concluído ---"))
