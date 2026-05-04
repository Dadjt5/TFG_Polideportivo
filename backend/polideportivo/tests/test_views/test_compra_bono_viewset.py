from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from django.contrib.auth import get_user_model

from polideportivo.models import (
    UsuarioFinal,
    CompraBono,
    Bono,
    EstadoReserva
)

User = get_user_model()


class CompraBonoViewSetTests(APITestCase):

    def setUp(self):
        self.usuario_login = User.objects.create_user(
            username="usuario",
            email="usuario@test.com",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.usuario_login, fechaNacimiento=date(2001,1,1))

        self.bono = Bono.objects.create(
            usos=10,
            precioOtros=50
        )

        # visible
        self.compra_visible = CompraBono.objects.create(
            usuarioFinal=self.usuario_final,
            bono=self.bono,
            estado=EstadoReserva.CONFIRMADA
        )

        # otro estado (no debe aparecer)
        CompraBono.objects.create(
            usuarioFinal=self.usuario_final,
            bono=self.bono,
            estado=EstadoReserva.CANCELADO
        )

    def test_usuario_solo_ve_compras_confirmadas(self):
        self.client.force_authenticate(user=self.usuario_login)

        response = self.client.get("/api/v1/compraBono/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)