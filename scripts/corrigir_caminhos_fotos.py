"""
Script para corrigir caminhos de fotos que usam barras invertidas (\) do Windows.
Converte para barras normais (/) para compatibilidade com Linux/Docker.
"""
import os
import sys
import django

# Configuração do Ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.models import Aluno

def corrigir_caminhos_fotos():
    print("=" * 70)
    print("SCRIPT: Corrigir Caminhos de Fotos")
    print("=" * 70)
    
    # Busca todos os alunos com foto
    alunos_com_foto = Aluno.objects.filter(foto__isnull=False).exclude(foto='')
    total = alunos_com_foto.count()
    
    print(f"\n📊 Total de alunos com foto: {total}")
    
    if total == 0:
        print("\n✅ Nenhum aluno com foto encontrado.")
        return
    
    print(f"\n🔍 Verificando caminhos...\n")
    print("-" * 70)
    
    corrigidos = 0
    ja_corretos = 0
    
    for idx, aluno in enumerate(alunos_com_foto, 1):
        caminho_antigo = aluno.foto.name
        
        # Verifica se tem barras invertidas
        if '\\' in caminho_antigo:
            # Corrige substituindo \ por /
            caminho_novo = caminho_antigo.replace('\\', '/')
            
            print(f"[{idx}/{total}] {aluno.nome}")
            print(f"    Antes: {caminho_antigo}")
            print(f"    Depois: {caminho_novo}")
            
            # Atualiza apenas o campo foto
            aluno.foto.name = caminho_novo
            aluno.save(update_fields=['foto'])
            
            print(f"    ✅ Corrigido!")
            corrigidos += 1
        else:
            ja_corretos += 1
    
    print("\n" + "=" * 70)
    print("RELATÓRIO FINAL")
    print("=" * 70)
    print(f"✅ Caminhos corrigidos: {corrigidos}")
    print(f"✓  Já estavam corretos: {ja_corretos}")
    print(f"📊 Total processado:    {total}")
    print("=" * 70)
    
    if corrigidos > 0:
        print("\n⚠️  ATENÇÃO: Recarregue a página no navegador (Ctrl+Shift+R)")

if __name__ == "__main__":
    try:
        corrigir_caminhos_fotos()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
