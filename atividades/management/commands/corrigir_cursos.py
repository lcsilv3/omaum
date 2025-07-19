"""Comando para corrigir atividades sem curso."""

from django.core.management.base import BaseCommand
from atividades.models import Atividade


class Command(BaseCommand):
    """Comando para corrigir atividades que têm turmas mas não têm curso."""
    
    help = 'Corrige atividades que têm turmas mas não têm curso definido'

    def handle(self, *args, **options):
        """Executa a correção."""
        self.stdout.write('Verificando atividades que precisam de correção...')
        
        # Buscar atividades sem curso mas com turmas
        atividades_sem_curso = Atividade.objects.filter(
            curso__isnull=True
        ).prefetch_related('turmas__curso')
        
        corrigidas = 0
        for atividade in atividades_sem_curso:
            if atividade.turmas.exists():
                # Pegar o curso da primeira turma
                primeira_turma = atividade.turmas.first()
                if primeira_turma and primeira_turma.curso:
                    atividade.curso = primeira_turma.curso
                    atividade.save()
                    corrigidas += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Atividade '{atividade.nome}' corrigida - "
                            f"curso: {primeira_turma.curso.nome}"
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f"{corrigidas} atividades foram corrigidas.")
        )
        
        # Verificar se ainda há inconsistências
        inconsistencias = 0
        for atividade in Atividade.objects.all().prefetch_related('turmas__curso'):
            if atividade.turmas.exists():
                cursos_das_turmas = set(
                    turma.curso_id for turma in atividade.turmas.all() 
                    if turma.curso
                )
                if atividade.curso and len(cursos_das_turmas) > 0:
                    if atividade.curso.id not in cursos_das_turmas:
                        self.stdout.write(
                            self.style.WARNING(
                                f"⚠️  Inconsistência: Atividade '{atividade.nome}' - "
                                f"curso: {atividade.curso.nome}, "
                                f"turmas de cursos diferentes"
                            )
                        )
                        inconsistencias += 1
        
        if inconsistencias == 0:
            self.stdout.write(
                self.style.SUCCESS("✓ Nenhuma inconsistência encontrada!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"⚠️  {inconsistencias} inconsistências encontradas.")
            )
