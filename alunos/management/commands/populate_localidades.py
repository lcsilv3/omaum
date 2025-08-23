from django.core.management.base import BaseCommand
from django.db import transaction
from alunos.models import Pais, Estado, Cidade, Bairro

BRASIL_PAISES = [
    {"codigo": "BRA", "nome": "Brasil", "nacionalidade": "Brasileira"},
]

ESTADOS_BR = [
    ("AC", "Acre", "Norte"),
    ("AL", "Alagoas", "Nordeste"),
    ("AP", "Amapá", "Norte"),
    ("AM", "Amazonas", "Norte"),
    ("BA", "Bahia", "Nordeste"),
    ("CE", "Ceará", "Nordeste"),
    ("DF", "Distrito Federal", "Centro-Oeste"),
    ("ES", "Espírito Santo", "Sudeste"),
    ("GO", "Goiás", "Centro-Oeste"),
    ("MA", "Maranhão", "Nordeste"),
    ("MT", "Mato Grosso", "Centro-Oeste"),
    ("MS", "Mato Grosso do Sul", "Centro-Oeste"),
    ("MG", "Minas Gerais", "Sudeste"),
    ("PA", "Pará", "Norte"),
    ("PB", "Paraíba", "Nordeste"),
    ("PR", "Paraná", "Sul"),
    ("PE", "Pernambuco", "Nordeste"),
    ("PI", "Piauí", "Nordeste"),
    ("RJ", "Rio de Janeiro", "Sudeste"),
    ("RN", "Rio Grande do Norte", "Nordeste"),
    ("RS", "Rio Grande do Sul", "Sul"),
    ("RO", "Rondônia", "Norte"),
    ("RR", "Roraima", "Norte"),
    ("SC", "Santa Catarina", "Sul"),
    ("SP", "São Paulo", "Sudeste"),
    ("SE", "Sergipe", "Nordeste"),
    ("TO", "Tocantins", "Norte"),
]

CIDADES_MINIMAS = {
    "SP": ["São Paulo", "Campinas", "Santos"],
    "RJ": ["Rio de Janeiro", "Niterói"],
    "MG": ["Belo Horizonte", "Uberlândia"],
    "BA": ["Salvador"],
    "PR": ["Curitiba"],
    "RS": ["Porto Alegre"],
    "PE": ["Recife"],
    "CE": ["Fortaleza"],
    "DF": ["Brasília"],
}

BAIRROS_EXEMPLO = {
    "São Paulo": ["Centro", "Pinheiros", "Moema"],
    "Rio de Janeiro": ["Centro", "Copacabana", "Barra da Tijuca"],
    "Belo Horizonte": ["Centro", "Savassi"],
    "Salvador": ["Centro", "Barra"],
}

class Command(BaseCommand):
    help = "Popula tabelas de País, Estado, Cidade e opcionalmente Bairro com dados básicos do Brasil."

    def add_arguments(self, parser):
        parser.add_argument("--with-bairros", action="store_true", help="Também criar registros de bairros de exemplo")
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Substitui (apaga) os registros existentes antes de popular",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        with_bairros = options["with_bairros"]
        replace = options["replace"]

        if replace:
            self.stdout.write(self.style.WARNING("Apagando dados existentes..."))
            Bairro.objects.all().delete()
            Cidade.objects.all().delete()
            Estado.objects.all().delete()
            Pais.objects.filter(codigo="BRA").delete()

        for p in BRASIL_PAISES:
            pais, created = Pais.objects.get_or_create(
                codigo=p["codigo"],
                defaults={"nome": p["nome"], "nacionalidade": p["nacionalidade"], "ativo": True},
            )
            self.stdout.write(self.style.SUCCESS(f"País {'criado' if created else 'existente'}: {pais.nome}"))

        estados_cache = {}
        for sigla, nome, regiao in ESTADOS_BR:
            estado, created = Estado.objects.get_or_create(codigo=sigla, defaults={"nome": nome, "regiao": regiao})
            estados_cache[sigla] = estado
            if created:
                self.stdout.write(self.style.SUCCESS(f"Estado criado: {nome} ({sigla})"))

        for sigla, lista in CIDADES_MINIMAS.items():
            estado = estados_cache.get(sigla)
            if not estado:
                continue
            for nome_cidade in lista:
                cidade, created = Cidade.objects.get_or_create(nome=nome_cidade, estado=estado)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Cidade criada: {nome_cidade} - {estado.codigo}"))

        if with_bairros:
            for cidade_nome, bairros in BAIRROS_EXEMPLO.items():
                for cidade in Cidade.objects.filter(nome=cidade_nome):
                    for bairro_nome in bairros:
                        bairro, created = Bairro.objects.get_or_create(nome=bairro_nome, cidade=cidade)
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Bairro criado: {bairro_nome} ({cidade_nome})"))

        self.stdout.write(self.style.SUCCESS("População de localidades concluída."))
