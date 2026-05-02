from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from ...models import (
    TDA, TarifaTDA, UsuarioFinal, EstadoReserva
)


class TDAUnitariasTest(TestCase):

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

        self.tarifa = TarifaTDA.objects.create(
            precioUAM=10,
            precioOtros=20
        )

    def test_str(self):
        tda = TDA.objects.create(
            tarifa=self.tarifa,
            fechaInicio=date.today(),
            fechaExpiracion=date.today()
        )

        self.assertEqual(str(tda), f"Tarjeta deportiva anual con fecha de inicio: {date.today()} y fecha de expiracion: {date.today()}")

    def test_calcular_precio_uam(self):
        tda = TDA(tarifa=self.tarifa, usuarioFinal=self.usuario)

        self.assertEqual(tda.calcularPrecio(), 10)

    def test_calcular_precio_externo(self):
        self.usuario.esUAM = False
        self.usuario.save()

        tda = TDA(tarifa=self.tarifa, usuarioFinal=self.usuario)

        self.assertEqual(tda.calcularPrecio(), 20)

    def test_compra_sin_tarifa(self):
        TarifaTDA.objects.all().delete()

        resultado = TDA.compraTDA(self.usuario)

        self.assertIsNone(resultado)
    
    def test_compra_con_tda_activa_devuelve_none(self):
        TDA.objects.create(
            usuarioFinal=self.usuario,
            estado=EstadoReserva.CONFIRMADA,
            tarifa=self.tarifa,
            fechaExpiracion=date.today()
        )

        resultado = TDA.compraTDA(self.usuario)

        self.assertIsNone(resultado)
    
    def test_compra_con_tda_pendiente(self):
        TDA.objects.create(
            usuarioFinal=self.usuario,
            estado=EstadoReserva.PENDIENTE,
            tarifa=self.tarifa,
            fechaExpiracion=date.today()
        )

        resultado = TDA.compraTDA(self.usuario)

        self.assertIsNotNone(resultado)

    def test_compra_con_tda_pendiente_pasada(self):
        TDA.objects.create(
            usuarioFinal=self.usuario,
            estado=EstadoReserva.CONFIRMADA,
            tarifa=self.tarifa,
            fechaExpiracion=date.today() - timedelta(days=1)
        )

        resultado = TDA.compraTDA(self.usuario)

        self.assertIsNotNone(resultado)