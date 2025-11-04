import csv
import unicodedata
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from alunos.utils import get_tipo_codigo_model, get_codigo_model


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

                fieldnames = reader.fieldnames or []
                if not fieldnames:
                    self.stdout.write(
                        self.style.ERROR("Arquivo CSV sem cabeçalho detectado.")
                    )
                    return

                def normalize_header(value: str) -> str:
                    """Remove acentos, espaços extras e padroniza para comparação."""

                    normalized = unicodedata.normalize("NFKD", value or "")
                    normalized = "".join(
                        ch for ch in normalized if not unicodedata.combining(ch)
                    )
                    return normalized.strip().upper()

                header_map = {
                    normalize_header(original): original
                    for original in fieldnames
                    if original is not None and original.strip()
                }

                normalized_headers = set(header_map.keys())

                def resolve_column(possible_keys):
                    """Retorna a primeira coluna disponível dentre as opções fornecidas."""

                    for candidate in possible_keys:
                        if candidate in header_map:
                            return candidate
                    return None

                tipo_col_key = resolve_column(
                    [
                        "DESCRICAO TIPO",
                        "TIPO",
                        "TIPO NOME",
                        "NOME TIPO",
                        "NOME",
                    ]
                )
                tipo_desc_col_key = (
                    resolve_column(
                        [
                            "DESCRICAO TIPO",
                            "TIPO DESCRICAO",
                            "DESCRICAO",
                        ]
                    )
                    or tipo_col_key
                )
                codigo_col_key = resolve_column(
                    [
                        "DESCRICAO CODIGO",
                        "CODIGO",
                        "NOME CODIGO",
                        "NOME",
                    ]
                )
                codigo_desc_col_key = (
                    resolve_column(
                        [
                            "DESCRICAO CODIGO",
                            "CODIGO DESCRICAO",
                            "DESCRICAO",
                        ]
                    )
                    or codigo_col_key
                )

                somente_tipos = normalized_headers.issubset({"NOME", "DESCRICAO"})

                if tipo_col_key and codigo_col_key and not somente_tipos:
                    import_mode = "codigos"
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Modo de importação: Tipos e Códigos iniciáticos."
                        )
                    )
                elif tipo_col_key and tipo_desc_col_key:
                    import_mode = "tipos"
                    self.stdout.write(
                        self.style.SUCCESS(
                            "Modo de importação: Apenas Tipos de Código iniciáticos."
                        )
                    )
                else:
                    colunas_disponiveis = ", ".join(fieldnames)
                    self.stdout.write(
                        self.style.ERROR(
                            "Cabeçalho do CSV incompatível. Colunas disponíveis: "
                            f"{colunas_disponiveis}."
                        )
                    )
                    return

                def get_value(row, key):
                    """Recupera o valor da coluna original mapeada para a chave normalizada."""

                    if not key:
                        return ""

                    original = header_map.get(key)
                    return (row.get(original) or "").strip() if original else ""

                tipos_criados = 0
                tipos_atualizados = 0
                codigos_criados = 0
                codigos_atualizados = 0
                codigos_ignorados = 0

                TipoCodigo = get_tipo_codigo_model()
                if not TipoCodigo:
                    self.stdout.write(
                        self.style.ERROR("Modelo TipoCodigo indisponível.")
                    )
                    return

                Codigo = get_codigo_model() if import_mode == "codigos" else None
                if import_mode == "codigos" and not Codigo:
                    self.stdout.write(self.style.ERROR("Modelo Codigo indisponível."))
                    return

                with transaction.atomic():
                    for row in reader:
                        try:
                            if import_mode == "codigos":
                                codigo_nome = get_value(row, codigo_col_key)
                                tipo_nome = get_value(row, tipo_col_key)
                                tipo_descricao = get_value(row, tipo_desc_col_key)
                                codigo_descricao = get_value(row, codigo_desc_col_key)

                                if not tipo_nome or not codigo_nome:
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f"Linha ignorada por dados ausentes: {row}"
                                        )
                                    )
                                    continue

                                if not tipo_descricao:
                                    tipo_descricao = tipo_nome
                                if not codigo_descricao:
                                    codigo_descricao = codigo_nome

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
                                if tipo_descricao and tipo.descricao != tipo_descricao:
                                    tipo.descricao = tipo_descricao
                                    tipo.save(update_fields=["descricao"])
                                    tipos_atualizados += 1

                                codigo, created = Codigo.objects.get_or_create(
                                    nome=codigo_nome,
                                    defaults={
                                        "tipo_codigo": tipo,
                                        "descricao": codigo_descricao,
                                    },
                                )

                                if created:
                                    codigos_criados += 1
                                else:
                                    if (
                                        codigo.tipo_codigo_id != tipo.id
                                        or codigo.descricao != codigo_descricao
                                    ):
                                        codigo.tipo_codigo = tipo
                                        codigo.descricao = codigo_descricao
                                        codigo.save(
                                            update_fields=[
                                                "tipo_codigo",
                                                "descricao",
                                            ]
                                        )
                                        codigos_atualizados += 1
                                    else:
                                        codigos_ignorados += 1

                            else:
                                tipo_nome = get_value(row, tipo_col_key)
                                descricao = get_value(row, tipo_desc_col_key)

                                if not tipo_nome or not descricao:
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f"Linha ignorada por dados ausentes: {row}"
                                        )
                                    )
                                    continue

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
                                elif tipo.descricao != descricao:
                                    tipo.descricao = descricao
                                    tipo.save(update_fields=["descricao"])
                                    tipos_atualizados += 1

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
            if tipos_atualizados:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Tipos de Código atualizados: {tipos_atualizados}"
                    )
                )
            if import_mode == "codigos":
                self.stdout.write(
                    self.style.SUCCESS(f"Códigos criados: {codigos_criados}")
                )
                if codigos_atualizados:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Códigos atualizados: {codigos_atualizados}"
                        )
                    )
                self.stdout.write(
                    self.style.WARNING(
                        f"Códigos ignorados (já consistentes): {codigos_ignorados}"
                    )
                )
            self.stdout.write(self.style.SUCCESS("Importação concluída com sucesso!"))

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"Arquivo não encontrado em: {csv_file_path}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro inesperado: {e}"))
