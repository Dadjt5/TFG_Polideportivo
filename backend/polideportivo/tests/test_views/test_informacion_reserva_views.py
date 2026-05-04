from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
import json

from polideportivo.models import (
    Actividad, Instalacion, TipoInstalacion, UsuarioFinal, Pabellon, TarifaInstalacion,
    Monitor, ActividadComun
)

class TarifaActividadViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Instalacion test"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.tarifa = ActividadComun.objects.create()

        self.actividad = Actividad.objects.create(
            id=1,
            monitor=self.monitor,
            instalacion=self.instalacion,
            nombre="Actividad test",
            tarifa=self.tarifa
        )

    def test_obtener_tarifa_actividad_ok(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"/api/v1/tarifas/actividades/{self.actividad.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("tarifa", response.data)
        self.assertIn("descuento", response.data)

    def test_sin_auth(self):
        response = self.client.get(
            f"/api/v1/tarifas/actividades/{self.actividad.id}/"
        )

        self.assertEqual(response.status_code, 401)

class TarifaInstalacionViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.pabellon = Pabellon.objects.create()

        self.tarifa = TarifaInstalacion.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion test",
            tipoInstalacion=TipoInstalacion.SALA_MULTIUSOS,
            luz=True,
            pabellon=self.pabellon,
            numeroCalles=0,
            tarifa=self.tarifa
        )

    def test_tarifa_instalacion_ok(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"/api/v1/tarifas/instalaciones/{self.instalacion.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("tarifa", response.data)

    def test_tarifa_con_fecha(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"/api/v1/tarifas/instalaciones/{self.instalacion.id}/?fecha=2026-04-30"
        )

        self.assertEqual(response.status_code, 200)

    def test_sin_auth(self):
        response = self.client.get(
            f"/api/v1/tarifas/instalaciones/{self.instalacion.id}/"
        )

        self.assertEqual(response.status_code, 401)


class ReservasPorDiaViewTests(APITestCase):

    def setUp(self):
        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion test",
            tipoInstalacion=TipoInstalacion.SALA_MULTIUSOS,
            numeroCalles=0,
            pabellon=self.pabellon,
        )

        self.fecha = date.today()

    def test_reservas_por_dia_ok(self):
        response = self.client.get(
            f"/api/v1/instalaciones/{self.instalacion.id}/obtener/alquileres/?fecha={self.fecha}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("abierto", response.data)

    def test_instalacion_sin_agenda(self):
        response = self.client.get(
            f"/api/v1/instalaciones/{self.instalacion.id}/obtener/alquileres/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("slots", response.data)