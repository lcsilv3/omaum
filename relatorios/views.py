from django.shortcuts import render, get_object_or_404, redirect
from .models import Relatorio
from .forms import RelatorioForm
from django.contrib.auth.decorators import login_required


@login_required
def listar_relatorios(request):
    """Lista todos os relatórios disponíveis."""
    relatorios = Relatorio.objects.all()
    return render(
        request,
        "relatorios/index.html",
        {"relatorios": relatorios},
    )


@login_required
def detalhar_relatorio(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    return render(
        request, "relatorios/detalhar_relatorio.html", {"relatorio": relatorio}
    )


@login_required
def criar_relatorio(request):
    if request.method == "POST":
        form = RelatorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("relatorios:listar_relatorios")
    else:
        form = RelatorioForm()
    return render(request, "relatorios/form_relatorio.html", {"form": form})


@login_required
def editar_relatorio(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    if request.method == "POST":
        form = RelatorioForm(request.POST, instance=relatorio)
        if form.is_valid():
            form.save()
            return redirect("relatorios:listar_relatorios")
    else:
        form = RelatorioForm(instance=relatorio)
    return render(request, "relatorios/form_relatorio.html", {"form": form})


@login_required
def excluir_relatorio(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    if request.method == "POST":
        relatorio.delete()
        return redirect("relatorios:listar_relatorios")
    return render(
        request, "relatorios/confirmar_exclusao.html", {"relatorio": relatorio}
    )


@login_required
def relatorio_alunos(request):
    # Logic to generate the student report
    return render(request, "relatorios/relatorio_alunos.html")


@login_required
def relatorio_presencas(request):
    # Logic to generate the attendance report
    return render(request, "relatorios/relatorio_presencas.html")


@login_required
def relatorio_punicoes(request):
    # Logic to generate the punishment report
    return render(request, "relatorios/relatorio_punicoes.html")


@login_required
def relatorio_alunos_pdf(request):
    # Logic to generate the PDF report for students
    # This might involve rendering a template to PDF or using a library like ReportLab
    return render(request, "relatorios/relatorio_alunos_pdf.html")
