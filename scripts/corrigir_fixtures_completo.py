#!/usr/bin/env python3
"""
Script para corrigir fixtures de forma abrangente.
Corrige:
1. Remove permissions e content types (conflitos de auto-geração)
2. Mapeia situacao de texto completo para código de 1 caractere
3. Remove campos inexistentes de Turma
4. Qualquer outra inconsistência entre dev e prod
"""

import json
import sys
from pathlib import Path


def corrigir_fixtures(arquivo_entrada, arquivo_saida):
    """
    Corrige fixtures para serem compatíveis com produção.

    Args:
        arquivo_entrada: Path do arquivo JSON de entrada
        arquivo_saida: Path do arquivo JSON corrigido
    """
    print(f"Lendo {arquivo_entrada}...")
    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Total de registros originais: {len(data)}")

    # Contadores
    stats = {
        "removidos_permission": 0,
        "removidos_contenttype": 0,
        "corrigidos_situacao": 0,
        "corrigidos_situacao_iniciatica": 0,
        "campos_turma_removidos": 0,
        "turmas_processadas": 0,
    }

    # 1. Filtrar permissions e content types
    print("\n1. Removendo permissions e content types...")
    data_filtrada = []
    for obj in data:
        if obj["model"] == "auth.permission":
            stats["removidos_permission"] += 1
            continue
        if obj["model"] == "contenttypes.contenttype":
            stats["removidos_contenttype"] += 1
            continue
        data_filtrada.append(obj)

    print(f"   - Removidas {stats['removidos_permission']} permissions")
    print(f"   - Removidos {stats['removidos_contenttype']} content types")

    # 2. Corrigir campos de situacao em Aluno
    print("\n2. Corrigindo campos de situação em Aluno...")
    mapa_situacao = {"ATIVO": "a", "INATIVO": "i", "SUSPENSO": "s", "TRANCADO": "t"}

    mapa_situacao_iniciatica = {
        "ATIVO": "A",
        "INATIVO": "I",
        "EXONERADO": "E",
        "DESLIGADO": "D",
    }

    for obj in data_filtrada:
        if obj["model"] == "alunos.aluno":
            fields = obj["fields"]

            # Corrigir situacao
            if "situacao" in fields and isinstance(fields["situacao"], str):
                if len(fields["situacao"]) > 1:
                    valor_original = fields["situacao"]
                    fields["situacao"] = mapa_situacao.get(valor_original, "a")
                    stats["corrigidos_situacao"] += 1

            # Corrigir situacao_iniciatica
            if "situacao_iniciatica" in fields and isinstance(
                fields["situacao_iniciatica"], str
            ):
                if len(fields["situacao_iniciatica"]) > 1:
                    valor_original = fields["situacao_iniciatica"]
                    fields["situacao_iniciatica"] = mapa_situacao_iniciatica.get(
                        valor_original, "I"
                    )
                    stats["corrigidos_situacao_iniciatica"] += 1

    print(f"   - Corrigidos {stats['corrigidos_situacao']} campos situacao")
    print(
        f"   - Corrigidos {stats['corrigidos_situacao_iniciatica']} campos situacao_iniciatica"
    )

    # 3. Limpar campos inexistentes de Turma
    print("\n3. Removendo campos inexistentes de Turma...")

    # Campos válidos conforme modelo atual em produção
    campos_validos_turma = {
        "nome",
        "curso",
        "descricao",
        "num_livro",
        "perc_presenca_minima",
        "data_iniciacao",
        "data_inicio_ativ",
        "data_prim_aula",
        "data_termino_atividades",
        "dias_semana",
        "horario",
        "local",
        "vagas",
        "status",
        "ativo",
        "created_at",
        "updated_at",
    }

    for obj in data_filtrada:
        if obj["model"] == "turmas.turma":
            stats["turmas_processadas"] += 1
            fields = obj["fields"]
            campos_atuais = list(fields.keys())

            for campo in campos_atuais:
                if campo not in campos_validos_turma:
                    fields.pop(campo)
                    stats["campos_turma_removidos"] += 1

    print(f"   - Processadas {stats['turmas_processadas']} turmas")
    print(f"   - Removidos {stats['campos_turma_removidos']} campos inexistentes")

    # Salvar arquivo corrigido
    print(f"\nSalvando {arquivo_saida}...")
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(data_filtrada, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print("RESUMO DA CORREÇÃO")
    print(f"{'=' * 60}")
    print(f"Registros originais: {len(data)}")
    print(f"Registros finais: {len(data_filtrada)}")
    print(f"Removidos: {len(data) - len(data_filtrada)}")
    print(f"\nDetalhamento:")
    for chave, valor in stats.items():
        print(f"  - {chave}: {valor}")
    print(f"{'=' * 60}")
    print(f"\nArquivo corrigido salvo: {arquivo_saida}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arquivo_entrada = sys.argv[1]
        arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else "fixtures_corrigido.json"
    else:
        # Usar arquivo padrão se não especificado
        arquivo_entrada = "dev_data_20251126_090717.json"
        arquivo_saida = "dev_data_corrigido.json"

    corrigir_fixtures(arquivo_entrada, arquivo_saida)
