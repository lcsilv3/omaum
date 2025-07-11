from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Atividade
from cursos.models import Curso
from turmas.models import Turma
from django.db.models import Q

def api_filtrar_atividades(request):
    q = request.GET.get('q', '').strip()
    curso_id = request.GET.get('curso', '')
    turma_id = request.GET.get('turma', '')

    atividades = Atividade.objects.all()
    if q:
        atividades = atividades.filter(Q(nome__icontains=q) | Q(descricao__icontains=q))
    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    atividades = atividades.distinct()

    # Cursos disponíveis para as atividades filtradas
    cursos = Curso.objects.filter(atividades__in=atividades).distinct()
    
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
        'atividades/academicas/partials/atividades_tabela_body.html',
        {'atividades': atividades}
    )

    cursos_json = [{'id': c.codigo_curso, 'nome': c.nome} for c in cursos]
    turmas_json = [{'id': t.id, 'nome': t.nome} for t in turmas]

    return JsonResponse({
        'atividades_html': atividades_html,
        'cursos': cursos_json,
        'turmas': turmas_json,
    })
