from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from polideportivo.models import (
    UsuarioFinal,
    Monitor,
    Administrador,
    Pabellon,
    Instalacion,
    TarifaInstalacion,
    TarifaTDA,
    ActividadComun,
    GrupoReducido,
    Fisioterapia,
    Configuracion
)

class GestionUsuariosViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador_usuarios = True
        self.admin.save()

        UsuarioFinal.objects.create(nombre="U1")
        Monitor.objects.create(nombre="M1")
        Administrador.objects.create(rol="A1")

    def test_get_usuarios_ok(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/v1/usuarios/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("usuariosFinales", response.data)
        self.assertIn("monitores", response.data)
        self.assertIn("administradores", response.data)

    def test_sin_auth(self):
        response = self.client.get("/api/v1/usuarios/")
        self.assertEqual(response.status_code, 403)

class GestionEspaciosViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador_espacios = True
        self.admin.save()

        Pabellon.objects.create(nombre="P1")
        Instalacion.objects.create(nombre="I1")

    def test_get_espacios_ok(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/v1/espacios/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("pabellones", response.data)
        self.assertIn("instalaciones", response.data)

    def test_sin_auth(self):
        response = self.client.get("/api/v1/espacios/")
        self.assertEqual(response.status_code, 403)


class GestionTarifasViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador_tarifas = True
        self.admin.save()

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
        self.assertEqual(response.status_code, 403)

    
class ObtenerConfiguracionViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

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

    def test_patch_configuracion_error(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            "/api/v1/configuracion/",
            {},
            format="json"
        )

        self.assertEqual(response.status_code, 400)