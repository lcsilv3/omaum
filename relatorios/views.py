from django.shortcuts import render
from django.http import HttpResponse
from alunos.models import Aluno  # Update the import to use the correct app
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def relatorio_alunos(request):
    alunos = Aluno.objects.all()
    context = {
        'alunos': alunos,
    }
    return render(request, 'relatorios/relatorio_alunos.html', context)

def relatorio_alunos_pdf(request):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 750, "Relatório de Alunos")

    alunos = Aluno.objects.all()
    y = 700
    for aluno in alunos:
        p.drawString(100, y, f"{aluno.nome} - {aluno.cpf}")
        y -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
