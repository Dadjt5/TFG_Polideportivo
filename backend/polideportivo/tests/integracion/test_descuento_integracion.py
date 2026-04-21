from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model

from ...models import (
    Descuento, Actividad, Instalacion, TipoInstalacion,
    Monitor, Pabellon, Deporte
)

User = get_user_model()


class DescuentoIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="monitor", password="1234")
        self.monitor = Monitor.objects.create(user=self.user)

        self.pabellon = Pabellon.objects.create()

        self.deporte = Deporte.objects.create(titulo="Yoga")

        self.instalacion = Instalacion.objects.create(
            nombre="Pista tenis",
            tipoInstalacion=TipoInstalacion.PISTA_TENIS,
            pabellon=self.pabellon
        )

        self.actividad = Actividad.objects.create(
            nombre="Tenis",
            instalacion=self.instalacion,
            monitor=self.monitor,
            deportes=self.deporte
        )

    def test_obtener_descuentos_por_actividad(self):
        d = Descuento.objects.create(
            nombre="Promo",
            porcentaje=10,
            fechaInicio=date(2024, 1, 1),
            fechaFinValidez=date(2026, 12, 31),
            combinable=True,
        )

        d.deportes.add(self.actividad.deportes)

        resultado = Descuento.obtenerDescuentos(
            actividad=self.actividad
        )

        self.assertIsNotNone(resultado)

    def test_obtener_descuentos_por_instalacion(self):
        d = Descuento.objects.create(
            nombre="Promo pista",
            porcentaje=15,
            fechaInicio=date(2024, 1, 1),
            fechaFinValidez=date(2026, 12, 31),
            combinable=True,
            tiposInstalacion=[TipoInstalacion.PISTA_TENIS]
        )

        resultado = Descuento.obtenerDescuentos(
            instalacion=self.instalacion
        )

        self.assertIsNotNone(resultado)

    def test_no_descuentos_fuera_fecha(self):
        Descuento.objects.create(
            nombre="Caducado",
            porcentaje=20,
            fechaInicio=date(2020, 1, 1),
            fechaFinValidez=date(2021, 1, 1)
        )

        resultado = Descuento.obtenerDescuentos(
            instalacion=self.instalacion
        )

        self.assertIsNone(resultado)