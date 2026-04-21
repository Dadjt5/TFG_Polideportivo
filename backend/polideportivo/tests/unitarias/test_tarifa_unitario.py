from django.test import TestCase

from ...models import TarifaTDA


class TarifaTDAUnitariasTest(TestCase):

    def test_creacion_objeto(self):
        tarifa = TarifaTDA(
            precioUAM=10,
            precioOtros=20,
            precioReposicion=5
        )

        self.assertEqual(tarifa.precioUAM, 10)
        self.assertEqual(tarifa.precioOtros, 20)
        self.assertEqual(tarifa.precioReposicion, 5)

    def test_str_incluye_precios(self):
        tarifa = TarifaTDA(
            precioUAM=99,
            precioOtros=50
        )

        self.assertIn("99", str(tarifa))
        self.assertIn("50", str(tarifa))

    def test_herencia_abstracta(self):
        from ...models.tarifa import Tarifa

        self.assertTrue(issubclass(TarifaTDA, Tarifa))