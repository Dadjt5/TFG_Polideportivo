from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

from polideportivo.models import Administrador, RolAdministrador

User = get_user_model()

class AdministradorViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.admin = Administrador.objects.create(
            user=self.user,
            rol=RolAdministrador.TARIFAS
        )

        self.user.administrador = self.admin
        self.user.save()

    def test_no_puede_crear_administrador_raiz(self):
        self.client.force_authenticate(user=self.user)

        datos = {
            "rol": RolAdministrador.RAIZ
        }

        response = self.client.post("/api/v1/administradores/", datos)

        self.assertEqual(response.status_code, 400)

    def test_no_puede_convertir_en_raiz(self):
        admin_objetivo = User.objects.create_user(
            username="admin2",
            password="1234"
        )

        admin_obj = Administrador.objects.create(
            user=admin_objetivo,
            rol=RolAdministrador.TARIFAS
        )

        admin_objetivo.administrador = admin_obj
        admin_objetivo.save()

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f"/api/v1/administradores/{admin_obj.id}/",
            {"rol": RolAdministrador.RAIZ}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_puede_eliminar_admin_raiz(self):
        raiz_user = User.objects.create_user(
            username="raiz",
            password="1234"
        )

        admin_raiz = Administrador.objects.create(
            user=raiz_user,
            rol=RolAdministrador.RAIZ
        )

        raiz_user.administrador = admin_raiz
        raiz_user.save()

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f"/api/v1/administradores/{admin_raiz.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)