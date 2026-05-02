from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

from polideportivo.models import Actividad, Instalacion


class NuevaSesionViewTests(APITestCase):

    def setUp(self):
        self.instalacion = Instalacion.objects.create(
            nombre="Pista 1"
        )

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            instalacion=self.instalacion
        )

    @patch("polideportivo.views.Actividad.nuevaSesion")
    @patch("polideportivo.views.Instalacion.controlarHorarioActividad")
    def test_crear_sesiones_correctamente(self, mock_control, mock_nueva):

        mock_control.return_value = True
        mock_nueva.return_value = True

        self.client.force_authenticate(user=self._crear_admin_espacios())

        datos = [
            {
                "dia": "lunes",
                "horaInicio": "10:00",
                "horaFin": "11:00"
            }
        ]

        response = self.client.post(
            f"/api/v1/actividad/{self.actividad.id}/sesiones/",
            datos,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    @patch("polideportivo.views.Instalacion.controlarHorarioActividad")
    def test_horario_no_valido(self, mock_control):

        mock_control.return_value = False

        self.client.force_authenticate(user=self._crear_admin_espacios())

        response = self.client.post(
            f"/api/v1/actividad/{self.actividad.id}/sesiones/",
            [{
                "dia": "lunes",
                "horaInicio": "10:00",
                "horaFin": "11:00"
            }],
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class SesionesMonitorTests(APITestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.monitor_user = User.objects.create_user(
            username="monitor",
            password="1234"
        )
        self.monitor_user.is_monitor = True
        self.monitor_user.save()

    def test_obtener_sesiones_monitor(self):
        self.client.force_authenticate(user=self.monitor_user)

        response = self.client.get("/api/v1/monitor/1/sesiones/")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)


class DetalleSesionTests(APITestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.monitor_user = User.objects.create_user(
            username="monitor",
            password="1234"
        )
        self.monitor_user.is_monitor = True
        self.monitor_user.save()

    def test_detalle_sesion(self):
        self.client.force_authenticate(user=self.monitor_user)

        response = self.client.get("/api/v1/actividad/1/sesion/1/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("actividad", response.data)
        self.assertIn("participantes", response.data)


class GuardarAsistenciaTests(APITestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.monitor_user = User.objects.create_user(
            username="monitor",
            password="1234"
        )
        self.monitor_user.is_monitor = True
        self.monitor_user.save()

    def test_guardar_asistencia(self):
        self.client.force_authenticate(user=self.monitor_user)

        datos = {
            "participantes": [
                {
                    "id": 1,
                    "presente": True
                }
            ]
        }

        response = self.client.post(
            "/api/v1/actividad/1/sesion/1/asistencia/",
            datos,
            format="json"
        )

        self.assertEqual(response.status_code, 200)