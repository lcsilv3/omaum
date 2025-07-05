from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Curso
from .serializers import CursoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cursos to be viewed or edited.
    """
    queryset = Curso.objects.all().order_by('id')
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticated]
