"""
Testes de integração para o sistema completo.
"""

import pytest
from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone

from tests.factories import (
    AlunoFactory, CursoFactory, TurmaFactory, MatriculaFactory,
    PresencaFactory, UserFactory, DadosTesteCompletos
)
from alunos.models import Aluno
from cursos.models import Curso
from matriculas.models import Matricula
from turmas.models import Turma
from presencas.models import Presenca


class FluxoCompletoSistemaTest(TransactionTestCase):
    """Testes do fluxo completo do sistema."""
    
    def setUp(self):
        self.user = UserFactory()
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_fluxo_completo_aluno_matricula_turma_presenca(self):
        """Teste do fluxo completo: aluno -> matrícula -> turma -> presença."""
        
        # 1. Criar aluno
        aluno_data = {
            'nome': 'João Silva',
            'cpf': '123.456.789-00',
            'email': 'joao@example.com',
            # 'telefone' removido
            # 'endereco' removido
            'data_nascimento': '1990-01-01',
            'ativo': True
        }
        
        # Criar aluno via API
        response = self.client.post(
            reverse('alunos:api_criar'),
            aluno_data,
            content_type='application/json'
        )
        assert response.status_code == 201
        
        aluno = Aluno.objects.get(cpf='123.456.789-00')
        
    # 2. Criar curso
    curso = CursoFactory(nome='Curso de Python')
        
        # 3. Matricular aluno no curso
        matricula_data = {
            'aluno': aluno.id,
            'curso': curso.id,
            'valor_pago': '300.00',
            'observacoes': 'Matrícula com desconto'
        }
        
        response = self.client.post(
            reverse('matriculas:api_criar'),
            matricula_data,
            content_type='application/json'
        )
        assert response.status_code == 201
        
        matricula = Matricula.objects.get(aluno=aluno, curso=curso)
        
        # 4. Criar turma
        turma = TurmaFactory(curso=curso)
        turma.alunos.add(aluno)
        
        # 5. Registrar presença
        presenca_data = {
            'aluno': aluno.id,
            'turma': turma.id,
            'data_aula': timezone.now().date(),
            'observacoes': 'Presente na aula'
        }
        
        response = self.client.post(
            reverse('presencas:api_criar'),
            presenca_data,
            content_type='application/json'
        )
        assert response.status_code == 201
        
        presenca = Presenca.objects.get(aluno=aluno, turma=turma)
        
        # Verificar relacionamentos
        assert matricula.aluno == aluno
        assert matricula.curso == curso
        assert turma.alunos.filter(id=aluno.id).exists()
        assert presenca.aluno == aluno
        assert presenca.turma == turma
        
        # Verificar valores
        assert matricula.valor_pago == Decimal('300.00')
    # valor_pendente = curso.preco - matricula.valor_pago  # campo removido
        assert valor_pendente == Decimal('200.00')
    
    def test_fluxo_multiplos_alunos_mesma_turma(self):
        """Teste do fluxo com múltiplos alunos na mesma turma."""
        
        # Criar curso e turma
        curso = CursoFactory()
        turma = TurmaFactory(curso=curso)
        
        # Criar múltiplos alunos
        alunos = AlunoFactory.create_batch(5)
        
        # Matricular todos os alunos
        matriculas = []
        for aluno in alunos:
            matricula = MatriculaFactory(aluno=aluno, curso=curso)
            matriculas.append(matricula)
            turma.alunos.add(aluno)
        
        # Registrar presenças para todos
        presencas = []
        for aluno in alunos:
            presenca = PresencaFactory(aluno=aluno, turma=turma)
            presencas.append(presenca)
        
        # Verificar que todos estão matriculados
        assert len(matriculas) == 5
        assert turma.alunos.count() == 5
        assert len(presencas) == 5
        
        # Verificar relacionamentos
        for i, aluno in enumerate(alunos):
            assert matriculas[i].aluno == aluno
            assert matriculas[i].curso == curso
            assert presencas[i].aluno == aluno
            assert presencas[i].turma == turma
    
    def test_fluxo_um_aluno_multiplos_cursos(self):
        """Teste do fluxo com um aluno em múltiplos cursos."""
        
        # Criar aluno
        aluno = AlunoFactory()
        
        # Criar múltiplos cursos
        cursos = CursoFactory.create_batch(3)
        
        # Matricular aluno em todos os cursos
        matriculas = []
        turmas = []
        presencas = []
        
        for curso in cursos:
            # Matricular
            matricula = MatriculaFactory(aluno=aluno, curso=curso)
            matriculas.append(matricula)
            
            # Criar turma
            turma = TurmaFactory(curso=curso)
            turma.alunos.add(aluno)
            turmas.append(turma)
            
            # Registrar presença
            presenca = PresencaFactory(aluno=aluno, turma=turma)
            presencas.append(presenca)
        
        # Verificar que o aluno está em todos os cursos
        assert len(matriculas) == 3
        assert len(turmas) == 3
        assert len(presencas) == 3
        
        # Verificar relacionamentos
        for i, curso in enumerate(cursos):
            assert matriculas[i].aluno == aluno
            assert matriculas[i].curso == curso
            assert turmas[i].curso == curso
            assert presencas[i].aluno == aluno
            assert presencas[i].turma == turmas[i]
    
    def test_performance_sistema_completo(self):
        """Teste de performance do sistema completo."""
        import time
        
        # Criar cenário complexo
        cenarios = DadosTesteCompletos.criar_cenario_complexo()
        
        # Medir tempo de consultas complexas
        start_time = time.time()
        
        # Consulta 1: Todos os alunos com suas matrículas
        alunos_com_matriculas = Aluno.objects.select_related(
            'tipo_aluno'
        ).prefetch_related('matricula_set__curso').all()
        
        # Consulta 2: Todas as turmas com seus alunos
        turmas_com_alunos = Turma.objects.select_related(
            'curso', 'status'
        ).prefetch_related('alunos').all()
        
        # Consulta 3: Todas as presenças
        presencas = Presenca.objects.select_related(
            'aluno', 'turma__curso', 'status'
        ).all()
        
        end_time = time.time()
        
        # Verificar que as consultas são rápidas
        assert end_time - start_time < 2.0
        
        # Verificar que os dados foram carregados
        assert len(list(alunos_com_matriculas)) > 0
        assert len(list(turmas_com_alunos)) > 0
        assert len(list(presencas)) > 0


