from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth import get_user_model

from ...models import (
    Bono, CompraBono, UsuarioFinal, EstadoReserva, Rol
)

User = get_user_model()


class BonoUnitTest(TestCase):
    def test_str(self):
        bono = Bono.objects.create(
            usos=20,
            validez=2
        )

        self.assertEqual(
            str(bono),
            "Bono de 20 usos en un máximo de 2 años"
        )


class CompraBonoUnitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.usuario = UsuarioFinal.objects.create(
            esUAM=True,
            tieneAbono=False,
            tieneTDA=False,
            fechaNacimiento=date(2001,1,1),
            user=self.user
        )

        self.bono = Bono.objects.create(
            usos=10,
            precioTDA=5,
            precioUAM=8,
            precioAbono=6,
            precioOtros=10,
        )

        self.compra = CompraBono.objects.create(
            usuarioFinal=self.usuario,
            bono=self.bono
        )

    def test_contar(self):
        self.assertEqual(CompraBono.contar(), 1)

    def test_calcular_precio_uam(self):
        self.assertEqual(self.compra.calcularPrecio(), 8)

    def test_calcular_precio_tda(self):
        self.usuario.tieneTDA = True
        self.usuario.esUAM = False
        self.usuario.rol = Rol.EXTERNO
        self.usuario.save()

        self.assertEqual(self.compra.calcularPrecio(), 5)

    def test_calcular_precio_abono(self):
        self.usuario.tieneAbono = True
        self.usuario.save()

        self.assertEqual(self.compra.calcularPrecio(), 6)

    def test_confirmar_compra(self):
        self.compra.confirmarCompra()
        self.compra.refresh_from_db()

        self.assertEqual(
            self.compra.estado,
            EstadoReserva.CONFIRMADA
        )

    def test_cancelar_compra(self):
        self.compra.cancelarCompra()
        self.compra.refresh_from_db()

        self.assertEqual(
            self.compra.estado,
            EstadoReserva.CANCELADO
        )

    def test_usos_restantes(self):
        self.compra.vecesUsado = 3
        self.assertEqual(
            self.compra.usosRestantes,
            7
        )

    def test_activo(self):
        self.compra.fechaExpiracion = timezone.now() + timedelta(days=10)
        self.assertTrue(self.compra.activo)