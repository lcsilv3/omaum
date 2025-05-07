from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError
from importlib import import_module
from django.urls import reverse


def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    from importlib import import_module
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


@login_required
def listar_matriculas(request):
    """Lista todas as matrículas."""
    Matricula = get_model("matriculas", "Matricula")
    matriculas = Matricula.objects.all().select_related("aluno", "turma")
    return render(
        request,
        "matriculas/listar_matriculas.html",
        {"matriculas": matriculas},
    )


@login_required
def detalhar_matricula(request, id):
    """Exibe os detalhes de uma matrícula."""
    Matricula = get_model("matriculas", "Matricula")
    matricula = get_object_or_404(Matricula, id=id)
    return render(
        request, "matriculas/detalhar_matricula.html", {"matricula": matricula}
    )


@login_required
def realizar_matricula(request):
    """Realiza uma nova matrícula."""
    Aluno = get_model("alunos", "Aluno")
    Turma = get_model("turmas", "Turma")
    Matricula = get_model("matriculas", "Matricula")

    if request.method == "POST":
        aluno_id = request.POST.get("aluno")
        turma_id = request.POST.get("turma")

        if not aluno_id or not turma_id:
            messages.error(request, "Selecione um aluno e uma turma.")
            return redirect("matriculas:realizar_matricula")

        aluno = get_object_or_404(Aluno, cpf=aluno_id)
        turma = get_object_or_404(Turma, id=turma_id)
        # Verificar se já existe matrícula
        if Matricula.objects.filter(aluno=aluno, turma=turma).exists():
            messages.warning(
                request,
                f"O aluno {aluno.nome} já está matriculado nesta turma.",
            )
            return redirect("matriculas:listar_matriculas")

        try:
            matricula = Matricula(
                aluno=aluno,
                turma=turma,
                data_matricula=timezone.now().date(),
                ativa=True,
                status="A",  # Ativa
            )
            matricula.full_clean()  # Valida o modelo
            matricula.save()
            messages.success(
                request,
                f"Matrícula realizada com sucesso para {aluno.nome} na turma {turma.nome}.",
            )
            return redirect("matriculas:listar_matriculas")
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, f"Erro ao realizar matrícula: {str(e)}")

    # Para o método GET, exibir o formulário
    alunos = Aluno.objects.all()
    turmas = Turma.objects.filter(status="A")  # Apenas turmas ativas
    return render(
        request,
        "matriculas/realizar_matricula.html",
        {"alunos": alunos, "turmas": turmas},
    )


@login_required
def cancelar_matricula(request, id):
    """Cancela uma matrícula existente."""
    Matricula = get_model("matriculas", "Matricula")
    matricula = get_object_or_404(Matricula, id=id)

    if request.method == "POST":
        matricula.status = "C"  # Cancelada
        matricula.save()
        messages.success(
            request,
            f"Matrícula de {matricula.aluno.nome} na turma {matricula.turma.nome} cancelada com sucesso.",
        )
        return redirect("matriculas:listar_matriculas")

    return render(
        request, "matriculas/cancelar_matricula.html", {"matricula": matricula}
    )


@login_required
def cancelar_matricula_por_turma_aluno(request, turma_id, aluno_cpf):
    """Cancela uma matrícula identificada pela turma e pelo CPF do aluno."""
    Matricula = get_model("matriculas", "Matricula")
    Aluno = get_model("alunos", "Aluno")
    Turma = get_model("turmas", "Turma")
    
    # Obter os objetos necessários
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    turma = get_object_or_404(Turma, id=turma_id)
    matricula = get_object_or_404(Matricula, aluno=aluno, turma=turma)
    
    if request.method == "POST":
        matricula.status = "C"  # Cancelada
        matricula.save()
        messages.success(
            request,
            f"Matrícula de {aluno.nome} na turma {turma.nome} cancelada com sucesso."
        )
        return redirect("turmas:detalhar_turma", turma_id=turma_id)
    
    # Para requisições GET, exibir página de confirmação
    return render(
        request, 
        "matriculas/cancelar_matricula.html", 
        {
            "matricula": matricula,
            "return_url": reverse("turmas:detalhar_turma", args=[turma_id])
        }
    )


