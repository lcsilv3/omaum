from rest_framework import viewsets
from ..models import Aluno
from alunos.serializers import AlunoSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get("q", "")
        if query:
            queryset = queryset.filter(nome__icontains=query)
        return queryset
