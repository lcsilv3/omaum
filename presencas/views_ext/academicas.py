# ...código existente...
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from alunos.models import Aluno
from presencas.models import Presenca

def listar_presencas_academicas(request):
    cursos = Curso.objects.all()
    turmas = Turma.objects.all()
    atividades = AtividadeAcademica.objects.all()
    alunos = Aluno.objects.all()

    # Filtros
    curso_id = request.GET.get('curso')
    turma_id = request.GET.get('turma')
    atividade_id = request.GET.get('atividade')
    aluno_id = request.GET.get('aluno')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    presencas = Presenca.objects.all()

    if curso_id:
        turmas = Turma.objects.filter(curso_id=curso_id)
        presencas = presencas.filter(turma__curso_id=curso_id)
    if turma_id:
        atividades = Atividade.objects.filter(turma_id=turma_id)
        presencas = presencas.filter(turma_id=turma_id)
    if atividade_id:
        presencas = presencas.filter(atividade_id=atividade_id)
    if aluno_id:
        presencas = presencas.filter(aluno_id=aluno_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    context = {
        'presencas': presencas,
        'cursos': cursos,
        'turmas': turmas,
        'atividades': atividades,
        'alunos': alunos,
    }
    return render(request, 'presencas/academicas/listar_presencas_academicas.html', context)
# ...código existente...