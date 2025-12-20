"""
Script para migrar backup JSON de schema antigo para novo schema PostgreSQL.
Trata incompatibilidades de campos e conversões necessárias.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence


# Mapeamentos de conversão
SITUACAO_ALUNO_MAP = {
    "ATIVO": "a",
    "INATIVO": "i",
    "SUSPENSO": "s",
    "ARQUIVADO": "r",
    "FALECIDO": "f",
    "EXCLUIDO": "e",
    "a": "a",  # já convertido
    "i": "i",
    "s": "s",
    "r": "r",
    "f": "f",
    "e": "e",
}

DEFAULT_INPUT_PATH = Path(
    r"C:\Users\Ordem\OneDrive\10 PROJETOS\dev_data_20251126_090717.json"
)
DEFAULT_OUTPUT_PATH = Path(r"C:\projetos\omaum\backup_migrado.json")
DEFAULT_EXCLUDED_MODELS = ("auth.permission", "contenttypes.contenttype")


def limpar_cpf(cpf: str | int | None) -> str:
    """Remove caracteres não numéricos e limita a 11 dígitos."""
    if not cpf:
        return ""

    apenas_numeros = re.sub(r"\D", "", str(cpf))
    return apenas_numeros[:11]


def converter_situacao_aluno(situacao: str | None) -> str:
    """Converte situação de texto completo para código de 1 caractere."""
    if not situacao:
        return "a"
    return SITUACAO_ALUNO_MAP.get(
        situacao.upper() if isinstance(situacao, str) else situacao, "a"
    )


def migrar_aluno(fields: dict) -> dict:
    """Migra campos do modelo Aluno antigo para novo."""
    # Converter situacao
    if "situacao" in fields:
        fields["situacao"] = converter_situacao_aluno(fields["situacao"])

    # Limpar CPF
    if "cpf" in fields:
        fields["cpf"] = limpar_cpf(fields["cpf"])

    # Remover campos que não existem mais (se houver)
    campos_remover = []
    for campo in campos_remover:
        fields.pop(campo, None)

    return fields


def migrar_turma(fields: dict) -> dict:
    """Migra campos do modelo Turma antigo para novo."""
    # Campos que existiam no backup mas não existem no modelo atual
    campos_remover = [
        "encerrada_em",
        "encerrada_por",
        "bloqueio_total",
        "bloqueio_ativo_em",
        "bloqueio_ativo_por",
        "justificativa_reabertura",
    ]

    for campo in campos_remover:
        fields.pop(campo, None)

    return fields


def migrar_codigo(fields: dict) -> dict:
    """Migra campos do modelo Codigo antigo para novo."""
    # Adicionar campo ativo se não existir (padrão True)
    if "ativo" not in fields:
        fields["ativo"] = True
    return fields


def migrar_tipocodigo(fields: dict) -> dict:
    """Migra campos do modelo TipoCodigo antigo para novo."""
    # Adicionar campo ativo se não existir (padrão True)
    if "ativo" not in fields:
        fields["ativo"] = True
    return fields


def migrar_registro(registro: dict) -> dict:
    """Migra um registro individual baseado no seu model."""
    model = registro.get("model", "")
    fields = registro.get("fields", {})

    # Aplicar migração específica por modelo
    if model == "alunos.aluno":
        fields = migrar_aluno(fields)
    elif model == "turmas.turma":
        fields = migrar_turma(fields)
    elif model == "alunos.codigo":
        fields = migrar_codigo(fields)
    elif model == "alunos.tipocodigo":
        fields = migrar_tipocodigo(fields)

    registro["fields"] = fields
    return registro


def processar_backup(
    caminho_entrada: Path,
    caminho_saida: Path,
    excluir_models: Iterable[str] | None = None,
) -> tuple[int, int]:
    """
    Processa arquivo de backup aplicando migrações.

    Args:
        caminho_entrada: Path do JSON original
        caminho_saida: Path do JSON migrado
        excluir_models: Lista de models a excluir (ex: ['auth.permission'])
    """
    if excluir_models is None:
        excluir_models = list(DEFAULT_EXCLUDED_MODELS)

    print(f"[*] Lendo backup: {caminho_entrada}")
    with caminho_entrada.open("r", encoding="utf-8") as handle:
        dados = json.load(handle)

    print(f"[*] Total de registros: {len(dados)}")

    # Filtrar models excluídos
    dados_filtrados = [reg for reg in dados if reg.get("model") not in excluir_models]
    print(f"[*] Após filtrar models: {len(dados_filtrados)}")

    # Migrar cada registro
    dados_migrados: list[dict] = []
    erros_encontrados: list[tuple[int, str, int | None, str]] = []

    for idx, registro in enumerate(dados_filtrados):
        try:
            registro_migrado = migrar_registro(registro)
            dados_migrados.append(registro_migrado)
        except Exception as exc:  # noqa: BLE001 - precisamos continuar processando
            erros_encontrados.append(
                (idx, registro.get("model", "unknown"), registro.get("pk"), str(exc))
            )
            print(
                f"[!] Erro ao migrar {registro.get('model')}(pk={registro.get('pk')}): {exc}"
            )

    print(f"[*] Registros migrados com sucesso: {len(dados_migrados)}")

    if erros_encontrados:
        print(f"\n[!] {len(erros_encontrados)} erros encontrados:")
        for idx, model, pk, erro in erros_encontrados[:10]:
            print(f"  - [{idx}] {model}(pk={pk}): {erro}")

    # Estatísticas por model
    models_count = {}
    for reg in dados_migrados:
        model = reg.get("model", "unknown")
        models_count[model] = models_count.get(model, 0) + 1

    print("\n[*] Distribuição por model:")
    for model in sorted(models_count.keys()):
        print(f"  {model}: {models_count[model]}")

    # Salvar resultado
    print(f"\n[*] Salvando backup migrado: {caminho_saida}")
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    with caminho_saida.open("w", encoding="utf-8") as handle:
        json.dump(dados_migrados, handle, ensure_ascii=False, indent=2)

    print("[✓] Migração concluída!")
    print(f"    Original: {len(dados)} registros")
    print(f"    Migrado: {len(dados_migrados)} registros")
    print(f"    Erros: {len(erros_encontrados)}")

    return len(dados_migrados), len(erros_encontrados)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Cria o parser CLI e devolve o namespace preenchido."""

    parser = argparse.ArgumentParser(
        description="Migra backups JSON antigos para o schema atual do OMAUM."
    )
    parser.add_argument(
        "-i",
        "--entrada",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Caminho do arquivo JSON exportado do schema antigo.",
    )
    parser.add_argument(
        "-o",
        "--saida",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Caminho do arquivo JSON que será gerado já no novo schema.",
    )
    parser.add_argument(
        "-x",
        "--excluir-model",
        dest="excluir_models",
        action="append",
        default=None,
        help="Model (app.Model) a remover do backup. Pode ser informado mais de uma vez.",
    )
    parser.add_argument(
        "--ignorar-inexistente",
        action="store_true",
        help="Mostra aviso ao invés de erro caso o arquivo de entrada não exista.",
    )

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Função principal utilizada ao rodar via linha de comando."""

    args = parse_args(argv)
    entrada: Path = args.entrada
    saida: Path = args.saida
    excluir_models = args.excluir_models

    if not entrada.exists():
        mensagem = f"[!] Arquivo não encontrado: {entrada}"
        print(mensagem)
        return 0 if args.ignorar_inexistente else 1

    total, erros = processar_backup(entrada, saida, excluir_models)

    if erros > 0:
        print(f"\n[!] Migração completou com {erros} erros.")
        print(
            "[*] Revise os erros acima e ajuste as funções de migração se necessário."
        )
        return 1

    print("\n[✓] Migração bem-sucedida sem erros!")
    print("\n[*] Para importar no PostgreSQL:")
    print(f"    docker cp {saida} omaum-web-prod:/app/backup_migrado.json")
    print(
        "    docker exec omaum-web-prod python manage.py loaddata /app/backup_migrado.json"
    )
    print(f"\n[*] Total migrado: {total} registros")
    return 0


if __name__ == "__main__":
    sys.exit(main())
