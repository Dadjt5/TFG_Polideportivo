from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model

from ...models import (
    Bono, CompraBono, EstadoReserva, UsuarioFinal, Pabellon,
    Instalacion
)

User = get_user_model()


class CompraBonoIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user)

        self.pabellon = Pabellon.objects.create(nombre="general")
        self.instalacion = Instalacion.objects.create(nombre="sala 01", pabellon=self.pabellon)
        self.bono = Bono.objects.create(
            usos=10,
            validez=2,
            instalacion=self.instalacion
        )

    def test_compra_bono_crea_compra_pendiente(self):
        compra = CompraBono.compraBono(
            bono=self.bono,
            usuario=self.usuario
        )

        self.assertIsNotNone(compra)
        self.assertEqual(
            compra.estado,
            EstadoReserva.PENDIENTE
        )
        self.assertIsNotNone(compra.fechaExpiracion)

    def test_no_permita_compra_confirmada_duplicada(self):
        CompraBono.objects.create(
            usuarioFinal=self.usuario,
            bono=self.bono,
            estado=EstadoReserva.CONFIRMADA
        )

        compra = CompraBono.compraBono(
            bono=self.bono,
            usuario=self.usuario
        )

        self.assertIsNone(compra)

    def test_cancela_compra_pendiente_anterior(self):
        anterior = CompraBono.objects.create(
            usuarioFinal=self.usuario,
            bono=self.bono,
            estado=EstadoReserva.PENDIENTE
        )

        nueva = CompraBono.compraBono(
            bono=self.bono,
            usuario=self.usuario
        )

        anterior.refresh_from_db()

        self.assertEqual(
            anterior.estado,
            EstadoReserva.CANCELADO
        )
        self.assertEqual(
            nueva.estado,
            EstadoReserva.PENDIENTE
        )