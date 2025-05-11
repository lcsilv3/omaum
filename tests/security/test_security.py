from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import AtividadeAcademica
from frequencias.models import Frequencia
from notas.models import Avaliacao
from pagamentos.models import Pagamento, TipoPagamento
import datetime

class SecurityTestCase(TestCase):
    """Testes de segurança para os módulos adicionais."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar usuários com diferentes níveis de permissão
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )
        
        self.staff_user = User.objects.create_user(
            username='staff',
            password='staffpassword',
            is_staff=True
        )
        
        self.normal_user = User.objects.create_user(
            username='user',
            password='userpassword'
        )
        
        # Adicionar permissões específicas ao usuário staff
        content_type = ContentType.objects.get_for_model(Aluno)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='view_aluno'
        )
        self.staff_user.user_permissions.add(permission)
        
        # Criar dados de teste
        self.aluno = Aluno.objects.create(
            cpf="12345678900",
            nome="Aluno Teste",
            email="aluno@teste.com",
            data_nascimento="1990-01-01"
        )
        
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        self.atividade = AtividadeAcademica.objects.create(
            nome="Atividade de Teste",
            descricao="Descrição da atividade",
            data_inicio=timezone.now(),
            responsavel="Professor Teste",
            tipo_atividade="aula",
            status="agendada"
        )
        self.atividade.turmas.add(self.turma)
        
        self.frequencia = Frequencia.objects.create(
            atividade=self.atividade,
            data=timezone.now().date(),
            observacoes="Frequência de teste"
        )
        
        self.avaliacao = Avaliacao.objects.create(
            nome="Avaliação de Teste",
            descricao="Descrição da avaliação",
            data=timezone.now().date(),
            peso=1.0,
            turma=self.turma,
            atividade=self.atividade
        )
        
        self.tipo_pagamento = TipoPagamento.objects.create(
            nome="Mensalidade",
            descricao="Pagamento mensal do curso",
            valor_padrao=500.00
        )
        
        self.pagamento = Pagamento.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            tipo_pagamento=self.tipo_pagamento,
            valor=500.00,
            data_vencimento=timezone.now().date() + datetime.timedelta(days=30),
            data_pagamento=None,
            status="pendente",
            forma_pagamento="",
            observacao="Mensalidade de teste"
        )
        
        # Clientes para fazer requisições
        self.admin_client = Client()
        self.staff_client = Client()
        self.user_client = Client()
        self.anonymous_client = Client()
        
        # Fazer login com os usuários
        self.admin_client.login(username='admin', password='adminpassword')
        self.staff_client.login(username='staff', password='staffpassword')
        self.user_client.login(username='user', password='userpassword')
    
    def test_acesso_anonimo_negado(self):
        """Testa se o acesso anônimo é negado para páginas protegidas."""
        urls = [
            reverse('alunos:listar_alunos'),
            reverse('turmas:listar_turmas'),
            reverse('atividades:listar_atividades'),
            reverse('frequencias:listar_frequencias'),
            reverse('notas:listar_avaliacoes'),
            reverse('pagamentos:listar_pagamentos'),
            reverse('alunos:criar_aluno'),
            reverse('frequencias:registrar_frequencia', args=[self.frequencia.id]),
            reverse('notas:lancar_notas', args=[self.avaliacao.id]),
            reverse('pagamentos:registrar_pagamento', args=[self.pagamento.id]),
        ]
        
        for url in urls:
            response = self.anonymous_client.get(url)
            self.assertIn(response.status_code, [302, 403], f"Acesso anônimo não foi negado para {url}")
            
            # Se for redirecionamento, verificar se é para a página de login
            if response.status_code == 302:
                self.assertIn('/accounts/login/', response.url, f"Redirecionamento incorreto para {url}")
    
    def test_acesso_usuario_sem_permissao(self):
        """Testa se o acesso é negado para usuários sem permissão."""
        urls = [
            reverse('alunos:editar_aluno', args=[self.aluno.cpf]),
            reverse('alunos:excluir_aluno', args=[self.aluno.cpf]),
            reverse('frequencias:criar_frequencia'),
            reverse('notas:criar_avaliacao'),
            reverse('pagamentos:criar_pagamento'),
        ]
        
        for url in urls:
            response = self.user_client.get(url)
            self.assertIn(response.status_code, [302, 403], f"Acesso não foi negado para {url}")
    
    def test_acesso_usuario_com_permissao(self):
        """Testa se o acesso é permitido para usuários com permissão."""
        # O usuário staff tem permissão para visualizar alunos
        response = self.staff_client.get(reverse('alunos:listar_alunos'))
        self.assertEqual(response.status_code, 200)
        
        # O usuário admin tem permissão para tudo
        urls = [
            reverse('alunos:listar_alunos'),
            reverse('alunos:criar_aluno'),
            reverse('alunos:editar_aluno', args=[self.aluno.cpf]),
            reverse('frequencias:listar_frequencias'),
            reverse('frequencias:criar_frequencia'),
            reverse('notas:listar_avaliacoes'),
            reverse('notas:criar_avaliacao'),
            reverse('pagamentos:listar_pagamentos'),
            reverse('pagamentos:criar_pagamento'),
        ]
        
        for url in urls:
            response = self.admin_client.get(url)
            self.assertEqual(response.status_code, 200, f"Acesso negado para admin em {url}")
    
    def test_csrf_protection(self):
        """Testa se a proteção CSRF está funcionando."""
        # Tentar enviar um formulário sem o token CSRF
        self.admin_client.handler.enforce_csrf_checks = True
        
        # Tentar criar um aluno sem o token CSRF
        response = self.admin_client.post(reverse('alunos:criar_aluno'), {
            'cpf': '98765432100',
            'nome': 'Aluno Sem CSRF',
            'email': 'aluno_csrf@teste.com',
            'data_nascimento': '1990-01-01'
        })
        
        # Verificar se a requisição foi rejeitada
        self.assertEqual(response.status_code, 403)
        
        # Verificar se o aluno não foi criado
        self.assertFalse(Aluno.objects.filter(cpf='98765432100').exists())
    
    def test_sql_injection_protection(self):
        """Testa se a proteção contra SQL Injection está funcionando."""
        # Tentar fazer uma busca com SQL Injection
        sql_injection_query = "' OR 1=1; --"
        
        response = self.admin_client.get(
            reverse('alunos:listar_alunos') + f"?q={sql_injection_query}"
        )
        
        # Verificar se a resposta foi bem-sucedida (não causou erro)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas os alunos legítimos estão na resposta
        self.assertContains(response, "Aluno Teste")
        self.assertEqual(len(response.context['alunos']), Aluno.objects.count())
    
    def test_xss_protection(self):
        """Testa se a proteção contra XSS está funcionando."""
        # Criar um aluno com script malicioso no nome
        xss_script = '<script>alert("XSS")</script>'
        
        aluno_xss = Aluno.objects.create(
            cpf="11122233344",
            nome=xss_script,
            email="aluno_xss@teste.com",
            data_nascimento="1990-01-01"
        )
        
        # Acessar a página de detalhes do aluno
        response = self.admin_client.get(reverse('alunos:detalhar_aluno', args=[aluno_xss.cpf]))
        
        # Verificar se o script foi escapado
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, xss_script)
        self.assertContains(response, '<script>alert("XSS")</script>')            reverse('atividades:listar_atividades'),