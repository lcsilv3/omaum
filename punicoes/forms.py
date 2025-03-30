from django import forms
import importlib

# Importando modelos usando importlib para evitar importações circulares
def get_model(app_name, model_name):
    module = importlib.import_module(f"{app_name}.models")
    return getattr(module, model_name)

class PunicaoForm(forms.ModelForm):
    class Meta:
        model = get_model('punicoes', 'Punicao')
        fields = ['aluno', 'tipo_punicao', 'descricao', 'data_aplicacao', 'data_termino', 'status', 'observacoes']
        widgets = {
            'data_aplicacao': forms.DateInput(attrs={'type': 'date'}),
            'data_termino': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

class TipoPunicaoForm(forms.ModelForm):
    class Meta:
        model = get_model('punicoes', 'TipoPunicao')
        fields = ['nome', 'descricao', 'gravidade']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }