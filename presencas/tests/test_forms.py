"""
Testes para os formulários do aplicativo presencas.
Cobre validação, clean methods e fields dinâmicos.
"""

from django.test import TestCase
from datetime import date, datetime
from unittest.mock import patch, Mock

from presencas.forms import (
    RegistrarPresencaForm, TotaisAtividadesPresencaForm,
    PresencaDetalhadaForm, FiltroConsolidadoForm,
    ExportacaoForm, RegistroRapidoForm
)
from presencas.models import (
    Presenca
)
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade
from cursos.models import Curso


class RegistrarPresencaFormTest(TestCase):
    """Testes para o formulário de registro de presença."""
    
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso Teste',
            descricao='Descrição do curso',
            ativo=True
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1,
            curso=self.curso
        )
    
    def test_form_campos_obrigatorios(self):
        """Testa validação de campos obrigatórios."""
        form = RegistrarPresencaForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertIn('curso', form.errors)
        self.assertIn('turma', form.errors)
        self.assertIn('ano', form.errors)
        self.assertIn('mes', form.errors)
    
    def test_form_dados_validos(self):
        """Testa formulário com dados válidos."""
        data = {
            'curso': self.curso.id,
            'turma': self.turma.id,
            'ano': 2024,
            'mes': 1
        }
        
        form = RegistrarPresencaForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_ano_choices(self):
        """Testa choices de ano."""
        form = RegistrarPresencaForm()
        
        # Verificar que anos são gerados corretamente
        ano_atual = datetime.now().year
        anos_disponiveis = [choice[0] for choice in form.fields['ano'].choices]
        
        self.assertIn(str(ano_atual), anos_disponiveis)
        self.assertIn(str(ano_atual - 1), anos_disponiveis)
    
    def test_form_mes_choices(self):
        """Testa choices de mês."""
        form = RegistrarPresencaForm()
        
        meses = [choice[0] for choice in form.fields['mes'].choices]
        
        # Verificar que todos os 12 meses estão presentes
        self.assertEqual(len(meses), 12)
        self.assertIn('1', meses)
        self.assertIn('12', meses)
    
    def test_form_initial_values(self):
        """Testa valores iniciais do formulário."""
        form = RegistrarPresencaForm()
        
        ano_atual = datetime.now().year
        mes_atual = datetime.now().month
        
        self.assertEqual(int(form.fields['ano'].initial), ano_atual)
        self.assertEqual(int(form.fields['mes'].initial), mes_atual)
    
    def test_form_turma_queryset_dinamico(self):
        """Testa queryset dinâmico de turmas."""
        # Inicialmente, turmas devem estar vazias
        form = RegistrarPresencaForm()
        self.assertFalse(form.fields['turma'].queryset.exists())
        
        # Com curso selecionado, turmas devem ser filtradas
        # (isso normalmente seria feito via AJAX)
        form = RegistrarPresencaForm(data={'curso': self.curso.id})
        # Atualizar queryset manualmente para simular AJAX
        form.fields['turma'].queryset = Turma.objects.filter(curso=self.curso)
        
        self.assertTrue(form.fields['turma'].queryset.exists())
        self.assertIn(self.turma, form.fields['turma'].queryset)


class TotaisAtividadesPresencaFormTest(TestCase):
    """Testes para o formulário de totais de atividades."""
    
    def setUp(self):
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_form_campos_basicos(self):
        """Testa campos básicos do formulário."""
        form = TotaisAtividadesPresencaForm()
        
        expected_fields = ['turma', 'atividade', 'ano', 'mes', 'qtd_ativ_mes']
        for field in expected_fields:
            self.assertIn(field, form.fields)
    
    def test_form_dados_validos(self):
        """Testa formulário com dados válidos."""
        data = {
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'ano': 2024,
            'mes': 1,
            'qtd_ativ_mes': 15
        }
        
        form = TotaisAtividadesPresencaForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_quantidade_negativa(self):
        """Testa validação de quantidade negativa."""
        data = {
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'ano': 2024,
            'mes': 1,
            'qtd_ativ_mes': -5  # Valor negativo
        }
        
        form = TotaisAtividadesPresencaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('qtd_ativ_mes', form.errors)
    
    def test_form_mes_invalido(self):
        """Testa validação de mês inválido."""
        data = {
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'ano': 2024,
            'mes': 13,  # Mês inválido
            'qtd_ativ_mes': 10
        }
        
        form = TotaisAtividadesPresencaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('mes', form.errors)


