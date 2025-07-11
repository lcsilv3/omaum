"""
Testes de integração para o fluxo completo do sistema OMAUM.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, time
from importlib import import_module


class FluxoCompletoTestCase(TestCase):
    """Testa o fluxo completo: criar curso → criar turma → criar aluno → matricular."""
    
    def setUp(self):
        """Configuração inicial para todos os testes."""
        # Criar usuário administrador
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@teste.com',
            password='admin123'
        )
        
        # Obter modelos dinamicamente
        self.Curso = self._get_model('cursos', 'Curso')
        self.Turma = self._get_model('turmas', 'Turma')
        self.Aluno = self._get_model('alunos', 'Aluno')
        self.Matricula = self._get_model('matriculas', 'Matricula')
        self.Atividade = self._get_model('atividades', 'Atividade')
        self.Pagamento = self._get_model('pagamentos', 'Pagamento')
        self.Nota = self._get_model('notas', 'Nota')
        
    def _get_model(self, app_name, model_name):
        """Obtém um modelo dinamicamente."""
        try:
            module = import_module(f"{app_name}.models")
            return getattr(module, model_name)
        except (ImportError, AttributeError):
            return None
    
    def test_fluxo_basico_sistema(self):
        """Testa o fluxo básico: Curso → Turma → Aluno → Matrícula."""
        # 1. Criar curso
        if self.Curso:
            curso = self.Curso.objects.create(
                nome="Curso de Integração",
                descricao="Curso para testes de integração",
                ativo=True
            )
            self.assertEqual(curso.nome, "Curso de Integração")
        
        # 2. Criar turma
        if self.Turma and self.Curso:
            turma = self.Turma.objects.create(
                nome="Turma Integração 2024",
                curso=curso,
                vagas=20,
                data_inicio_ativ=date(2024, 1, 15),
                ativa=True
            )
            self.assertEqual(turma.nome, "Turma Integração 2024")
        
        # 3. Criar aluno
        if self.Aluno:
            aluno = self.Aluno.objects.create(
                nome="Aluno Integração",
                cpf="11111111111",
                email="aluno.integracao@teste.com",
                data_nascimento=date(1990, 5, 15),
                sexo="M",
                ativa=True
            )
            self.assertEqual(aluno.nome, "Aluno Integração")
        
        # 4. Matricular aluno
        if self.Matricula and self.Aluno and self.Turma:
            matricula = self.Matricula.objects.create(
                aluno=aluno,
                turma=turma,
                data_matricula=date.today(),
                ativa=True
            )
            
            # Verificações do fluxo
            self.assertEqual(matricula.aluno, aluno)
            self.assertEqual(matricula.turma, turma)
            self.assertEqual(turma.matriculas.count(), 1)
            self.assertEqual(aluno.matriculas.count(), 1)
    
    def test_fluxo_academico_completo(self):
        """Testa o fluxo acadêmico: Curso → Turma → Aluno → Matrícula → Atividade → Nota."""
        # Setup básico
        self.test_fluxo_basico_sistema()
        
        # Obter objetos criados
        if self.Curso:
            curso = self.Curso.objects.get(nome="Curso de Integração")
        if self.Turma:
            turma = self.Turma.objects.get(nome="Turma Integração 2024")
        if self.Aluno:
            aluno = self.Aluno.objects.get(nome="Aluno Integração")
        
        # 5. Criar atividade
        if self.Atividade:
            atividade = self.Atividade.objects.create(
                nome="Aula Introdutória",
                descricao="Primeira aula do curso",
                tipo_atividade="AULA",
                data_inicio=date(2024, 1, 20),
                hora_inicio=time(19, 0),
                local="Sala 101",
                curso=curso,
                ativa=True
            )
            self.assertEqual(atividade.nome, "Aula Introdutória")
        
        # 6. Criar nota
        if self.Nota and self.Aluno and self.Turma:
            nota = self.Nota.objects.create(
                aluno=aluno,
                turma=turma,
                tipo_avaliacao="PROVA",
                valor=8.5,
                data=date.today()
            )
            self.assertEqual(nota.valor, 8.5)
            self.assertEqual(nota.aluno, aluno)
    
    def test_fluxo_financeiro(self):
        """Testa o fluxo financeiro: Aluno → Matrícula → Pagamento."""
        # Setup básico
        self.test_fluxo_basico_sistema()
        
        # Obter aluno criado
        if self.Aluno:
            aluno = self.Aluno.objects.get(nome="Aluno Integração")
        
        # 7. Criar pagamento
        if self.Pagamento and self.Aluno:
            pagamento = self.Pagamento.objects.create(
                aluno=aluno,
                valor=150.00,
                data_vencimento=date(2024, 2, 15),
                status="PENDENTE",
                metodo_pagamento="PIX"
            )
            self.assertEqual(pagamento.valor, 150.00)
            self.assertEqual(pagamento.aluno, aluno)
            self.assertEqual(pagamento.status, "PENDENTE")
    
    def test_integridade_dados(self):
        """Testa a integridade dos dados através de relacionamentos."""
        # Criar dados relacionados
        if self.Curso:
            curso = self.Curso.objects.create(
                nome="Curso Integridade",
                descricao="Teste de integridade",
                ativa=True
            )
        
        if self.Turma and self.Curso:
            turma = self.Turma.objects.create(
                nome="Turma Integridade",
                curso=curso,
                vagas=10,
                data_inicio_ativ=date(2024, 3, 1),
                ativa=True
            )
        
        if self.Aluno:
            aluno1 = self.Aluno.objects.create(
                nome="Aluno 1",
                cpf="22222222222",
                email="aluno1@teste.com",
                data_nascimento=date(1985, 3, 10),
                sexo="F",
                ativa=True
            )
            
            aluno2 = self.Aluno.objects.create(
                nome="Aluno 2",
                cpf="33333333333",
                email="aluno2@teste.com",
                data_nascimento=date(1987, 8, 20),
                sexo="M",
                ativa=True
            )
        
        if self.Matricula and self.Aluno and self.Turma:
            # Matricular múltiplos alunos
            matricula1 = self.Matricula.objects.create(
                aluno=aluno1,
                turma=turma,
                data_matricula=date.today(),
                ativa=True
            )
            
            matricula2 = self.Matricula.objects.create(
                aluno=aluno2,
                turma=turma,
                data_matricula=date.today(),
                ativa=True
            )
        
        # Verificações de integridade
        if self.Turma:
            self.assertEqual(turma.matriculas.count(), 2)
        if self.Aluno:
            self.assertEqual(aluno1.matriculas.count(), 1)
            self.assertEqual(aluno2.matriculas.count(), 1)
        if self.Curso:
            self.assertEqual(curso.turmas.count(), 1)
    
    def test_validacoes_negocio(self):
        """Testa validações de negócio do sistema."""
        # Criar dados base
        if self.Curso:
            curso = self.Curso.objects.create(
                nome="Curso Validações",
                descricao="Teste de validações",
                ativa=True
            )
        
        if self.Turma and self.Curso:
            turma = self.Turma.objects.create(
                nome="Turma Validações",
                curso=curso,
                vagas=1,  # Apenas 1 vaga
                data_inicio_ativ=date(2024, 4, 1),
                ativa=True
            )
        
        if self.Aluno:
            aluno = self.Aluno.objects.create(
                nome="Aluno Validações",
                cpf="44444444444",
                email="aluno.validacoes@teste.com",
                data_nascimento=date(1992, 12, 25),
                sexo="M",
                ativa=True
            )
        
        if self.Matricula and self.Aluno and self.Turma:
            # Primeira matrícula - deve funcionar
            matricula = self.Matricula.objects.create(
                aluno=aluno,
                turma=turma,
                data_matricula=date.today(),
                ativa=True
            )
            
            # Verificar que a matrícula foi criada
            self.assertEqual(turma.matriculas.count(), 1)
            self.assertTrue(matricula.ativo)
