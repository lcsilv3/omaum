"""Comando para corrigir inconsistências no módulo de presenças."""

from django.core.management.base import BaseCommand
from django.db import transaction
from presencas.models import Presenca, PresencaAcademica
import logging


class Command(BaseCommand):
    """Comando para corrigir presenças com dados inconsistentes."""
    
    help = 'Corrige presenças com dados inconsistentes (turmas, atividades, etc.)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem salvar alterações, apenas mostra o que seria feito',
        )

    def handle(self, *args, **options):
        """Executa a correção."""
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write('🔍 Modo DRY-RUN: Nenhuma alteração será salva')
        
        self.stdout.write('🔍 Verificando presenças que precisam de correção...')
        
        with transaction.atomic():
            # 1. Corrigir presenças sem turma quando há atividade
            self.stdout.write('\n📋 Verificando presenças sem turma...')
            presencas_sem_turma = Presenca.objects.filter(
                turma__isnull=True, 
                atividade__isnull=False
            ).select_related('atividade')
            
            corrigidas_turma = 0
            for presenca in presencas_sem_turma:
                if hasattr(presenca.atividade, 'turmas') and presenca.atividade.turmas.exists():
                    primeira_turma = presenca.atividade.turmas.first()
                    
                    self.stdout.write(
                        f"  → Presença ID {presenca.id} receberá turma: {primeira_turma.nome}"
                    )
                    
                    if not dry_run:
                        presenca.turma = primeira_turma
                        presenca.save()
                    
                    corrigidas_turma += 1
            
            # 2. Corrigir presenças acadêmicas inconsistentes
            self.stdout.write('\n📋 Verificando presenças acadêmicas...')
            presencas_academicas = PresencaAcademica.objects.select_related(
                'aluno', 'atividade', 'turma'
            ).all()
            
            corrigidas_academicas = 0
            for presenca in presencas_academicas:
                mudancas = []
                
                # Se tem atividade mas não tem turma
                if presenca.atividade and not presenca.turma:
                    if hasattr(presenca.atividade, 'turmas') and presenca.atividade.turmas.exists():
                        nova_turma = presenca.atividade.turmas.first()
                        mudancas.append(f"turma: {nova_turma.nome}")
                        
                        if not dry_run:
                            presenca.turma = nova_turma
                
                if mudancas:
                    self.stdout.write(
                        f"  → PresencaAcademica ID {presenca.id}: {', '.join(mudancas)}"
                    )
                    
                    if not dry_run:
                        presenca.save()
                    
                    corrigidas_academicas += 1
            
            if dry_run:
                # Rollback no dry-run
                transaction.set_rollback(True)
        
        # Estatísticas finais
        total_presencas = Presenca.objects.count()
        total_academicas = PresencaAcademica.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ {'Simulação concluída' if dry_run else 'Correção concluída'}!")
        )
        self.stdout.write(f"📊 Estatísticas:")
        self.stdout.write(f"   • Total de presenças: {total_presencas}")
        self.stdout.write(f"   • Total de presenças acadêmicas: {total_academicas}")
        self.stdout.write(f"   • Presenças corrigidas (turmas): {corrigidas_turma}")
        self.stdout.write(f"   • Presenças acadêmicas corrigidas: {corrigidas_academicas}")
        
        if dry_run:
            self.stdout.write("\n💡 Execute sem --dry-run para aplicar as correções")
