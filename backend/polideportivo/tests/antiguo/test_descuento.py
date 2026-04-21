from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta, date

from ..models import Descuento, Deporte, TipoInstalacion, Pabellon, Instalacion

class DescuentoTests(TestCase):
    def setUp(self):
        self.futbol = Deporte.objects.create(titulo="Fútbol")
        self.baloncesto = Deporte.objects.create(titulo="Baloncesto")

        self.hoy = now().date()
        self.ayer = self.hoy - timedelta(days=1)
        self.manana = self.hoy + timedelta(days=1)

        pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(pabellon=pabellon)

        self.desc1 = Descuento.objects.create(
            nombre="Descuento 10%",
            porcentaje=10,
            combinable=True,
            prioritario=False,
            tiposInstalacion=[TipoInstalacion.PISCINA],
            fechaInicio=date(2000, 1, 1),
            fechaFinValidez=date(3000, 2, 1)
        )

        self.desc1.deportes.add(self.futbol)

        self.desc2 = Descuento.objects.create(
            nombre="Descuento 20%",
            porcentaje=20,
            combinable=False,
            prioritario=True,
            tiposInstalacion=[TipoInstalacion.SALA_MUSCULACION],
            fechaInicio=date(2000, 1, 1),
            fechaFinValidez=date(3000, 2, 1)
        )

        self.desc2.deportes.add(self.baloncesto)


    # ----------------- STR -----------------

    def test_str_descuento(self):
        self.assertIn("Descuento 10%", str(self.desc1))
        self.assertIn("10%", str(self.desc1))


    # ----------------- CONTAR -----------------

    def test_contar_descuentos(self):
        self.assertEqual(Descuento.contar(), 2)


    # ----------------- CALCULAR PORCENTAJE -----------------

    def test_calcular_porcentaje(self):
        total = Descuento._calcular_porcentaje([self.desc1, self.desc2])
        self.assertEqual(total, 30)


    # ----------------- PRIORITARIO Y COMBINABLE -----------------

    def test_filtrar_descuentos_prioritario(self):
        resultado = Descuento._filtrar_descuentos(Descuento.objects.all())

        # Desc2 es prioritario por lo que solo se elige Desc2
        self.assertEqual(resultado['porcentaje_total'], 20)
        self.assertEqual(resultado['descuentos'][0], self.desc2)

    def test_filtrar_descuentos_combinables(self):
        self.desc2.prioritario = False
        self.desc2.save()

        resultado = Descuento._filtrar_descuentos(Descuento.objects.all())

        self.assertEqual(resultado['porcentaje_total'], 20)
        self.assertIn(self.desc2, resultado['descuentos'])


    # ----------------- OBTENER DESCUENTOS -----------------

    def test_obtener_descuentos_por_deporte(self):
        class ActividadMock:
            def __init__(self, deporte, instalacion):
                self.deportes = deporte
                self.instalacion = instalacion

        actividad = ActividadMock(
            deporte=self.futbol,
            instalacion=self.instalacion
        )

        resultado = Descuento.obtenerDescuentos(actividad=actividad)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['porcentaje_total'], 10)
        self.assertIn(self.desc1, resultado['descuentos'])

    def test_obtener_descuentos_por_instalacion(self):
        class InstalacionMock:
            tipoInstalacion = TipoInstalacion.PISCINA
        resultado = Descuento.obtenerDescuentos(instalacion=InstalacionMock())

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['porcentaje_total'], 10)
        self.assertIn(self.desc1, resultado['descuentos'])