from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module
from django.db import IntegrityError


def get_models():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")


def get_forms():
    cursos_forms = import_module("cursos.forms")
    return getattr(cursos_forms, "CursoForm")


@login_required
def listar_cursos(request):
    """Lista todos os cursos cadastrados."""
    Curso = get_models()
    cursos = Curso.objects.all()
    return render(request, "cursos/listar_cursos.html", {"cursos": cursos})


@login_required
def criar_curso(request):
    """Cria um novo curso."""
    CursoForm = get_forms()
    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso criado com sucesso!")
            return redirect("cursos:listar_cursos")
    else:
        form = CursoForm()
    return render(request, "cursos/criar_curso.html", {"form": form})


@login_required
def detalhar_curso(request, id):
    """Exibe os detalhes de um curso."""
    Curso = get_models()
    curso = get_object_or_404(Curso, id=id)
    return render(request, "cursos/detalhar_curso.html", {"curso": curso})


@login_required
def editar_curso(request, id):
    """Edita um curso existente."""
    Curso = get_models()
    CursoForm = get_forms()
    curso = get_object_or_404(Curso, id=id)

    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso atualizado com sucesso!")
            return redirect("cursos:listar_cursos")
    else:
        form = CursoForm(instance=curso)

    return render(
        request, "cursos/editar_curso.html", {"form": form, "curso": curso}
    )


@login_required
def excluir_curso(request, id):
    """Exclui um curso com verificação robusta de dependências."""
    Curso = get_models()
    curso = get_object_or_404(Curso, id=id)

    # Buscar dependências
    turmas = list(getattr(curso, 'turmas', []).all()) if hasattr(curso, 'turmas') else []
    atividades = []
    notas = []
    matriculas = []
    pagamentos = []
    try:
        from atividades.models import AtividadeAcademica
        atividades = list(AtividadeAcademica.objects.filter(curso=curso))
    except Exception:
        pass
    try:
        from notas.models import Nota
        notas = list(Nota.objects.filter(curso=curso))
    except Exception:
        pass
    try:
        from matriculas.models import Matricula
        matriculas = list(Matricula.objects.filter(turma__curso=curso))
    except Exception:
        pass
    try:
        from pagamentos.models import Pagamento
        pagamentos = list(Pagamento.objects.filter(turma__curso=curso))
    except Exception:
        pass

    dependencias = {
        'turmas': turmas,
        'atividades': atividades,
        'notas': notas,
        'matriculas': matriculas,
        'pagamentos': pagamentos,
    }

    if request.method == "POST":
        # Impede exclusão se houver dependências
        if any(len(lst) > 0 for lst in dependencias.values()):
            messages.error(
                request,
                "Não é possível excluir o curso pois existem registros vinculados (turmas, atividades, notas, matrículas, pagamentos, etc.). Remova as dependências antes de tentar novamente.",
                extra_tags="safe"
            )
            return redirect("cursos:excluir_curso", id=curso.id)
        try:
            curso.delete()
            messages.success(request, "Curso excluído com sucesso!")
            return redirect("cursos:listar_cursos")
        except IntegrityError:
            messages.error(
                request,
                "Não foi possível excluir o curso, pois existem registros vinculados a ele (ex: turmas, alunos, atividades, notas, matrículas, pagamentos, etc.). "
                "Para excluir este curso, primeiro remova ou transfira todas as dependências listadas abaixo.",
                extra_tags="safe"
            )
            return redirect("cursos:excluir_curso", id=curso.id)

    return render(request, "cursos/excluir_curso.html", {"curso": curso, "dependencias": dependencias})


@login_required
def exportar_cursos(request):
    """Exporta os dados dos cursos para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse

        Curso = get_models()
        cursos = Curso.objects.all()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="cursos.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "Código",
                "Nome",
                "Descrição",
                "Duração (meses)",
            ]
        )

        for curso in cursos:
            writer.writerow(
                [
                    curso.codigo_curso,
                    curso.nome,
                    curso.descricao,
                    curso.duracao,
                ]
            )

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

            Curso = get_models()

            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []

            for row in reader:
                try:
                    # Processar código do curso
                    codigo_curso = None
                    try:
                        codigo_curso = int(row.get("Código", "").strip())
                    except ValueError:
                        errors.append(f"Código de curso inválido: {row.get('Código', '')}")
                        continue

                    # Verificar se já existe um curso com este código
                    if Curso.objects.filter(codigo_curso=codigo_curso).exists():
                        errors.append(f"Já existe um curso com o código {codigo_curso}")
                        continue

                    # Processar duração
                    duracao = 6  # Valor padrão
                    try:
                        if row.get("Duração (meses)"):
                            duracao = int(row.get("Duração (meses)"))
                    except ValueError:
                        errors.append(f"Duração inválida: {row.get('Duração (meses)', '')}")
                        continue

                    # Criar o curso
                    Curso.objects.create(
                        codigo_curso=codigo_curso,
                        nome=row.get("Nome", "").strip(),
                        descricao=row.get("Descrição", "").strip(),
                        duracao=duracao,
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
