from django.test import TestCase

from ...models import (
    ActividadComun,
    GrupoReducido,
    Fisioterapia
)


class TarifasUnitariasTest(TestCase):

    def test_actividad_comun_str(self):
        tarifa = ActividadComun(
            precioUAM=10,
            precioOtros=20,
            numeroHorasSemana=5
        )

        self.assertIn("UAM", str(tarifa))
        self.assertIn("5", str(tarifa))

    def test_grupo_reducido_str(self):
        tarifa = GrupoReducido(
            precio=100
        )

        self.assertIn("100", str(tarifa))

    def test_fisioterapia_str(self):
        tarifa = Fisioterapia(
            precioConsultaOtros=30,
            precioSesiones1_5Otros=50,
            precioSesiones6Otros=70
        )

        self.assertIn("30", str(tarifa))

    def test_herencia_tarifa_actividad(self):
        self.assertTrue(
            issubclass(ActividadComun, GrupoReducido.__bases__[0])
        )