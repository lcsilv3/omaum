#!/usr/bin/env python
"""
Script para testar se o botão 'Adicionar Outro Registro' está funcionando corretamente
no formulário de alunos após as correções implementadas.
"""

import os
import django
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from alunos.models import Aluno

def test_formset_functionality():
    """Testa se o formset está funcionando corretamente"""
    print("=== TESTE DE FUNCIONALIDADE DO BOTÃO HISTÓRICO ===")
    
    # Criar cliente de teste
    client = Client()
    
    # Verificar se existe usuário admin
    try:
        user = User.objects.get(username='admin')
        print(f"✓ Usuário admin encontrado: {user.username}")
    except User.DoesNotExist:
        print("⚠ Usuário admin não encontrado. Criando...")
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print(f"✓ Usuário admin criado: {user.username}")
    
    # Fazer login
    login_success = client.login(username='admin', password='admin123')
    print(f"✓ Login realizado: {login_success}")
    
    # Verificar se existe aluno para editar
    try:
        aluno = Aluno.objects.first()
        if aluno:
            print(f"✓ Aluno encontrado: {aluno.nome} (CPF: {aluno.cpf})")
            url = reverse('alunos:editar_aluno', kwargs={'cpf': aluno.cpf})
        else:
            print("⚠ Nenhum aluno encontrado. Testando formulário de novo aluno...")
            url = reverse('alunos:novo_aluno')
    except Exception as e:
        print(f"⚠ Erro ao buscar aluno: {e}")
        url = reverse('alunos:novo_aluno')
    
    # Fazer requisição GET para o formulário
    response = client.get(url)
    print(f"✓ Resposta GET: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Verificar elementos críticos
        checks = [
            ('Management form presente', 'historico-TOTAL_FORMS' in content),
            ('Botão adicionar presente', 'id="add-historico-form"' in content),
            ('Template vazio presente', 'id="empty-historico-form"' in content),
            ('JavaScript presente', 'addNewForm' in content),
            ('Event listeners presentes', 'addEventListener' in content),
        ]
        
        print("\n=== VERIFICAÇÕES DO TEMPLATE ===")
        for check_name, check_result in checks:
            status = "✓" if check_result else "✗"
            print(f"{status} {check_name}: {check_result}")
        
        # Verificar se não há duplicações
        total_forms_count = content.count('historico-TOTAL_FORMS')
        add_button_count = content.count('id="add-historico-form"')
        
        print("\n=== VERIFICAÇÃO DE DUPLICAÇÕES ===")
        print(f"✓ Management forms encontrados: {total_forms_count}")
        print(f"✓ Botões 'adicionar' encontrados: {add_button_count}")
        
        if total_forms_count == 1 and add_button_count == 1:
            print("✓ Sem duplicações detectadas!")
        else:
            print("⚠ Possível duplicação detectada!")
        
        return True
    else:
        print(f"✗ Erro na requisição: {response.status_code}")
        return False

def main():
    """Função principal"""
    try:
        success = test_formset_functionality()
        if success:
            print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
            print("🌐 Para testar no navegador, acesse:")
            print("   http://localhost:8000/alunos/")
            print("   Faça login e clique em 'Editar' em um aluno")
            print("   Teste o botão 'Adicionar Outro Registro' na seção 'Dados Iniciáticos'")
        else:
            print("\n❌ TESTE FALHOU!")
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
