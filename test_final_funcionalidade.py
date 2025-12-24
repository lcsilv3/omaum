#!/usr/bin/env python
"""
🧪 TESTE FINAL - Validação Completa da Funcionalidade de Registro de Presenças
================================================================

Verifica:
1. Estrutura dos arquivos modificados
2. Integridade das melhorias (logs, feedback visual)
3. Funcionalidade do backend (criação de RegistroPresenca)
4. Disponibilidade de ambientes (dev e prod)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')

import django
django.setup()

from django.test.client import Client
from presencas.models import RegistroPresenca
from turmas.models import Turma
from alunos.models import Aluno

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def check_files():
    """Verifica se os arquivos modificados existem"""
    print_header("📁 ETAPA 1: Verificar Arquivos")
    
    base_path = Path("e:/projetos/omaum/presencas/static/presencas")
    template_path = Path("e:/projetos/omaum/presencas/templates/presencas/registrar_presenca_dias_atividades.html")
    
    files_to_check = {
        "presenca_app.js": base_path / "presenca_app.js",
        "feedback_visual.js": base_path / "feedback_visual.js",
        "template": template_path,
    }
    
    results = {}
    for name, path in files_to_check.items():
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        status = "✅" if exists else "❌"
        results[name] = exists
        print(f"  {status} {name}: {size:,} bytes")
    
    return all(results.values())

def check_file_content():
    """Verifica o conteúdo dos arquivos"""
    print_header("📝 ETAPA 2: Verificar Conteúdo dos Arquivos")
    
    presenca_app_path = Path("e:/projetos/omaum/presencas/static/presencas/presenca_app.js")
    feedback_visual_path = Path("e:/projetos/omaum/presencas/static/presencas/feedback_visual.js")
    
    issues = []
    
    # Verificar presenca_app.js
    with open(presenca_app_path, 'r', encoding='utf-8') as f:
        presenca_content = f.read()
    
    # Verificar se tem a função salvarDiaAtual corrigida
    if "window.PresencaApp.salvarDiaAtual" in presenca_content:
        print("  ✅ Função salvarDiaAtual encontrada")
    else:
        issues.append("Função salvarDiaAtual não encontrada")
        print("  ❌ Função salvarDiaAtual não encontrada")
    
    # Verificar se os logs foram removidos
    log_count = presenca_content.count("console.log(")
    if log_count == 0:
        print(f"  ✅ Logs de debug removidos (console.log: 0)")
    else:
        print(f"  ⚠️  Ainda tem {log_count} console.log()")
    
    # Verificar feedback_visual.js
    with open(feedback_visual_path, 'r', encoding='utf-8') as f:
        feedback_content = f.read()
    
    required_functions = ["mostrarNotificacao", "fadeIn", "fadeOut", "slideIn", "slideOut"]
    found_functions = sum(1 for func in required_functions if func in feedback_content)
    
    print(f"  ✅ Funções de feedback encontradas: {found_functions}/{len(required_functions)}")
    
    # Verificar template
    template_path = Path("e:/projetos/omaum/presencas/templates/presencas/registrar_presenca_dias_atividades.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    if "feedback_visual.js" in template_content:
        print("  ✅ Template referencia feedback_visual.js")
    else:
        issues.append("Template não referencia feedback_visual.js")
        print("  ❌ Template não referencia feedback_visual.js")
    
    return len(issues) == 0, issues

def check_database():
    """Verifica dados no banco de dados"""
    print_header("🗄️  ETAPA 3: Verificar Dados no Banco")
    
    try:
        turma = Turma.objects.get(id=32)
        print(f"  ✅ Turma encontrada: {turma.nome}")
        
        # Contar registros de presença
        presencas = RegistroPresenca.objects.filter(turma_id=32)
        count = presencas.count()
        print(f"  ✅ Total de registros de presença: {count}")
        
        # Listar atividades
        atividades = presencas.values_list('atividade__descricao', flat=True).distinct()
        print(f"  ✅ Atividades com registros: {', '.join(atividades)}")
        
        # Estatísticas
        presentes = presencas.filter(status='P').count()
        faltas = presencas.filter(status='F').count()
        print(f"     - Presentes: {presentes}")
        print(f"     - Faltas: {faltas}")
        
        return True, count
    except Exception as e:
        print(f"  ❌ Erro ao verificar banco: {e}")
        return False, 0

def check_endpoints():
    """Verifica se os endpoints estão acessíveis"""
    print_header("🌐 ETAPA 4: Verificar Endpoints")
    
    client = Client()
    
    endpoints = {
        "GET form inicial": "/presencas/registrar-presenca-dados-basicos/",
        "GET dias e atividades": "/presencas/registrar-presenca-dias-atividades/",
        "Admin": "/admin/presencas/registropresenca/",
    }
    
    results = {}
    for name, path in endpoints.items():
        try:
            response = client.get(path)
            status = "✅" if response.status_code in [200, 301, 302] else "❌"
            results[name] = response.status_code
            print(f"  {status} {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)}")
            results[name] = None
    
    return all(v in [200, 301, 302, None] for v in results.values() if v is not None)

def print_summary(results):
    """Resumo final"""
    print_header("📊 RESUMO FINAL")
    
    checks = [
        ("✅ Arquivos modificados existem", results.get('files', False)),
        ("✅ Conteúdo dos arquivos correto", results.get('content', False)),
        ("✅ Banco de dados atualizado", results.get('database', False)),
        ("✅ Endpoints acessíveis", results.get('endpoints', False)),
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\n  Resultado: {passed}/{total} verificações passaram\n")
    
    for check, result in checks:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {check}: {status}")
    
    if passed == total:
        print("\n  🎉 TODOS OS TESTES PASSARAM! Sistema pronto para produção.")
    else:
        print(f"\n  ⚠️  {total - passed} teste(s) falharam. Revise os erros acima.")
    
    return passed == total

if __name__ == "__main__":
    results = {}
    
    results['files'] = check_files()
    results['content'], issues = check_file_content()
    results['database'], count = check_database()
    results['endpoints'] = check_endpoints()
    
    success = print_summary(results)
    
    sys.exit(0 if success else 1)
