"""Serializers para o aplicativo Matriculas."""

from rest_framework import serializers
from matriculas.models import Matricula


class MatriculaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Matricula."""

    class Meta:
        """
        Classe Meta para definir o modelo e os campos a serem serializados.

        Atributos:
            model: Define o modelo associado ao serializer.
            fields: Especifica que todos os campos do modelo
                serão serializados.
        """

        model = Matricula
        fields = "__all__"
