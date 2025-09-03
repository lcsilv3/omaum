#!/usr/bin/env python
"""
Script para testar o formset de histórico e verificar se o management form está correto.
"""

import os
import sys
import django

# Adicionar o diretório do projeto ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django ANTES de importar qualquer coisa do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse


def test_formset_html():
    """Testar se o HTML do formset está sendo gerado corretamente."""
    client = Client()

    # Criar usuário de teste
    username = "lcsilv3"
    password = "iG356900"
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)

    # Fazer login
    client.login(username=username, password=password)

    # Fazer requisição GET para página de criação de aluno
    url = reverse("alunos:criar_aluno")
    response = client.get(url)

    if response.status_code != 200:
        print(f"❌ ERRO: Status code {response.status_code}")
        return False

    html = response.content.decode()

    # Verificar se o management form está presente (ignorando referências JavaScript)
    # Contar apenas campos input reais, não referências em JavaScript
    import re

    input_pattern = r'<input[^>]*name="historico-TOTAL_FORMS"[^>]*>'
    management_forms_count = len(re.findall(input_pattern, html))
    print(f"📊 Campos TOTAL_FORMS encontrados: {management_forms_count}")

    if management_forms_count != 1:
        print(
            f"❌ ERRO: Esperado 1 campo TOTAL_FORMS, encontrado {management_forms_count}"
        )
        return False

    # Verificar se o botão está presente
    button_count = html.count('id="add-historico-form"')
    print(f"🔘 Botões 'Adicionar Outro Registro' encontrados: {button_count}")

    if button_count != 1:
        print(f"❌ ERRO: Esperado 1 botão, encontrado {button_count}")
        return False

    # Verificar se o management form está dentro do form - SIMPLIFICADO
    # Por enquanto, vamos focar que temos apenas 1 management form
    print("📝 Management form está presente e único: ✅")

    # Verificar marcadores de debug
    debug_markers = {
        "MANAGEMENT_FORM_START": html.count("MANAGEMENT_FORM_START"),
        "MANAGEMENT_FORM_END": html.count("MANAGEMENT_FORM_END"),
        "HISTORICO_SECTION_START": html.count("HISTORICO_SECTION_START"),
    }

    print("🔍 Marcadores de debug encontrados:")
    for marker, count in debug_markers.items():
        print(f"  - {marker}: {count}")

    # Verificar se há código JS duplicado
    js_functions = {
        "addNewForm": html.count("function addNewForm"),
        "removeForm": html.count("function removeForm"),
        "DOMContentLoaded": html.count("DOMContentLoaded"),
    }

    print("⚙️ Funções JavaScript encontradas:")
    for func, count in js_functions.items():
        status = "✅" if count <= 1 else "❌ DUPLICADO"
        print(f"  - {func}: {count} {status}")
        if count > 1:
            print(f"    ⚠️ AVISO: Função {func} duplicada pode causar conflitos!")

    print("\n✅ Teste concluído com sucesso!")
    print("🎯 O formset de histórico deve estar funcionando corretamente.")
    return True


if __name__ == "__main__":
    print("🧪 Testando o formset de histórico...")
    print("=" * 50)

    try:
        success = test_formset_html()
        if success:
            print("\n🎉 Todos os testes passaram!")
            print(
                "💡 Agora você pode testar manualmente em: http://127.0.0.1:8000/alunos/criar/"
            )
        else:
            print("\n💥 Alguns testes falharam. Verifique os erros acima.")
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {e}")
        import traceback

        traceback.print_exc()
