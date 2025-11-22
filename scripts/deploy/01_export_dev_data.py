#!/usr/bin/env python
"""
Script de Exportação de Dados de Desenvolvimento para Produção
Exporta dados do SQLite (dev) em formato compatível com PostgreSQL
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Configurar Django
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.development")

import django

django.setup()

from django.core import serializers
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

# Apps e modelos a exportar (ordem importa por causa de FKs)
EXPORT_ORDER = [
    # Core e autenticação
    "auth.User",
    "auth.Group",
    # Apps do sistema (ordem de dependência)
    "cursos.Curso",
    "alunos.Aluno",
    "turmas.Turma",
    "matriculas.Matricula",
    "atividades.Atividade",
    "presencas.RegistroPresenca",
    "frequencias.Frequencia",
    "notas.Nota",
    "pagamentos.Pagamento",
]


def export_data():
    """Exporta dados em formato JSON."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = Path(__file__).parent / "exports"
    export_dir.mkdir(exist_ok=True)

    output_file = export_dir / f"dev_data_{timestamp}.json"

    print(f"\n{'='*60}")
    print(f"EXPORTAÇÃO DE DADOS - DESENVOLVIMENTO → PRODUÇÃO")
    print(f"{'='*60}\n")

    all_objects = []
    stats = {}

    for model_path in EXPORT_ORDER:
        try:
            app_label, model_name = model_path.split(".")
            model = apps.get_model(app_label, model_name)

            objects = model.objects.all()
            count = objects.count()

            if count > 0:
                print(f"✓ {model_path:30} → {count:4} registros")
                all_objects.extend(objects)
                stats[model_path] = count
            else:
                print(f"  {model_path:30} → (vazio)")

        except Exception as e:
            print(f"✗ {model_path:30} → ERRO: {e}")

    # Serializar dados
    print(f"\n{'─'*60}")
    print("Serializando dados...")

    data = serializers.serialize(
        "json",
        all_objects,
        indent=2,
        use_natural_foreign_keys=True,
        use_natural_primary_keys=False,
    )

    # Salvar arquivo
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(data)

    file_size = output_file.stat().st_size / 1024  # KB

    print(f"✓ Dados exportados com sucesso!")
    print(f"\n{'='*60}")
    print(f"RESUMO DA EXPORTAÇÃO")
    print(f"{'='*60}")
    print(f"Arquivo: {output_file}")
    print(f"Tamanho: {file_size:.2f} KB")
    print(f"Total de modelos: {len(stats)}")
    print(f"Total de registros: {sum(stats.values())}")
    print(f"{'='*60}\n")

    # Salvar estatísticas
    stats_file = export_dir / f"stats_{timestamp}.json"
    with open(stats_file, "w") as f:
        json.dump(
            {
                "timestamp": timestamp,
                "file": str(output_file),
                "size_kb": file_size,
                "stats": stats,
                "total_records": sum(stats.values()),
            },
            f,
            indent=2,
        )

    return str(output_file), stats


if __name__ == "__main__":
    try:
        output_file, stats = export_data()
        print(f"✅ Exportação concluída!")
        print(f"📁 Arquivo: {output_file}")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERRO na exportação: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
