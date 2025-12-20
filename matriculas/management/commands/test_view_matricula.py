"""
Management command para testar renderização da view real.
"""

from django.core.management.base import BaseCommand
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from matriculas.views_tradicionais import criar_matricula


class Command(BaseCommand):
    help = "Testa renderização da view criar_matricula"

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Criar user fake
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("Nenhum usuário encontrado"))
            return
        
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("TESTE DA VIEW criar_matricula"))
        self.stdout.write("=" * 80)

        # Criar request fake
        factory = RequestFactory()
        request = factory.get('/matriculas/realizar/?turma=32')
        request.user = user
        
        # Chamar view
        response = criar_matricula(request)
        
        self.stdout.write(f"\nStatus Code: {response.status_code}")
        
        # Pegar conteúdo HTML
        html = response.content.decode('utf-8')
        
        # Contar select com id_aluno
        if 'id="id_aluno"' in html:
            self.stdout.write(self.style.SUCCESS("✓ Campo id_aluno encontrado no HTML"))
        else:
            self.stdout.write(self.style.ERROR("✗ Campo id_aluno NÃO encontrado"))
        
        # Verificar classe select2-enable
        if 'select2-enable' in html:
            self.stdout.write(self.style.SUCCESS("✓ Classe select2-enable encontrada"))
        else:
            self.stdout.write(self.style.ERROR("✗ Classe select2-enable NÃO encontrada"))
        
        # Contar options
        option_count = html.count('<option value=')
        self.stdout.write(f"\n✓ Total de <option value=> no HTML: {option_count}")
        
        # Procurar por options de alunos específicos
        if 'Alice Fernandes' in html:
            self.stdout.write(self.style.SUCCESS("✓ Aluno 'Alice Fernandes' encontrado no HTML"))
        else:
            self.stdout.write(self.style.ERROR("✗ Aluno 'Alice Fernandes' NÃO encontrado"))
        
        # Extrair trecho do select de aluno
        start_idx = html.find('id="id_aluno"')
        if start_idx > 0:
            # Voltar para pegar a tag <select>
            select_start = html.rfind('<select', max(0, start_idx - 500), start_idx)
            # Avançar para pegar o </select>
            select_end = html.find('</select>', start_idx) + 9
            
            select_html = html[select_start:select_end]
            
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write("TRECHO DO SELECT DE ALUNO:")
            self.stdout.write("=" * 80)
            
            # Mostrar primeiras 1000 caracteres
            self.stdout.write(select_html[:1500])
            self.stdout.write("\n[... continuação truncada ...]")
        
        # Verificar se jQuery está carregado
        if 'jquery' in html.lower():
            self.stdout.write(self.style.SUCCESS("\n✓ jQuery encontrado no HTML"))
        else:
            self.stdout.write(self.style.WARNING("\n⚠ jQuery NÃO encontrado"))
        
        # Verificar se select2 está carregado
        if 'select2' in html.lower():
            self.stdout.write(self.style.SUCCESS("✓ Select2 encontrado no HTML"))
        else:
            self.stdout.write(self.style.WARNING("⚠ Select2 NÃO encontrado"))
        
        # Verificar se formulario_matricula.js está carregado
        if 'formulario_matricula.js' in html:
            self.stdout.write(self.style.SUCCESS("✓ formulario_matricula.js encontrado"))
        else:
            self.stdout.write(self.style.ERROR("✗ formulario_matricula.js NÃO encontrado"))
        
        self.stdout.write("\n" + "=" * 80)
