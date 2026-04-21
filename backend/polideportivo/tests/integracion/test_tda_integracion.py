from django.test import TestCase
from unittest.mock import patch
from datetime import date
from django.contrib.auth import get_user_model

from ...models import (
    TDA, TarifaTDA, EstadoReserva, UsuarioFinal
)


class TDAIntegracionTest(TestCase):
    def setUp(self):
        User = get_user_model()

        self.tarifa = TarifaTDA.objects.create(
            precioUAM=10,
            precioOtros=20
        )

        self.user = User.objects.create(
            username="usuario_test",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(
            nombre="usuario_test",
            user=self.user,
            fechaNacimiento=date(2001,1,1),
            esUAM=True
        )

    def test_contar_tdas(self):
        self.assertEqual(TDA.contar(), 0)

    def test_creacion_tda(self):
        tda = TDA.objects.create(
            usuarioFinal=self.usuario,
            tarifa=self.tarifa,
            estado=EstadoReserva.PENDIENTE
        )

        self.assertIsNotNone(tda.id)

    def test_calcular_precio_real(self):
        tda = TDA.objects.create(
            usuarioFinal=self.usuario,
            tarifa=self.tarifa
        )

        self.assertEqual(tda.calcularPrecio(), 10)

    def test_creacion_tda(self):
        tda = TDA.objects.create(
            usuarioFinal=self.usuario,
            tarifa=self.tarifa,
            estado=EstadoReserva.PENDIENTE
        )

        self.assertIsNotNone(tda.id)
    
    def test_compra_tda_flujo_completo(self):
        tda = TDA.compraTDA(self.usuario)

        self.assertIsNotNone(tda)
        self.assertEqual(tda.usuarioFinal, self.usuario)
        self.assertEqual(tda.estado, EstadoReserva.PENDIENTE)
        self.assertIsNotNone(tda.fechaExpiracion)

        tda.confirmarCompra()
        self.assertTrue(tda.usuarioFinal.tieneTDA)
        self.assertEqual(tda.estado, EstadoReserva.CONFIRMADA)

        tda.cancelarCompra()
        self.assertFalse(TDA.objects.filter(usuarioFinal=self.usuario).exists())

    def test_calcular_precio_real(self):
        tda = TDA.objects.create(
            usuarioFinal=self.usuario,
            tarifa=self.tarifa
        )

        self.assertEqual(tda.calcularPrecio(), 10)