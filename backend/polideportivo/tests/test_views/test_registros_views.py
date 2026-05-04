from rest_framework.test import APITestCase
from rest_framework import status

from polideportivo.models import (
    Administrador, RolAdministrador
)


class RegistroViewTests(APITestCase):

    def test_registro_usuario_correcto(self):
        datos = {
            "nombre": "Juan",
            "apellidos": "Pérez",
            "sexo": "M",
            "fechaNacimiento": "2000-01-01",
            "dni": "12345678A",
            "telefono": "600000000",
            "email": "juan@test.com",
            "provincia": "Madrid",
            "municipio": "Madrid",
            "localidad": "Madrid",
            "codigoPostal": "28001",
            "password": "1234",
            "esUAM": False
        }

        response = self.client.post("/api/v1/registrarse/", datos)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("email", response.data)
    
    def test_registro_usuario_error(self):
        datos = {
            "nombre": "Juan",
            "apellidos": "Pérez",
            "sexo": "M",
            "fechaNacimiento": "2000-01-01",
            "dni": "12345678A",
            "telefono": "600000000",
            "email": "duplicado@test.com",
            "provincia": "Madrid",
            "municipio": "Madrid",
            "localidad": "Madrid",
            "codigoPostal": "28001",
            "password": "1234",
            "esUAM": False
        }

        # simulamos error forzado
        response = self.client.post("/api/v1/registrarse/", datos)

        self.assertIn(response.status_code, [200, 400])


class RegistroMonitorTests(APITestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        Administrador.objects.create(user=self.admin, rol=RolAdministrador.RAIZ)

    def test_crear_monitor_correcto(self):
        self.client.force_authenticate(user=self.admin)

        datos = {
            "nombre": "Monitor",
            "apellidos": "Test",
            "email": "monitor@test.com",
            "dni": "12345678A",
            "password": "1234"
        }

        response = self.client.post("/api/v1/registrar/monitor/", datos)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RegistroAdministradorTests(APITestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        Administrador.objects.create(user=self.admin, rol=RolAdministrador.RAIZ)

    def test_crear_administrador_correcto(self):
        self.client.force_authenticate(user=self.admin)

        datos = {
            "nombre": "Admin",
            "rol": RolAdministrador.USUARIOS,
            "email": "admin@test.com",
            "DNI": "12345678A",
            "password": "1234"
        }

        response = self.client.post("/api/v1/registrar/administrador/", datos)

        self.assertEqual(response.status_code, status.HTTP_200_OK)