from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from .models import PresencaAcademica
from alunos.models import Aluno
from turmas.models import Turma


class PresencaAcademicaTestCase(TestCase):
    def setUp(self):
        # Criar um usuário para os testes
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )

        # Adicionar permissões necessárias ao usuário
        permissions = Permission.objects.filter(
            codename__in=[
                "view_presencaacademica",
                "add_presencaacademica",
                "change_presencaacademica",
                "delete_presencaacademica",
            ]
        )
        self.user.user_permissions.set(permissions)

        # Criar objetos necessários para os testes
        self.aluno = Aluno.objects.create(
            nome="Aluno Teste", cpf="12345678901"
        )
        self.turma = Turma.objects.create(nome="Turma Teste")
        self.presenca = PresencaAcademica.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=timezone.now().date(),
            presente=True,
        )

    def test_listar_presencas_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("presencas:listar_presencas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "presencas/listar_presencas.html")
        self.assertContains(response, self.aluno.nome)

    def test_registrar_presenca_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("presencas:registrar_presenca"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "presencas/registrar_presenca.html")

        # Testar POST
        data = {
            "aluno": self.aluno.id,
            "turma": self.turma.id,
            "data": timezone.now().date(),
            "presente": True,
        }
        response = self.client.post(
            reverse("presencas:registrar_presenca"), data
        )
        self.assertRedirects(response, reverse("presencas:listar_presencas"))
        self.assertEqual(PresencaAcademica.objects.count(), 2)

    def test_editar_presenca_view(self):
        self.client.login(username="testuser", password="12345")
        url = reverse("presencas:editar_presenca", args=[self.presenca.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "presencas/editar_presenca.html")

        # Testar POST
        data = {
            "aluno": self.aluno.id,
            "turma": self.turma.id,
            "data": timezone.now().date(),
            "presente": False,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("presencas:listar_presencas"))
        self.presenca.refresh_from_db()
        self.assertFalse(self.presenca.presente)

    def test_excluir_presenca_view(self):
        self.client.login(username="testuser", password="12345")
        url = reverse("presencas:excluir_presenca", args=[self.presenca.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "presencas/excluir_presenca.html")

        # Testar POST
        response = self.client.post(url)
        self.assertRedirects(response, reverse("presencas:listar_presencas"))
        self.assertEqual(PresencaAcademica.objects.count(), 0)

    def test_detalhar_presenca_view(self):
        self.client.login(username="testuser", password="12345")
        url = reverse("presencas:detalhar_presenca", args=[self.presenca.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "presencas/detalhar_presenca.html")
        self.assertContains(response, self.aluno.nome)

    def test_permissoes_required(self):
        # Criar um usuário sem permissões
        user_sem_permissao = User.objects.create_user(
            username="sempermissao", password="12345"
        )
        self.client.login(username="sempermissao", password="12345")

        # Testar acesso às views
        urls = [
            reverse("presencas:listar_presencas"),
            reverse("presencas:registrar_presenca"),
            reverse("presencas:editar_presenca", args=[self.presenca.id]),
            reverse("presencas:excluir_presenca", args=[self.presenca.id]),
            reverse("presencas:detalhar_presenca", args=[self.presenca.id]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)  # Forbidden
