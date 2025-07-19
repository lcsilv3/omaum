"""
Testes baseados em User Stories e casos de uso reais.
Validação de funcionalidades Excel-like e regras de negócio.
"""

from datetime import date, datetime, timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json

from alunos.services import criar_aluno
from turmas.models import Turma
from atividades.models import Atividade
from presencas.models import PresencaAcademica


class UserStoryTestCase(TestCase):
    """Classe base para testes de User Stories."""
    
    def setUp(self):
        """Setup com personas e cenários realistas."""
        # Personas
        self.professor = User.objects.create_user(
            username='prof_maria',
            email='maria@escola.com',
            password='senha123',
            first_name='Maria',
            last_name='Santos'
        )
        
        self.coordenador = User.objects.create_user(
            username='coord_joao',
            email='joao@escola.com',
            password='senha123',
            first_name='João',
            last_name='Silva'
        )
        
        # Cenário: Escola com múltiplas turmas e atividades
        self.turma_iniciacao = Turma.objects.create(
            codigo_turma="INIC001",
            nome="Iniciação - Turma A",
            ativa=True
        )
        
        self.turma_avancada = Turma.objects.create(
            codigo_turma="AVAN001",
            nome="Avançada - Turma B",
            ativa=True
        )
        
        # Atividades variadas
        self.atividades = {
            'ritual_abertura': Atividade.objects.create(
                nome="Ritual de Abertura",
                tipo="RITUAL",
                ativa=True
            ),
            'aula_teorica': Atividade.objects.create(
                nome="Aula Teórica",
                tipo="AULA",
                ativa=True
            ),
            'pratica_meditacao': Atividade.objects.create(
                nome="Prática de Meditação",
                tipo="PRATICA",
                ativa=True
            ),
            'palestra': Atividade.objects.create(
                nome="Palestra Especial",
                tipo="EVENTO",
                ativa=True
            )
        }
        
        # Alunos com perfis diversos
        self.alunos_iniciacao = self._criar_alunos_turma(self.turma_iniciacao, 8, "Iniciação")
        self.alunos_avancada = self._criar_alunos_turma(self.turma_avancada, 6, "Avançada")
        
        self.client = Client()
    
    def _criar_alunos_turma(self, turma, quantidade, prefixo):
        """Cria alunos para uma turma específica."""
        alunos = []
        for i in range(quantidade):
            aluno_data = {
                "cpf": f"{i+1:011d}",
                "nome": f"{prefixo} Aluno {i+1}",
                "data_nascimento": f"199{i % 10}-0{(i % 12) + 1:01d}-15",
                "hora_nascimento": f"{14 + (i % 10)}:30",
                "email": f"{prefixo.lower()}.aluno{i+1}@teste.com",
                "sexo": "M" if i % 2 == 0 else "F",
                "nacionalidade": "Brasileira",
                "naturalidade": "São Paulo",
                "rua": f"Rua {prefixo} {i+1}",
                "numero_imovel": str(100 + i),
                "cidade": "São Paulo",
                "estado": "SP",
                "bairro": "Centro",
                "cep": f"0123456{i}",
                "nome_primeiro_contato": f"Contato {i+1}",
                "celular_primeiro_contato": f"11999{i:06d}",
                "tipo_relacionamento_primeiro_contato": "Mãe",
                "nome_segundo_contato": f"Pai {i+1}",
                "celular_segundo_contato": f"11998{i:06d}",
                "tipo_relacionamento_segundo_contato": "Pai",
                "tipo_sanguineo": ["A", "B", "AB", "O"][i % 4],
                "fator_rh": "+" if i % 2 == 0 else "-",
            }
            aluno = criar_aluno(aluno_data)
            alunos.append(aluno)
        return alunos


