from rest_framework import serializers
from importlib import import_module
from .utils import (
    get_models,
    get_form_class,
    get_model_class,
    get_turma_model,
    get_aluno_model,
    get_cursos,
    get_turmas,
    get_atividades_academicas,
)
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