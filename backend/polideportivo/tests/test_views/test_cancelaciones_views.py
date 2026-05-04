from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from unittest.mock import patch
from datetime import date, time

from polideportivo.models import (
    Pago, ReservaActividad, Alquiler, CompraAbono, Monitor, Actividad, EstadoPago,
    CompraBono, EstadoPago, Configuracion, UsuarioFinal, Instalacion, Pabellon, Bono,
    AbonoVerano
)

class CancelarPagoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.bono = Bono.objects.create()

        self.compra = CompraBono.objects.create(
            id=1,
            bono=self.bono,
            usuarioFinal=self.usuario,
            vecesUsado=0
        )

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario,
            objeto=self.compra,
            content_type_id=1,
            object_id=1,
            estadoPago=EstadoPago.PAGADO
        )

    def test_cancelar_pago_ok(self):
        self.client.force_authenticate(user=self.user)

        self.pago.cancelarPago = lambda x: None

        response = self.client.post(
            f"/api/v1/pagos/{self.pago.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)


class CancelarReservaActividadViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Instalacion test"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            id=1,
            monitor=self.monitor,
            instalacion=self.instalacion,
            nombre="Actividad test"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.reserva = ReservaActividad.objects.create(
            id=1,
            actividad=self.actividad,
            usuarioFinal=self.usuario
        )

    def test_cancelar_reserva_ok(self):
        self.client.force_authenticate(user=self.user)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario,
            objeto=self.reserva,
            content_type_id=1,
            object_id=1,
            estadoPago=EstadoPago.PAGADO
        )

        Configuracion.objects.create(dias_minimo_cancelacion=999)

        response = self.client.delete(
            f"/api/v1/reservas/{self.reserva.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)

    def test_reserva_fuera_plazo(self):
        self.client.force_authenticate(user=self.user)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario,
            objeto=self.reserva,
            content_type_id=1,
            object_id=1,
            estadoPago=EstadoPago.PAGADO
        )

        Configuracion.objects.create(dias_minimo_cancelacion=0)

        response = self.client.delete(
            f"/api/v1/reservas/{self.reserva.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 400)


class CancelarAlquilerViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(pabellon=self.pabellon)

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.alquiler = Alquiler.objects.create(
            id=1,
            instalacion=self.instalacion,
            usuarioFinal=self.usuario,
            fecha="2030-01-01",
            horaInicio=time(10,0),
            horaFin=time(12,0)
        )

    @patch("stripe.Refund.create")
    def test_cancelar_alquiler_ok(self, mock_refund):
        mock_refund.return_value = {"id": "re_123"}

        self.client.force_authenticate(user=self.user)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario,
            objeto=self.alquiler,
            content_type_id=1,
            object_id=1,
            estadoPago=EstadoPago.PAGADO
        )

        self.pago.stripe_payment_intent = "pi_test_ok"

        response = self.client.delete(
            f"/api/v1/alquileres/{self.alquiler.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)

    def test_alquiler_iniciado(self):
        self.client.force_authenticate(user=self.user)

        self.alquiler.fecha = "2000-01-01"
        self.alquiler.save()

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario,
            objeto=self.alquiler,
            content_type_id=1,
            object_id=1,
            estadoPago=EstadoPago.PAGADO
        )

        response = self.client.delete(
            f"/api/v1/alquileres/{self.alquiler.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 400)


class CancelarAbonoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.abono = AbonoVerano.objects.create()

        self.compra = CompraAbono.objects.create(
            id=1,
            usuarioFinal=self.usuario,
            abonoVerano=self.abono
        )

    def test_cancelar_abono_ok(self):
        self.client.force_authenticate(user=self.user)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario,
            objeto=self.compra,
            content_type_id=1,
            object_id=1,
            estadoPago=EstadoPago.PAGADO
        )

        response = self.client.delete(
            f"/api/v1/abonos/{self.compra.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)


class CancelarBonoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))
        self.bono = Bono.objects.create()

        self.compra = CompraBono.objects.create(
            id=1,
            bono=self.bono,
            usuarioFinal=self.usuario,
            vecesUsado=0
        )

    @patch("stripe.Refund.create")
    def test_cancelar_bono_ok(self, mock_refund):
        mock_refund.return_value = {"id": "re_test"}

        self.client.force_authenticate(user=self.user)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario,
            objeto=self.compra,
            content_type_id=1,
            object_id=1,
            estadoPago=EstadoPago.PAGADO,
            stripe_payment_intent="pi_test"
        )

        response = self.client.delete(
            f"/api/v1/bonos/{self.compra.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)

    def test_bono_usado_no_se_elimina(self):
        self.client.force_authenticate(user=self.user)

        self.pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuario,
            objeto=self.compra,
            content_type_id=1,
            object_id=1,
            estadoPago=EstadoPago.PAGADO
        )

        self.compra.vecesUsado = 5
        self.compra.save()

        response = self.client.delete(
            f"/api/v1/bonos/{self.compra.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)