from django.test import TestCase
from unittest.mock import patch, MagicMock, PropertyMock
from decimal import Decimal

from ...models import Pago, EstadoPago, TipoPago


class PagoUnitariasTest(TestCase):

    def setUp(self):
        self.usuario = MagicMock()
        self.usuario.id = 1
        self.usuario.user.email = "test@test.com"

        self.objeto = MagicMock()
        self.objeto = MagicMock(spec=[
            'id', 'calcularPrecio', 'calcularDescuento', 'confirmarCompra', 'cancelarCompra'
        ])

        self.objeto.id = 10
        self.objeto.calcularPrecio.return_value = 100
        self.objeto.calcularDescuento.return_value = {}

        self.config = MagicMock()
        self.config.porcentaje_maximo = 50

    @patch("django.contrib.contenttypes.models.ContentType.objects.get_for_model")
    @patch("polideportivo.models.Pago.objects.create")
    @patch("polideportivo.models.Configuracion.objects.first")
    def test_nuevo_pago_calculo_basico(self, mock_config, mock_create, mock_content_type):
        mock_config.return_value = self.config
        mock_create.return_value = MagicMock()
        mock_content_type.return_value = MagicMock(pk=1)

        Pago.nuevoPago(
            concepto="test",
            usuario=self.usuario,
            tipo=TipoPago.UNICO,
            objeto=self.objeto
        )

        self.objeto.calcularPrecio.assert_called_once()

    def test_contar(self):
        with patch("polideportivo.models.Pago.objects.count", return_value=5):
            self.assertEqual(Pago.contar(), 5)

    def test_contar_dinero(self):
        with patch("polideportivo.models.Pago.objects.filter") as mock_filter:
            mock_filter.return_value.aggregate.return_value = {"total": 200}
            self.assertEqual(Pago.contarDinero(), 200)

    def test_confirmar_pago(self):
        pago = MagicMock()
        pago.objeto = MagicMock()

        Pago.confirmarPago(pago)

        pago.objeto.confirmarCompra.assert_called_once()
        self.assertEqual(pago.estadoPago, EstadoPago.PAGADO)

    @patch("stripe.Refund.create")
    def test_cancelar_pago_unico(self, mock_refund):
        pago = MagicMock()
        pago.stripe_payment_intent = "pi_123"
        pago.objeto = MagicMock()

        Pago.cancelarPago(pago, tipo="unico")

        mock_refund.assert_called_once()
        pago.objeto.cancelarCompra.assert_called_once()
        
    def test_str_pago(self):
        pago = Pago(
            concepto="reserva pista",
            coste=50,
            estadoPago=EstadoPago.PENDIENTE
        )

        self.assertEqual(str(pago), "Pago reserva pista, de coste 50 en estado Pendiente de pago")
    
    def test_contar(self):
        with patch("polideportivo.models.Pago.objects.count", return_value=7):
            self.assertEqual(Pago.contar(), 7)
    
    def test_contar_dinero_sin_pagos(self):
        with patch("polideportivo.models.Pago.objects.filter") as mock_filter:
            mock_filter.return_value.aggregate.return_value = {"total": None}
            self.assertEqual(Pago.contarDinero(), 0)
    
    @patch("stripe.Subscription.delete")
    def test_cancelar_pago_subscripcion_unitario(self, mock_delete):
        pago = Pago(
            concepto="test",
            stripe_subscription_id="sub_123"
        )

        mock_objeto = MagicMock()

        with patch.object(Pago, "objeto", new_callable=PropertyMock) as mock_objeto_prop:
            mock_objeto_prop.return_value = mock_objeto

            with patch.object(pago, "save") as mock_save:
                resultado = pago.cancelarPago(tipo="subscripcion")

                mock_delete.assert_called_once_with("sub_123")
                mock_objeto.cancelarCompra.assert_called_once()
                self.assertEqual(pago.estadoPago, EstadoPago.CANCELADO)
                self.assertIsNone(pago.stripe_payment_intent)
                self.assertIsNone(pago.stripe_price_id)
                self.assertIsNone(pago.stripe_subscription_id)
                mock_save.assert_called_once()
                self.assertTrue(resultado)