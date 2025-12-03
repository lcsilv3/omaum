"""Smoke tests para o fluxo de edição em lote via AJAX."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestEdicaoLoteAjaxSmoke:
    """Garantias mínimas do endpoint usado no checklist diário."""

    endpoint_name = "presencas:editar_lote_dias_atividades_ajax"

    def test_redireciona_sem_autenticacao(self, client):
        url = reverse(self.endpoint_name)
        response = client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response.status_code == 302

    def test_responde_json_para_usuario_logado(self, client, django_user_model):
        usuario = django_user_model.objects.create_user(
            username="smoke",
            email="smoke@example.com",
            password="senha-super-segura",
        )
        client.force_login(usuario)

        url = reverse(self.endpoint_name)
        response = client.get(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        assert response.status_code == 501
        payload = response.json()
        assert payload["success"] is False
        assert "Fluxo avançado" in payload["message"]
