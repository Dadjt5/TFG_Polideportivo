from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from polideportivo.models import TDA, UsuarioFinal

User = get_user_model()

class ValidarTDAViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user)

        self.tda = TDA.objects.create(
            usuarioFinal=None,
            codigo_qr="ABC123"
        )

    def test_validar_tda_correctamente(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/v1/tda/validar/", {
            "codigo": "ABC123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tda.refresh_from_db()

        self.assertEqual(self.tda.usuarioFinal, self.usuario_final)
    
    def test_codigo_invalido(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/v1/tda/validar/", {
            "codigo": "ERROR"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)