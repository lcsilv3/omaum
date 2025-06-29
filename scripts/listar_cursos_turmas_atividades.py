from cursos.models import Curso
from turmas.models import Turma
from atividades.models import AtividadeAcademica

print("Iniciando listagem de cursos, turmas e atividades...\n")

try:
    cursos = Curso.objects.all()
    if not cursos.exists():
        print("Nenhum curso encontrado.")
    for curso in cursos:
        print(f'Curso: {curso.nome} (ID: {curso.id})')
        turmas = Turma.objects.filter(curso=curso)
        if not turmas.exists():
            print('  Nenhuma turma para este curso.')
        else:
            for turma in turmas:
                print(f'  Turma: {turma.nome} (ID: {turma.id})')
                try:
                    atividades = AtividadeAcademica.objects.filter(turmas=turma)
                    if atividades.exists():
                        for atividade in atividades:
                            print(f'    Atividade: {atividade.nome} (ID: {atividade.id})')
                    else:
                        print('    Nenhuma atividade para esta turma.')
                except Exception as e:
                    print(f'    Erro ao buscar atividades para a turma {turma.nome}: {e}')
except Exception as e:
    print(f'Erro geral ao buscar cursos/turmas/atividades: {e}')