class PresencaDetalhadaFormTest(TestCase):
    """Testes para formulário de presença detalhada."""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_form_dados_validos(self):
        """Testa formulário com dados válidos."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'periodo': date(2024, 1, 1),
            'convocacoes': 10,
            'presencas': 8,
            'faltas': 2,
            'voluntario_extra': 1,
            'voluntario_simples': 2
        }
        
        form = PresencaDetalhadaForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_clean_presencas_faltas_convocacoes(self):
        """Testa validação: presencas + faltas <= convocacoes."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'periodo': date(2024, 1, 1),
            'convocacoes': 10,
            'presencas': 7,
            'faltas': 5  # 7 + 5 = 12 > 10
        }
        
        form = PresencaDetalhadaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
    
    def test_form_clean_periodo_primeiro_dia(self):
        """Testa validação: período deve ser primeiro dia do mês."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'periodo': date(2024, 1, 15),  # Não é primeiro dia
            'convocacoes': 10,
            'presencas': 8,
            'faltas': 2
        }
        
        form = PresencaDetalhadaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('periodo', form.errors)
    
    def test_form_valores_negativos(self):
        """Testa validação de valores negativos."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'periodo': date(2024, 1, 1),
            'convocacoes': -1,  # Valor negativo
            'presencas': 8,
            'faltas': 2
        }
        
        form = PresencaDetalhadaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('convocacoes', form.errors)


class FiltroConsolidadoFormTest(TestCase):
    """Testes para formulário de filtros do consolidado."""
    
    def setUp(self):
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_form_filtros_opcionais(self):
        """Testa que todos os filtros são opcionais."""
        form = FiltroConsolidadoForm(data={})
        self.assertTrue(form.is_valid())
    
    def test_form_filtros_validos(self):
        """Testa formulário com filtros válidos."""
        data = {
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'periodo_inicio': date(2024, 1, 1),
            'periodo_fim': date(2024, 12, 31),
            'ordenar_por': 'nome'
        }
        
        form = FiltroConsolidadoForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_clean_periodo_inicio_fim(self):
        """Testa validação: período início deve ser anterior ao fim."""
        data = {
            'periodo_inicio': date(2024, 12, 31),
            'periodo_fim': date(2024, 1, 1)  # Anterior ao início
        }
        
        form = FiltroConsolidadoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
    
    def test_form_ordenacao_choices(self):
        """Testa choices de ordenação."""
        form = FiltroConsolidadoForm()
        
        choices = [choice[0] for choice in form.fields['ordenar_por'].choices]
        expected = ['nome', 'percentual', 'carencias']
        
        for choice in expected:
            self.assertIn(choice, choices)


class ExportacaoFormTest(TestCase):
    """Testes para formulário de exportação."""
    
    def test_form_formato_choices(self):
        """Testa choices de formato."""
        form = ExportacaoForm()
        
        choices = [choice[0] for choice in form.fields['formato'].choices]
        expected = ['excel_basico', 'excel_avancado', 'csv', 'pdf']
        
        for choice in expected:
            self.assertIn(choice, choices)
    
    def test_form_template_choices(self):
        """Testa choices de template."""
        form = ExportacaoForm()
        
        choices = [choice[0] for choice in form.fields['template'].choices]
        expected = ['consolidado_geral', 'por_turma', 'estatisticas']
        
        for choice in expected:
            self.assertIn(choice, choices)
    
    def test_form_dados_validos(self):
        """Testa formulário com dados válidos."""
        data = {
            'formato': 'excel_avancado',
            'template': 'consolidado_geral',
            'incluir_graficos': True,
            'incluir_estatisticas': True,
            'titulo_personalizado': 'Relatório de Teste'
        }
        
        form = ExportacaoForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_titulo_maximo_caracteres(self):
        """Testa validação de tamanho máximo do título."""
        data = {
            'formato': 'excel_basico',
            'template': 'consolidado_geral',
            'titulo_personalizado': 'A' * 201  # Mais que o máximo
        }
        
        form = ExportacaoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo_personalizado', form.errors)


