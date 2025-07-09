from rest_framework import serializers
from .models import Presenca


class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = '__all__'
