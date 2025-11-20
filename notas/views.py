from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Avg, Count, Max, Min
from django.core.paginator import Paginator
from .models import Nota
from .forms import NotaForm
from alunos.services import (
    listar_alunos as listar_alunos_service,
    buscar_alunos_por_nome_ou_cpf,
)
from cursos.services import listar_cursos as listar_cursos_service
import csv


@login_required
def listar_notas(request):
    """Lista todas as notas cadastradas."""
    # Obter parâmetros de busca e filtro
    query = request.GET.get("q", "")
    aluno_id = request.GET.get("aluno", "")
    curso_id = request.GET.get("curso", "")
    periodo = request.GET.get("periodo", "")

    # Filtrar notas
    notas = Nota.objects.all().select_related("aluno", "curso", "turma")

    if query:
        notas = notas.filter(
            Q(aluno__nome__icontains=query) | Q(curso__nome__icontains=query)
        )

    if aluno_id:
        notas = notas.filter(aluno__cpf=aluno_id)

    if curso_id:
        notas = notas.filter(curso_id=curso_id)

    # Filtrar por período
    if periodo:
        from datetime import datetime, timedelta

        hoje = datetime.now()
        if periodo == "atual":
            notas = notas.filter(data__month=hoje.month, data__year=hoje.year)
        elif periodo == "ultimo_mes":
            mes_passado = hoje - timedelta(days=30)
            notas = notas.filter(
                data__month=mes_passado.month, data__year=mes_passado.year
            )
        elif periodo == "ultimo_trimestre":
            tres_meses_atras = hoje - timedelta(days=90)
            notas = notas.filter(data__gte=tres_meses_atras)
        elif periodo == "ultimo_semestre":
            seis_meses_atras = hoje - timedelta(days=180)
            notas = notas.filter(data__gte=seis_meses_atras)

    # Ordenar por data mais recente
    notas = notas.order_by("-data")

    # Calcular estatísticas
    estatisticas = notas.aggregate(
        total_notas=Count("id"),
        media_geral=Avg("nota"),
        nota_maxima=Max("nota"),
        nota_minima=Min("nota"),
    )
    # Valores padrão se não houver notas
    estatisticas["total_notas"] = estatisticas["total_notas"] or 0
    estatisticas["media_geral"] = estatisticas["media_geral"] or 0
    estatisticas["nota_maxima"] = estatisticas["nota_maxima"] or 0
    estatisticas["nota_minima"] = estatisticas["nota_minima"] or 0

    # Paginação
    paginator = Paginator(notas, 10)  # 10 notas por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Obter alunos e cursos para os filtros
    alunos = listar_alunos_service()
    cursos = listar_cursos_service()

    # Se for requisição AJAX, retornar JSON com os dados
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        from django.template.loader import render_to_string

        tabela_html = render_to_string(
            "notas/_tabela_notas_parcial.html", {"notas": page_obj, "request": request}
        )
        paginacao_html = render_to_string(
            "notas/_paginacao_parcial.html", {"page_obj": page_obj, "request": request}
        )

        return JsonResponse(
            {"tabela_html": tabela_html, "paginacao_html": paginacao_html}
        )

    context = {
        "notas": page_obj,
        "page_obj": page_obj,
        "query": query,
        "alunos": alunos,
        "cursos": cursos,
        "filtros": {"aluno": aluno_id, "curso": curso_id, "periodo": periodo},
        "estatisticas": estatisticas,
        "total_notas": notas.count(),
    }

    return render(request, "notas/listar_notas.html", context)


@login_required
def detalhar_nota(request, nota_id):
    """Exibe os detalhes de uma nota."""
    nota = get_object_or_404(Nota, id=nota_id)
    return render(request, "notas/detalhar_nota.html", {"nota": nota})


@login_required
def criar_nota(request):
    """Cria uma nova nota."""
    if request.method == "POST":
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save()
            messages.success(request, "Nota registrada com sucesso!")
            return redirect("notas:detalhar_nota", nota_id=nota.id)
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = NotaForm()

    return render(request, "notas/formulario_nota.html", {"form": form})


@login_required
def editar_nota(request, nota_id):
    """Edita uma nota existente."""
    nota = get_object_or_404(Nota, id=nota_id)

    if request.method == "POST":
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            nota = form.save()
            messages.success(request, "Nota atualizada com sucesso!")
            return redirect("notas:detalhar_nota", nota_id=nota.id)
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = NotaForm(instance=nota)
        # Formatar a data no formato correto para o input type="date"
        if nota.data:
            form.initial["data"] = nota.data.strftime("%Y-%m-%d")

    return render(request, "notas/formulario_nota.html", {"form": form, "nota": nota})


@login_required
def excluir_nota(request, nota_id):
    """Exclui uma nota com padrão de exclusão segura."""
    nota = get_object_or_404(Nota, id=nota_id)

    # Buscar dependências (exemplo: pagamentos, presenças, etc. - atualmente não há)
    dependencias = {}
    # Se no futuro houver dependências, adicionar aqui

    if request.method == "POST":
        if any(len(lst) > 0 for lst in dependencias.values()):
            messages.error(
                request,
                "Não é possível excluir a nota pois existem registros vinculados. Remova as dependências antes de tentar novamente.",
                extra_tags="safe",
            )
            return redirect("notas:excluir_nota", nota_id=nota.id)
        nota.delete()
        messages.success(request, "Nota excluída com sucesso!")
        return redirect("notas:listar_notas")

    return render(
        request, "notas/excluir_nota.html", {"nota": nota, "dependencias": dependencias}
    )


