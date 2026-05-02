from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from polideportivo.models import (
    ReservaActividad,
    Alquiler,
    Pago,
    Actividad,
    Instalacion,
    Pabellon,
    Sesion,
    Deporte,
    Monitor,
    UsuarioFinal,
    EstadoReserva,
    EstadoPago
)


class EstadisticasViewTests(APITestCase):

    def setUp(self):
        Deporte.objects.create(titulo="Fútbol")
        Instalacion.objects.create(nombre="Pista 1")
        Actividad.objects.create(nombre="Yoga")
        Pabellon.objects.create(nombre="Pabellón A")

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

        self.usuario_final = self.user

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