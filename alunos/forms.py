from django import forms
from core.models import Aluno
from django.core.exceptions import ValidationError

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'curso']  # Add other fields as needed

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if len(matricula) != 8:
            raise ValidationError("A matrícula deve ter 8 dígitos.")
        return matricula

    def clean(self):
        cleaned_data = super().clean()
        # Add any cross-field validations here
        return cleaned_data

class ImportForm(forms.Form):
    file = forms.FileField()

