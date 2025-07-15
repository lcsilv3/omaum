#!/usr/bin/env python
"""
Script simplificado para testar o formulário de alunos
"""

import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from alunos.models import Aluno

def test_formset():
    print("=== TESTE DO FORMULÁRIO DE HISTÓRICO ===")
    
    # Criar cliente
    client = Client()
    
    # Verificar/criar usuário admin
    try:
        User.objects.get(username='admin')
    except User.DoesNotExist:
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    
    # Login
    client.login(username='admin', password='admin123')
    
    # Buscar aluno ou usar formulário novo
    aluno = Aluno.objects.first()
    if aluno:
        url = reverse('alunos:editar_aluno', kwargs={'cpf': aluno.cpf})
        print(f"Testando edição do aluno: {aluno.nome}")
    else:
        url = reverse('alunos:novo_aluno')
        print("Testando formulário de novo aluno")
    
    # Fazer requisição
    response = client.get(url)
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Verificações básicas
        checks = {
            'Management form': 'historico-TOTAL_FORMS' in content,
            'Botão adicionar': 'add-historico-form' in content,
            'Template vazio': 'empty-historico-form' in content,
            'JavaScript': 'addNewForm' in content
        }
        
        print("\nVerificações:")
        all_good = True
        for name, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {name}: {result}")
            if not result:
                all_good = False
        
        if all_good:
            print("\n🎉 SUCESSO! Todos os elementos estão presentes.")
            print("🌐 Para testar no navegador:")
            print("   1. Execute: python manage.py runserver")
            print("   2. Acesse: http://localhost:8000/alunos/")
            print("   3. Faça login (admin/admin123)")
            print("   4. Edite um aluno e teste o botão 'Adicionar Outro Registro'")
        else:
            print("\n❌ ERRO! Alguns elementos estão faltando.")
        
        return all_good
    else:
        print(f"Erro HTTP: {response.status_code}")
        return False

if __name__ == '__main__':
    test_formset()
