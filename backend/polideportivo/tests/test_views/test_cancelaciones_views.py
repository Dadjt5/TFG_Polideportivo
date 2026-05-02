from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from polideportivo.models import (
    Pago,
    ReservaActividad,
    Alquiler,
    CompraAbono,
    CompraBono,
    EstadoPago,
    Configuracion
)

class CancelarPagoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.pago = Pago.objects.create(
            usuarioFinal=self.user,
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

        self.reserva = ReservaActividad.objects.create(
            id=1,
            usuarioFinal=self.user
        )

    def test_cancelar_reserva_ok(self):
        self.client.force_authenticate(user=self.user)

        Pago.objects.create(
            content_type_id=1,
            object_id=self.reserva.id
        ).cancelarPago = lambda x: None

        Configuracion.objects.create(dias_minimo_cancelacion=0)

        response = self.client.delete(
            f"/api/v1/reservas/{self.reserva.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)

    def test_reserva_fuera_plazo(self):
        self.client.force_authenticate(user=self.user)

        Configuracion.objects.create(dias_minimo_cancelacion=999)

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

        self.alquiler = Alquiler.objects.create(
            id=1,
            fecha="2030-01-01",
            horaInicio="10:00:00"
        )

    def test_cancelar_alquiler_ok(self):
        self.client.force_authenticate(user=self.user)

        Pago.objects.create(
            content_type_id=1,
            object_id=self.alquiler.id,
            estadoPago=EstadoPago.PAGADO
        ).cancelarPago = lambda x: None

        response = self.client.delete(
            f"/api/v1/alquileres/{self.alquiler.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)

    def test_alquiler_iniciado(self):
        self.client.force_authenticate(user=self.user)

        self.alquiler.fecha = "2000-01-01"
        self.alquiler.save()

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

        self.compra = CompraAbono.objects.create(
            id=1
        )

    def test_cancelar_abono_ok(self):
        self.client.force_authenticate(user=self.user)

        Pago.objects.create(
            content_type_id=1,
            object_id=self.compra.id
        ).cancelarPago = lambda x: None

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

        self.compra = CompraBono.objects.create(
            id=1,
            vecesUsado=0
        )

    def test_cancelar_bono_ok(self):
        self.client.force_authenticate(user=self.user)

        Pago.objects.create(
            content_type_id=1,
            object_id=self.compra.id,
            estadoPago=EstadoPago.PAGADO
        ).cancelarPago = lambda x: None
 
        response = self.client.delete(
            f"/api/v1/bonos/{self.compra.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)

    def test_bono_usado_no_se_elimina(self):
        self.client.force_authenticate(user=self.user)

        self.compra.vecesUsado = 5
        self.compra.save()

        response = self.client.delete(
            f"/api/v1/bonos/{self.compra.id}/cancelar/"
        )

        self.assertEqual(response.status_code, 200)