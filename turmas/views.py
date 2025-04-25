import csv
import io
import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from django.utils import timezone
from importlib import import_module

from .models import Turma
from cursos.models import Curso
from alunos.models import Aluno
from matriculas.models import Matricula

def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


def get_turma_model():
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


@login_required
def listar_turmas(request):
    Turma = get_turma_model()
    turmas = Turma.objects.all()
    # Preparar informações adicionais para cada turma
    turmas_com_info = []
    for turma in turmas:
        # Verificar pendências na instrutoria
        tem_pendencia_instrutoria = (
            not turma.instrutor
            or not turma.instrutor_auxiliar
            or not turma.auxiliar_instrucao
        )
        # Calcular vagas disponíveis
        total_alunos = (
            turma.matriculas.filter(status="A").count()
            if hasattr(turma, "matriculas")
            else 0
        )
        vagas_disponiveis = turma.vagas - total_alunos

        turmas_com_info.append(
            {
                "turma": turma,
                "total_alunos": total_alunos,
                "vagas_disponiveis": vagas_disponiveis,
                "tem_pendencia_instrutoria": tem_pendencia_instrutoria,
            }
        )

    return render(
        request,
        "turmas/listar_turmas.html",
        {"turmas_com_info": turmas_com_info},
    )


@login_required
def criar_turma(request):
    """Cria uma nova turma."""
    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, "Turma criada com sucesso!")
            return redirect("turmas:detalhar_turma", id=turma.id)
    else:
        form = TurmaForm()
    
    # Obter todos os alunos ativos para o contexto
    try:
        Aluno = import_module("alunos.models").Aluno
        alunos = Aluno.objects.filter(situacao="ATIVO")
    except (ImportError, AttributeError):
        alunos = []
    
    # Certifique-se de que os cursos estão sendo carregados
    from cursos.models import Curso
    cursos = Curso.objects.all().order_by('codigo_curso')
    
    # Adicione um log para depuração
    print(f"Carregando {len(cursos)} cursos")
    
    return render(
        request,
        "turmas/criar_turma.html",
        {
            "form": form,
            "alunos": alunos,
            "cursos": cursos,
        },
    )
