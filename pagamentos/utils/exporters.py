"""
Funções para exportação de dados em diferentes formatos.
"""
import io
import csv
import logging
from django.http import HttpResponse
import xlsxwriter

logger = logging.getLogger(__name__)

def generate_pdf(html_content, filename="pagamentos.pdf"):
    """
    Gera um arquivo PDF a partir de conteúdo HTML.
    (Implementação real depende de biblioteca como WeasyPrint/xhtml2pdf)
    """
    try:
        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {str(e)}")
        return HttpResponse(f"Erro ao gerar PDF: {str(e)}", status=500)

def generate_csv(pagamentos):
    """
    Gera um arquivo CSV com os pagamentos.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagamentos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Aluno', 'CPF', 'Valor', 'Data de Vencimento', 'Status', 'Data de Pagamento', 'Método de Pagamento', 'Observações'])
    for pagamento in pagamentos:
        writer.writerow([
            pagamento.aluno.nome,
            pagamento.aluno.cpf,
            pagamento.valor,
            pagamento.data_vencimento.strftime('%d/%m/%Y'),
            pagamento.get_status_display(),
            pagamento.data_pagamento.strftime('%d/%m/%Y') if pagamento.data_pagamento else '-',
            pagamento.get_metodo_pagamento_display() if hasattr(pagamento, 'get_metodo_pagamento_display') else '-',
            pagamento.observacoes,
        ])
    return response

def generate_excel(pagamentos):
    """
    Gera um arquivo Excel com os pagamentos.
    """
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#F7F7F7',
        'border': 1
    })
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    money_format = workbook.add_format({'num_format': 'R$ #,##0.00'})
    headers = ['Aluno', 'CPF', 'Valor', 'Data de Vencimento', 'Status', 'Data de Pagamento', 'Método de Pagamento', 'Observações']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    for row, pagamento in enumerate(pagamentos, start=1):
        worksheet.write(row, 0, pagamento.aluno.nome)
        worksheet.write(row, 1, pagamento.aluno.cpf)
        worksheet.write(row, 2, pagamento.valor, money_format)
        worksheet.write(row, 3, pagamento.data_vencimento, date_format)
        worksheet.write(row, 4, pagamento.get_status_display())
        worksheet.write(row, 5, pagamento.data_pagamento if pagamento.data_pagamento else '-', date_format if pagamento.data_pagamento else None)
        worksheet.write(row, 6, pagamento.get_metodo_pagamento_display() if hasattr(pagamento, 'get_metodo_pagamento_display') else '-')
        worksheet.write(row, 7, pagamento.observacoes)
    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 1, 15)
    worksheet.set_column(2, 2, 12)
    worksheet.set_column(3, 3, 18)
    worksheet.set_column(4, 4, 15)
    worksheet.set_column(5, 5, 18)
    worksheet.set_column(6, 6, 20)
    worksheet.set_column(7, 7, 40)
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="pagamentos.xlsx"'
    return response
