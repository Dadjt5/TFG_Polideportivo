from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from unittest.mock import Mock, patch
from datetime import date

from ..models import (
    Pago, UsuarioFinal, Configuracion, EstadoPago, TipoPago,
    CompraBono, Bono
)


class PagoTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user1",
            email="test@test.com",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(
            user=self.user,
            fechaNacimiento=date(2000, 1, 1)
        )

        bono = Bono.objects.create(
            usos=5,
            validez=2,
            precioTDA=10,
            precioUAM=15,
            precioAbono=12,
            precioOtros=100
        )

        self.objeto = CompraBono.compraBono(bono=bono, usuario=self.usuario)
        self.content_type = ContentType.objects.get_for_model(CompraBono)

        Configuracion.objects.create(porcentaje_maximo=50)

    # ----------------- STR -----------------

    def test_str(self):
        pago = Pago.objects.create(
            concepto="Test",
            coste=100,
            usuarioFinal=self.usuario,
            content_type=self.content_type,
            object_id=1
        )

        self.assertIn("Pago Test", str(pago))

    # ----------------- CONTAR -----------------

    def test_contar(self):
        Pago.objects.create(concepto="P1", usuarioFinal=self.usuario,
                            content_type=self.content_type, object_id=1)
        Pago.objects.create(concepto="P2", usuarioFinal=self.usuario,
                            content_type=self.content_type, object_id=1)

        self.assertEqual(Pago.contar(), 2)

    # ----------------- DINERO -----------------

    def test_contarDinero(self):
        Pago.objects.create(
            concepto="P1",
            costeFinal=50,
            estadoPago=EstadoPago.PAGADO,
            usuarioFinal=self.usuario,
            content_type=self.content_type,
            object_id=1
        )

        Pago.objects.create(
            concepto="P2",
            costeFinal=30,
            estadoPago=EstadoPago.PAGADO,
            usuarioFinal=self.usuario,
            content_type=self.content_type,
            object_id=1
        )

        self.assertEqual(Pago.contarDinero(), 80)

    # ----------------- NUEVO PAGO -----------------

    def test_nuevoPago(self):
        pago = Pago.nuevoPago(
            concepto="Pago Test",
            usuario=self.usuario,
            tipo=TipoPago.UNICO,
            objeto=self.objeto
        )

        self.assertEqual(pago.coste, 100)
        self.assertEqual(pago.descuentoAplicado, 0)
        self.assertEqual(pago.estadoPago, EstadoPago.PENDIENTE)

    # ----------------- CONFIRMAR -----------------

    def test_confirmarPago(self):
        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.UNICO, self.objeto)
        pago.objeto = self.objeto

        result = pago.confirmarPago()

        self.assertTrue(result)
        self.assertEqual(pago.estadoPago, EstadoPago.PAGADO)

    # ----------------- CANCELAR -----------------

    @patch("stripe.Refund.create")
    def test_cancelarPago_unico(self, refund_mock):
        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.UNICO, self.objeto)
        pago.objeto = self.objeto
        pago.stripe_payment_intent = "pi_test"

        result = pago.cancelarPago(tipo="unico")

        self.assertTrue(result)
        self.assertEqual(pago.estadoPago, EstadoPago.CANCELADO)
        refund_mock.assert_called_once()

    @patch("stripe.Subscription.delete")
    def test_cancelarPago_subscripcion(self, subs_mock):
        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.MENSUAL, self.objeto)
        pago.objeto = self.objeto
        pago.stripe_subscription_id = "sub_test"

        pago.cancelarPago(tipo="subscripcion")

        subs_mock.assert_called_once()

    # ----------------- COMPROBAR PAGO -----------------

    @patch("stripe.PaymentIntent.retrieve")
    def test_comprobarPago_unico(self, intent_mock):
        intent_mock.return_value.status = "succeeded"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.UNICO, self.objeto)
        pago.stripe_payment_intent = "pi_test"

        self.assertTrue(pago.comprobarPago())

    @patch("stripe.PaymentIntent.retrieve")
    def test_comprobarPago_unico_false(self, intent_mock):
        intent_mock.return_value.status = "requires_payment_method"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.UNICO, self.objeto)
        pago.stripe_payment_intent = "pi_test"

        self.assertFalse(pago.comprobarPago())

    @patch("stripe.Subscription.retrieve")
    def test_comprobarPago_subscripcion(self, sub_mock):
        sub_mock.return_value.status = "active"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.MENSUAL, self.objeto)
        pago.stripe_subscription_id = "sub_test"

        self.assertTrue(pago.comprobarPago())

    @patch("stripe.Subscription.retrieve")
    def test_comprobarPago_subscripcion_false(self, sub_mock):
        sub_mock.return_value.status = "canceled"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.MENSUAL, self.objeto)
        pago.stripe_subscription_id = "sub_test"

        self.assertFalse(pago.comprobarPago())

    # ----------------- PAGO UNICO STRIPE -----------------

    @patch("stripe.PaymentIntent.create")
    def test_aplicarPagoUnico(self, intent_mock):
        intent_mock.return_value.id = "pi_test"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.UNICO, self.objeto)
        pago.aplicarPagoUnico(self.usuario)

        self.assertEqual(pago.stripe_payment_intent, "pi_test")

    # ----------------- SUBSCRIPCIONES -----------------

    @patch("stripe.Subscription.create")
    @patch("stripe.Price.create")
    @patch("stripe.Customer.create")
    def test_aplicarSubscripcion(self, customer_mock, price_mock, sub_mock):
        customer_mock.return_value.id = "cus_test"
        price_mock.return_value.id = "price_test"
        sub_mock.return_value.id = "sub_test"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.MENSUAL, self.objeto)

        pago.aplicarSubscripcion(self.usuario)

        self.assertEqual(pago.stripe_subscription_id, "sub_test")

    @patch("stripe.Subscription.create")
    @patch("stripe.Price.create")
    @patch("stripe.Customer.create")
    def test_aplicarSubscripcion_cuatrimestral(self, customer_mock, price_mock, sub_mock):
        customer_mock.return_value.id = "cus_test"
        price_mock.return_value.id = "price_test"
        sub_mock.return_value.id = "sub_test"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.CUATRIMESTRAL, self.objeto)
        pago.aplicarSubscripcion(self.usuario)

        args = price_mock.call_args[1]
        self.assertEqual(args["recurring"]["interval_count"], 4)

    @patch("stripe.Subscription.create")
    @patch("stripe.Price.create")
    @patch("stripe.Customer.create")
    def test_aplicarSubscripcion_anual(self, customer_mock, price_mock, sub_mock):
        customer_mock.return_value.id = "cus_test"
        price_mock.return_value.id = "price_test"
        sub_mock.return_value.id = "sub_test"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.ANUAL, self.objeto)
        pago.aplicarSubscripcion(self.usuario)

        args = price_mock.call_args[1]
        self.assertEqual(args["recurring"]["interval"], "year")

    @patch("stripe.Subscription.create")
    @patch("stripe.Price.create")
    def test_aplicarSubscripcion_price_existente(self, price_mock, sub_mock):
        self.usuario.stripe_customer_id = "cus_existente"
        self.usuario.save()

        price_mock.return_value.id = "price_test"
        sub_mock.return_value.id = "sub_test"

        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.MENSUAL, self.objeto)
        pago.stripe_price_id = "price_existente"

        pago.aplicarSubscripcion(self.usuario)

        price_mock.assert_not_called()

    def test_aplicarSubscripcion_tipo_invalido(self):
        pago = Pago.nuevoPago("Test", self.usuario, TipoPago.UNICO, self.objeto)

        result = pago.aplicarSubscripcion(self.usuario)

        self.assertIsNone(result)