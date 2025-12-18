"""
Teste funcional simples para verificar o cascade Estado → Cidade → Bairro
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from alunos.models import Estado, Cidade, Bairro

User = get_user_model()


class TestCascataEstadoCidadeAPI(TestCase):
    """Testa as APIs que alimentam o cascade Estado → Cidade → Bairro."""
    
    def setUp(self):
        """Criar usuário, fazer login e verificar dados."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )
        
        # Adiciona permissões necessárias
        perms = Permission.objects.filter(
            codename__in=['add_aluno', 'change_aluno', 'view_aluno']
        )
        self.user.user_permissions.set(perms)
        
        self.client.login(username='testuser', password='testpass123')
        
        # Cria dados de teste
        self.estado_al = Estado.objects.create(
            nome="Alagoas", codigo="AL", regiao="Nordeste"
        )
        self.estado_sp = Estado.objects.create(
            nome="São Paulo", codigo="SP", regiao="Sudeste"
        )
        
        # Cidades de Alagoas
        self.cidade_maceio = Cidade.objects.create(
            nome="Maceió", estado=self.estado_al
        )
        self.cidade_arapiraca = Cidade.objects.create(
            nome="Arapiraca", estado=self.estado_al
        )
        
        # Cidades de São Paulo
        self.cidade_sp = Cidade.objects.create(
            nome="São Paulo", estado=self.estado_sp
        )
        
        # Bairros de Maceió
        self.bairro_pajucara = Bairro.objects.create(
            nome="Pajuçara", cidade=self.cidade_maceio
        )
        self.bairro_ponta_verde = Bairro.objects.create(
            nome="Ponta Verde", cidade=self.cidade_maceio
        )
        
        # Verificar se há dados de teste
        self.estado_count = Estado.objects.count()
        self.cidade_count = Cidade.objects.count()
        self.bairro_count = Bairro.objects.count()
        
        print(f"\n📊 Dados criados para teste:")
        print(f"   Estados: {self.estado_count}")
        print(f"   Cidades: {self.cidade_count}")
        print(f"   Bairros: {self.bairro_count}")
    
    def test_01_form_loads(self):
        """Testa se a página do formulário carrega sem erros."""
        response = self.client.get('/alunos/criar/')
        
        print(f"\n✅ Status da página: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        
        # Verificar se os campos estão presentes
        self.assertContains(response, 'id_estado_ref')
        self.assertContains(response, 'id_cidade_ref')
        self.assertContains(response, 'id_bairro_ref')
        
        print("✅ Campos estado_ref, cidade_ref e bairro_ref presentes no HTML")
    
    def test_02_api_cidades_por_estado(self):
        """Testa se a API de cidades por estado funciona."""
        if self.estado_count == 0:
            self.skipTest("Sem estados cadastrados no banco")
        
        # Pegar o primeiro estado (AL geralmente)
        estado = Estado.objects.first()
        print(f"\n🔍 Testando cidades do estado: {estado.codigo} - {estado.nome}")
        
        url = f'/alunos/api/localidade/estados/{estado.id}/cidades/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        cidades = response.json()
        print(f"✅ API retornou {len(cidades)} cidades")
        
        if len(cidades) > 0:
            print(f"   Primeiras 3 cidades: {[c['display'] for c in cidades[:3]]}")
        
        self.assertIsInstance(cidades, list)
    
    def test_03_api_bairros_por_cidade(self):
        """Testa se a API de bairros por cidade funciona."""
        if self.cidade_count == 0:
            self.skipTest("Sem cidades cadastradas no banco")
        
        # Pegar a primeira cidade
        cidade = Cidade.objects.first()
        print(f"\n🔍 Testando bairros da cidade: {cidade.nome}")
        
        url = f'/alunos/api/localidade/cidades/{cidade.id}/bairros/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        bairros = response.json()
        print(f"✅ API retornou {len(bairros)} bairros")
        
        if len(bairros) > 0:
            print(f"   Primeiros 3 bairros: {[b['nome'] for b in bairros[:3]]}")
        
        self.assertIsInstance(bairros, list)
    
    def test_04_javascript_present(self):
        """Verifica se o JavaScript de cascade está presente no HTML."""
        response = self.client.get('/alunos/criar/')
        
        content = response.content.decode('utf-8')
        
        # Verificar se o script de cascade está presente
        self.assertIn('carregarCidadesPorEstado', content)
        self.assertIn('carregarBairrosPorCidade', content)
        self.assertIn('id_estado_ref', content)
        
        print("\n✅ JavaScript de cascade encontrado no HTML")
    
    def test_05_flow_estado_to_cidade(self):
        """Simula o fluxo completo: seleciona estado, verifica cidades."""
        if self.estado_count == 0 or self.cidade_count == 0:
            self.skipTest("Dados insuficientes para teste de fluxo")
        
        # 1. Acessar formulário
        response = self.client.get('/alunos/criar/')
        self.assertEqual(response.status_code, 200)
        print("\n✅ Passo 1: Formulário carregado")
        
        # 2. Simular seleção de estado (AL)
        estado_al = Estado.objects.filter(codigo='AL').first()
        
        if estado_al:
            print(f"✅ Passo 2: Estado AL encontrado (ID: {estado_al.id})")
            
            # 3. Chamar API de cidades
            url = f'/alunos/api/localidade/estados/{estado_al.id}/cidades/'
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, 200)
            cidades = response.json()
            
            print(f"✅ Passo 3: API retornou {len(cidades)} cidades de AL")
            
            self.assertGreater(len(cidades), 0, "AL deveria ter cidades cadastradas")
            
            # 4. Simular seleção de cidade
            if len(cidades) > 0:
                primeira_cidade_id = cidades[0]['id']
                print(f"✅ Passo 4: Primeira cidade: {cidades[0]['display']}")
                
                # 5. Chamar API de bairros
                url_bairros = f'/alunos/api/localidade/cidades/{primeira_cidade_id}/bairros/'
                response_bairros = self.client.get(url_bairros)
                
                self.assertEqual(response_bairros.status_code, 200)
                bairros = response_bairros.json()
                
                print(f"✅ Passo 5: API retornou {len(bairros)} bairros")
                print("\n🎉 FLUXO COMPLETO TESTADO COM SUCESSO!")
        else:
            self.skipTest("Estado AL não encontrado no banco")
