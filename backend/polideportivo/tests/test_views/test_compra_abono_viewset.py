from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from polideportivo.models import (
    UsuarioFinal,
    CompraAbono,
    AbonoDeportivo,
    EstadoReserva
)

User = get_user_model()


class CompraAbonoViewSetTests(APITestCase):

    def setUp(self):
        self.usuario_login_1 = User.objects.create_user(
            username="usuario1",
            email="usuario1@test.com",
            password="1234"
        )

        self.usuario_login_2 = User.objects.create_user(
            username="usuario2",
            email="usuario2@test.com",
            password="1234"
        )

        self.usuario_final_1 = UsuarioFinal.objects.create(user=self.usuario_login_1)
        self.usuario_final_2 = UsuarioFinal.objects.create(user=self.usuario_login_2)

        self.abono = AbonoDeportivo.objects.create(
            nombre="Abono mensual",
            precio=20
        )

        # Compra que sí debe aparecer
        self.compra_visible = CompraAbono.objects.create(
            usuarioFinal=self.usuario_final_1,
            abono=self.abono,
            estado=EstadoReserva.CONFIRMADA
        )

        # Compra de otro usuario
        CompraAbono.objects.create(
            usuarioFinal=self.usuario_final_2,
            abono=self.abono,
            estado=EstadoReserva.CONFIRMADA
        )

        # Compra no confirmada
        CompraAbono.objects.create(
            usuarioFinal=self.usuario_final_1,
            abono=self.abono,
            estado=EstadoReserva.CANCELADA
        )

    def test_usuario_solo_ve_sus_compras_confirmadas(self):
        self.client.force_authenticate(user=self.usuario_login_1)

        response = self.client.get("/api/compra-abonos/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.compra_visible.id)