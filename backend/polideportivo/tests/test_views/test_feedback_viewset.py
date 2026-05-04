from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from polideportivo.models import Feedback

User = get_user_model()


class FeedbackViewSetTests(APITestCase):

    def setUp(self):
        self.usuario_admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="1234"
        )

        self.usuario_normal = User.objects.create_user(
            username="usuario",
            email="usuario@test.com",
            password="1234"
        )

        Feedback.objects.create(
            usuario=self.usuario_admin,
            mensaje="Muy bien"
        )

    def test_superusuario_puede_listar_feedback(self):
        self.client.force_authenticate(user=self.usuario_admin)

        response = self.client.get("/api/v1/feedback/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_usuario_normal_no_puede_ver_feedback(self):
        self.client.force_authenticate(user=self.usuario_normal)

        response = self.client.get("/api/v1/feedback/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_usuario_anonimo_puede_crear_feedback(self):
        datos = {
            "mensaje": "Muy bien"
        }

        response = self.client.post("/api/v1/feedback/", datos)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.count(), 2)