"""
Serializadores para a API de pagamentos.
"""
from rest_framework import serializers
from ..views.base import get_pagamento_model, get_aluno_model

Pagamento = get_pagamento_model()
Aluno = get_aluno_model()

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['cpf', 'nome', 'numero_iniciatico', 'email']

class PagamentoSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    metodo_pagamento_display = serializers.CharField(source='get_metodo_pagamento_display', read_only=True)
    
    class Meta:
        model = Pagamento
        fields = [
            'id', 'aluno', 'valor', 'data_vencimento', 'status', 'status_display',
            'observacoes', 'data_pagamento', 'valor_pago', 'metodo_pagamento',
            'metodo_pagamento_display', 'created_at', 'updated_at'
        ]