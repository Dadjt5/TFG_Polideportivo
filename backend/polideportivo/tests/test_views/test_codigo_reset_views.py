from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch
from datetime import timedelta, date
from django.utils import timezone

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

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

    @patch("api.views.resend.Emails.send")
    @patch("api.views.random.randint")
    def test_enviar_codigo_correctamente(self, mock_random, mock_resend):
        mock_random.return_value = 123456
        mock_resend.return_value = {"id": "email_test"}

        response = self.client.post("/api/v1/password_reset/", {
            "email": "usuario@test.com",
            "tipo": "enviar"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            CodigoResetPassword.objects.filter(email="usuario@test.com").exists()
        )

        mock_resend.assert_called_once()

    def test_email_no_existe(self):
        response = self.client.post("/api/v1/password_reset/", {
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

        response = self.client.post("/api/v1/password_reset/", {
            "email": user.email,
            "tipo": "verificar",
            "codigo": "123456"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id_usuario", response.data)

    def test_codigo_invalido(self):
        response = self.client.post("/api/v1/password_reset/", {
            "email": "usuario@test.com",
            "tipo": "verificar",
            "codigo": "000000"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_tipo_invalido(self):
        response = self.client.post("/api/v1/password_reset/", {
            "email": "usuario@test.com",
            "tipo": "otro"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)