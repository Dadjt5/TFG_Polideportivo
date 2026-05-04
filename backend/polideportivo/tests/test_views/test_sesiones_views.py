from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth import get_user_model
from datetime import time, date

from polideportivo.models import Actividad, Instalacion, Monitor, Pabellon, Sesion, UsuarioFinal, Asistencia, RolAdministrador, Administrador


class NuevaSesionViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Pista 1",
            pabellon=self.pabellon
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            monitor=self.monitor,
            instalacion=self.instalacion
        )

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        Administrador.objects.create(user=self.admin, rol=RolAdministrador.RAIZ)

    @patch("polideportivo.models.Actividad.nuevaSesion")
    @patch("polideportivo.models.Instalacion.controlarHorarioActividad")
    def test_crear_sesiones_correctamente(self, mock_control, mock_nueva):

        mock_control.return_value = True
        mock_nueva.return_value = True

        self.client.force_authenticate(user=self.admin)

        datos = [
            {
                "dia": "lunes",
                "horaInicio": "10:00",
                "horaFin": "11:00"
            }
        ]

        response = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/sesion/",
            datos,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    @patch("polideportivo.models.Instalacion.controlarHorarioActividad")
    def test_horario_no_valido(self, mock_control):

        mock_control.return_value = False

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/sesion/",
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

        Monitor.objects.create(user=self.monitor_user)

    def test_obtener_sesiones_monitor(self):
        self.client.force_authenticate(user=self.monitor_user)

        response = self.client.get("/api/v1/monitores/1/sesiones/")

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

        self.monitor = Monitor.objects.create(user=self.monitor_user)

        self.user = User.objects.create_user(
            username="user2",
            password="1234"
        )
        
        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Pista 1",
            pabellon=self.pabellon
        )

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            monitor=self.monitor,
            instalacion=self.instalacion
        )

        self.sesion = Sesion.objects.create(actividad=self.actividad, horaInicio=time(9,0), horaFin=time(10,0))

    def test_detalle_sesion(self):
        self.client.force_authenticate(user=self.monitor_user)

        response = self.client.get(f"/api/v1/actividades/{self.actividad.id}/sesiones/{self.sesion.id}/")

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
        
        self.monitor = Monitor.objects.create(user=self.monitor_user)

        self.user = User.objects.create_user(
            username="user2",
            password="1234"
        )
        
        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Pista 1",
            pabellon=self.pabellon
        )

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            monitor=self.monitor,
            instalacion=self.instalacion
        )

        self.sesion = Sesion.objects.create(actividad=self.actividad, horaInicio=time(9,0), horaFin=time(10,0))

        Asistencia.objects.create(usuarioFinal=self.usuario, sesion=self.sesion)

    def test_guardar_asistencia(self):
        self.client.force_authenticate(user=self.monitor_user)

        datos = {
            "participantes": [
                {
                    "id": self.usuario.id,
                    "presente": True
                }
            ]
        }

        response = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/sesiones/{self.sesion.id}/asistencia/",
            datos,
            format="json"
        )

        self.assertEqual(response.status_code, 200)