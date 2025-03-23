from django.test import TestCase, Client
from django.urls import reverse
from cargos.models import CargoAdministrativo

class CargoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )

    def test_listar_cargos(self):
        response = self.client.get(reverse('cargos:listar_cargos_administrativos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coordenador')

    def test_detalhe_cargo(self):
        response = self.client.get(reverse('cargos:detalhe_cargo', args=[self.cargo.codigo_cargo]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coordenador')
        
    def test_criar_cargo(self):
        response = self.client.post(
            reverse('cargos:criar_cargo'),
            {
                'codigo_cargo': 'CARGO002',
                'nome': 'diretor',
                'descricao': 'Responsável pela direção do departamento.'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi criado e se o nome foi capitalizado corretamente
        cargo = CargoAdministrativo.objects.get(codigo_cargo='CARGO002')
        self.assertEqual(cargo.nome, 'Diretor')

    def test_editar_cargo(self):
        response = self.client.post(
            reverse('cargos:editar_cargo', args=[self.cargo.codigo_cargo]),
            {
                'codigo_cargo': 'CARGO001',
                'nome': 'coordenador sênior',
                'descricao': 'Coordenador com experiência avançada.'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi atualizado
        cargo = CargoAdministrativo.objects.get(codigo_cargo='CARGO001')
        self.assertEqual(cargo.nome, 'Coordenador Sênior')
        self.assertEqual(cargo.descricao, 'Coordenador com experiência avançada.')

    def test_excluir_cargo(self):
        response = self.client.post(
            reverse('cargos:excluir_cargo', args=[self.cargo.codigo_cargo])
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi excluído
        with self.assertRaises(CargoAdministrativo.DoesNotExist):
            CargoAdministrativo.objects.get(codigo_cargo='CARGO001')
