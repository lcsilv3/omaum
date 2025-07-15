from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Curso
from .forms import CursoForm
from . import services  # Importa a camada de serviço
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
import openpyxl


@login_required
def listar_cursos(request):
    """Lista todos os cursos cadastrados."""
    cursos = services.listar_cursos()
    return render(request, "cursos/listar_cursos.html", {"cursos": cursos})


@login_required
def relatorio_cursos(request):
    cursos = services.listar_cursos()
    data_emissao = datetime.now()
    context = {
        'titulo': 'Relatório de Cursos',
        'cursos': cursos,
        'data_emissao': data_emissao.strftime('%d/%m/%Y %H:%M'),
        'nome_organizacao': 'OMAUM - Ordem Mística de Aspiração Universal ao Mestrado',
        'nome_sistema': 'Sistema de Gestão Integrada'
    }
    return render(request, 'cursos/relatorio_cursos.html', context)


@login_required
def gerar_relatorio_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_cursos.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Cabeçalho Institucional
    data_emissao = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Linha 1: Nome da organização (centralizado)
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2.0, height - inch, "OMAUM - Ordem Mística de Aspiração Universal ao Mestrado")
    
    # Linha 2: Nome do sistema (centralizado) e Data (à direita)
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2.0, height - 1.2 * inch, "Sistema de Gestão Integrada")
    p.setFont("Helvetica", 8)
    p.drawRightString(width - inch, height - 1.2 * inch, f"Data de Emissão: {data_emissao}")

    # Linha 3: Título do Relatório (centralizado)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2.0, height - 1.5 * inch, "Relatório de Cursos")

    p.setFont("Helvetica", 12)
    y = height - 1.9 * inch # Ajuste na posição inicial da tabela
    
    # Cabeçalhos da tabela
    p.setFont("Helvetica-Bold", 12)
    p.drawString(inch, y, "ID")
    p.drawString(1.5 * inch, y, "Nome")
    p.drawString(4 * inch, y, "Descrição")
    p.line(inch, y - 0.1 * inch, width - inch, y - 0.1 * inch)
    y -= 0.3 * inch

    cursos = services.listar_cursos()
    p.setFont("Helvetica", 10)
    for curso in cursos:
        if y < inch:
            p.showPage()
            p.setFont("Helvetica-Bold", 12)
            p.drawCentredString(width / 2.0, height - inch, "Relatório de Cursos (Continuação)")
            y = height - 1.5 * inch
            p.setFont("Helvetica-Bold", 12)
            p.drawString(inch, y, "ID")
            p.drawString(1.5 * inch, y, "Nome")
            p.drawString(4 * inch, y, "Descrição")
            p.line(inch, y - 0.1 * inch, width - inch, y - 0.1 * inch)
            y -= 0.3 * inch
            p.setFont("Helvetica", 10)

        p.drawString(inch, y, str(curso.id))
        p.drawString(1.5 * inch, y, curso.nome)
        
        # Lógica para quebrar a linha da descrição
        descricao_text = curso.descricao if curso.descricao else ""
        text_object = p.beginText(4 * inch, y)
        text_object.setFont("Helvetica", 10)
        
        # Quebra a linha a cada 50 caracteres
        wrapped_text = [descricao_text[i:i+50] for i in range(0, len(descricao_text), 50)]
        
        for line in wrapped_text:
            text_object.textLine(line)
        
        p.drawText(text_object)
        
        # Ajusta a posição Y com base no número de linhas da descrição
        y -= (0.2 * inch * len(wrapped_text)) + 0.1 * inch


    p.showPage()
    p.save()

    return response


@login_required
def criar_curso(request):
    """Cria um novo curso utilizando a camada de serviço."""
    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            try:
                services.criar_curso(
                    nome=form.cleaned_data['nome'], 
                    descricao=form.cleaned_data['descricao']
                )
                messages.success(request, "Curso criado com sucesso!")
                return redirect("cursos:listar_cursos")
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = CursoForm()
    return render(request, "cursos/criar_curso.html", {"form": form})


@login_required
def detalhar_curso(request, id):
    """Exibe os detalhes de um curso."""
    curso = services.obter_curso_por_id(id)
    if not curso:
        messages.error(request, "Curso não encontrado.")
        return redirect("cursos:listar_cursos")
    return render(request, "cursos/detalhar_curso.html", {"curso": curso})


@login_required
def editar_curso(request, id):
    """Edita um curso existente utilizando a camada de serviço."""
    curso = services.obter_curso_por_id(id)
    if not curso:
        messages.error(request, "Curso não encontrado.")
        return redirect("cursos:listar_cursos")

    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            services.atualizar_curso(
                curso_id=id, 
                nome=form.cleaned_data['nome'], 
                descricao=form.cleaned_data['descricao']
            )
            messages.success(request, "Curso atualizado com sucesso!")
            return redirect("cursos:listar_cursos")
    else:
        form = CursoForm(instance=curso)
    return render(request, "cursos/editar_curso.html", {"form": form, "curso": curso})


@login_required
def excluir_curso(request, id):
    """Exclui um curso utilizando a camada de serviço."""
    curso = services.obter_curso_por_id(id)
    if not curso:
        messages.error(request, "Curso não encontrado.")
        return redirect("cursos:listar_cursos")

    dependencias = services.verificar_dependencias_curso(curso)

    if request.method == "POST":
        try:
            if services.excluir_curso(id):
                messages.success(request, "Curso excluído com sucesso!")
                return redirect("cursos:listar_cursos")
            else:
                # Este else pode não ser alcançado devido à exceção, mas é uma boa prática
                messages.error(request, "Não foi possível excluir o curso.")
        except ValueError as e:
            messages.error(request, str(e))
            # Redireciona de volta para a página de exclusão para mostrar as dependências
            return redirect("cursos:excluir_curso", id=id)
        except IntegrityError:
            messages.error(request, "Erro de integridade. Verifique as dependências.")
            return redirect("cursos:excluir_curso", id=id)

    return render(request, "cursos/excluir_curso.html", {"curso": curso, "dependencias": dependencias})


@login_required
def exportar_cursos(request):
    """Exporta os dados dos cursos para um arquivo XLSX."""
    try:
        cursos = services.listar_cursos()

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="cursos.xlsx"'

        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Cursos"

        # Cabeçalhos
        worksheet.append(
            [
                "Nome",
                "Descrição",
            ]
        )

        # Dados
        for curso in cursos:
            worksheet.append(
                [
                    curso.nome,
                    curso.descricao,
                ]
            )

        workbook.save(response)
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar cursos: {str(e)}")
        return redirect("cursos:listar_cursos")


@login_required
def importar_cursos(request):
    """Importa cursos de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper

            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []

            for row in reader:
                try:
                    nome = row.get("Nome", "").strip()
                    descricao = row.get("Descrição", "").strip()
                    Curso.objects.create(
                        nome=nome,
                        descricao=descricao,
                    )

                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")

            if errors:
                messages.warning(
                    request,
                    f"{count} cursos importados com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(request, f"... e mais {len(errors) - 5} erros.")
            else:
                messages.success(request, f"{count} cursos importados com sucesso!")
            return redirect("cursos:listar_cursos")
        except Exception as e:
            messages.error(request, f"Erro ao importar cursos: {str(e)}")

    return render(request, "cursos/importar_cursos.html")
