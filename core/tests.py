from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser

from core.models import ConfiguracaoSistema, LogAtividade
from core.utils import (
    registrar_log,
    garantir_configuracao_sistema,
)
from core.middleware import manutencao_middleware


class ConfiguracaoSistemaTests(TestCase):
    """Testes para o modelo ConfiguracaoSistema"""

    def test_criacao_configuracao(self):
        """Testa a criação de uma configuração do sistema"""
        config = ConfiguracaoSistema.objects.create(
            nome_sistema="Sistema de Teste",
            versao="1.0.0",
            manutencao_ativa=False,
        )
        self.assertEqual(config.nome_sistema, "Sistema de Teste")
        self.assertEqual(config.versao, "1.0.0")
        self.assertFalse(config.manutencao_ativa)

    def test_str_representation(self):
        """Testa a representação string do modelo"""
        config = ConfiguracaoSistema.objects.create(
            nome_sistema="Sistema de Teste", versao="1.0.0"
        )
        self.assertEqual(str(config), "Sistema de Teste v1.0.0")


class LogAtividadeTests(TestCase):
    """Testes para o modelo LogAtividade"""

    def test_criacao_log(self):
        """Testa a criação de um log de atividade"""
        log = LogAtividade.objects.create(
            usuario="usuario_teste",
            acao="Ação de teste",
            tipo="INFO",
            detalhes="Detalhes da ação de teste",
        )
        self.assertEqual(log.usuario, "usuario_teste")
        self.assertEqual(log.acao, "Ação de teste")
        self.assertEqual(log.tipo, "INFO")
        self.assertEqual(log.detalhes, "Detalhes da ação de teste")

    def test_str_representation(self):
        """Testa a representação string do modelo"""
        log = LogAtividade.objects.create(
            usuario="usuario_teste", acao="Ação de teste", tipo="INFO"
        )
        self.assertEqual(str(log), "INFO: Ação de teste por usuario_teste")

    def test_ordering(self):
        """Testa a ordenação dos logs (mais recentes primeiro)"""
        from django.utils import timezone
        import datetime

        # Criar o primeiro log com uma data específica
        data_antiga = timezone.now() - datetime.timedelta(minutes=5)
        LogAtividade.objects.create(
            usuario="user1",
            acao="acao1",
            data=data_antiga,  # Definir uma data mais antiga
        )

        # Criar o segundo log com a data atual (mais recente)
        log2 = LogAtividade.objects.create(
            usuario="user2",
            acao="acao2",
            # data padrão será timezone.now()
        )

        # Buscar todos os logs (devem estar ordenados por data decrescente)
        logs = LogAtividade.objects.all()

        # Verificar se o log2 (mais recente) aparece primeiro
        self.assertEqual(logs[0], log2)


class UtilsTests(TestCase):
    """Testes para as funções utilitárias"""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_registrar_log(self):
        """Testa o registro de logs"""
        request = self.factory.get("/")
        request.user = self.user

        # Registra um log
        registrar_log(request, "Teste de log", "INFO", "Detalhes do teste")

        # Verifica se o log foi criado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "testuser")
        self.assertEqual(log.acao, "Teste de log")
        self.assertEqual(log.tipo, "INFO")
        self.assertEqual(log.detalhes, "Detalhes do teste")

    def test_registrar_log_anonimo(self):
        """Testa o registro de logs para usuários anônimos"""
        request = self.factory.get("/")
        request.user = AnonymousUser()

        # Registra um log
        registrar_log(request, "Teste de log anônimo")

        # Verifica se o log foi criado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "Anônimo")
        self.assertEqual(log.acao, "Teste de log anônimo")

    def test_garantir_configuracao_sistema(self):
        """Testa a função que garante a existência de uma configuração"""
        # Inicialmente não deve haver configurações
        self.assertEqual(ConfiguracaoSistema.objects.count(), 0)

        # Chama a função para garantir uma configuração
        config = garantir_configuracao_sistema()

        # Deve haver exatamente uma configuração
        self.assertEqual(ConfiguracaoSistema.objects.count(), 1)
        self.assertEqual(config.nome_sistema, "Sistema de Gestão de Iniciados da OmAum")

        # Chamar novamente não deve criar outra configuração
        config2 = garantir_configuracao_sistema()
        self.assertEqual(ConfiguracaoSistema.objects.count(), 1)
        self.assertEqual(config, config2)


