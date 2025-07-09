"""
Serializers para o app Atividades.
Este módulo contém os serializers para a API REST das atividades.
"""

from rest_framework import serializers
from importlib import import_module
from .models import AtividadeAcademica, AtividadeRitualistica


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


class AtividadeAcademicaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo AtividadeAcademica."""
    
    curso = CursoSerializer(read_only=True)
    turmas = TurmaSerializer(many=True, read_only=True)
    curso_id = serializers.IntegerField(write_only=True, required=False)
    turmas_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = AtividadeAcademica
        fields = [
            'id', 'nome', 'descricao', 'tipo_atividade', 'data_inicio',
            'data_fim', 'hora_inicio', 'hora_fim', 'local', 'responsavel',
            'status', 'ativo', 'convocacao', 'curso', 'turmas',
            'curso_id', 'turmas_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """Cria uma nova atividade acadêmica."""
        turmas_ids = validated_data.pop('turmas_ids', [])
        atividade = AtividadeAcademica.objects.create(**validated_data)
        
        if turmas_ids:
            Turma = get_model_dynamically('turmas', 'Turma')
            turmas = Turma.objects.filter(id__in=turmas_ids)
            atividade.turmas.set(turmas)
        
        return atividade
    
    def update(self, instance, validated_data):
        """Atualiza uma atividade acadêmica."""
        turmas_ids = validated_data.pop('turmas_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if turmas_ids is not None:
            Turma = get_model_dynamically('turmas', 'Turma')
            turmas = Turma.objects.filter(id__in=turmas_ids)
            instance.turmas.set(turmas)
        
        return instance


class AtividadeRitualisticaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo AtividadeRitualistica."""
    
    turma = TurmaSerializer(read_only=True)
    participantes = serializers.StringRelatedField(many=True, read_only=True)
    turma_id = serializers.IntegerField(write_only=True, required=False)
    participantes_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = AtividadeRitualistica
        fields = [
            'id', 'nome', 'descricao', 'data', 'hora_inicio', 'hora_fim',
            'local', 'responsavel', 'status', 'convocacao', 'ativo',
            'turma', 'participantes', 'turma_id', 'participantes_ids',
            'duracao_prevista'
        ]
    
    def create(self, validated_data):
        """Cria uma nova atividade ritualística."""
        participantes_ids = validated_data.pop('participantes_ids', [])
        atividade = AtividadeRitualistica.objects.create(**validated_data)
        
        if participantes_ids:
            Aluno = get_model_dynamically('alunos', 'Aluno')
            participantes = Aluno.objects.filter(cpf__in=participantes_ids)
            atividade.participantes.set(participantes)
        
        return atividade
    
    def update(self, instance, validated_data):
        """Atualiza uma atividade ritualística."""
        participantes_ids = validated_data.pop('participantes_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if participantes_ids is not None:
            Aluno = get_model_dynamically('alunos', 'Aluno')
            participantes = Aluno.objects.filter(cpf__in=participantes_ids)
            instance.participantes.set(participantes)
        
        return instance


class PresencaAcademicaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo PresencaAcademica."""
    
    aluno = serializers.StringRelatedField(read_only=True)
    atividade = serializers.StringRelatedField(read_only=True)
    turma = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = get_model_dynamically('atividades', 'PresencaAcademica')
        fields = [
            'id', 'aluno', 'atividade', 'turma', 'data', 'presente',
            'registrado_por', 'data_registro'
        ]
        read_only_fields = ['data_registro']


class PresencaRitualisticaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo PresencaRitualistica."""
    
    aluno = serializers.StringRelatedField(read_only=True)
    atividade = serializers.StringRelatedField(read_only=True)
    turma = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = get_model_dynamically('atividades', 'PresencaRitualistica')
        fields = [
            'id', 'aluno', 'atividade', 'turma', 'data', 'presente',
            'registrado_por', 'data_registro'
        ]
        read_only_fields = ['data_registro']