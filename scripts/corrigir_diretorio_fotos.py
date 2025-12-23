"""
Script para corrigir diretório de fotos dos alunos.

Problema: Fotos foram salvas com caminho 'fotos_alunos/' mas o modelo usa 'alunos/fotos/'.
Este script:
1. Corrige caminhos no banco de dados
2. Limpa registros sem arquivo físico correspondente
"""
import os
import sys
import django

# Configuração do Ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.models import Aluno
from django.conf import settings

def corrigir_diretorios_fotos():
    print("=" * 70)
    print("SCRIPT: Corrigir Diretórios de Fotos")
    print("=" * 70)
    
    # Busca todos os alunos com foto
    alunos_com_foto = Aluno.objects.filter(foto__isnull=False).exclude(foto='')
    total = alunos_com_foto.count()
    
    print(f"\n📊 Total de alunos com foto no banco: {total}")
    
    if total == 0:
        print("\n✅ Nenhum aluno com foto encontrado.")
        return
    
    print(f"\n🔍 Verificando arquivos físicos e corrigindo caminhos...\n")
    print("-" * 70)
    
    stats = {
        'ja_correto': 0,
        'corrigido_caminho': 0,
        'sem_arquivo': 0,
        'limpos': 0
    }
    
    for idx, aluno in enumerate(alunos_com_foto, 1):
        caminho_banco = aluno.foto.name
        caminho_fisico = aluno.foto.path
        
        print(f"[{idx}/{total}] {aluno.nome}")
        print(f"    Caminho no banco: {caminho_banco}")
        
        # Verifica se arquivo existe
        arquivo_existe = os.path.exists(caminho_fisico)
        
        if arquivo_existe:
            print(f"    ✅ Arquivo existe: {caminho_fisico}")
            stats['ja_correto'] += 1
        else:
            # Tenta corrigir o caminho
            if caminho_banco.startswith('fotos_alunos/'):
                # Corrige para alunos/fotos/
                caminho_correto = caminho_banco.replace('fotos_alunos/', 'alunos/fotos/')
                caminho_fisico_correto = os.path.join(settings.MEDIA_ROOT, caminho_correto)
                
                if os.path.exists(caminho_fisico_correto):
                    print(f"    ⚠️  Corrigindo caminho para: {caminho_correto}")
                    aluno.foto.name = caminho_correto
                    aluno.save(update_fields=['foto'])
                    print(f"    ✅ Caminho corrigido!")
                    stats['corrigido_caminho'] += 1
                else:
                    print(f"    ❌ Arquivo não existe nem no caminho correto")
                    print(f"       Procurou em: {caminho_fisico_correto}")
                    print(f"    🗑️  Removendo referência do banco...")
                    aluno.foto = None
                    aluno.save(update_fields=['foto'])
                    stats['limpos'] += 1
            else:
                print(f"    ❌ Arquivo não existe: {caminho_fisico}")
                print(f"    🗑️  Removendo referência do banco...")
                aluno.foto = None
                aluno.save(update_fields=['foto'])
                stats['limpos'] += 1
        
        print()
    
    print("=" * 70)
    print("RELATÓRIO FINAL")
    print("=" * 70)
    print(f"✅ Já estavam corretos:    {stats['ja_correto']}")
    print(f"🔧 Caminhos corrigidos:    {stats['corrigido_caminho']}")
    print(f"🗑️  Referências limpas:    {stats['limpos']}")
    print(f"📊 Total processado:       {total}")
    print("=" * 70)
    
    if stats['limpos'] > 0:
        print(f"\n⚠️  {stats['limpos']} alunos ficaram sem foto.")
        print("   Execute: python scripts/preencher_fotos_alunos.py")

if __name__ == "__main__":
    try:
        corrigir_diretorios_fotos()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
