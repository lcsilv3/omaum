# Função duplicada - removida para evitar F811
# def editar_pagamento(request, id):
#     pagamento = get_object_or_404(Pagamento, id=id)
#     if request.method == 'POST':
#         form = PagamentoForm(request.POST, request.FILES, instance=pagamento)
#         if form.is_valid():
#             form.save()
#             # redirecione conforme sua lógica
#         else:
#             # Se inválido, o form já vem preenchido com os dados e erros
#             pass
#     else:
#         form = PagamentoForm(instance=pagamento)
#     return render(request, 'pagamentos/editar_pagamento.html', {
#         'form': form,
#         'pagamento': pagamento,
#     })
