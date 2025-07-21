#!/usr/bin/env python
import os
import django
from django.test import RequestFactory
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from presencas.views.registro_rapido import RegistroRapidoView

# Simula uma requisição GET para o endpoint
factory = RequestFactory()
request = factory.get('/presencas/ajax/alunos-turma/?turma_id=1')

# Adiciona um usuário fake para passar pelo decorator @login_required
request.user = User.objects.first() or User.objects.create_user('test', 'test@test.com', 'test')

# Testa o endpoint
try:
    response = RegistroRapidoView.obter_alunos_turma_ajax(request)
    print(f'Status Code: {response.status_code}')
    print(f'Content: {response.content.decode()}')
except Exception as e:
    print(f'Erro: {e}')
    import traceback
    traceback.print_exc()
