"""
Comando para importar bairros (distritos) das cidades usando a API do IBGE.
"""
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from alunos.models import Cidade, Bairro


class Command(BaseCommand):
    help = "Importa bairros (distritos) das cidades usando a API do IBGE"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limite",
            type=int,
            default=None,
            help="Limita o número de cidades a processar (para testes)",
        )
        parser.add_argument(
            "--estado",
            type=str,
            default=None,
            help="Processa apenas cidades de um estado específico (sigla, ex: MA)",
        )

    def handle(self, *args, **options):
        limite = options["limite"]
        estado_filter = options["estado"]

        # Filtra cidades
        cidades_qs = Cidade.objects.select_related("estado")
        if estado_filter:
            cidades_qs = cidades_qs.filter(estado__codigo=estado_filter.upper())

        if limite:
            cidades_qs = cidades_qs[:limite]

        total_cidades = cidades_qs.count()
        self.stdout.write(f"\n📊 Total de cidades a processar: {total_cidades}\n")

        processadas = 0
        com_bairros = 0
        sem_bairros = 0
        erros = 0

        for cidade in cidades_qs:
            processadas += 1

            # Verifica se já tem bairros
            if Bairro.objects.filter(cidade=cidade).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"[{processadas}/{total_cidades}] {cidade.nome} ({cidade.estado.codigo}) - "
                        f"Já tem bairros, pulando..."
                    )
                )
                com_bairros += 1
                continue

            # Busca código IBGE da cidade
            if not cidade.codigo_ibge:
                self.stdout.write(
                    self.style.ERROR(
                        f"[{processadas}/{total_cidades}] {cidade.nome} ({cidade.estado.codigo}) - "
                        f"Sem código IBGE!"
                    )
                )
                erros += 1
                continue

            # Busca distritos na API do IBGE
            try:
                url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{cidade.codigo_ibge}/distritos"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                distritos = response.json()

                if not distritos:
                    # Se não tem distritos, cria alguns bairros genéricos
                    bairros_genericos = [
                        "Centro",
                        "Zona Norte",
                        "Zona Sul",
                        "Zona Leste",
                        "Zona Oeste",
                    ]
                    with transaction.atomic():
                        for nome in bairros_genericos:
                            Bairro.objects.get_or_create(
                                nome=nome, cidade=cidade
                            )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[{processadas}/{total_cidades}] {cidade.nome} ({cidade.estado.codigo}) - "
                            f"✅ Criados {len(bairros_genericos)} bairros genéricos"
                        )
                    )
                    com_bairros += 1
                else:
                    # Importa distritos como bairros
                    with transaction.atomic():
                        for distrito in distritos:
                            Bairro.objects.get_or_create(
                                nome=distrito["nome"], cidade=cidade
                            )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[{processadas}/{total_cidades}] {cidade.nome} ({cidade.estado.codigo}) - "
                            f"✅ Importados {len(distritos)} distritos"
                        )
                    )
                    com_bairros += 1

            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"[{processadas}/{total_cidades}] {cidade.nome} ({cidade.estado.codigo}) - "
                        f"Erro na API: {e}"
                    )
                )
                erros += 1
                # Cria bairros genéricos em caso de erro
                bairros_genericos = ["Centro", "Outro"]
                with transaction.atomic():
                    for nome in bairros_genericos:
                        Bairro.objects.get_or_create(nome=nome, cidade=cidade)
                sem_bairros += 1

        # Resumo final
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("\n📊 RESUMO DA IMPORTAÇÃO:\n"))
        self.stdout.write(f"   Total processadas: {processadas}")
        self.stdout.write(f"   ✅ Com bairros: {com_bairros}")
        self.stdout.write(f"   ⚠️  Sem bairros: {sem_bairros}")
        self.stdout.write(f"   ❌ Erros: {erros}")
        self.stdout.write("\n" + "=" * 60 + "\n")
