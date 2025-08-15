#!/usr/bin/env python
"""
Django management command para testar o formulário
"""

from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from alunos.models import Aluno


class Command(BaseCommand):
    help = "Testa o formulário de histórico de alunos"

    def handle(self, *args, **options):
        self.stdout.write("=== TESTE DO FORMULÁRIO DE HISTÓRICO ===")

        # Criar cliente
        client = Client()

        # Verificar/criar usuário admin
        try:
            user = User.objects.get(username="admin")
            self.stdout.write(f"Usuário encontrado: {user.username}")
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                "admin", "admin@example.com", "admin123"
            )
            self.stdout.write(f"Usuário criado: {user.username}")

        # Login
        client.login(username="admin", password="admin123")

        # Buscar aluno ou usar formulário novo
        aluno = Aluno.objects.first()
        if aluno:
            url = reverse("alunos:editar_aluno", kwargs={"cpf": aluno.cpf})
            self.stdout.write(f"Testando edição do aluno: {aluno.nome}")
        else:
            url = reverse("alunos:novo_aluno")
            self.stdout.write("Testando formulário de novo aluno")

        # Fazer requisição
        response = client.get(url)

        if response.status_code == 200:
            content = response.content.decode("utf-8")

            # Verificações básicas
            checks = {
                "Management form": "historico-TOTAL_FORMS" in content,
                "Botão adicionar": "add-historico-form" in content,
                "Template vazio": "empty-historico-form" in content,
                "JavaScript addNewForm": "addNewForm" in content,
                "Event listeners": "addEventListener" in content,
            }

            self.stdout.write("\nVerificações:")
            all_good = True
            for name, result in checks.items():
                status = "✓" if result else "✗"
                self.stdout.write(f"  {status} {name}: {result}")
                if not result:
                    all_good = False

            # Verificar duplicações
            total_forms_count = content.count("historico-TOTAL_FORMS")
            add_button_count = content.count("add-historico-form")

            self.stdout.write("\nContadores:")
            self.stdout.write(f"  Management forms: {total_forms_count}")
            self.stdout.write(f"  Botões adicionar: {add_button_count}")

            if all_good and total_forms_count == 1 and add_button_count == 1:
                self.stdout.write(
                    self.style.SUCCESS(
                        "\n🎉 SUCESSO! Formulário está funcionando corretamente."
                    )
                )
                self.stdout.write("🌐 Para testar no navegador:")
                self.stdout.write("   1. Execute: python manage.py runserver")
                self.stdout.write("   2. Acesse: http://localhost:8000/alunos/")
                self.stdout.write("   3. Faça login e edite um aluno")
                self.stdout.write("   4. Teste o botão 'Adicionar Outro Registro'")
            else:
                self.stdout.write(
                    self.style.ERROR("\n❌ ERRO! Problemas encontrados no formulário.")
                )
        else:
            self.stdout.write(self.style.ERROR(f"Erro HTTP: {response.status_code}"))