@pytest.mark.django_db
class APIIntegrationTest(TestCase):
    """Testes de integração das APIs."""
    
    def setUp(self):
        self.user = UserFactory()
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_api_crud_completo_aluno(self):
        """Teste CRUD completo via API para aluno."""
        
        # CREATE
        aluno_data = {
            'nome': 'Maria Santos',
            'cpf': '987.654.321-00',
            'email': 'maria@example.com',
            # 'telefone' removido
            # 'endereco' removido
            'data_nascimento': '1985-05-15'
        }
        
        response = self.client.post(
            reverse('alunos:api_criar'),
            aluno_data,
            content_type='application/json'
        )
        assert response.status_code == 201
        
        # READ
        aluno = Aluno.objects.get(cpf='987.654.321-00')
        response = self.client.get(
            reverse('alunos:api_detalhe', kwargs={'pk': aluno.id})
        )
        assert response.status_code == 200
        data = response.json()
        assert data['nome'] == 'Maria Santos'
        
        # UPDATE
        update_data = {
            'nome': 'Maria Santos Silva',
            'email': 'maria.silva@example.com'
        }
        
        response = self.client.patch(
            reverse('alunos:api_detalhe', kwargs={'pk': aluno.id}),
            update_data,
            content_type='application/json'
        )
        assert response.status_code == 200
        
        # Verificar atualização
        aluno.refresh_from_db()
        assert aluno.nome == 'Maria Santos Silva'
        assert aluno.email == 'maria.silva@example.com'
        
        # DELETE
        response = self.client.delete(
            reverse('alunos:api_detalhe', kwargs={'pk': aluno.id})
        )
        assert response.status_code == 204
        
        # Verificar exclusão (soft delete)
        aluno.refresh_from_db()
        assert aluno.ativo is False
    
    def test_api_relacionamentos_complexos(self):
        """Teste de relacionamentos complexos via API."""
        
        # Criar dados base
        aluno = AlunoFactory()
        curso = CursoFactory()
        turma = TurmaFactory(curso=curso)
        
        # Criar matrícula via API
        matricula_data = {
            'aluno': aluno.id,
            'curso': curso.id,
            'valor_pago': '200.00'
        }
        
        response = self.client.post(
            reverse('matriculas:api_criar'),
            matricula_data,
            content_type='application/json'
        )
        assert response.status_code == 201
        
        # Adicionar aluno à turma
        turma.alunos.add(aluno)
        
        # Criar presença via API
        presenca_data = {
            'aluno': aluno.id,
            'turma': turma.id,
            'data_aula': timezone.now().date().isoformat()
        }
        
        response = self.client.post(
            reverse('presencas:api_criar'),
            presenca_data,
            content_type='application/json'
        )
        assert response.status_code == 201
        
        # Verificar relacionamentos via API
        response = self.client.get(
            reverse('alunos:api_detalhe', kwargs={'pk': aluno.id})
        )
        data = response.json()
        
        # Verificar que os relacionamentos estão corretos
        assert 'matriculas' in data
        assert 'presencas' in data
        assert len(data['matriculas']) == 1
        assert len(data['presencas']) == 1
    
    def test_api_filtros_e_busca(self):
        """Teste de filtros e busca via API."""
        
        # Criar dados de teste
        aluno1 = AlunoFactory(nome='João Silva')
        aluno2 = AlunoFactory(nome='Maria Santos')
        aluno3 = AlunoFactory(nome='Pedro Oliveira')
        
        # Teste de busca por nome
        response = self.client.get(
            reverse('alunos:api_buscar'),
            {'q': 'Silva'}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['nome'] == 'João Silva'
        
        # Teste de filtro por ativo
        aluno2.ativo = False
        aluno2.save()
        
        response = self.client.get(
            reverse('alunos:api_lista'),
            {'ativo': 'true'}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # aluno1 e aluno3
        
        # Teste de paginação
        response = self.client.get(
            reverse('alunos:api_lista'),
            {'page': 1, 'limit': 2}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data['results']) == 2
        assert 'next' in data or 'previous' in data


class ConcorrenciaTest(TransactionTestCase):
    """Testes de concorrência do sistema."""
    
    def test_matricula_concorrente(self):
        """Teste de matrícula concorrente."""
        import threading
        import time
        
        aluno = AlunoFactory()
        curso = CursoFactory()
        
        results = []
        errors = []
        
        def criar_matricula():
            try:
                with transaction.atomic():
                    matricula = MatriculaFactory(aluno=aluno, curso=curso)
                    results.append(matricula)
            except Exception as e:
                errors.append(e)
        
        # Criar duas threads tentando criar a mesma matrícula
        thread1 = threading.Thread(target=criar_matricula)
        thread2 = threading.Thread(target=criar_matricula)
        
        thread1.start()
        thread2.start()
        
        thread1.join()
        thread2.join()
        
        # Verificar que apenas uma matrícula foi criada
        assert len(results) == 1
        assert len(errors) == 1
        
        # Verificar que a matrícula foi criada corretamente
        matricula = Matricula.objects.get(aluno=aluno, curso=curso)
        assert matricula.aluno == aluno
        assert matricula.curso == curso
    
    def test_presenca_concorrente(self):
        """Teste de presença concorrente."""
        import threading
        
        aluno = AlunoFactory()
        turma = TurmaFactory()
        turma.alunos.add(aluno)
        
        data_aula = timezone.now().date()
        
        results = []
        errors = []
        
        def criar_presenca():
            try:
                with transaction.atomic():
                    presenca = PresencaFactory(
                        aluno=aluno,
                        turma=turma,
                        data_aula=data_aula
                    )
                    results.append(presenca)
            except Exception as e:
                errors.append(e)
        
        # Criar múltiplas threads tentando criar presenças
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=criar_presenca)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verificar que apenas uma presença foi criada
        assert len(results) == 1
        assert len(errors) == 2
        
        # Verificar que a presença foi criada corretamente
        presenca = Presenca.objects.get(
            aluno=aluno,
            turma=turma,
            data_aula=data_aula
        )
        assert presenca.aluno == aluno
        assert presenca.turma == turma


@pytest.mark.django_db
class IntegrationWorkflowTest:
    """Testes de workflow de integração."""
    
    def test_workflow_completo_escola(self):
        """Teste do workflow completo de uma escola."""
        # Cenário: Nova escola começando operação
        # 1. Criar tipos básicos
        from cursos.models import TipoCurso
        from matriculas.models import StatusMatricula
        from turmas.models import StatusTurma
        from presencas.models import StatusPresenca

        # Criar tipos
        tipo_curso_tecnico = TipoCurso.objects.create(
            nome='Técnico',
            descricao='Curso técnico'
        )
        status_matricula_ativa = StatusMatricula.objects.create(
            nome='Ativa',
            descricao='Matrícula ativa'
        )
        status_turma_andamento = StatusTurma.objects.create(
            nome='Em Andamento',
            descricao='Turma em andamento'
        )
        status_presenca_presente = StatusPresenca.objects.create(
            nome='Presente',
            descricao='Aluno presente'
        )

        # 2. Criar cursos
        curso_python = Curso.objects.create(
            nome='Python Básico',
            descricao='Curso de Python para iniciantes',
            tipo_curso=tipo_curso_tecnico,
        )
        curso_django = Curso.objects.create(
            nome='Django Avançado',
            descricao='Curso avançado de Django',
            tipo_curso=tipo_curso_tecnico,
        )

        # 3. Criar turmas
        turma_python = Turma.objects.create(
            nome='Python Básico - Turma A',
            curso=curso_python,
            status=status_turma_andamento,
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=60),
            capacidade_maxima=20,
            professor='Prof. João'
        )
        turma_django = Turma.objects.create(
            nome='Django Avançado - Turma B',
            curso=curso_django,
            status=status_turma_andamento,
            data_inicio=date.today() + timedelta(days=30),
            data_fim=date.today() + timedelta(days=120),
            capacidade_maxima=15,
            professor='Prof. Maria'
        )

        # 4. Criar alunos
        aluno1 = Aluno.objects.create(
            nome='João Silva',
            cpf='123.456.789-00',
            email='joao@example.com',
            data_nascimento=date(1990, 1, 1)
        )
        aluno2 = Aluno.objects.create(
            nome='Maria Santos',
            cpf='987.654.321-00',
            email='maria@example.com',
            data_nascimento=date(1985, 5, 15)
        )

        # 5. Criar matrículas
        matricula1 = Matricula.objects.create(
            aluno=aluno1,
            curso=curso_python,
            status=status_matricula_ativa,
            valor_pago=Decimal('400.00')
        )
        matricula2 = Matricula.objects.create(
            aluno=aluno2,
            curso=curso_python,
            status=status_matricula_ativa,
            valor_pago=Decimal('500.00')
        )
        matricula3 = Matricula.objects.create(
            aluno=aluno1,
            curso=curso_django,
            status=status_matricula_ativa,
            valor_pago=Decimal('600.00')
        )

        # 6. Adicionar alunos às turmas
        turma_python.alunos.add(aluno1, aluno2)
        turma_django.alunos.add(aluno1)

        # 7. Registrar presenças
        presenca1 = Presenca.objects.create(
            aluno=aluno1,
            turma=turma_python,
            status=status_presenca_presente,
            data_aula=date.today()
        )
        presenca2 = Presenca.objects.create(
            aluno=aluno2,
            turma=turma_python,
            status=status_presenca_presente,
            data_aula=date.today()
        )

        # Verificações finais
        assert Aluno.objects.count() == 2
        assert Curso.objects.count() == 2
        assert Turma.objects.count() == 2
        assert Matricula.objects.count() == 3
        assert Presenca.objects.count() == 2

        # Verificar relacionamentos
        assert aluno1.matricula_set.count() == 2
        assert aluno2.matricula_set.count() == 1
        assert turma_python.alunos.count() == 2
        assert turma_django.alunos.count() == 1

        # Verificar valores
        assert matricula1.valor_pago == Decimal('400.00')
        assert matricula2.valor_pago == Decimal('500.00')
        assert matricula3.valor_pago == Decimal('600.00')

        # Verificar valores pendentes
        # asserts de preco removidos

        print("✓ Workflow completo da escola executado com sucesso!")
        print(f"✓ {Aluno.objects.count()} alunos criados")
        print(f"✓ {Curso.objects.count()} cursos criados")
        print(f"✓ {Turma.objects.count()} turmas criadas")
        print(f"✓ {Matricula.objects.count()} matrículas criadas")
        print(f"✓ {Presenca.objects.count()} presenças registradas")
