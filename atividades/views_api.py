from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import AtividadeAcademica
from cursos.models import Curso
from turmas.models import Turma

def api_filtrar_atividades(request):
    q = request.GET.get('q', '').strip()
    curso_id = request.GET.get('curso', '')
    turma_id = request.GET.get('turma', '')

    atividades = AtividadeAcademica.objects.all()
    if q:
        atividades = atividades.filter(nome__icontains=q)
    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    atividades = atividades.distinct()

    # Cursos disponíveis para as atividades filtradas
    cursos = Curso.objects.filter(atividadeacademica__in=atividades).distinct()
    
    # Turmas disponíveis para as atividades filtradas
    if curso_id:
        turmas = Turma.objects.filter(curso_id=curso_id).distinct()
    elif turma_id:
        # Se só turma foi selecionada, mostre apenas essa turma
        turmas = Turma.objects.filter(id=turma_id)
        # Opcional: filtrar cursos para mostrar só o do turma selecionada
        cursos = Curso.objects.filter(id=turmas.first().curso_id) if turmas.exists() else Curso.objects.none()
    else:
        turmas = Turma.objects.all().distinct()

    atividades_html = render_to_string(
        'atividades/_tabela_atividades.html',
        {'atividades': atividades}
    )

    cursos_json = [{'id': c.id, 'nome': c.nome} for c in cursos]
    turmas_json = [{'id': t.id, 'nome': t.nome} for t in turmas]

    return JsonResponse({
        'atividades_html': atividades_html,
        'cursos': cursos_json,
        'turmas': turmas_json,
    })
