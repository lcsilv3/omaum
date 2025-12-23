#!/usr/bin/env python
"""Management command para debug do Select2"""
from django.core.management.base import BaseCommand
import re
from django.test import Client


class Command(BaseCommand):
    help = 'Debug do formulário de matrícula e Select2'

    def handle(self, *args, **options):
        from alunos.models import Aluno
        from turmas.models import Turma
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        self.stdout.write("=" * 80)
        self.stdout.write("DEBUG: Formulário de Matrícula e Select2")
        self.stdout.write("=" * 80)
        
        # Verificação do banco
        self.stdout.write("\n1️⃣ BANCO DE DADOS:")
        alunos_ativos = Aluno.objects.filter(situacao='a').count()
        turmas_ativas = Turma.objects.filter(ativo=True).count()
        self.stdout.write(f"✓ Alunos ativos: {alunos_ativos}")
        self.stdout.write(f"✓ Turmas ativas: {turmas_ativas}")
        
        # Criar/obter usuário de teste
        self.stdout.write("\n2️⃣ AUTENTICAÇÃO:")
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                self.stdout.write(self.style.ERROR("❌ Nenhum superusuário encontrado"))
                return
            self.stdout.write(f"✓ Usando usuário: {user.username}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro ao obter usuário: {e}"))
            return
        
        # Acesso à página com autenticação
        self.stdout.write("\n3️⃣ ACESSO À PÁGINA (AUTENTICADO):")
        client = Client(SERVER_NAME='localhost')
        
        # Fazer login
        client.force_login(user)
        self.stdout.write("✓ Login realizado")
        
        try:
            response = client.get('/matriculas/criar/', HTTP_HOST='localhost')
            self.stdout.write(f"✓ Status HTTP: {response.status_code}")
            
            if response.status_code == 302:
                location = response.get('Location', 'não informado')
                self.stdout.write(self.style.WARNING(
                    f"⚠️  Redirecionamento para: {location}"
                ))
                return
            elif response.status_code != 200:
                self.stdout.write(self.style.ERROR(
                    f"❌ Erro HTTP {response.status_code}"
                ))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Exceção: {str(e)}"))
            import traceback
            self.stdout.write(traceback.format_exc())
            return
        
        # Análise HTML
        self.stdout.write("\n4️⃣ ANÁLISE HTML:")
        html = response.content.decode('utf-8')
        
        # Procurar SELECT
        aluno_select = re.search(
            r'<select[^>]*id="id_aluno"[^>]*>.*?</select>',
            html,
            re.DOTALL
        )
        
        if aluno_select:
            self.stdout.write(self.style.SUCCESS("✓ SELECT encontrado"))
            
            # Contar opções
            options = re.findall(r'<option[^>]*>', aluno_select.group(0))
            self.stdout.write(f"✓ Total de opções: {len(options)}")
            
            if len(options) < alunos_ativos:
                self.stdout.write(self.style.ERROR(
                    f"❌ PROBLEMA: Esperado {alunos_ativos}, encontrado {len(options)}"
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"✅ OK: {len(options)} opções no SELECT"
                ))
                
            # Verificar Select2
            if 'select2-enable' in aluno_select.group(0):
                self.stdout.write("✓ Classe 'select2-enable' presente")
            else:
                self.stdout.write(self.style.WARNING(
                    "⚠️  Classe 'select2-enable' ausente"
                ))
        else:
            self.stdout.write(self.style.ERROR(
                "❌ CRÍTICO: SELECT não encontrado no HTML"
            ))
            
            # Listar todos os SELECTs
            selects = re.findall(r'<select[^>]*id="([^"]*)"', html)
            if selects:
                self.stdout.write(f"   SELECTs encontrados: {', '.join(selects)}")
        
        self.stdout.write("\n" + "=" * 80)
