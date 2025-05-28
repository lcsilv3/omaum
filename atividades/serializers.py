from rest_framework import serializers
from importlib import import_module

def get_models():
    """Obtém os modelos necessários dinamicamente."""
    atividades_module = import_module("atividades.models")
    cursos_module = import_module("cursos.models")
    turmas_module = import_module("turmas.models")
    
    return {
        'AtividadeAcademica': getattr(atividades_module, "AtividadeAcademica"),
        'Curso': getattr(cursos_module, "Curso"),
        'Turma': getattr(turmas_module, "Turma"),
    }

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_models()['Curso']
        fields = ['id', 'nome']

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_models()['Turma']
        fields = ['id', 'nome']

class AtividadeAcademicaSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    turmas = TurmaSerializer(many=True, read_only=True)
    
    class Meta:
        model = get_models()['AtividadeAcademica']
        fields = ['id', 'nome', 'descricao', 'curso', 'turmas', 'tipo', 'status', 'data_inicio']