from django.test import TestCase
from cargos.models import CargoAdministrativo


class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo="CARGO001",
            nome="Coordenador",
            descricao="Responsável pela coordenação do curso.",
        )
        self.assertEqual(cargo.nome, "Coordenador")
        self.assertEqual(cargo.codigo_cargo, "CARGO001")
