from rest_framework.test import APITestCase
from rest_framework import status
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

        self.usuario_final = UsuarioFinal.objects.create(user=self.usuario_login)

        self.bono = Bono.objects.create(
            nombre="Bono 10 usos",
            precio=50
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
            estado=EstadoReserva.CANCELADA
        )

    def test_usuario_solo_ve_compras_confirmadas(self):
        self.client.force_authenticate(user=self.usuario_login)

        response = self.client.get("/api/compra-bono/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_crear_compra_asigna_usuario_final(self):
        self.client.force_authenticate(user=self.usuario_login)

        datos = {
            "bono": self.bono.id
        }

        response = self.client.post("/api/compra-bono/", datos)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        compra = CompraBono.objects.latest("id")
        self.assertEqual(compra.usuarioFinal, self.usuario_final)