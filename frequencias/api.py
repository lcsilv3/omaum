from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Frequencia
from .serializers import FrequenciaSerializer

class FrequenciaViewSet(viewsets.ModelViewSet):
    queryset = Frequencia.objects.all()
    serializer_class = FrequenciaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Frequencia.objects.all()
        aluno_id = self.request.query_params.get('aluno')
        turma_id = self.request.query_params.get('turma')
        
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
            
        return queryset
