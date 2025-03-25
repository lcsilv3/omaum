from django import forms
import importlib

def criar_form_atividade_academica():
    """
    Cria o formulário para atividades acadêmicas usando importação dinâmica
    para evitar referências circulares.
    """
    class AtividadeAcademicaForm(forms.ModelForm):
        class Meta:
            model = None  # Será definido no __init__
            fields = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')
            
        def __init__(self, *args, **kwargs):
            # Importação dinâmica do modelo
            from .models import AtividadeAcademica
            self.Meta.model = AtividadeAcademica
            super().__init__(*args, **kwargs)
            
            # Importação dinâmica da turma
            turmas_module = importlib.import_module('turmas.models')
            Turma = getattr(turmas_module, 'Turma')
            
            # Configurar queryset
            self.fields['turma'].queryset = Turma.objects.all()
    
    return AtividadeAcademicaForm

def criar_form_atividade_ritualistica():
    """
    Cria o formulário para atividades ritualísticas usando importação dinâmica
    para evitar referências circulares.
    """
    class AtividadeRitualisticaForm(forms.ModelForm):
        todos_alunos = forms.BooleanField(required=False, label="Incluir todos os alunos da turma")
        
        class Meta:
            model = None  # Será definido no __init__
            fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'turma', 'alunos', 'todos_alunos']

        def __init__(self, *args, **kwargs):
            # Importação dinâmica dos modelos
            from .models import AtividadeRitualistica
            self.Meta.model = AtividadeRitualistica
            
            super().__init__(*args, **kwargs)
            
            # Importação dinâmica usando importlib
            turmas_module = importlib.import_module('turmas.models')
            alunos_module = importlib.import_module('alunos.models')
            
            Turma = getattr(turmas_module, 'Turma')
            Aluno = getattr(alunos_module, 'Aluno')
            
            # Configurar os querysets
            self.fields['turma'].queryset = Turma.objects.all()
            self.fields['alunos'].queryset = Aluno.objects.all()
            self.fields['alunos'].widget = forms.CheckboxSelectMultiple()
            self.fields['alunos'].required = False
   
    return AtividadeRitualisticaForm