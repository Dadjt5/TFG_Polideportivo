from django.test import TestCase

from ...models import TarifaInstalacion


class TarifaInstalacionUnitariasTest(TestCase):

    def test_creacion_objeto(self):
        tarifa = TarifaInstalacion(
            precioAbonado=10,
            precioUAM=20,
            precioTDA=30,
            precioOtros=40,
            costeIluminacion=5
        )

        self.assertEqual(tarifa.precioAbonado, 10)
        self.assertEqual(tarifa.precioUAM, 20)
        self.assertEqual(tarifa.costeIluminacion, 5)

    def test_str(self):
        tarifa = TarifaInstalacion(precioUAM=99)

        self.assertIn("99", str(tarifa))

    def test_herencia_tarifa(self):
        from ...models.tarifa import Tarifa

        self.assertTrue(issubclass(TarifaInstalacion, Tarifa))