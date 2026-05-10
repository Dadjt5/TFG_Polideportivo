from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from datetime import date, timedelta

from polideportivo.models import (
    Actividad, Instalacion, Alquiler, ReservaActividad, CompraAbono, CompraBono,
    TDA, AbonoDeportivo, Pago, Bono, TipoPago, TipoInstalacion, UsuarioFinal,
    Pabellon, Monitor, Configuracion
)

class ReservarActividadViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )


        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(pabellon=self.pabellon)

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(nombre="Actividad test", instalacion=self.instalacion, monitor=self.monitor)

    @patch("polideportivo.models.ReservaActividad.nuevaReserva")
    @patch("polideportivo.models.Pago.nuevoPago")
    def test_reserva_actividad_ok(self, mock_nuevo_pago, mock_nueva_reserva):
        mock_nueva_reserva.return_value = object()
        mock_nuevo_pago.return_value = type("Pago", (), {"id": 1})()
        self.client.force_authenticate(user=self.user)
        data = {"complementos": {"forma": TipoPago.UNICO}}
        response = self.client.post(f"/api/v1/actividades/{self.actividad.id}/reservar/", data, format="json")
        self.assertEqual(response.status_code, 200)


class ReservaInstalacionViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        Configuracion.objects.create()

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))
        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion test",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.SALA_MULTIUSOS,
            numeroCalles=0
        )

    @patch("polideportivo.models.Alquiler.nuevaReserva")
    @patch("polideportivo.models.Pago.nuevoPago")
    def test_reserva_instalacion_ok(self, mock_nuevo_pago, mock_nueva_reserva):
        mock_nueva_reserva.return_value = object()
        mock_nuevo_pago.return_value = type("Pago", (), {"id": 1})()
        self.client.force_authenticate(user=self.user)
        data = {"complementos": {"fecha": str(date.today() + timedelta(days=1)), "horas": ["10:00:00", "11:00:00"], "luz": False}}
        response = self.client.post(f"/api/v1/instalaciones/{self.instalacion.id}/alquilar/", data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_sin_horas(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "complementos": {
                "fecha": str(date.today()),
                "horas": []
            }
        }

        response = self.client.post(
            f"/api/v1/instalaciones/{self.instalacion.id}/alquilar/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 400)


class ComprarAbonoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.abono = AbonoDeportivo.objects.create(nombre="Abono test")

    @patch("polideportivo.models.CompraAbono.compraAbono")
    @patch("polideportivo.models.Pago.nuevoPago")
    def test_comprar_abono_ok(self, mock_nuevo_pago, mock_compra_abono):
        mock_compra_abono.return_value = object()
        mock_nuevo_pago.return_value = type("Pago", (), {"id": 1})()
        self.client.force_authenticate(user=self.user)
        data = {"tipoAbono": "abono_deportivo", "complementos": {"forma": TipoPago.UNICO}}
        response = self.client.post(f"/api/v1/abonos/{self.abono.id}/comprar/", data, format="json")
        self.assertEqual(response.status_code, 200)


    def test_forma_pago_invalida(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "tipoAbono": "abono_deportivo",
            "complementos": {
                "forma": "INVALIDO"
            }
        }

        response = self.client.post(
            f"/api/v1/abonos/{self.abono.id}/comprar/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, 400)


class ComprarBonoViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.bono = Bono.objects.create(usos=10)

    @patch("polideportivo.models.CompraBono.compraBono")
    @patch("polideportivo.models.Pago.nuevoPago")
    def test_comprar_bono_ok(self, mock_nuevo_pago, mock_compra_bono):
        mock_compra_bono.return_value = object()
        mock_nuevo_pago.return_value = type("Pago", (), {"id": 1})()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/v1/bonos/{self.bono.id}/comprar/")
        self.assertEqual(response.status_code, 200)

    def test_comprar_bono_error(self):
        self.client.force_authenticate(user=self.user)

        CompraBono.compraBono = lambda *args: None

        response = self.client.post(
            f"/api/v1/bonos/{self.bono.id}/comprar/"
        )

        self.assertEqual(response.status_code, 400)


class ComprarTDAViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

    @patch("polideportivo.models.TDA.compraTDA")
    @patch("polideportivo.models.Pago.nuevoPago")
    def test_comprar_tda_ok(self, mock_nuevo_pago, mock_compra_tda):
        mock_compra_tda.return_value = object()
        mock_nuevo_pago.return_value = type("Pago", (), {"id": 1})()
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/v1/tda/comprar/")
        self.assertEqual(response.status_code, 200)

    @patch("polideportivo.models.TDA.compraTDA")
    def test_comprar_tda_error(self, mock_compra_tda):
        mock_compra_tda.return_value = None
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/v1/tda/comprar/")
        self.assertEqual(response.status_code, 400)