from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from datetime import date

from polideportivo.models import (
    UsuarioFinal, Monitor, Administrador, Pabellon, Instalacion,
    TarifaInstalacion, TarifaTDA, ActividadComun, GrupoReducido,
    Fisioterapia, Configuracion, RolAdministrador
)

class GestionUsuariosViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.monitor = User.objects.create_user(
            username="monitor",
            password="1234"
        )

        UsuarioFinal.objects.create(nombre="U1", fechaNacimiento=date(2001,1,1), user=self.user)
        Monitor.objects.create(nombre="M1", user=self.monitor)
        Administrador.objects.create(rol=RolAdministrador.USUARIOS, user=self.admin)

    def test_get_usuarios_ok(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/v1/usuarios/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("usuariosFinales", response.data)
        self.assertIn("monitores", response.data)
        self.assertIn("administradores", response.data)

    def test_sin_auth(self):
        response = self.client.get("/api/v1/usuarios/")
        self.assertEqual(response.status_code, 401)

class GestionEspaciosViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        Administrador.objects.create(rol=RolAdministrador.ESPACIOS, user=self.admin)

        self.pabellon = Pabellon.objects.create(nombre="P1")
        Instalacion.objects.create(nombre="I1", pabellon=self.pabellon)

    def test_get_espacios_ok(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/v1/espacios/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("pabellones", response.data)
        self.assertIn("instalaciones", response.data)

    def test_sin_auth(self):
        response = self.client.get("/api/v1/espacios/")
        self.assertEqual(response.status_code, 401)


class GestionTarifasViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        Administrador.objects.create(rol=RolAdministrador.TARIFAS, user=self.admin)

        TarifaInstalacion.objects.create(titulo="TI1")
        TarifaTDA.objects.create(titulo="T1")
        ActividadComun.objects.create(titulo="A1")
        GrupoReducido.objects.create(titulo="G1")
        Fisioterapia.objects.create(titulo="F1")

    def test_get_tarifas_ok(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/v1/tarifas/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("tarifasInstalacion", response.data)
        self.assertIn("tarifasTDA", response.data)
        self.assertIn("tarifasActividadComun", response.data)
        self.assertIn("tarifasGrupoReducido", response.data)
        self.assertIn("tarifasFisioterapia", response.data)

    def test_sin_auth(self):
        response = self.client.get("/api/v1/tarifas/")
        self.assertEqual(response.status_code, 401)

    
class ObtenerConfiguracionViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        Administrador.objects.create(rol=RolAdministrador.RAIZ, user=self.user)

        Configuracion.objects.create()

    def test_get_configuracion_ok(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/v1/configuracion/")

        self.assertEqual(response.status_code, 200)

    def test_patch_configuracion_ok(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "clave": "valor"
        }

        response = self.client.patch(
            "/api/v1/configuracion/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_patch_configuracion_ok(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            "/api/v1/configuracion/",
            {},
            format="json"
        )

        self.assertEqual(response.status_code, 200)