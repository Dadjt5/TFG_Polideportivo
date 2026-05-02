from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from polideportivo.models import (
    UsuarioFinal,
    Monitor,
    Administrador,
    RolAdministrador
)

User = get_user_model()

class MeAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario",
            email="usuario@test.com",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user)
        self.user.is_usuario_final = True
        self.user.save()

    def test_usuario_autenticado_recibe_su_info(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["usuario_final_id"], self.usuario_final.id)
        self.assertIsNone(response.data["monitor_id"])
        self.assertIsNone(response.data["administrador_id"])
    
    def test_usuario_sin_relaciones(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNone(response.data["monitor_id"])
        self.assertIsNone(response.data["administrador_id"])


    def test_usuario_no_autenticado_no_puede_acceder(self):
        response = self.client.get("/api/me/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)