@login_required
def exportar_notas_csv(request):
    """Exporta as notas para um arquivo CSV."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="notas.csv"'

    writer = csv.writer(response)
    writer.writerow(["Aluno", "Curso", "Turma", "Nota", "Peso", "Data"])

    notas = Nota.objects.all().select_related("aluno", "curso", "turma")
    for nota in notas:
        writer.writerow(
            [
                nota.aluno.nome,
                nota.curso.nome,
                nota.turma.nome if nota.turma else "N/A",
                nota.valor,
                nota.peso,
                nota.data.strftime("%d/%m/%Y"),
            ]
        )

    return response


@login_required
def exportar_notas_excel(request):
    """Exporta as notas para um arquivo Excel."""
    import xlsxwriter
    from io import BytesIO

    # Criar um buffer de memória para o arquivo Excel
    output = BytesIO()

    # Criar um novo workbook e adicionar uma planilha
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Notas")

    # Definir estilos - Corrigido o atributo 'color' para 'font_color'
    header_format = workbook.add_format(
        {
            "bold": True,
            "bg_color": "#4472C4",
            "font_color": "white",  # Corrigido de 'color' para 'font_color'
            "border": 1,
        }
    )

    # Escrever cabeçalhos
    headers = ["Aluno", "Curso", "Turma", "Nota", "Peso", "Data"]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    # Buscar todas as notas
    notas = Nota.objects.all().select_related("aluno", "curso", "turma")

    # Escrever dados
    for row_num, nota in enumerate(notas, 1):
        worksheet.write(row_num, 0, nota.aluno.nome)
        worksheet.write(row_num, 1, nota.curso.nome)
        worksheet.write(row_num, 2, nota.turma.nome if nota.turma else "N/A")
        worksheet.write(row_num, 3, float(nota.valor))
        worksheet.write(row_num, 4, float(nota.peso))
        worksheet.write(row_num, 5, nota.data.strftime("%d/%m/%Y"))

    # Fechar o workbook (em vez de salvar)
    workbook.close()

    # Configurar a resposta HTTP
    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="notas.xlsx"'

    return response


@login_required
def dashboard_notas(request):
    """Exibe um dashboard com estatísticas sobre as notas."""
    # Estatísticas gerais
    total_notas = Nota.objects.count()
    media_geral = Nota.objects.aggregate(Avg("valor"))["valor__avg"] or 0

    # Notas por curso (para gráfico)
    notas_por_curso = list(
        Nota.objects.values("curso__nome")
        .annotate(total=Count("id"), media=Avg("valor"))
        .order_by("-total")
    )

    # Distribuição de notas (para gráfico)
    from django.db.models import Case, When, IntegerField

    distribuicao = (
        Nota.objects.annotate(
            faixa=Case(
                When(valor__lt=5, then=0),  # Abaixo de 5
                When(valor__lt=7, then=1),  # Entre 5 e 6.9
                When(valor__lt=9, then=2),  # Entre 7 e 8.9
                default=3,  # 9 ou mais
                output_field=IntegerField(),
            )
        )
        .values("faixa")
        .annotate(total=Count("id"))
        .order_by("faixa")
    )

    # Converter para formato adequado para gráficos
    faixas_notas = ["Abaixo de 5", "Entre 5 e 6.9", "Entre 7 e 8.9", "9 ou mais"]
    dados_distribuicao = [0, 0, 0, 0]  # Inicializar com zeros

    for item in distribuicao:
        dados_distribuicao[item["faixa"]] = item["total"]

    # Notas recentes
    notas_recentes = (
        Nota.objects.all().select_related("aluno", "curso").order_by("-data")[:5]
    )

    context = {
        "total_notas": total_notas,
        "media_geral": round(media_geral, 2),
        "notas_por_curso": notas_por_curso,
        "faixas_notas": faixas_notas,
        "dados_distribuicao": dados_distribuicao,
        "notas_recentes": notas_recentes,
    }

    return render(request, "notas/dashboard_notas.html", context)


@login_required
def relatorio_notas(request):
    """Exibe um relatório com estatísticas sobre as notas."""
    # Estatísticas gerais
    total_notas = Nota.objects.count()
    media_geral = Nota.objects.aggregate(Avg("valor"))["valor__avg"] or 0

    # Estatísticas por curso
    cursos_stats = (
        Nota.objects.values("curso__nome")
        .annotate(
            total=Count("id"),
            media=Avg("valor"),
            maxima=Max("valor"),
            minima=Min("valor"),
        )
        .order_by("-total")
    )

    # Estatísticas por aluno
    alunos_stats = (
        Nota.objects.values("aluno__nome")
        .annotate(
            total=Count("id"),
            media=Avg("valor"),
            maxima=Max("valor"),
            minima=Min("valor"),
        )
        .order_by("-media")[:10]
    )  # Top 10 alunos por média

    context = {
        "total_notas": total_notas,
        "media_geral": media_geral,
        "cursos_stats": cursos_stats,
        "alunos_stats": alunos_stats,
    }

    return render(request, "notas/relatorio_notas.html", context)


@login_required
def buscar_alunos(request):
    """API endpoint para buscar alunos."""
    query = request.GET.get("q", "")
    if len(query) < 2:
        return JsonResponse({"results": []})

    alunos = buscar_alunos_por_nome_ou_cpf(query)[:10]

    results = [
        {"id": aluno.cpf, "text": f"{aluno.nome} (CPF: {aluno.cpf})"}
        for aluno in alunos
    ]

    return JsonResponse({"results": results})


@login_required
def verificar_aluno_matriculado(request, aluno_id, turma_id):
    """Verifica se um aluno está matriculado em uma turma."""
    try:
        from matriculas.models import Matricula

        matricula = Matricula.objects.filter(
            aluno__cpf=aluno_id,
            turma__id=turma_id,
            status="A",  # Ativa
        ).exists()

        return JsonResponse({"matriculado": matricula})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
