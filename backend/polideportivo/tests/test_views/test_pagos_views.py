from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from polideportivo.models import (
    Pago,
    EstadoPago,
    TipoPago,
    ReservaActividad,
    Alquiler,
    CompraAbono,
    CompraBono,
    TDA,
    Actividad,
    Instalacion
)

class ResumenPagoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = self.user

        self.pago = Pago.objects.create(
            usuarioFinal=self.usuario_final,
            concepto="test",
            coste=10,
            costeFinal=10,
            descuentoAplicado=0,
            descripcionPorcentajes="",
            estadoPago=EstadoPago.PENDIENTE
        )

    def test_resumen_reserva_actividad(self):
        self.client.force_authenticate(user=self.user)

        self.pago.objeto = ReservaActividad(
            id=1,
            actividad=Actividad(nombre="Actividad")
        )

        response = self.client.get(
            f"/api/v1/pagos/resumen/reserva_actividad/{self.pago.id}/"
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

        self.pago = Pago.objects.create(
            usuarioFinal=self.user,
            estadoPago=EstadoPago.PENDIENTE,
            tipoPago=TipoPago.UNICO
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

        self.pago.estadoPago = EstadoPago.CONFIRMADO
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

        self.assertEqual(response.status_code, 400)

class ConfirmarPagoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.pago = Pago.objects.create(
            usuarioFinal=self.user,
            estadoPago=EstadoPago.PENDIENTE
        )

    def test_confirmar_pago_ok(self):
        self.client.force_authenticate(user=self.user)

        self.pago.comprobarPago = lambda: True
        self.pago.confirmarPago = lambda: None

        response = self.client.post(
            f"/api/v1/pagos/{self.pago.id}/confirmar/"
        )

        self.assertEqual(response.status_code, 200)

    def test_pago_fallido(self):
        self.client.force_authenticate(user=self.user)

        self.pago.comprobarPago = lambda: False
        self.pago.cancelarPago = lambda: None

        response = self.client.post(
            f"/api/v1/pagos/{self.pago.id}/confirmar/"
        )

        self.assertEqual(response.status_code, 400)
    

class StripeWebhookViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.pago = Pago.objects.create(
            usuarioFinal=self.user,
            stripe_subscription_id="sub_123"
        )

    def test_webhook_value_error(self):
        response = self.client.post(
            "/api/v1/stripe/webhook/",
            data="invalid_payload",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="bad_signature"
        )

        self.assertEqual(response.status_code, 400)

    def test_webhook_signature_error(self):
        response = self.client.post(
            "/api/v1/stripe/webhook/",
            data="{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="bad_signature"
        )

        self.assertEqual(response.status_code, 400)

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