from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from datetime import date

from polideportivo.models import (
    Pago, EstadoPago, TipoPago, ReservaActividad, Actividad,
    UsuarioFinal, CompraAbono, AbonoVerano, Configuracion
)

class ResumenPagoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        Configuracion.objects.create()

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.abonoVerano = AbonoVerano.objects.create()
        self.objeto = CompraAbono.objects.create(abonoVerano=self.abonoVerano, usuarioFinal=self.usuario_final)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario_final,
            objeto=self.objeto,
             estadoPago=EstadoPago.PENDIENTE,
            content_type_id=1,
            object_id=1,
            tipoPago=TipoPago.UNICO,
            stripe_payment_intent="pi_123"
        )


    def test_resumen_compra_abono(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"/api/v1/pagos/resumen/comprar_abono/{self.pago.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("pago", response.data)

    def test_tipo_no_soportado(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"/api/v1/pagos/resumen/invalido/{self.pago.id}/"
        )

        self.assertEqual(response.status_code, 400)

class CrearIntentoPagoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        Configuracion.objects.create()

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.abonoVerano = AbonoVerano.objects.create()
        self.objeto = CompraAbono.objects.create(abonoVerano=self.abonoVerano, usuarioFinal=self.usuario_final)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario_final,
            objeto=self.objeto,
            estadoPago=EstadoPago.PENDIENTE,
            content_type_id=1,
            object_id=1,
            tipoPago=TipoPago.UNICO,
            stripe_payment_intent="pi_123"
        )


    def test_intento_pago_unico_ok(self):
        self.client.force_authenticate(user=self.user)

        self.pago.aplicarPagoUnico = lambda uf: type("Intent", (), {"client_secret": "abc"})()

        response = self.client.post(
            f"/api/v1/pagos/{self.pago.id}/comenzar/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("client_secret", response.data)

    def test_pago_no_pendiente(self):
        self.client.force_authenticate(user=self.user)

        self.pago.estadoPago = EstadoPago.PAGADO
        self.pago.save()

        response = self.client.post(
            f"/api/v1/pagos/{self.pago.id}/comenzar/"
        )

        self.assertEqual(response.status_code, 400)

    def test_intento_subscripcion_invalida(self):
        self.client.force_authenticate(user=self.user)

        self.pago.tipoPago = TipoPago.MENSUAL
        self.pago.save()

        self.pago.aplicarSubscripcion = lambda uf: None

        response = self.client.post(
            f"/api/v1/pagos/{self.pago.id}/comenzar/"
        )

        self.assertEqual(response.status_code, 200)

class ConfirmarPagoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        Configuracion.objects.create()

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.abonoVerano = AbonoVerano.objects.create()
        self.objeto = CompraAbono.objects.create(abonoVerano=self.abonoVerano, usuarioFinal=self.usuario_final)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario_final,
            objeto=self.objeto,
            estadoPago=EstadoPago.PENDIENTE,
            content_type_id=1,
            object_id=1,
            tipoPago=TipoPago.UNICO,
            stripe_payment_intent="pi_123"
        )


    def test_confirmar_pago_ok(self):
        self.client.force_authenticate(user=self.user)

        import stripe
        stripe.PaymentIntent.retrieve = lambda x: type(
            "Intent", (), {"status": "succeeded"}
        )()

        response = self.client.post(
            f"/api/v1/pagos/{self.pago.id}/confirmar/"
        )

        self.assertEqual(response.status_code, 200)


class StripeWebhookViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        Configuracion.objects.create()

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.abonoVerano = AbonoVerano.objects.create()
        self.objeto = CompraAbono.objects.create(abonoVerano=self.abonoVerano, usuarioFinal=self.usuario_final)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario_final,
            objeto=self.objeto,
            content_type_id=1,
            object_id=1,
            tipoPago=TipoPago.UNICO,
            stripe_payment_intent="pi_123"
        )


    def test_invoice_payment_failed(self):
        """
        Simulamos evento de Stripe de fallo de pago
        """

        event = {
            "type": "invoice.payment_failed",
            "data": {
                "object": {
                    "subscription": "sub_123"
                }
            }
        }

        # Mock de Stripe construct_event
        import stripe
        stripe.Webhook.construct_event = lambda payload, sig, secret: event

        # Mock cancelación + notificación
        self.pago.cancelarPago = lambda x: None

        response = self.client.post(
            "/api/v1/stripe/webhook/",
            data=event,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="valid"
        )

        self.assertEqual(response.status_code, 200)

    def test_webhook_subscription_not_found(self):
        event = {
            "type": "invoice.payment_failed",
            "data": {
                "object": {
                    "subscription": "no_existe"
                }
            }
        }

        import stripe
        stripe.Webhook.construct_event = lambda payload, sig, secret: event

        response = self.client.post(
            "/api/v1/stripe/webhook/",
            data=event,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="valid"
        )

        self.assertEqual(response.status_code, 200)