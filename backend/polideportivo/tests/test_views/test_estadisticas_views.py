from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import date
from django.contrib.auth import get_user_model

from polideportivo.models import (
    Actividad, Instalacion, Pabellon, Deporte,
    UsuarioFinal, Administrador, Monitor
)


class EstadisticasViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        Deporte.objects.create(titulo="Fútbol")

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create(nombre="Pabellón A")

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Pista 1"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            id=1,
            monitor=self.monitor,
            instalacion=self.instalacion,
            nombre="Yoga"
        )

    def test_estadisticas_devuelve_estructura_correcta(self):
        response = self.client.get("/api/v1/estadisticas/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("instalaciones", response.data)
        self.assertIn("actividades", response.data)
        self.assertIn("deportes", response.data)
        self.assertIn("usuarios", response.data)
        self.assertIn("tiposActividad", response.data)
        self.assertIn("tiposInstalacion", response.data)
        self.assertIn("tiposDeporte", response.data)
    
    
class TiposViewsTests(APITestCase):

    def test_tipos_devuelve_todos_los_catalogos(self):
        response = self.client.get("/api/v1/tipos/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("tiposActividad", response.data)
        self.assertIn("tiposInstalacion", response.data)
        self.assertIn("tiposReserva", response.data)
        self.assertIn("terrenos", response.data)
        self.assertIn("estados", response.data)
        self.assertIn("dias", response.data)
        self.assertIn("periodos", response.data)


class ObtenerEstadisticasAdministradorViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.administrador = Administrador.objects.create(user=self.admin)


    def test_estadisticas_admin_ok(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            "/api/v1/estadisticas/administrador/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("ingresos_mes", response.data)

    def test_estadisticas_con_filtros(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            "/api/v1/estadisticas/administrador/?mes=1&anio=2025"
        )

        self.assertEqual(response.status_code, 200)


class ObtenerEstadisticasUsuarioFinalViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

    def test_estadisticas_usuario_ok(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/v1/estadisticas/usuarioFinal/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("reservas_totales", response.data)

    def test_estadisticas_usuario_datos(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/v1/estadisticas/usuarioFinal/"
        )

        self.assertTrue("reservas_por_mes" in response.data)
        self.assertTrue("actividades_usuario" in response.data)