@login_required
def detalhar_turma(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    # Verificar pendências na instrutoria
    tem_pendencia_instrutoria = (
        not turma.instrutor
        or not turma.instrutor_auxiliar
        or not turma.auxiliar_instrucao
    )
    # Calcular informações de matrículas
    alunos_matriculados_count = (
        turma.matriculas.filter(status="A").count()
        if hasattr(turma, "matriculas")
        else 0
    )
    vagas_disponiveis = turma.vagas - alunos_matriculados_count
    # Obter matrículas ativas
    matriculas = (
        turma.matriculas.filter(status="A")
        if hasattr(turma, "matriculas")
        else []
    )
    context = {
        "turma": turma,
        "matriculas": matriculas,
        "alunos_matriculados_count": alunos_matriculados_count,
        "vagas_disponiveis": vagas_disponiveis,
        "tem_pendencia_instrutoria": tem_pendencia_instrutoria,
    }
    return render(request, "turmas/detalhar_turma.html", context)


@login_required
def editar_turma(request, id):
    """Edita uma turma existente."""
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso!")
            return redirect("turmas:detalhar_turma", id=turma.id)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = TurmaForm(instance=turma)
    # Obter todos os alunos ativos para o formulário
    Aluno = get_model("alunos", "Aluno")
    alunos = Aluno.objects.filter(situacao="ATIVO")
    return render(
        request,
        "turmas/editar_turma.html",
        {
            "form": form,
            "turma": turma,
            "alunos": alunos,  # Passar todos os alunos ativos para o template
        },
    )


@login_required
def excluir_turma(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        turma.delete()
        messages.success(request, "Turma excluída com sucesso!")
        return redirect("turmas:listar_turmas")
    return render(request, "turmas/excluir_turma.html", {"turma": turma})


@login_required
def listar_alunos_matriculados(request, id):
    Turma = get_turma_model()
    turma = get_object_or_404(Turma, id=id)
    alunos = turma.alunos.all() if hasattr(turma, "alunos") else []
    return render(
        request,
        "turmas/listar_alunos_matriculados.html",
        {"turma": turma, "alunos": alunos},
    )


@login_required
def matricular_aluno(request, turma_id):
    """Matricula um aluno em uma turma específica."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()
    turma = get_object_or_404(Turma, id=id)
    if request.method == "POST":
        aluno_cpf = request.POST.get("aluno")
        aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
        # Verificar se existe um modelo de Matricula
        try:
            Matricula = import_module("matriculas.models").Matricula
            # Criar uma matrícula em vez de adicionar diretamente à relação many-to-many
            Matricula.objects.create(
                aluno=aluno,
                turma=turma,
                data_matricula=timezone.now().date(),
                status="A",  # Ativa
            )
        except (ImportError, AttributeError):
            # Fallback: adicionar diretamente à relação many-to-many se o modelo Matricula não existir
            if hasattr(turma, "alunos"):
                turma.alunos.add(aluno)
        messages.success(
            request, f"Aluno {aluno.nome} matriculado com sucesso!"
        )
        return redirect("turmas:detalhar_turma", id=turma.id)
    # Obter alunos disponíveis para matrícula
    try:
        # Se existir um modelo de Matricula, excluir alunos já matriculados
        Matricula = import_module("matriculas.models").Matricula
        alunos_matriculados = Matricula.objects.filter(
            turma=turma, status="A"
        ).values_list("aluno__cpf", flat=True)
        alunos_disponiveis = Aluno.objects.exclude(cpf__in=alunos_matriculados)
    except (ImportError, AttributeError):
        # Fallback
        if hasattr(turma, "alunos"):
            alunos_disponiveis = Aluno.objects.exclude(turmas=turma)
        else:
            alunos_disponiveis = Aluno.objects.all()
    # Adicionar informação de vagas disponíveis
    vagas_disponiveis = (
        turma.vagas_disponiveis
        if hasattr(turma, "vagas_disponiveis")
        else turma.vagas
    )
    return render(
        request,
        "turmas/matricular_aluno.html",
        {
            "turma": turma,
            "alunos": alunos_disponiveis,
            "vagas_disponiveis": vagas_disponiveis,
        },
    )


@login_required
def cancelar_matricula(request, turma_id, aluno_cpf):
    """Cancela a matrícula de um aluno em uma turma."""
    Turma = get_turma_model()
    Aluno = get_aluno_model()
    turma = get_object_or_404(Turma, id=turma_id)
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    # Verificar se o aluno está matriculado na turma
    try:
        # Importar o modelo Matricula dinamicamente
        from importlib import import_module

        matriculas_module = import_module("matriculas.models")
        Matricula = getattr(matriculas_module, "Matricula")
        matricula = Matricula.objects.get(aluno=aluno, turma=turma)
        if request.method == "POST":
            # Cancelar a matrícula
            matricula.status = "C"  # Cancelada
            matricula.save()
            messages.success(
                request,
                f"Matrícula do aluno {aluno.nome} na turma {turma.nome} cancelada com sucesso.",
            )
            return redirect("turmas:detalhar_turma", id=turma.id)
        # Se for GET, mostrar página de confirmação
        return render(
            request,
            "turmas/cancelar_matricula.html",
            {"turma": turma, "aluno": aluno},
        )
    except (ImportError, AttributeError) as e:
        messages.error(
            request, f"Erro ao acessar o modelo de matrículas: {str(e)}"
        )
        return redirect("turmas:detalhar_turma", id=turma.id)
    except Matricula.DoesNotExist:
        messages.error(
            request,
            f"O aluno {aluno.nome} não está matriculado na turma {turma.nome}.",
        )
        return redirect("turmas:detalhar_turma", id=turma.id)

@login_required
def exportar_turmas(request):
    """Exporta os dados das turmas para um arquivo CSV ou Excel."""
    formato = request.GET.get('formato', 'csv')
    
    # Filtros
    query = request.GET.get('q', '')
    curso_id = request.GET.get('curso', '')
    status = request.GET.get('status', '')
    
    # Consulta base
    turmas = Turma.objects.all()
    
    # Aplicar filtros
    if query:
        turmas = turmas.filter(
            Q(nome__icontains=query) | 
            Q(instrutor__nome__icontains=query) |
            Q(curso__nome__icontains=query)
        )
    
    if curso_id:
        turmas = turmas.filter(curso__codigo_curso=curso_id)
    
    if status:
        turmas = turmas.filter(status=status)
    
    # Ordenar
    turmas = turmas.order_by('nome')
    
    # Definir nome do arquivo
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename = f"turmas_export_{timestamp}"
    
    if formato == 'excel':
        # Exportar para Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Estilos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#F0F0F0',
            'border': 1
        })
        
        # Cabeçalhos
        headers = [
            'ID', 'Nome', 'Curso', 'Vagas', 'Status', 'Data Início', 
            'Data Fim', 'Instrutor', 'Instrutor Auxiliar', 'Local', 'Horário'
        ]
        
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        
        # Dados
        for row_num, turma in enumerate(turmas, 1):
            worksheet.write(row_num, 0, turma.id)
            worksheet.write(row_num, 1, turma.nome)
            worksheet.write(row_num, 2, turma.curso.nome if turma.curso else '')
            worksheet.write(row_num, 3, turma.vagas)
            worksheet.write(row_num, 4, turma.get_status_display())
            worksheet.write(row_num, 5, turma.data_inicio.strftime('%d/%m/%Y') if turma.data_inicio else '')
            worksheet.write(row_num, 6, turma.data_fim.strftime('%d/%m/%Y') if turma.data_fim else '')
            worksheet.write(row_num, 7, turma.instrutor.nome if turma.instrutor else '')
            worksheet.write(row_num, 8, turma.instrutor_auxiliar.nome if turma.instrutor_auxiliar else '')
            worksheet.write(row_num, 9, turma.local or '')
            worksheet.write(row_num, 10, turma.horario or '')
        
        # Ajustar largura das colunas
        for i, header in enumerate(headers):
            worksheet.set_column(i, i, len(header) + 5)
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        return response
    else:
        # Exportar para CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Nome', 'Curso', 'Vagas', 'Status', 'Data Início', 
            'Data Fim', 'Instrutor', 'Instrutor Auxiliar', 'Local', 'Horário'
        ])
        
        for turma in turmas:
            writer.writerow([
                turma.id,
                turma.nome,
                turma.curso.nome if turma.curso else '',
                turma.vagas,
                turma.get_status_display(),
                turma.data_inicio.strftime('%d/%m/%Y') if turma.data_inicio else '',
                turma.data_fim.strftime('%d/%m/%Y') if turma.data_fim else '',
                turma.instrutor.nome if turma.instrutor else '',
                turma.instrutor_auxiliar.nome if turma.instrutor_auxiliar else '',
                turma.local or '',
                turma.horario or ''
            ])
        
        return response

@login_required
def relatorio_turmas(request):
    """Gera relatórios sobre as turmas."""
    # Estatísticas gerais
    total_turmas = Turma.objects.count()
    turmas_ativas = Turma.objects.filter(status='ATIVA').count()
    turmas_planejadas = Turma.objects.filter(status='PLANEJADA').count()
    turmas_concluidas = Turma.objects.filter(status='CONCLUIDA').count()
    turmas_canceladas = Turma.objects.filter(status='CANCELADA').count()
    
    # Estatísticas por curso
    cursos = Curso.objects.all()
    estatisticas_cursos = []
    
    for curso in cursos:
        turmas_curso = Turma.objects.filter(curso=curso)
        total_turmas_curso = turmas_curso.count()
        
        if total_turmas_curso > 0:
            turmas_ativas_curso = turmas_curso.filter(status='ATIVA').count()
            turmas_planejadas_curso = turmas_curso.filter(status='PLANEJADA').count()
            turmas_concluidas_curso = turmas_curso.filter(status='CONCLUIDA').count()
            
            # Calcular média de alunos por turma
            total_alunos = 0
            for turma in turmas_curso:
                total_alunos += Matricula.objects.filter(turma=turma, ativa=True).count()
            
            media_alunos = total_alunos / total_turmas_curso if total_turmas_curso > 0 else 0
            
            estatisticas_cursos.append({
                'curso': curso,
                'total_turmas': total_turmas_curso,
                'turmas_ativas': turmas_ativas_curso,
                'turmas_planejadas': turmas_planejadas_curso,
                'turmas_concluidas': turmas_concluidas_curso,
                'media_alunos': round(media_alunos, 1)
            })
    
    # Turmas com mais alunos
    turmas_populares = Turma.objects.annotate(
        total_alunos=Count('matricula', filter=Q(matricula__ativa=True))
    ).order_by('-total_alunos')[:5]
    
    # Instrutores com mais turmas
    instrutores_ativos = Aluno.objects.filter(
        Q(turma_instrutor__isnull=False) | 
        Q(turma_instrutor_auxiliar__isnull=False)
    ).distinct()
    
    estatisticas_instrutores = []
    for instrutor in instrutores_ativos:
        turmas_como_instrutor = Turma.objects.filter(instrutor=instrutor).count()
        turmas_como_auxiliar = Turma.objects.filter(instrutor_auxiliar=instrutor).count()
        total_turmas_instrutor = turmas_como_instrutor + turmas_como_auxiliar
        
        if total_turmas_instrutor > 0:
            estatisticas_instrutores.append({
                'instrutor': instrutor,
                'turmas_como_instrutor': turmas_como_instrutor,
                'turmas_como_auxiliar': turmas_como_auxiliar,
                'total_turmas': total_turmas_instrutor
            })
    
    estatisticas_instrutores.sort(key=lambda x: x['total_turmas'], reverse=True)
    estatisticas_instrutores = estatisticas_instrutores[:5]
    
    context = {
        'total_turmas': total_turmas,
        'turmas_ativas': turmas_ativas,
        'turmas_planejadas': turmas_planejadas,
        'turmas_concluidas': turmas_concluidas,
        'turmas_canceladas': turmas_canceladas,
        'estatisticas_cursos': estatisticas_cursos,
        'turmas_populares': turmas_populares,
        'estatisticas_instrutores': estatisticas_instrutores
    }
    
    return render(request, 'turmas/relatorio_turmas.html', context)

@login_required
def dashboard_turmas(request):
    """Exibe um dashboard com informações sobre as turmas."""
    # Estatísticas gerais
    total_turmas = Turma.objects.count()
    turmas_ativas = Turma.objects.filter(status='ATIVA').count()
    turmas_planejadas = Turma.objects.filter(status='PLANEJADA').count()
    turmas_concluidas = Turma.objects.filter(status='CONCLUIDA').count()
    turmas_canceladas = Turma.objects.filter(status='CANCELADA').count()
    
    # Dados para gráfico de status
    dados_status = [
        {'status': 'Ativas', 'quantidade': turmas_ativas, 'cor': '#28a745'},
        {'status': 'Planejadas', 'quantidade': turmas_planejadas, 'cor': '#17a2b8'},
        {'status': 'Concluídas', 'quantidade': turmas_concluidas, 'cor': '#6c757d'},
        {'status': 'Canceladas', 'quantidade': turmas_canceladas, 'cor': '#dc3545'}
    ]
    
    # Turmas por curso
    cursos = Curso.objects.all()
    dados_cursos = []
    
    cores_cursos = [
        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
        '#5a5c69', '#858796', '#f8f9fc', '#d1d3e2', '#b7b9cc'
    ]
    
    for i, curso in enumerate(cursos):
        total_turmas_curso = Turma.objects.filter(curso=curso).count()
        if total_turmas_curso > 0:
            dados_cursos.append({
                'curso': curso.nome,
                'quantidade': total_turmas_curso,
                'cor': cores_cursos[i % len(cores_cursos)]
            })
    
    # Turmas recentes
    turmas_recentes = Turma.objects.order_by('-id')[:5]
    
    # Turmas com vagas disponíveis
    turmas_com_vagas = []
    for turma in Turma.objects.filter(status='ATIVA'):
        total_matriculados = Matricula.objects.filter(turma=turma, ativa=True).count()
        vagas_disponiveis = turma.vagas - total_matriculados
        
        if vagas_disponiveis > 0:
            turmas_com_vagas.append({
                'turma': turma,
                'vagas_disponiveis': vagas_disponiveis,
                'percentual_ocupacao': (total_matriculados / turma.vagas) * 100
            })
    
    turmas_com_vagas.sort(key=lambda x: x['vagas_disponiveis'], reverse=True)
    turmas_com_vagas = turmas_com_vagas[:5]
    
    context = {
        'total_turmas': total_turmas,
        'turmas_ativas': turmas_ativas,
        'turmas_planejadas': turmas_planejadas,
        'turmas_concluidas': turmas_concluidas,
        'turmas_canceladas': turmas_canceladas,
        'dados_status': dados_status,
        'dados_cursos': dados_cursos,
        'turmas_recentes': turmas_recentes,
        'turmas_com_vagas': turmas_com_vagas
    }
    
    return render(request, 'turmas/dashboard.html', context)
