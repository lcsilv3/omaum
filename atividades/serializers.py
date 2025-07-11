"""
Serializers para o app Atividades.
Este módulo contém os serializers para a API REST das atividades.
"""

from rest_framework import serializers
from importlib import import_module
from .models import Atividade, Presenca


def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    try:
        module = import_module(f"{app_name}.models")
        return getattr(module, model_name)
    except (ImportError, AttributeError):
        return None


class CursoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Curso."""
    
    class Meta:
        model = get_model_dynamically('cursos', 'Curso')
        fields = ['id', 'nome', 'descricao']


class TurmaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Turma."""
    
    class Meta:
        model = get_model_dynamically('turmas', 'Turma')
        fields = ['id', 'nome', 'curso']


class AtividadeSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Atividade."""
    
    curso = CursoSerializer(read_only=True)
    turmas = TurmaSerializer(many=True, read_only=True)
    curso_id = serializers.IntegerField(write_only=True, required=False)
    turmas_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Atividade
        fields = [
            'id', 'nome', 'descricao', 'tipo_atividade', 'data_inicio',
            'data_fim', 'hora_inicio', 'hora_fim', 'local', 'responsavel',
            'status', 'ativo', 'convocacao', 'curso', 'turmas',
            'curso_id', 'turmas_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """Cria uma nova atividade."""
        turmas_ids = validated_data.pop('turmas_ids', [])
        atividade = Atividade.objects.create(**validated_data)
        
        if turmas_ids:
            Turma = get_model_dynamically('turmas', 'Turma')
            turmas = Turma.objects.filter(id__in=turmas_ids)
            atividade.turmas.set(turmas)
        
        return atividade
    
    def update(self, instance, validated_data):
        """Atualiza uma atividade."""
        turmas_ids = validated_data.pop('turmas_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if turmas_ids is not None:
            Turma = get_model_dynamically('turmas', 'Turma')
            turmas = Turma.objects.filter(id__in=turmas_ids)
            instance.turmas.set(turmas)
        
        return instance


class PresencaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Presenca."""
    
    aluno = serializers.StringRelatedField(read_only=True)
    atividade = serializers.StringRelatedField(read_only=True)
    turma = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Presenca
        fields = [
            'id', 'aluno', 'atividade', 'turma', 'data', 'presente',
            'registrado_por', 'data_registro'
        ]
        read_only_fields = ['data_registro']


# Serializers para criação/atualização com IDs
class AtividadeCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de atividade."""
    
    class Meta:
        model = Atividade
        fields = [
            'nome', 'descricao', 'tipo_atividade', 'data_inicio',
            'data_fim', 'hora_inicio', 'hora_fim', 'local', 'responsavel',
            'status', 'ativo', 'convocacao', 'curso'
        ]


class PresencaCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de presença."""
    
    class Meta:
        model = Presenca
        fields = [
            'aluno', 'atividade', 'turma', 'data', 'presente',
            'registrado_por'
        ]