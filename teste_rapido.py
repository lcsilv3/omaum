#!/usr/bin/env python
"""Teste rápido do formset"""

print("🧪 Teste do Formset - Verificação Rápida")
print("=" * 50)

try:
    import os
    import django
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
    django.setup()
    
    from django.test import Client
    from django.contrib.auth.models import User
    from django.urls import reverse
    
    print("✅ Django configurado com sucesso")
    
    # Cliente de teste
    client = Client()
    
    # Criar/obter usuário
    username = 'lcsilv3'
    password = 'iG356900'
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'password': password}
    )
    if created:
        user.set_password(password)
        user.save()
    
    # Fazer login
    login_success = client.login(username=username, password=password)
    print(f"✅ Login: {'sucesso' if login_success else 'falha'}")
    
    # Testar página
    url = reverse('alunos:criar_aluno')
    response = client.get(url)
    
    print(f"✅ Status da página: {response.status_code}")
    
    if response.status_code == 200:
        html = response.content.decode()
        
        # Verificações básicas
        checks = {
            'TOTAL_FORMS': html.count('name="historico-TOTAL_FORMS"'),
            'Botão Add': html.count('id="add-historico-form"'),
            'Management Start': html.count('MANAGEMENT_FORM_START'),
            'Management End': html.count('MANAGEMENT_FORM_END'),
            'DOMContentLoaded': html.count('DOMContentLoaded'),
        }
        
        print("\n📊 Resultados das verificações:")
        for item, count in checks.items():
            status = "✅" if count == 1 else ("⚠️" if count > 1 else "❌")
            print(f"  {item}: {count} {status}")
        
        # Verificar se management form está dentro do form
        form_start = html.find('<form')
        form_end = html.find('</form>')
        mgmt_pos = html.find('name="historico-TOTAL_FORMS"')
        
        if all(pos != -1 for pos in [form_start, form_end, mgmt_pos]):
            within_form = form_start < mgmt_pos < form_end
            print(f"  Management no <form>: {'✅' if within_form else '❌'}")
        
        print("\n🎯 DIAGNÓSTICO:")
        if checks['TOTAL_FORMS'] == 1 and checks['Botão Add'] == 1:
            print("✅ Template está correto!")
            print("✅ O botão deve funcionar no navegador!")
        else:
            print("❌ Há problemas no template que precisam ser corrigidos")
            
    else:
        print(f"❌ Erro na página: {response.status_code}")
        
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()

print("\n🏁 Teste concluído!")
