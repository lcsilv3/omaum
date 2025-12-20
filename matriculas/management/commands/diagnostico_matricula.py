"""
Management command para diagnosticar problemas no formulário de matrícula.
"""

from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from matriculas.forms import MatriculaForm


class Command(BaseCommand):
    help = "Diagnostica problemas no formulário de matrícula"

    def handle(self, *args, **options):
        User = get_user_model()
        
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("DIAGNÓSTICO DO FORMULÁRIO DE MATRÍCULA"))
        self.stdout.write("=" * 80)

        # Criar formulário
        form = MatriculaForm()
        
        # Verificar campo turma
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("CAMPO TURMA:")
        self.stdout.write("=" * 80)
        turma_queryset = form.fields['turma'].queryset
        self.stdout.write(f"✓ Total de turmas no queryset: {turma_queryset.count()}")
        
        if turma_queryset.exists():
            self.stdout.write("\nPrimeiras 5 turmas:")
            for turma in turma_queryset[:5]:
                self.stdout.write(f"  - ID {turma.id}: {turma.nome}")
        
        # Verificar campo aluno
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("CAMPO ALUNO:")
        self.stdout.write("=" * 80)
        aluno_queryset = form.fields['aluno'].queryset
        self.stdout.write(f"✓ Total de alunos no queryset: {aluno_queryset.count()}")
        
        if aluno_queryset.exists():
            self.stdout.write("\nPrimeiros 10 alunos:")
            for aluno in aluno_queryset[:10]:
                self.stdout.write(f"  - ID {aluno.id}: {aluno.nome} (situação={aluno.situacao})")
        else:
            self.stdout.write(self.style.ERROR("\n⚠ PROBLEMA: Nenhum aluno no queryset!"))
        
        # Verificar widgets
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("WIDGETS:")
        self.stdout.write("=" * 80)
        self.stdout.write(f"Widget Turma: {form.fields['turma'].widget.__class__.__name__}")
        self.stdout.write(f"  - Atributos: {form.fields['turma'].widget.attrs}")
        self.stdout.write(f"\nWidget Aluno: {form.fields['aluno'].widget.__class__.__name__}")
        self.stdout.write(f"  - Atributos: {form.fields['aluno'].widget.attrs}")
        
        # Renderizar campo aluno e verificar HTML
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("HTML RENDERIZADO DO CAMPO ALUNO:")
        self.stdout.write("=" * 80)
        aluno_html = str(form['aluno'])
        
        # Contar options
        option_count = aluno_html.count('<option')
        self.stdout.write(f"✓ Total de <option> tags no HTML: {option_count}")
        
        if option_count == 0:
            self.stdout.write(self.style.ERROR("⚠ PROBLEMA: Nenhum <option> no HTML!"))
        else:
            # Mostrar primeiras 500 caracteres do HTML
            self.stdout.write(f"\nPrimeiros 500 caracteres do HTML:")
            self.stdout.write("-" * 80)
            self.stdout.write(aluno_html[:500])
            self.stdout.write("-" * 80)
        
        # Verificar se select2-enable está presente
        if 'select2-enable' in aluno_html:
            self.stdout.write(self.style.SUCCESS("\n✓ Classe 'select2-enable' encontrada no HTML"))
        else:
            self.stdout.write(self.style.WARNING("\n⚠ Classe 'select2-enable' NÃO encontrada no HTML"))
        
        # Verificar ID do campo
        if 'id_aluno' in aluno_html:
            self.stdout.write(self.style.SUCCESS("✓ ID 'id_aluno' encontrado no HTML"))
        else:
            self.stdout.write(self.style.ERROR("⚠ ID 'id_aluno' NÃO encontrado no HTML"))
        
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("DIAGNÓSTICO CONCLUÍDO"))
        self.stdout.write("=" * 80)
