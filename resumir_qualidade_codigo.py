#!/usr/bin/env python3
"""
Script para retomar a melhoria da qualidade do código.
Baseado no checkpoint salvo em CHECKPOINT_QUALIDADE_CODIGO.md

Uso:
    python resumir_qualidade_codigo.py [--auto] [--report-only]
    
Opções:
    --auto: Aplica correções automáticas sem interação
    --report-only: Apenas gera relatório, não aplica correções
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description=""):
    """Executa comando e retorna resultado."""
    print(f"🔍 {description}")
    print(f"Executando: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - Sucesso")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} - Erro")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
    
    return result

def get_ruff_stats():
    """Obtém estatísticas do ruff."""
    cmd = "python -m ruff check --statistics ."
    result = run_command(cmd, "Coletando estatísticas do ruff")
    return result

def check_django():
    """Verifica se Django está funcionando."""
    cmd = "python manage.py check"
    result = run_command(cmd, "Verificando Django")
    return result.returncode == 0

def apply_automatic_fixes():
    """Aplica correções automáticas."""
    cmd = "python -m ruff check --fix ."
    result = run_command(cmd, "Aplicando correções automáticas")
    return result

def apply_unsafe_fixes():
    """Aplica correções não seguras."""
    cmd = "python -m ruff check --fix --unsafe-fixes ."
    result = run_command(cmd, "Aplicando correções não seguras")
    return result

def generate_report():
    """Gera relatório detalhado."""
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE QUALIDADE DO CÓDIGO")
    print("="*60)
    
    # Estatísticas gerais
    stats_result = get_ruff_stats()
    
    # Status do Django
    django_ok = check_django()
    print(f"\n🌟 Status Django: {'✅ OK' if django_ok else '❌ ERRO'}")
    
    # Erros por categoria
    print("\n📋 Analisando erros por categoria...")
    categories = ["F401", "E402", "F405", "F403", "F811", "F821", "E722", "F841"]
    
    for category in categories:
        cmd = f"python -m ruff check --select {category} . | head -5"
        result = run_command(cmd, f"Verificando {category}")
    
    return stats_result, django_ok

def main():
    parser = argparse.ArgumentParser(description="Retoma melhoria da qualidade do código")
    parser.add_argument("--auto", action="store_true", help="Aplica correções automáticas")
    parser.add_argument("--report-only", action="store_true", help="Apenas gera relatório")
    parser.add_argument("--unsafe", action="store_true", help="Aplica correções não seguras")
    
    args = parser.parse_args()
    
    print("🚀 RETOMANDO MELHORIA DA QUALIDADE DO CÓDIGO")
    print("="*50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("manage.py"):
        print("❌ Erro: Arquivo manage.py não encontrado!")
        print("Execute este script no diretório raiz do projeto Django.")
        sys.exit(1)
    
    # Verificar se checkpoint existe
    if not os.path.exists("CHECKPOINT_QUALIDADE_CODIGO.md"):
        print("❌ Erro: Arquivo CHECKPOINT_QUALIDADE_CODIGO.md não encontrado!")
        print("Execute a tarefa de melhoria primeiro.")
        sys.exit(1)
    
    # Gerar relatório inicial
    stats_result, django_ok = generate_report()
    
    if args.report_only:
        print("\n✅ Relatório gerado com sucesso!")
        return
    
    if not django_ok:
        print("\n❌ Django não está funcionando! Resolva os erros primeiro.")
        sys.exit(1)
    
    # Aplicar correções se solicitado
    if args.auto:
        print("\n🔧 Aplicando correções automáticas...")
        
        # Correções seguras
        fix_result = apply_automatic_fixes()
        
        # Correções não seguras se solicitado
        if args.unsafe:
            print("\n⚠️  Aplicando correções não seguras...")
            unsafe_result = apply_unsafe_fixes()
        
        # Verificar Django novamente
        print("\n🔍 Verificando Django após correções...")
        django_ok_after = check_django()
        
        if not django_ok_after:
            print("❌ Django quebrou após correções! Reversão recomendada.")
            sys.exit(1)
        
        # Relatório final
        print("\n📊 RELATÓRIO FINAL")
        print("="*30)
        final_stats, _ = generate_report()
        
        print("\n✅ Correções aplicadas com sucesso!")
        print("💡 Próximos passos:")
        print("   1. Revisar arquivos modificados")
        print("   2. Executar testes")
        print("   3. Continuar com correções manuais se necessário")
    
    else:
        print("\n💡 Use --auto para aplicar correções automáticas")
        print("💡 Use --report-only para apenas gerar relatório")
        print("💡 Use --unsafe para aplicar correções não seguras")

if __name__ == "__main__":
    main()