@login_required
def exportar_matriculas(request):
    """Exporta os dados das matrículas para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        
        Matricula = get_model("matriculas", "Matricula")
        matriculas = Matricula.objects.all().select_related('aluno', 'turma', 'turma__curso')
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="matriculas.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "ID",
            "Aluno (CPF)",
            "Aluno (Nome)",
            "Turma",
            "Curso",
            "Data da Matrícula",
            "Status"
        ])
        
        for matricula in matriculas:
            writer.writerow([
                matricula.id,
                matricula.aluno.cpf,
                matricula.aluno.nome,
                matricula.turma.nome,
                matricula.turma.curso.nome if matricula.turma.curso else "",
                matricula.data_matricula,
                matricula.get_status_display()
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar matrículas: {str(e)}")
        return redirect("matriculas:listar_matriculas")

@login_required
def importar_matriculas(request):
    """Importa matrículas de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper
            from django.utils import timezone
            
            Matricula = get_model("matriculas", "Matricula")
            Aluno = get_model("alunos", "Aluno")
            Turma = get_model("turmas", "Turma")
            
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Buscar aluno pelo CPF
                    aluno = None
                    aluno_cpf = row.get("Aluno (CPF)", "").strip()
                    if aluno_cpf:
                        try:
                            aluno = Aluno.objects.get(cpf=aluno_cpf)
                        except Aluno.DoesNotExist:
                            errors.append(f"Aluno não encontrado com CPF: {aluno_cpf}")
                            continue
                    else:
                        errors.append("CPF do aluno não especificado")
                        continue
                    
                    # Buscar turma pelo nome ou ID
                    turma = None
                    turma_nome = row.get("Turma", "").strip()
                    if turma_nome:
                        try:
                            turma = Turma.objects.get(nome=turma_nome)
                        except Turma.DoesNotExist:
                            try:
                                turma = Turma.objects.get(id=turma_nome)
                            except (Turma.DoesNotExist, ValueError):
                                errors.append(f"Turma não encontrada: {turma_nome}")
                                continue
                    else:
                        errors.append("Turma não especificada")
                        continue
                    
                    # Verificar se já existe matrícula
                    if Matricula.objects.filter(aluno=aluno, turma=turma).exists():
                        errors.append(f"O aluno {aluno.nome} já está matriculado na turma {turma.nome}")
                        continue
                    
                    # Processar data da matrícula
                    data_matricula = timezone.now().date()
                    try:
                        if row.get("Data da Matrícula"):
                            data_matricula = timezone.datetime.strptime(
                                row.get("Data da Matrícula"), "%d/%m/%Y"
                            ).date()
                    except ValueError as e:
                        errors.append(f"Erro no formato de data: {str(e)}")
                        continue
                    
                    # Processar status
                    status = "A"  # Ativa por padrão
                    status_texto = row.get("Status", "").strip()
                    if status_texto:
                        status_map = {"Ativa": "A", "Cancelada": "C", "Finalizada": "F"}
                        status = status_map.get(status_texto, "A")
                    
                    # Criar a matrícula
                    matricula = Matricula(
                        aluno=aluno,
                        turma=turma,
                        data_matricula=data_matricula,
                        ativa=(status == "A"),
                        status=status
                    )
                    
                    # Validar o modelo
                    matricula.full_clean()
                    matricula.save()
                    
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(
                    request,
                    f"{count} matrículas importadas com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} matrículas importadas com sucesso!"
                )
            return redirect("matriculas:listar_matriculas")
        except Exception as e:
            messages.error(request, f"Erro ao importar matrículas: {str(e)}")
    
    return render(request, "matriculas/importar_matriculas.html")
