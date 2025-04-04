# Código da Funcionalidade: iniciacoes - Parte 3/3
*Gerado automaticamente*



## iniciacoes\tests\test_views_avancado.py

python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time, timedelta
import json

class IniciacaoViewAvancadoTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Criar um usuário de teste e fazer login
        self.usuario = User.objects.create_user(username='usuarioteste', password='12345')
        self.client.login(username='usuarioteste', password='12345')
        
        # Criar vários alunos para testar paginação e filtros
        self.aluno1 = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        
        self.aluno2 = Aluno.objects.create(
            cpf='98765432109',
            nome='Maria Oliveira',
            data_nascimento=date(1992, 5, 15),
            hora_nascimento=time(10, 0),
            email='maria@example.com',
            sexo='F',
            nacionalidade='Brasileira',
            naturalidade='Rio de Janeiro',
            rua='Rua Exemplo',
            numero_imovel='456',
            cidade='Rio de Janeiro',
            estado='RJ',
            bairro='Copacabana',
            cep='22000000',
            nome_primeiro_contato='Pedro Oliveira',
            celular_primeiro_contato='21999999999',
            tipo_relacionamento_primeiro_contato='Pai',
            nome_segundo_contato='Ana Oliveira',
            celular_segundo_contato='21988888888',
            tipo_relacionamento_segundo_contato='Mãe',
            tipo_sanguineo='O',
            fator_rh='-'
        )
        
        # Criar várias iniciações para testar paginação
        data_base = date(2023, 1, 1)
        cursos = ['Yoga', 'Meditação', 'Reiki', 'Tai Chi', 'Chi Kung', 
                 'Aromaterapia', 'Cromoterapia', 'Acupuntura', 'Shiatsu', 
                 'Reflexologia', 'Ayurveda', 'Fitoterapia']
        
        for i, curso in enumerate(cursos):
            aluno = self.aluno1 if i % 2 == 0 else self.aluno2
            Iniciacao.objects.create(
                aluno=aluno,
                nome_curso=curso,
                data_iniciacao=data_base + timedelta(days=i*30),
                observacoes=f"Observação para o curso de {curso}"
            )
    
    def test_paginacao(self):
        response = self.client.get(reverse('iniciacoes:listar_iniciacoes'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 10)  # 10 itens por página
        
        # Testar segunda página
        response = self.client.get(f"{reverse('iniciacoes:listar_iniciacoes')}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 2)  # 2 itens restantes
    
    def test_filtro_aluno(self):
        url = f"{reverse('iniciacoes:listar_iniciacoes')}?aluno={self.aluno1.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas as iniciações do aluno1 estão presentes
        for iniciacao in response.context['page_obj']:
            self.assertEqual(iniciacao.aluno.id, self.aluno1.id)
    
    def test_filtro_curso(self):
        url = f"{reverse('iniciacoes:listar_iniciacoes')}?curso=Yoga"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas as iniciações com "Yoga" no nome do curso estão presentes
        for iniciacao in response.context['page_obj']:
            self.assertIn('Yoga', iniciacao.nome_curso)
    
    def test_filtro_data(self):
        data_inicio = date(2023, 3, 1).strftime('%Y-%m-%d')
        data_fim = date(2023, 6, 30).strftime('%Y-%m-%d')
        url = f"{reverse('iniciacoes:listar_iniciacoes')}?data_inicio={data_inicio}&data_fim={data_fim}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas as iniciações dentro do período estão presentes
        for iniciacao in response.context['page_obj']:
            self.assertTrue(iniciacao.data_iniciacao >= date(2023, 3, 1))
            self.assertTrue(iniciacao.data_iniciacao <= date(2023, 6, 30))
    
    def test_busca_geral(self):
        url = f"{reverse('iniciacoes:listar_iniciacoes')}?search=Reiki"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas as iniciações com "Reiki" no nome do curso estão presentes
        for iniciacao in response.context['page_obj']:
            self.assertIn('Reiki', iniciacao.nome_curso)
    
    def test_criar_iniciacao_duplicada(self):
        # Tentar criar uma iniciação duplicada (mesmo aluno e curso)
        iniciacao_existente = Iniciacao.objects.filter(aluno=self.aluno1).first()
        
        form_data = {
            'aluno': self.aluno1.id,
            'nome_curso': iniciacao_existente.nome_curso,
            'data_iniciacao': '2023-12-01',
            'observacoes': 'Tentativa de duplicação'
        }
        
        response = self.client.post(reverse('iniciacoes:criar_iniciacao'), form_data)
        self.assertEqual(response.status_code, 200)  # Permanece no formulário
        self.assertContains(response, "já possui uma iniciação no curso")



