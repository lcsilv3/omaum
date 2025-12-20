"""
Script para preencher fotos de alunos usando API RandomUser.

Uso:
    python scripts/preencher_fotos_alunos.py              # Apenas alunos sem foto
    python scripts/preencher_fotos_alunos.py --force      # Atualiza todos os alunos
    python scripts/preencher_fotos_alunos.py --dry-run    # Simula sem aplicar mudanças
"""
import os
import sys
import django
import random
import requests
import argparse
from django.core.files.base import ContentFile
from django.db.models import Q

# --- Configuração do Ambiente Django ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()
# ----------------------------------------

from alunos.models import Aluno

# Lista expandida de URLs de fotos aleatórias (API RandomUser)
# Usando range maior para maior variedade
FOTOS_MASCULINAS = [
    f"https://randomuser.me/api/portraits/men/{i}.jpg" for i in range(0, 100)
]
FOTOS_FEMININAS = [
    f"https://randomuser.me/api/portraits/women/{i}.jpg" for i in range(0, 100)
]


def preencher_fotos(force=False, dry_run=False):
    """
    Preenche a foto para alunos ativos que não têm uma.
    
    Args:
        force (bool): Se True, atualiza fotos mesmo de alunos que já têm
        dry_run (bool): Se True, apenas simula sem salvar mudanças
    """
    print("=" * 70)
    print("SCRIPT: Preencher Fotos de Alunos")
    print("=" * 70)
    
    if dry_run:
        print("⚠️  MODO DRY-RUN: Nenhuma mudança será aplicada\n")
    
    if force:
        print("🔄 MODO FORCE: Atualizando fotos de TODOS os alunos ativos\n")
    
    # Filtra alunos ativos (situacao='a')
    if force:
        alunos = Aluno.objects.filter(situacao='a')
        print(f"📊 Total de alunos ativos: {alunos.count()}")
    else:
        # Apenas alunos sem foto
        alunos = Aluno.objects.filter(
            Q(foto__isnull=True) | Q(foto=""), 
            situacao='a'
        )
        total_ativos = Aluno.objects.filter(situacao='a').count()
        print(f"📊 Total de alunos ativos: {total_ativos}")
        print(f"📊 Alunos sem foto: {alunos.count()}")

    if not alunos.exists():
        print("\n✅ Todos os alunos ativos já possuem fotos!")
        return

    print(f"\n🚀 Processando {alunos.count()} alunos...\n")
    print("-" * 70)

    # Estatísticas
    stats = {
        'masculino': 0,
        'feminino': 0,
        'outro': 0,
        'sucesso': 0,
        'erro': 0
    }

    for idx, aluno in enumerate(alunos, 1):
        # Conta por sexo
        if aluno.sexo == "F":
            stats['feminino'] += 1
            url = random.choice(FOTOS_FEMININAS)
            sexo_label = "Feminino"
        elif aluno.sexo == "M":
            stats['masculino'] += 1
            url = random.choice(FOTOS_MASCULINAS)
            sexo_label = "Masculino"
        else:
            stats['outro'] += 1
            # Para "Outro", usa aleatoriamente masculino ou feminino
            url = random.choice(FOTOS_MASCULINAS + FOTOS_FEMININAS)
            sexo_label = "Outro"

        print(f"[{idx}/{alunos.count()}] {aluno.nome} ({sexo_label})")
        
        if dry_run:
            print(f"    → Foto seria baixada de: {url}")
            stats['sucesso'] += 1
            continue

        try:
            # Baixa a imagem
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            # Remove foto antiga se existir e force=True
            if force and aluno.foto:
                try:
                    aluno.foto.delete(save=False)
                except Exception:
                    pass  # Ignora erros ao deletar foto antiga

            # Cria um nome de arquivo único
            nome_arquivo = f"aluno_{aluno.id}_{random.randint(10000, 99999)}.jpg"

            # Salva o arquivo usando o sistema de arquivos do Django
            aluno.foto.save(nome_arquivo, ContentFile(response.content), save=True)

            print(f"    ✅ Foto atribuída com sucesso!")
            stats['sucesso'] += 1

        except requests.RequestException as e:
            print(f"    ❌ Erro de rede: {e}")
            stats['erro'] += 1
        except Exception as e:
            print(f"    ❌ Erro inesperado: {e}")
            stats['erro'] += 1

    # Relatório final
    print("\n" + "=" * 70)
    print("RELATÓRIO FINAL")
    print("=" * 70)
    print(f"✅ Sucessos:          {stats['sucesso']}")
    print(f"❌ Erros:             {stats['erro']}")
    print(f"👨 Masculino:         {stats['masculino']}")
    print(f"👩 Feminino:          {stats['feminino']}")
    if stats['outro'] > 0:
        print(f"⚧  Outro:             {stats['outro']}")
    print(f"📊 Total processado:  {stats['sucesso'] + stats['erro']}")
    print("=" * 70)
    
    if dry_run:
        print("\n⚠️  Este foi um DRY-RUN. Execute sem --dry-run para aplicar mudanças.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preenche fotos de alunos usando RandomUser API"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Atualiza fotos mesmo de alunos que já têm'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simula execução sem aplicar mudanças'
    )
    
    args = parser.parse_args()
    
    try:
        preencher_fotos(force=args.force, dry_run=args.dry_run)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