class ViewsTests(TestCase):
    """Testes para as views"""

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Cria um usuário normal
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

        # Cria um usuário staff
        self.staff_user = User.objects.create_user(
            username="staffuser",
            email="staff@example.com",
            password="staffpassword",
            is_staff=True,
        )

        # Garante que existe uma configuração
        self.config = garantir_configuracao_sistema()

    def test_pagina_inicial(self):
        """Testa a página inicial"""
        response = self.client.get(reverse("core:pagina_inicial"))
        self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "home.html")

    def test_entrar_get(self):
        """Testa a página de login (GET)"""
        response = self.client.get(reverse("core:entrar"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/login.html")

    def test_entrar_post_sucesso(self):
        """Testa o login com sucesso"""
        response = self.client.post(
            reverse("core:entrar"),
            {"username": "testuser", "password": "testpassword"},
        )
        self.assertRedirects(response, reverse("core:pagina_inicial"))

        # Verifica se o log foi registrado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "testuser")
        self.assertEqual(log.acao, "Login realizado com sucesso")

    def test_entrar_post_falha(self):
        """Testa o login com credenciais inválidas"""
        response = self.client.post(
            reverse("core:entrar"),
            {"username": "testuser", "password": "senhaerrada"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/login.html")

    def test_sair(self):
        """Testa o logout"""
        # Primeiro faz login
        self.client.login(username="testuser", password="testpassword")

        # Depois faz logout (POST é necessário para LogoutView)
        response = self.client.post(reverse("core:sair"))
        self.assertRedirects(response, "/")

        # Verifica se o usuário está deslogado
        response = self.client.get(reverse("core:painel_controle"))
        self.assertEqual(
            response.status_code, 302
        )  # 302 é o código para redirecionamento

    def test_painel_controle_sem_permissao(self):
        """Testa acesso ao painel de controle sem permissão"""
        # Usuário não autenticado deve ser redirecionado para login
        response = self.client.get(reverse("core:painel_controle"))
        self.assertEqual(
            response.status_code, 302
        )  # 302 é o código para redirecionamento

        # Usuário normal não deve ter acesso
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("core:painel_controle"))
        self.assertRedirects(response, reverse("core:pagina_inicial"))

    def test_painel_controle_com_permissao(self):
        """Testa acesso ao painel de controle com permissão"""
        self.client.login(username="staffuser", password="staffpassword")
        response = self.client.get(reverse("core:painel_controle"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/painel_controle.html")

    def test_atualizar_configuracao_sem_permissao(self):
        """Testa atualização de configuração sem permissão"""
        # Usuário não autenticado deve ser redirecionado para login
        response = self.client.get(reverse("core:atualizar_configuracao"))
        self.assertEqual(
            response.status_code, 302
        )  # 302 é o código para redirecionamento

        # Usuário normal não deve ter acesso
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("core:atualizar_configuracao"))
        self.assertRedirects(response, reverse("core:pagina_inicial"))

    def test_atualizar_configuracao_get(self):
        """Testa a página de atualização de configuração (GET)"""
        self.client.login(username="staffuser", password="staffpassword")
        response = self.client.get(reverse("core:atualizar_configuracao"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/atualizar_configuracao.html")

    def test_atualizar_configuracao_post(self):
        """Testa a atualização de configuração (POST)"""
        self.client.login(username="staffuser", password="staffpassword")
        response = self.client.post(
            reverse("core:atualizar_configuracao"),
            {
                "nome_sistema": "Sistema Atualizado",
                "versao": "2.0.0",
                "manutencao_ativa": "on",
                "mensagem_manutencao": "Mensagem de manutenção atualizada",
            },
        )
        self.assertRedirects(response, reverse("core:painel_controle"))

        # Verifica se a configuração foi atualizada
        config = ConfiguracaoSistema.objects.get(pk=1)
        self.assertEqual(config.nome_sistema, "Sistema Atualizado")
        self.assertEqual(config.versao, "2.0.0")
        self.assertTrue(config.manutencao_ativa)
        self.assertEqual(
            config.mensagem_manutencao, "Mensagem de manutenção atualizada"
        )

        # Verifica se o log foi registrado
        log = LogAtividade.objects.last()
        self.assertEqual(log.acao, "Configurações do sistema atualizadas")


class MiddlewareTests(TestCase):
    """Testes para o middleware de manutenção"""

    def setUp(self):
        self.factory = RequestFactory()

        # Cria um usuário normal
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

        # Cria um usuário staff
        self.staff_user = User.objects.create_user(
            username="staffuser",
            email="staff@example.com",
            password="staffpassword",
            is_staff=True,
        )

        # Garante que existe uma configuração
        self.config = garantir_configuracao_sistema()

        # Define uma função simples para o middleware chamar
        def get_response(request):
            return "response"

        self.middleware = manutencao_middleware(get_response)

    def test_middleware_sem_manutencao(self):
        """Testa o middleware quando o sistema não está em manutenção"""
        self.config.manutencao_ativa = False
        self.config.save()

        request = self.factory.get("/")
        request.user = self.user

        response = self.middleware(request)
        self.assertEqual(response, "response")
