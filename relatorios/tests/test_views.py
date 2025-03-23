from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from alunos.models import Aluno
from presencas.models import PresencaAcademica
from punicoes.models import Punicao
from datetime import date, time, timedelta

class RelatorioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Criar usuário de teste com permissões
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Adicionar permissões necessárias
        content_type = ContentType.objects.get_for_model(Aluno)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='view_aluno'
        )
        self.user.user_permissions.add(permission)
        
        content_type = ContentType.objects.get_for_model(PresencaAcademica)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='view_presencaacademica'
        )
        self.user.user_permissions.add(permission)
        
        content_type = ContentType.objects.get_for_model(Punicao)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='view_punicao'
        )
        self.user.user_permissions.add(permission)
        
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Criar aluno de teste
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='Maria Oliveira',
            data_nascimento=date(1985, 5, 15),
            hora_nascimento=time(14, 30),
            email='maria@example.com',
            sexo='F',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='João Oliveira',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Pai',
            nome_segundo_contato='Ana Oliveira',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Mãe',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        
        # Criar dados de teste para presenças
        self.presenca = PresencaAcademica.objects.create(
            aluno=self.aluno,
            data=date.today(),
            presente=True
        )
        
        # Criar dados de teste para punições
        self.punicao = Punicao.objects.create(
            aluno=self.aluno,
            tipo_punicao='Advertência',
            data=date.today(),
            descricao='Teste de punição'
        )

    def test_relatorio_alunos(self):
        response = self.client.get(reverse('relatorio_alunos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')
        
        # Testar filtros
        response = self.client.get(f"{reverse('relatorio_alunos')}?nome=Maria")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')
        
        response = self.client.get(f"{reverse('relatorio_alunos')}?nome=Inexistente")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Maria Oliveira')

    def test_relatorio_alunos_pdf(self):
        response = self.client.get(reverse('relatorio_alunos_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Testar com filtros
        response = self.client.get(f"{reverse('relatorio_alunos_pdf')}?nome=Maria")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_relatorio_presencas(self):
        response = self.client.get(reverse('relatorio_presencas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')
        
        # Testar filtros
        response = self.client.get(f"{reverse('relatorio_presencas')}?aluno={self.aluno.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')
        
        # Testar filtro de data
        data_hoje = date.today().strftime('%Y-%m-%d')
        response = self.client.get(f"{reverse('relatorio_presencas')}?data_inicio={data_hoje}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')

    def test_relatorio_presencas_pdf(self):
        response = self.client.get(reverse('relatorio_presencas_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Testar com filtros
        response = self.client.get(f"{reverse('relatorio_presencas_pdf')}?aluno={self.aluno.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_relatorio_punicoes(self):
        response = self.client.get(reverse('relatorio_punicoes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')
        self.assertContains(response, 'Advertência')
        
        # Testar filtros
        response = self.client.get(f"{reverse('relatorio_punicoes')}?aluno={self.aluno.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')
        
        response = self.client.get(f"{reverse('relatorio_punicoes')}?tipo_punicao=Advertência")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')

    def test_relatorio_punicoes_pdf(self):
        response = self.client.get(reverse('relatorio_punicoes_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # Testar com filtros
        response = self.client.get(f"{reverse('relatorio_punicoes_pdf')}?aluno={self.aluno.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        
        response = self.client.get(f"{reverse('relatorio_punicoes_pdf')}?tipo_punicao=Advertência")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')