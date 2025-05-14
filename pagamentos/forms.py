from django import forms
from django.utils import timezone
from .models import Pagamento
from alunos.models import Aluno


class PagamentoForm(forms.ModelForm):
    """
    Formulário para criação e edição de pagamentos.
    """
    
    class Meta:
        model = Pagamento
        fields = ['aluno', 'observacoes', 'valor', 'data_vencimento', 'status', 
                 'data_pagamento', 'valor_pago']
        
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control select2'}),
            'observacoes': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '255'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_pago': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Definir valor padrão para data_vencimento (30 dias a partir de hoje)
        if not self.instance.pk:  # Se for um novo pagamento
            self.initial['data_vencimento'] = (timezone.now().date() + 
                                              timezone.timedelta(days=30)).strftime('%Y-%m-%d')
        else:  # Se for edição de um pagamento existente
            # Garantir que as datas estejam no formato correto para o input type="date"
            if self.instance.data_vencimento:
                self.initial['data_vencimento'] = self.instance.data_vencimento.strftime('%Y-%m-%d')
            
            if self.instance.data_pagamento:
                self.initial['data_pagamento'] = self.instance.data_pagamento.strftime('%Y-%m-%d')
        
        # Tornar os campos data_pagamento e valor_pago não obrigatórios
        self.fields['data_pagamento'].required = False
        self.fields['valor_pago'].required = False    
    def clean(self):
        cleaned_data = super().clean()
        
        # Garantir que data_vencimento tenha um valor
        data_vencimento = cleaned_data.get('data_vencimento')
        if not data_vencimento:
            cleaned_data['data_vencimento'] = timezone.now().date() + timezone.timedelta(days=30)
            self.instance.data_vencimento = cleaned_data['data_vencimento']
        
        # Validar campos quando o status for PAGO
        status = cleaned_data.get('status')
        if status == 'PAGO':
            data_pagamento = cleaned_data.get('data_pagamento')
            valor_pago = cleaned_data.get('valor_pago')
            
            if not data_pagamento:
                cleaned_data['data_pagamento'] = timezone.now().date()
                self.instance.data_pagamento = cleaned_data['data_pagamento']
            
            if not valor_pago:
                valor = cleaned_data.get('valor')
                if valor:
                    cleaned_data['valor_pago'] = valor
                    self.instance.valor_pago = valor
        
        return cleaned_data
        return cleaned_data