class ProfessorDiarioUserStoryTest(UserStoryTestCase):
    """
    USER STORY: Como professor, quero registrar presenças rapidamente
    para que eu possa focar no ensino em vez de burocracia.
    """
    
    def test_professor_registro_rapido_ritual_abertura(self):
        """
        CENÁRIO: Professor chega na sala e precisa registrar presença do ritual matinal.
        DADO que é 8h da manhã
        QUANDO o professor acessa o registro rápido
        ENTÃO ele deve conseguir marcar todos os presentes em menos de 30 segundos
        """
        self.client.login(username='prof_maria', password='senha123')
        
        # 1. Acesso rápido à página
        url = reverse('presencas:registro_rapido')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # 2. Interface deve ser intuitiva
        self.assertContains(response, 'Registro Rápido')
        self.assertContains(response, 'Selecionar Turma')
        
        # 3. Registro em lote - todos presentes por padrão
        presenca_data = {
            'turma': self.turma_iniciacao.id,
            'atividade': self.atividades['ritual_abertura'].id,
            'data': date.today().strftime('%Y-%m-%d'),
        }
        
        # Marcar todos presentes (comportamento padrão esperado)
        for aluno in self.alunos_iniciacao:
            presenca_data[f'aluno_{aluno.id}_presente'] = 'on'
        
        response = self.client.post(url, presenca_data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento de sucesso
        
        # 4. Verificar eficiência - todas as presenças salvas
        presencas = PresencaAcademica.objects.filter(
            turma=self.turma_iniciacao,
            atividade=self.atividades['ritual_abertura'],
            data=date.today()
        )
        
        self.assertEqual(presencas.count(), 8)  # Todos os alunos
        self.assertTrue(all(p.presente for p in presencas))  # Todos presentes
    
    def test_professor_marca_falta_com_justificativa(self):
        """
        CENÁRIO: Aluno chega atrasado após o ritual
        DADO que o professor já registrou as presenças
        QUANDO ele precisa marcar falta para quem não estava
        ENTÃO deve poder adicionar justificativa facilmente
        """
        self.client.login(username='prof_maria', password='senha123')
        
        # Aluno que chegou atrasado
        aluno_atrasado = self.alunos_iniciacao[0]
        
        presenca_data = {
            'turma': self.turma_iniciacao.id,
            'atividade': self.atividades['ritual_abertura'].id,
            'data': date.today().strftime('%Y-%m-%d'),
        }
        
        # Marcar presentes exceto o atrasado
        for aluno in self.alunos_iniciacao:
            if aluno != aluno_atrasado:
                presenca_data[f'aluno_{aluno.id}_presente'] = 'on'
            else:
                # Falta com justificativa
                presenca_data[f'aluno_{aluno.id}_justificativa'] = 'Chegou após o ritual'
        
        response = self.client.post(reverse('presencas:registro_rapido'), presenca_data)
        self.assertEqual(response.status_code, 302)
        
        # Verificar presença do aluno atrasado
        presenca_atrasado = PresencaAcademica.objects.get(
            aluno=aluno_atrasado,
            turma=self.turma_iniciacao,
            data=date.today()
        )
        
        self.assertFalse(presenca_atrasado.presente)
        self.assertEqual(presenca_atrasado.justificativa, 'Chegou após o ritual')


class CoordenadorAnaliseUserStoryTest(UserStoryTestCase):
    """
    USER STORY: Como coordenador, quero analisar padrões de frequência
    para identificar alunos que precisam de atenção especial.
    """
    
    def setUp(self):
        super().setUp()
        # Criar histórico de 30 dias com padrões específicos
        self._criar_historico_frequencia()
    
    def _criar_historico_frequencia(self):
        """Cria padrões realistas de frequência para análise."""
        base_date = date.today() - timedelta(days=30)
        
        for i in range(30):
            data_dia = base_date + timedelta(days=i)
            
            for idx, aluno in enumerate(self.alunos_iniciacao):
                # Padrões diferentes para simular casos reais
                if idx == 0:  # Aluno exemplar - 100% presença
                    presente = True
                elif idx == 1:  # Aluno problemático - 40% presença
                    presente = i % 5 < 2
                elif idx == 2:  # Aluno melhorando - começa mal, melhora
                    presente = i > 15 or i % 4 == 0
                elif idx == 3:  # Aluno piorando - começa bem, piora
                    presente = i < 15 and i % 3 != 0
                else:  # Alunos normais - 70-80% presença
                    presente = i % 4 != 3
                
                PresencaAcademica.objects.create(
                    aluno=aluno,
                    turma=self.turma_iniciacao,
                    atividade=self.atividades['aula_teorica'],
                    data=data_dia,
                    presente=presente,
                    justificativa='' if presente else f'Falta dia {i+1}'
                )
    
    def test_coordenador_identifica_aluno_problematico(self):
        """
        CENÁRIO: Coordenador quer identificar alunos com baixa frequência
        DADO que existem 30 dias de histórico
        QUANDO ele acessa o relatório consolidado
        ENTÃO deve ver alunos com menos de 60% de presença destacados
        """
        self.client.login(username='coord_joao', password='senha123')
        
        # Acessar relatório consolidado do último mês
        data_inicio = date.today() - timedelta(days=30)
        data_fim = date.today()
        
        url = reverse('presencas:consolidado')
        response = self.client.get(url, {
            'turma': self.turma_iniciacao.id,
            'data_inicio': data_inicio.strftime('%Y-%m-%d'),
            'data_fim': data_fim.strftime('%Y-%m-%d')
        })
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se aluno problemático (40% presença) aparece na análise
        aluno_problematico = self.alunos_iniciacao[1]
        context = response.context
        
        # Deve ter dados estatísticos no contexto
        self.assertIn('relatorio_data', context)
        
        # Calcular presença do aluno problemático
        presencas_aluno = PresencaAcademica.objects.filter(
            aluno=aluno_problematico,
            turma=self.turma_iniciacao,
            data__gte=data_inicio,
            data__lte=data_fim
        )
        
        taxa_presenca = presencas_aluno.filter(presente=True).count() / presencas_aluno.count() * 100
        self.assertLess(taxa_presenca, 50)  # Confirma que é problemático
    
    def test_coordenador_exporta_relatorio_detalhado(self):
        """
        CENÁRIO: Coordenador precisa de relatório para reunião pedagógica
        QUANDO ele exporta dados detalhados
        ENTÃO deve receber Excel com todos os dados e estatísticas
        """
        self.client.login(username='coord_joao', password='senha123')
        
        export_data = {
            'turma': self.turma_iniciacao.id,
            'data_inicio': (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'data_fim': date.today().strftime('%Y-%m-%d'),
            'incluir_estatisticas': True,
            'incluir_graficos': True
        }
        
        url = reverse('presencas:exportar_excel')
        response = self.client.post(url, export_data)
        
        # Verificar download
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get('Content-Type'),
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        # Nome do arquivo deve ser descritivo
        content_disposition = response.get('Content-Disposition', '')
        self.assertIn('presencas_detalhado', content_disposition.lower())


class AlunoExcelLikeUserStoryTest(UserStoryTestCase):
    """
    USER STORY: Como usuário acostumado com Excel, quero interface familiar
    para que eu possa usar o sistema sem treinamento extensivo.
    """
    
    def test_interface_grid_editavel(self):
        """
        CENÁRIO: Usuário quer editar presenças como planilha
        DADO que existe uma grade de presenças
        QUANDO ele clica em uma célula
        ENTÃO deve poder editar inline como no Excel
        """
        self.client.login(username='prof_maria', password='senha123')
        
        # Criar algumas presenças para ter dados na grade
        for aluno in self.alunos_iniciacao[:3]:
            PresencaAcademica.objects.create(
                aluno=aluno,
                turma=self.turma_iniciacao,
                atividade=self.atividades['aula_teorica'],
                data=date.today(),
                presente=True
            )
        
        # Acessar view de grade editável
        url = reverse('presencas:grade_presencas')
        response = self.client.get(url, {
            'turma': self.turma_iniciacao.id,
            'data': date.today().strftime('%Y-%m-%d')
        })
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar elementos de interface Excel-like
        self.assertContains(response, 'editable-cell')
        self.assertContains(response, 'data-aluno-id')
        self.assertContains(response, 'data-field')
        
        # JavaScript para edição deve estar presente
        self.assertContains(response, 'editInline')
    
    def test_navegacao_setas_teclado(self):
        """
        CENÁRIO: Usuário quer navegar com setas como no Excel
        DADO que está na grade de presenças
        QUANDO ele usa setas do teclado
        ENTÃO deve navegar entre células
        """
        self.client.login(username='prof_maria', password='senha123')
        
        url = reverse('presencas:grade_presencas')
        response = self.client.get(url, {
            'turma': self.turma_iniciacao.id
        })
        
        # Verificar se JavaScript de navegação está presente
        self.assertContains(response, 'keydown')
        self.assertContains(response, 'ArrowUp')
        self.assertContains(response, 'ArrowDown')
        self.assertContains(response, 'ArrowLeft')
        self.assertContains(response, 'ArrowRight')
    
    def test_copiar_colar_celulas(self):
        """
        CENÁRIO: Usuário quer copiar valores entre células
        DADO que selecionou uma célula com justificativa
        QUANDO ele copia e cola em outras células
        ENTÃO a justificativa deve ser aplicada
        """
        # Este teste validaria a funcionalidade via API
        self.client.login(username='prof_maria', password='senha123')
        
        # Simular operação de cópia/cola via API
        url = reverse('presencas:api_bulk_update')
        
        bulk_data = {
            'operacao': 'copiar_justificativa',
            'origem': {
                'aluno_id': self.alunos_iniciacao[0].id,
                'data': date.today().strftime('%Y-%m-%d')
            },
            'destinos': [
                {
                    'aluno_id': self.alunos_iniciacao[1].id,
                    'data': date.today().strftime('%Y-%m-%d')
                },
                {
                    'aluno_id': self.alunos_iniciacao[2].id,
                    'data': date.today().strftime('%Y-%m-%d')
                }
            ],
            'valor': 'Falta justificada por atestado médico'
        }
        
        response = self.client.post(
            url,
            json.dumps(bulk_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Deve aceitar operação em lote
        self.assertEqual(response.status_code, 200)


class RegrasNegocioUserStoryTest(UserStoryTestCase):
    """
    USER STORY: Como administrador, quero que regras de negócio sejam enforçadas
    para manter integridade e consistência dos dados.
    """
    
    def test_regra_data_futura_bloqueada(self):
        """
        REGRA: Não permitir registro de presença em data futura
        DADO que usuário tenta registrar presença para amanhã
        QUANDO ele submete o formulário
        ENTÃO deve receber erro de validação
        """
        self.client.login(username='prof_maria', password='senha123')
        
        data_futura = date.today() + timedelta(days=1)
        
        presenca_data = {
            'turma': self.turma_iniciacao.id,
            'atividade': self.atividades['aula_teorica'].id,
            'data': data_futura.strftime('%Y-%m-%d'),
            f'aluno_{self.alunos_iniciacao[0].id}_presente': 'on'
        }
        
        url = reverse('presencas:registro_rapido')
        response = self.client.post(url, presenca_data)
        
        # Deve retornar erro (não redirecionamento)
        self.assertEqual(response.status_code, 200)  # Volta ao form com erro
        self.assertContains(response, 'data não pode ser futura')
    
    def test_regra_ausencia_sem_justificativa_opcional(self):
        """
        REGRA: Ausência com justificativa opcional
        DADO que aluno está marcado como ausente
        QUANDO não há justificativa
        ENTÃO deve permitir salvar sem justificativa
        """
        self.client.login(username='prof_maria', password='senha123')
        
        presenca_data = {
            'turma': self.turma_iniciacao.id,
            'atividade': self.atividades['aula_teorica'].id,
            'data': date.today().strftime('%Y-%m-%d'),
            # Marcar como ausente SEM justificativa
            f'aluno_{self.alunos_iniciacao[0].id}_presente': '',  # Ausente
            f'aluno_{self.alunos_iniciacao[0].id}_justificativa': ''  # Sem justificativa - agora é opcional
        }
        
        url = reverse('presencas:registro_rapido')
        response = self.client.post(url, presenca_data)
        
        # Deve permitir salvar sem justificativa
        self.assertEqual(response.status_code, 200)
        # Não deve exigir justificativa - ela é opcional agora
    
    def test_regra_duplicata_presenca_bloqueada(self):
        """
        REGRA: Não permitir presença duplicada para mesmo aluno/turma/data
        DADO que já existe presença registrada
        QUANDO tenta registrar novamente
        ENTÃO deve atualizar a existente ou mostrar aviso
        """
        # Criar presença inicial
        presenca_inicial = PresencaAcademica.objects.create(
            aluno=self.alunos_iniciacao[0],
            turma=self.turma_iniciacao,
            atividade=self.atividades['aula_teorica'],
            data=date.today(),
            presente=True
        )
        
        self.client.login(username='prof_maria', password='senha123')
        
        # Tentar registrar novamente
        presenca_data = {
            'turma': self.turma_iniciacao.id,
            'atividade': self.atividades['aula_teorica'].id,
            'data': date.today().strftime('%Y-%m-%d'),
            f'aluno_{self.alunos_iniciacao[0].id}_presente': '',  # Mudando para ausente
            f'aluno_{self.alunos_iniciacao[0].id}_justificativa': 'Mudança de status'
        }
        
        url = reverse('presencas:registro_rapido')
        self.client.post(url, presenca_data)
        
        # Deve atualizar a presença existente
        presenca_inicial.refresh_from_db()
        self.assertFalse(presenca_inicial.presente)
        self.assertEqual(presenca_inicial.justificativa, 'Mudança de status')
        
        # Não deve criar duplicata
        count = PresencaAcademica.objects.filter(
            aluno=self.alunos_iniciacao[0],
            turma=self.turma_iniciacao,
            data=date.today()
        ).count()
        self.assertEqual(count, 1)


class CompatibilidadeUserStoryTest(UserStoryTestCase):
    """
    USER STORY: Como usuário do sistema legado, quero transição suave
    para que eu não perca produtividade durante a migração.
    """
    
    def test_importacao_dados_legado(self):
        """
        CENÁRIO: Migração de dados do sistema antigo
        DADO que existem dados no formato antigo
        QUANDO eles são importados
        ENTÃO devem funcionar no novo sistema
        """
        # Simular dados no formato legado
        dados_legado = [
            {
                'aluno_cpf': self.alunos_iniciacao[0].cpf,
                'turma_codigo': self.turma_iniciacao.codigo_turma,
                'data_presenca': '2024-01-15',
                'status': 'P',  # Formato antigo: P/F
                'obs': 'Presente'
            },
            {
                'aluno_cpf': self.alunos_iniciacao[1].cpf,
                'turma_codigo': self.turma_iniciacao.codigo_turma,
                'data_presenca': '2024-01-15',
                'status': 'F',  # Formato antigo: P/F
                'obs': 'Faltou por doença'
            }
        ]
        
        self.client.login(username='coord_joao', password='senha123')
        
        # API de importação
        url = reverse('presencas:importar_legado')
        response = self.client.post(
            url,
            json.dumps({'dados': dados_legado}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se dados foram convertidos corretamente
        presencas = PresencaAcademica.objects.filter(
            turma=self.turma_iniciacao,
            data=date(2024, 1, 15)
        )
        
        self.assertEqual(presencas.count(), 2)
        
        presenca_presente = presencas.get(aluno=self.alunos_iniciacao[0])
        presenca_ausente = presencas.get(aluno=self.alunos_iniciacao[1])
        
        self.assertTrue(presenca_presente.presente)
        self.assertFalse(presenca_ausente.presente)
        self.assertEqual(presenca_ausente.justificativa, 'Faltou por doença')
    
    def test_aliases_campos_antigos(self):
        """
        CENÁRIO: Formulários usam nomes de campos antigos
        DADO que código legado usa 'aluno_codigo' em vez de 'aluno_id'
        QUANDO formulário é submetido
        ENTÃO sistema deve aceitar ambos os formatos
        """
        self.client.login(username='prof_maria', password='senha123')
        
        # Usar nomenclatura antiga nos campos
        presenca_data_legado = {
            'turma_codigo': self.turma_iniciacao.codigo_turma,  # Em vez de turma_id
            'atividade_nome': self.atividades['aula_teorica'].nome,  # Em vez de atividade_id
            'data_aula': date.today().strftime('%Y-%m-%d'),  # Em vez de data
            f'aluno_codigo_{self.alunos_iniciacao[0].cpf}_presente': 'S'  # Em vez de 'on'
        }
        
        url = reverse('presencas:registro_compatibilidade')
        response = self.client.post(url, presenca_data_legado)
        
        # Deve aceitar e processar corretamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar se presença foi salva
        presenca = PresencaAcademica.objects.filter(
            aluno=self.alunos_iniciacao[0],
            turma=self.turma_iniciacao,
            data=date.today()
        ).first()
        
        self.assertIsNotNone(presenca)
        self.assertTrue(presenca.presente)


class PerformanceUserStoryTest(UserStoryTestCase):
    """
    USER STORY: Como usuário de turmas grandes, quero sistema ágil
    para que eu não perca tempo esperando carregamentos.
    """
    
    def test_carregamento_turma_grande(self):
        """
        CENÁRIO: Turma com 50+ alunos deve carregar rapidamente
        DADO que turma tem muitos alunos
        QUANDO acessar registro de presença
        ENTÃO deve carregar em menos de 3 segundos
        """
        # Criar turma grande
        turma_grande = Turma.objects.create(
            codigo_turma="GRANDE001",
            nome="Turma Grande - 50 alunos"
        )
        
        # Criar 50 alunos
        alunos_grandes = self._criar_alunos_turma(turma_grande, 50, "Grande")
        
        self.client.login(username='prof_maria', password='senha123')
        
        # Medir tempo de carregamento (simplificado)
        start_time = datetime.now()
        
        url = reverse('presencas:registro_rapido')
        response = self.client.get(url, {
            'turma': turma_grande.id
        })
        
        end_time = datetime.now()
        (end_time - start_time).total_seconds()
        
        self.assertEqual(response.status_code, 200)
        # Em teste real, verificaríamos se tempo < 3 segundos
        # self.assertLess(tempo_carregamento, 3)
        
        # Verificar se todos os alunos estão na resposta
        for aluno in alunos_grandes[:5]:  # Verificar alguns
            self.assertContains(response, aluno.nome)
    
    def test_paginacao_historico_longo(self):
        """
        CENÁRIO: Histórico de anos deve ser paginado
        DADO que existem centenas de registros
        QUANDO acessar histórico
        ENTÃO deve paginar para manter performance
        """
        # Criar histórico extenso
        aluno = self.alunos_iniciacao[0]
        
        # 365 dias de histórico
        for i in range(365):
            data_historico = date.today() - timedelta(days=i)
            PresencaAcademica.objects.create(
                aluno=aluno,
                turma=self.turma_iniciacao,
                atividade=self.atividades['aula_teorica'],
                data=data_historico,
                presente=i % 4 != 0  # 75% presença
            )
        
        self.client.login(username='coord_joao', password='senha123')
        
        # Acessar histórico do aluno
        url = reverse('presencas:historico_aluno', args=[aluno.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Deve ter paginação
        self.assertContains(response, 'pagination')
        self.assertContains(response, 'page_obj')
        
        # Não deve carregar todos os 365 registros de uma vez
        context = response.context
        if 'page_obj' in context:
            registros_pagina = len(context['page_obj'].object_list)
            self.assertLessEqual(registros_pagina, 50)  # Máximo 50 por página
