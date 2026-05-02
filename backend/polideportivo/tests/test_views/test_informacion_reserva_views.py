from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
import json

from polideportivo.models import (
    Actividad,
    Instalacion,
    ReservaActividad,
    Alquiler,
    Agenda,
    Descuento,
    TipoInstalacion,
    EstadoReserva,
    Dia
)

class TarifaActividadViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.user.usuario_final = True
        self.user.save()

        self.actividad = Actividad.objects.create(
            nombre="Actividad test"
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

        self.assertEqual(response.status_code, 403)

class TarifaInstalacionViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.user.usuario_final = True
        self.user.save()

        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion test",
            tipoInstalacion=TipoInstalacion.PISTA,
            luz=True,
            numeroCalles=0
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

        self.assertEqual(response.status_code, 403)


class ReservasPorDiaViewTests(APITestCase):

    def setUp(self):
        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion test",
            tipoInstalacion=TipoInstalacion.PISTA,
            numeroCalles=0
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