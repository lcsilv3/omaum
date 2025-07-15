import csv
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from alunos.models import TipoCodigo, Codigo


class Command(BaseCommand):
    help = "Importa códigos de uma planilha CSV para o banco de dados."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "csv_file", type=str, help="O caminho para o arquivo CSV a ser importado."
        )

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]
        self.stdout.write(
            self.style.SUCCESS(
                f'Iniciando a importação do arquivo "{csv_file_path}"...'
            )
        )

        try:
            with open(csv_file_path, mode="r", encoding="latin-1") as file:
                reader = csv.DictReader(file, delimiter=";")

                codigos_criados = 0
                tipos_criados = 0
                codigos_ignorados = 0

                with transaction.atomic():
                    for row in reader:
                        try:
                            # Usando 'nome' em vez de 'codigo' conforme modelo atual
                            codigo_nome = row.get("CODIGO", row.get("NOME", "")).strip()
                            tipo_nome = row["TIPO"].strip()
                            descricao = row["DESCRICAO"].strip()

                            if not codigo_nome or not tipo_nome or not descricao:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"Linha ignorada por dados ausentes: {row}"
                                    )
                                )
                                continue

                            # Cria ou obtém o TipoCodigo
                            tipo, created = TipoCodigo.objects.get_or_create(
                                nome=tipo_nome
                            )
                            if created:
                                tipos_criados += 1
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f'Novo tipo criado: "{tipo_nome}"'
                                    )
                                )

                            # Cria o Codigo se ele não existir (usando campo correto)
                            _, created = Codigo.objects.get_or_create(
                                nome=codigo_nome,
                                defaults={"tipo_codigo": tipo, "descricao": descricao},
                            )

                            if created:
                                codigos_criados += 1
                            else:
                                codigos_ignorados += 1

                        except (ValueError, KeyError) as e:
                            self.stdout.write(
                                self.style.ERROR(f"Erro ao processar linha {row}: {e}")
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Um erro inesperado ocorreu na linha {row}: {e}"
                                )
                            )

            self.stdout.write(self.style.SUCCESS("\n--- Resumo da Importação ---"))
            self.stdout.write(
                self.style.SUCCESS(f"Tipos de Código criados: {tipos_criados}")
            )
            self.stdout.write(self.style.SUCCESS(f"Códigos criados: {codigos_criados}"))
            self.stdout.write(
                self.style.WARNING(
                    f"Códigos ignorados (já existentes): {codigos_ignorados}"
                )
            )
            self.stdout.write(self.style.SUCCESS("Importação concluída com sucesso!"))

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"Arquivo não encontrado em: {csv_file_path}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro inesperado: {e}"))
