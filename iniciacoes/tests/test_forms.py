from django.test import TestCase
from iniciacoes.forms import IniciacaoForm
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoFormTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(
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
        
        # Criar uma iniciação para testar a validação de duplicidade
        self.iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )
    
    def test_form_valido(self):
        # Testando um formulário com dados válidos
        form_data = {
            'aluno': self.aluno.id,
            'nome_curso': 'Curso de Meditação',  # Curso diferente
            'data_iniciacao': date(2023, 11, 1),
            'observacoes': 'Teste de observação'
        }
        form = IniciacaoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalido_curso_duplicado(self):
        # Testando um formulário com curso duplicado para o mesmo aluno
        form_data = {
            'aluno': self.aluno.id,
            'nome_curso': 'Curso de Iniciação',  # Mesmo curso que já existe
            'data_iniciacao': date(2023, 11, 1),
            'observacoes': 'Teste de observação'
        }
        form = IniciacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
    
    def test_form_campos_obrigatorios(self):
        # Testando um formulário sem campos obrigatórios
        form_data = {
            'observacoes': 'Apenas observações'
        }
        form = IniciacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('aluno', form.errors)
        self.assertIn('nome_curso', form.errors)
        self.assertIn('data_iniciacao', form.errors)
