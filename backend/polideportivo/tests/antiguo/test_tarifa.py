from django.test import TestCase

from ..models import (
    ActividadComun, GrupoReducido, Fisioterapia, 
    TarifaInstalacion, TarifaTDA
)


class TarifaActividadTests(TestCase):

    # ----------------- ACTIVIDAD COMUN -----------------

    def test_str_actividad_comun(self):
        tarifa = ActividadComun.objects.create(
            precioUAM=10,
            precioOtros=20,
            numeroHorasSemana=3
        )

        texto = str(tarifa)

        self.assertIn("10", texto)
        self.assertIn("20", texto)
        self.assertIn("3", texto)

    # ----------------- GRUPO REDUCIDO -----------------

    def test_str_grupo_reducido(self):
        tarifa = GrupoReducido.objects.create(
            numeroHoras=2,
            numeroPersonas=5,
            precio=50
        )

        texto = str(tarifa)

        self.assertIn("50", texto)

    # ----------------- FISIOTERAPIA -----------------

    def test_str_fisioterapia(self):
        tarifa = Fisioterapia.objects.create(
            precioConsultaOtros=30,
            precioSesiones1_5Otros=25,
            precioSesiones6Otros=20
        )

        texto = str(tarifa)

        self.assertIn("30", texto)
        self.assertIn("25", texto)
        self.assertIn("20", texto)


class TarifaInstalacionTests(TestCase):

    # ----------------- STR -----------------

    def test_str_tarifa_instalacion(self):
        tarifa = TarifaInstalacion.objects.create(
            precioAbonado=5,
            precioUAM=10,
            precioTDA=8,
            precioOtros=15,
            costeIluminacion=3
        )

        texto = str(tarifa)



class TarifaTDATests(TestCase):

    # ----------------- STR -----------------

    def test_str_tarifa_tda(self):
        tarifa = TarifaTDA.objects.create(
            precioUAM=12,
            precioOtros=18,
            precioReposicion=5
        )

        texto = str(tarifa)

        self.assertIn("12", texto)
        self.assertIn("18", texto)