# c:/projetos/omaum/turmas/serializers.py
from rest_framework import serializers
from .models import Turma


class TurmaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Turma, otimizado para legibilidade e performance.
    """

    curso = serializers.SerializerMethodField()
    vagas_preenchidas = serializers.IntegerField(
        source="matriculas.count", read_only=True
    )

    class Meta:
        model = Turma
        fields = [
            "id",
            "nome",
            "curso",
            "data_inicio_ativ",
            "data_termino_atividades",
            "vagas",
            "vagas_preenchidas",
            "status",
        ]
        read_only_fields = ["status"]

    def get_curso(self, obj):
        """Carrega dinamicamente o CursoSerializer para evitar importação circular."""
        from cursos.serializers import CursoSerializer
        return CursoSerializer(obj.curso).data