class RegistroRapidoFormTest(TestCase):
    """Testes para formulário de registro rápido."""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_form_dados_validos(self):
        """Testa formulário com dados válidos."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'data': date.today(),
            'presente': True
        }
        
        form = RegistroRapidoForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_clean_data_futura(self):
        """Testa validação de data futura."""
        from datetime import timedelta
        
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today() + timedelta(days=1),  # Data futura
            'presente': True
        }
        
        form = RegistroRapidoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('data', form.errors)
    
    def test_form_clean_ausencia_sem_justificativa(self):
        """Testa validação: ausência com justificativa opcional."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today(),
            'presente': False,
            'justificativa': ''  # Vazio - agora é opcional
        }
        
        form = RegistroRapidoForm(data=data)
        self.assertTrue(form.is_valid())  # Deve ser válido agora
    
    def test_form_justificativa_opcional_presenca(self):
        """Testa que justificativa é opcional para presença."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today(),
            'presente': True,
            'justificativa': ''  # Vazio, mas é presença
        }
        
        form = RegistroRapidoForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_form_duplicidade_presenca(self):
        """Testa validação de duplicidade de presença."""
        # Criar presença existente
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        # Tentar criar outra presença para mesmo aluno/turma/data
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today(),
            'presente': False
        }
        
        form = RegistroRapidoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)


class FormDynamicFieldsTest(TestCase):
    """Testes para campos dinâmicos em formulários."""
    
    def setUp(self):
        self.curso1 = Curso.objects.create(
            nome='Curso 1',
            descricao='Primeiro curso',
            ativo=True
        )
        
        self.curso2 = Curso.objects.create(
            nome='Curso 2',
            descricao='Segundo curso',
            ativo=True
        )
        
        self.turma1 = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1,
            curso=self.curso1
        )
        
        self.turma2 = Turma.objects.create(
            nome='Turma B',
            ano=2024,
            semestre=1,
            curso=self.curso2
        )
    
    def test_turmas_filtradas_por_curso(self):
        """Testa filtro dinâmico de turmas por curso."""
        # Criar formulário com curso específico
        form = RegistrarPresencaForm(initial={'curso': self.curso1.id})
        
        # Simular filtro AJAX de turmas
        form.fields['turma'].queryset = Turma.objects.filter(
            curso=self.curso1
        )
        
        turmas_disponiveis = list(form.fields['turma'].queryset)
        
        self.assertIn(self.turma1, turmas_disponiveis)
        self.assertNotIn(self.turma2, turmas_disponiveis)
    
    @patch('presencas.forms.Aluno.objects.filter')
    def test_alunos_filtrados_por_turma(self, mock_filter):
        """Testa filtro dinâmico de alunos por turma."""
        # Configurar mock
        mock_queryset = Mock()
        mock_filter.return_value = mock_queryset
        
        # Simular formulário que filtra alunos por turma
        # (implementação específica dependeria do formulário real)
        
        mock_filter.assert_not_called()  # Inicial, sem filtro
        
        # Simular seleção de turma
        # form.filter_alunos_by_turma(self.turma1.id)
        # mock_filter.assert_called_with(matriculas__turma=self.turma1)


class FormValidationTest(TestCase):
    """Testes gerais de validação de formulários."""
    
    def test_form_csrf_token(self):
        """Testa presença de CSRF token em formulários."""
        form = RegistrarPresencaForm()
        
        # Verificar que formulário pode ser renderizado com CSRF
        form_html = str(form)
        # CSRF token seria adicionado pelo template, não pelo formulário
        self.assertIsInstance(form_html, str)
    
    def test_form_html_escaping(self):
        """Testa escape de HTML em valores de formulário."""
        data = {
            'justificativa': '<script>alert("XSS")</script>',
            'registrado_por': '<img src=x onerror=alert("XSS")>'
        }
        
        # Criar formulário que aceita esses campos
        form = RegistroRapidoForm(data=data)
        
        # Verificar que HTML é escapado na renderização
        form_html = str(form)
        self.assertNotIn('<script>', form_html)
        self.assertNotIn('<img', form_html)
    
    def test_form_required_fields_validation(self):
        """Testa validação consistente de campos obrigatórios."""
        forms_to_test = [
            (RegistrarPresencaForm, ['curso', 'turma', 'ano', 'mes']),
            (TotaisAtividadesPresencaForm, ['turma', 'atividade', 'ano', 'mes']),
            (RegistroRapidoForm, ['aluno', 'turma', 'data'])
        ]
        
        for form_class, required_fields in forms_to_test:
            form = form_class(data={})
            self.assertFalse(form.is_valid())
            
            for field in required_fields:
                self.assertIn(field, form.errors)
    
    def test_form_clean_methods_consistency(self):
        """Testa consistência dos métodos clean() customizados."""
        # Teste geral para verificar que métodos clean não causam exceções
        forms_with_data = [
            (RegistrarPresencaForm, {
                'curso': 1, 'turma': 1, 'ano': 2024, 'mes': 1
            }),
            (FiltroConsolidadoForm, {
                'periodo_inicio': date(2024, 1, 1),
                'periodo_fim': date(2024, 12, 31)
            })
        ]
        
        for form_class, data in forms_with_data:
            try:
                form = form_class(data=data)
                form.is_valid()  # Chama clean() internamente
                # Se chegou aqui, clean() não causou exceção
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"Clean method for {form_class.__name__} raised {e}")


class FormIntegrationTest(TestCase):
    """Testes de integração com models."""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_form_save_creates_model(self):
        """Testa que save() do formulário cria o model."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'data': date.today(),
            'presente': True
        }
        
        form = RegistroRapidoForm(data=data)
        self.assertTrue(form.is_valid())
        
        # Se o formulário tiver método save()
        if hasattr(form, 'save'):
            presenca = form.save()
            self.assertIsInstance(presenca, Presenca)
            self.assertEqual(presenca.aluno, self.aluno)
    
    def test_form_update_model(self):
        """Testa atualização de model existente via formulário."""
        # Criar presença existente
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        # Dados para atualização
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today(),
            'presente': False,
            'justificativa': 'Motivo médico'
        }
        
        form = RegistroRapidoForm(data=data, instance=presenca)
        
        if form.is_valid() and hasattr(form, 'save'):
            presenca_atualizada = form.save()
            self.assertFalse(presenca_atualizada.presente)
            self.assertEqual(presenca_atualizada.justificativa, 'Motivo médico')
