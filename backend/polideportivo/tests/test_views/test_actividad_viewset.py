from unittest.mock import patch, MagicMock
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date, time


from polideportivo.models import Actividad, Monitor, Asistencia, UsuarioFinal, Sesion, Pabellon, Instalacion

User = get_user_model()


class ActividadViewSetTests(APITestCase):

    def setUp(self):
        self.usuario_monitor = User.objects.create_user(
            username="monitor",
            email="monitor@test.com",
            password="1234"
        )

        self.monitor = Monitor.objects.create(user=self.usuario_monitor)

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Instalacion test"
        )

        self.actividad_monitor = Actividad.objects.create(
            nombre="Yoga",
            instalacion=self.instalacion,
            monitor=self.monitor
        )

        self.actividad_general = Actividad.objects.create(
            nombre="Pilates",
            instalacion=self.instalacion,
            monitor=self.monitor
        )

    def test_monitor_solo_ve_sus_actividades(self):
        self.client.force_authenticate(user=self.usuario_monitor)

        response = self.client.get("/api/v1/actividades/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], self.actividad_monitor.id)

    def test_usuario_anonimo_ve_todas_las_actividades(self):
        response = self.client.get("/api/v1/actividades/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    @patch("polideportivo.models.Pago.objects.get")
    @patch("polideportivo.models.Notificacion.notificarEliminacionActividad")
    def test_eliminar_actividad_cancela_pagos_y_envia_notificacion(
        self,
        mock_notificacion,
        mock_pago_get
    ):
        pago_mock = MagicMock()
        mock_pago_get.return_value = pago_mock

        self.client.force_authenticate(user=self.usuario_monitor)

        response = self.client.delete(f"/api/v1/actividades/{self.actividad_general.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(
            Actividad.objects.filter(id=self.actividad_general.id).exists()
        )


class AsistenciaViewSetTests(APITestCase):

    def setUp(self):
        self.usuario_login = User.objects.create_user(
            username="usuario",
            email="usuario@test.com",
            password="1234"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.usuario_login, fechaNacimiento=date(2001,1,1))

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Instalacion test"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            id=1,
            monitor=self.monitor,
            instalacion=self.instalacion,
            nombre="Actividad test"
        )

        self.sesion = Sesion.objects.create(actividad=self.actividad, horaInicio=time(9,0), horaFin=time(10,0))

        self.asistencia = Asistencia.objects.create(
            usuarioFinal=self.usuario_final,
            sesion=self.sesion
        )

    def test_usuario_final_solo_ve_sus_asistencias(self):
        self.client.force_authenticate(user=self.usuario_login)

        response = self.client.get("/api/v1/asistencias/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_crear_asistencia_asigna_usuario_final(self):
        self.client.force_authenticate(user=self.usuario_login)

        datos = {
            "sesion": self.sesion.id
        }

        response = self.client.post("/api/v1/asistencias/", datos)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        asistencia = Asistencia.objects.first()
        self.assertEqual(asistencia.usuarioFinal, self.usuario_final)