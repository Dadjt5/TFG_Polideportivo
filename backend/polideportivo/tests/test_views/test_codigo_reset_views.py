from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

from polideportivo.models import (
    CodigoResetPassword,
    UsuarioFinal
)

User = get_user_model()

class CodigoNuevaPasswordTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario",
            email="usuario@test.com",
            password="1234"
        )

    @patch("polideportivo.views.random.randint")
    @patch("polideportivo.views.send_mail")
    def test_enviar_codigo_correctamente(self, mock_send_mail, mock_random):
        mock_random.return_value = 123456

        response = self.client.post("/api/v1/codigo-nueva-password/", {
            "email": "usuario@test.com",
            "tipo": "enviar"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            CodigoResetPassword.objects.filter(email="usuario@test.com").exists()
        )

        mock_send_mail.assert_called_once()

    def test_email_no_existe(self):
        response = self.client.post("/api/v1/codigo-nueva-password/", {
            "email": "noexiste@test.com",
            "tipo": "enviar"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_verificar_codigo_correcto(self):
        user = self.user

        codigo = CodigoResetPassword.objects.create(
            email=user.email,
            codigo="123456"
        )

        UsuarioFinal.objects.create(user=user)

        response = self.client.post("/api/v1/codigo-nueva-password/", {
            "email": user.email,
            "tipo": "verificar",
            "codigo": "123456"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id_usuario", response.data)

    def test_codigo_invalido(self):
        response = self.client.post("/api/v1/codigo-nueva-password/", {
            "email": "usuario@test.com",
            "tipo": "verificar",
            "codigo": "000000"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_codigo_invalido(self):
        response = self.client.post("/api/v1/codigo-nueva-password/", {
            "email": "usuario@test.com",
            "tipo": "verificar",
            "codigo": "000000"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_tipo_invalido(self):
        response = self.client.post("/api/v1/codigo-nueva-password/", {
            "email": "usuario@test.com",
            "tipo": "otro"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)