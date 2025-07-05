# c:/projetos/omaum/turmas/api_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Turma
from .serializers import TurmaSerializer
from . import services # Importando nosso serviço!
from django.core.exceptions import ValidationError

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all().select_related('curso')
    serializer_class = TurmaSerializer

    # Sobrescrever o método de criação para usar o serviço
    def create(self, request, *args, **kwargs):
        try:
            # Os dados validados pelo serializer são passados para o serviço
            nova_turma = services.criar_turma(request.data)
            serializer = self.get_serializer(nova_turma)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    # Criar uma rota customizada para matricular um aluno
    # Ex: POST /api/turmas/5/matricular/  (com 'aluno_id' no corpo da requisição)
    @action(detail=True, methods=['post'])
    def matricular(self, request, pk=None):
        turma = self.get_object()
        aluno_id = request.data.get('aluno_id')

        if not aluno_id:
            return Response({"error": "O campo 'aluno_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            services.matricular_aluno_em_turma(aluno_id=aluno_id, turma_id=turma.id)
            return Response({"message": "Aluno matriculado com sucesso."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)