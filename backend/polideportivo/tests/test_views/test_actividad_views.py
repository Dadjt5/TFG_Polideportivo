from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
import json

from polideportivo.models import (
    Actividad,
    ActividadComun,
    Instalacion,
    Monitor,
    TipoInstalacion,
    Administrador,
    RolAdministrador,
    Pabellon
)


class NuevaActividadViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user2 = User.objects.create(username="user2", password="1234")

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.administrador = Administrador.objects.create(
            user=self.admin,
            rol=RolAdministrador.RAIZ
        )

        self.pabellon = Pabellon.objects.create()

        self.tarifa = ActividadComun.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.SALA_MUSCULACION,
            aforoMaximo=100
        )

        self.monitor = Monitor.objects.create(nombre="Monitor", user=self.user2)

    @patch("polideportivo.models.Instalacion.controlarHorarioActividad")
    @patch("polideportivo.models.Monitor.comprobarDisponibilidad")
    def test_crear_actividad_ok(self, mock_monitor, mock_instalacion):
        mock_monitor.return_value = True
        mock_instalacion.return_value = True

        self.client.force_authenticate(user=self.admin)

        data = {
            "actividad": json.dumps({
                "nombre": "Actividad test",
                "tarifa": self.tarifa.id,
                "instalacion": self.instalacion.id,
                "monitor": self.monitor.id
            }),
            "sesiones": json.dumps([
                {
                    "dia": "lunes",
                    "horaInicio": "10:00",
                    "horaFin": "11:00",
                    "calle": None
                }
            ]),
            "periodo": "2026",
            "deportes": json.dumps("baloncesto")
        }

        response = self.client.post("/api/v1/actividades/crear/", data)

        self.assertEqual(response.status_code, 201)

    @patch("polideportivo.models.Instalacion.controlarHorarioActividad")
    @patch("polideportivo.models.Monitor.comprobarDisponibilidad")
    def test_crear_actividad_monitor_ocupado(self, mock_monitor, mock_instalacion):
        mock_monitor.return_value = False
        mock_instalacion.return_value = True

        self.client.force_authenticate(user=self.admin)

        data = {
            "actividad": json.dumps({
                "nombre": "Actividad test",
                "tarifa": self.tarifa.id,
                "instalacion": self.instalacion.id,
                "monitor": self.monitor.id
            }),
            "sesiones": json.dumps([]),
            "periodo": "2026",
            "deportes": json.dumps("baloncesto")
        }

        response = self.client.post("/api/v1/actividades/crear/", data)

        self.assertEqual(response.status_code, 400)

    @patch("polideportivo.models.Instalacion.controlarHorarioActividad")
    @patch("polideportivo.models.Monitor.comprobarDisponibilidad")
    def test_crear_actividad_sin_auth(self, mock_monitor, mock_instalacion):
        mock_monitor.return_value = False
        mock_instalacion.return_value = True

        data = {
            "actividad": json.dumps({
                "nombre": "Actividad test"
            }),
            "sesiones": json.dumps([]),
            "periodo": "2026",
            "deportes": json.dumps("baloncesto")
        }

        response = self.client.post("/api/v1/actividades/crear/", data)

        self.assertEqual(response.status_code, 401)



class EditarActividadViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.administrador = Administrador.objects.create(
            user=self.admin,
            rol=RolAdministrador.RAIZ
        )

        self.user2 = User.objects.create(username="user2", password="1234")

        self.tarifa = ActividadComun.objects.create()
        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.SALA_MUSCULACION,
            aforoMaximo=100
        )

        self.monitor = Monitor.objects.create(nombre="Monitor", user=self.user2)

        self.actividad = Actividad.objects.create(
            nombre="Actividad",
            tarifa=self.tarifa,
            instalacion=self.instalacion,
            monitor=self.monitor
        )

    @patch("polideportivo.models.Instalacion.controlarHorarioActividad")
    @patch("polideportivo.models.Monitor.comprobarDisponibilidad")
    def test_editar_actividad_ok(self, mock_monitor, mock_instalacion):
        mock_monitor.return_value = True
        mock_instalacion.return_value = True

        self.client.force_authenticate(user=self.admin)

        data = {
            "actividad": json.dumps({
                "id": self.actividad.id,
                "tarifa": self.tarifa.id,
                "instalacion": self.instalacion.id,
                "monitor": self.monitor.id
            }),
            "sesiones": json.dumps([]),
            "periodo": "2026",
            "deportes": json.dumps("tenis")
        }

        response = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/editar/",
            data
        )

        self.assertEqual(response.status_code, 200)

    def test_editar_actividad_no_existe(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "actividad": json.dumps({
                "id": 999,
                "tarifa": self.tarifa.id,
                "instalacion": self.instalacion.id,
                "monitor": self.monitor.id
            }),
            "sesiones": json.dumps([]),
            "periodo": "2026",
            "deportes": json.dumps("tenis")
        }

        response = self.client.post("/api/v1/actividades/999/editar/", data)

        self.assertEqual(response.status_code, 400)

    def test_editar_actividad_error_generico(self):
        self.client.force_authenticate(user=self.admin)

        data = {}  # rompe el json internamente

        response = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/editar/",
            data
        )

        self.assertEqual(response.status_code, 400)