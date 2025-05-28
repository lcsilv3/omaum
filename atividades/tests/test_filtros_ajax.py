from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class FiltrosAjaxTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="123")
        self.client = Client()
        self.client.login(username="testuser", password="123")

    def test_ajax_turmas_por_curso(self):
        from cursos.models import Curso
        from turmas.models import Turma
        curso = Curso.objects.create(nome="Curso Teste")
        turma = Turma.objects.create(nome="Turma 1", curso=curso)
        url = reverse("atividades:ajax_turmas_por_curso")
        response = self.client.get(url, {"curso_id": curso.id}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Turma 1", response.content.decode())