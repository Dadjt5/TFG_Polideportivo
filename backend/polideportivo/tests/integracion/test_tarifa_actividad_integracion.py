from django.test import TestCase

from ...models import (
    ActividadComun,
    GrupoReducido,
    Fisioterapia
)


class TarifasIntegracionTest(TestCase):

    def test_creacion_actividad_comun_db(self):
        tarifa = ActividadComun.objects.create(
            precioUAM=10,
            precioOtros=20,
            numeroHorasSemana=5
        )

        self.assertIsNotNone(tarifa.id)
        self.assertEqual(tarifa.numeroHorasSemana, 5)

    def test_creacion_grupo_reducido_db(self):
        tarifa = GrupoReducido.objects.create(
            precio=100,
            numeroHoras=2,
            numeroPersonas=4
        )

        self.assertEqual(tarifa.precio, 100)

    def test_creacion_fisioterapia_db(self):
        tarifa = Fisioterapia.objects.create(
            precioConsultaUAM=10,
            precioConsultaOtros=20
        )

        self.assertTrue(tarifa.id is not None)