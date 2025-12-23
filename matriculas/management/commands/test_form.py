#!/usr/bin/env python
"""Management command para testar o MatriculaForm"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Testa o MatriculaForm e seu queryset'

    def handle(self, *args, **options):
        from matriculas.forms import MatriculaForm
        from alunos.models import Aluno
        
        self.stdout.write("=" * 80)
        self.stdout.write("TESTE: MatriculaForm")
        self.stdout.write("=" * 80)
        
        # Criar formulário
        self.stdout.write("\n1️⃣ CRIANDO FORMULÁRIO:")
        form = MatriculaForm()
        
        # Verificar campo aluno
        self.stdout.write("\n2️⃣ CAMPO ALUNO:")
        aluno_field = form.fields['aluno']
        queryset = aluno_field.queryset
        
        self.stdout.write(f"✓ Queryset count: {queryset.count()}")
        self.stdout.write(f"✓ Widget: {type(aluno_field.widget).__name__}")
        self.stdout.write(f"✓ Widget attrs: {aluno_field.widget.attrs}")
        
        # Verificar se todos os alunos ativos estão no queryset
        alunos_total = Aluno.objects.filter(situacao='a').count()
        self.stdout.write(f"\n✓ Alunos com situacao='a': {alunos_total}")
        self.stdout.write(f"✓ Alunos no queryset: {queryset.count()}")
        
        if queryset.count() == alunos_total:
            self.stdout.write(self.style.SUCCESS(
                "✅ Queryset contém todos os alunos ativos"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ PROBLEMA: Queryset deveria ter {alunos_total} alunos, mas tem {queryset.count()}"
            ))
        
        # Listar primeiros 5 alunos
        self.stdout.write("\n3️⃣ PRIMEIROS 5 ALUNOS DO QUERYSET:")
        for i, aluno in enumerate(queryset[:5]):
            self.stdout.write(f"   {i+1}. {aluno.nome} (CPF: {aluno.cpf})")
        
        # Renderizar campo como HTML
        self.stdout.write("\n4️⃣ RENDERIZAÇÃO HTML:")
        html = str(aluno_field.widget.render('aluno', None, aluno_field.widget.attrs))
        
        # Contar opções no HTML
        import re
        options = re.findall(r'<option', html)
        self.stdout.write(f"✓ Opções no HTML renderizado: {len(options)}")
        
        if len(options) == queryset.count():
            self.stdout.write(self.style.SUCCESS(
                "✅ HTML contém todas as opções do queryset"
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f"⚠️  HTML tem {len(options)} opções, queryset tem {queryset.count()}"
            ))
        
        self.stdout.write("\n" + "=" * 80)
