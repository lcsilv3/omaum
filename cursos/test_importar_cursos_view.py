from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from cursos.models import Curso


@override_settings(ALLOWED_HOSTS=["testserver"])
class ImportarCursosViewTest(TestCase):
    """Garante que a view de importação consome a planilha padronizada."""

    def setUp(self) -> None:
        User = get_user_model()
        User.objects.create_user(
            username="import_view",
            email="import@example.com",
            password="12345",
        )
        assert self.client.login(username="import_view", password="12345")

    def test_importar_planilha_csv(self):
        caminho = Path("docs/Planilha de Cursos.csv")
        arquivo = SimpleUploadedFile(
            caminho.name,
            caminho.read_bytes(),
            content_type="text/csv",
        )

        resposta = self.client.post(
            reverse("cursos:importar_cursos"),
            {"arquivo": arquivo},
            follow=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertRedirects(resposta, reverse("cursos:listar_cursos"))
        mensagens = [
            mensagem.message for mensagem in get_messages(resposta.wsgi_request)
        ]
        self.assertTrue(any("processados" in mensagem for mensagem in mensagens))
        self.assertEqual(Curso.objects.count(), 3)
