from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time, timedelta

from ...models import (
    ReservaActividad, Alquiler, EstadoReserva, UsuarioFinal,
    Actividad, Instalacion, Pabellon, Monitor, Descuento,
    TarifaInstalacion
)

User = get_user_model()


class ReservaUnitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="12345678A", email="test@test.com", password="test")

        self.usuario = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user)

        self.pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(pabellon=self.pabellon)

        self.user2 = User.objects.create(username="monitor", password="1234")
        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(instalacion=self.instalacion, monitor=self.monitor)
    
    def test_str_reserva(self):
        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuario,
            actividad=self.actividad
        )

        self.assertIn("Reserva de", str(reserva))
    
    def test_str_alquiler(self):
        alquiler = Alquiler.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertIn("Alquiler de", str(alquiler))

    def test_calcular_descuento(self):
        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuario,
            actividad=self.actividad
        )

        d1 = Descuento.objects.create(
            nombre="desc1",
            porcentaje=10,
            fechaInicio=date.today(),
            fechaFinValidez=date.today() + timedelta(days=30),
            tiposInstalacion=[]
        )

        d2 = Descuento.objects.create(
            nombre="desc2",
            porcentaje=20,
            fechaInicio=date.today(),
            fechaFinValidez=date.today() + timedelta(days=30),
            tiposInstalacion=[]
        )

        reserva.descuentos.add(d1, d2)

        resultado = reserva.calcularDescuento()

        self.assertEqual(resultado["desc1"], 10)
        self.assertEqual(resultado["desc2"], 20)

    def test_confirmar_compra_actividad(self):
        reserva = ReservaActividad.objects.create(usuarioFinal=self.usuario, actividad=self.actividad, estado=EstadoReserva.PENDIENTE)

        reserva.confirmarCompra()

        self.assertEqual(reserva.estado, EstadoReserva.CONFIRMADA)

    def test_cancelar_compra_alquiler(self):
        alquiler = Alquiler(usuarioFinal=self.usuario, horaInicio=time(9,00), horaFin=time(10,0), instalacion=self.instalacion)
        alquiler.estado = EstadoReserva.CONFIRMADA

        alquiler.cancelarCompra()

        self.assertEqual(alquiler.estado, EstadoReserva.CANCELADO)

    def test_contar_reservas(self):
        self.assertEqual(ReservaActividad.contar(), 0)
    
    def test_calcular_precio_reserva_actividad(self):
        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuario,
            actividad=self.actividad
        )

        self.actividad._calcular_precio_base = lambda **kwargs: 50

        precio = reserva.calcularPrecio()

        self.assertEqual(precio, 50)
    
    def test_calcular_precio_alquiler_con_luz(self):
        self.instalacion.tarifa = TarifaInstalacion.objects.create(costeIluminacion=10)
        self.instalacion._calcular_precio_base = lambda usuario: 20

        alquiler = Alquiler(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            horaInicio=time(8, 0),
            horaFin=time(10, 0)
        )
        alquiler.numeroHoras = 2

        precio = alquiler.calcularPrecio()

        self.assertTrue(alquiler.luz)
        self.assertEqual(precio, 50)
    
    def test_calcular_precio_alquiler_sin_luz(self):
        self.instalacion.tarifa = TarifaInstalacion.objects.create(costeIluminacion=10)
        self.instalacion._calcular_precio_base = lambda usuario: 20

        alquiler = Alquiler(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            horaInicio=time(7, 0),
            horaFin=time(8, 0)
        )
        alquiler.numeroHoras = 1

        precio = alquiler.calcularPrecio()

        self.assertFalse(alquiler.luz)
        self.assertEqual(precio, 20)
    
    def test_save_calcula_numero_horas(self):
        alquiler = Alquiler.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(12, 30)
        )

        self.assertEqual(alquiler.numeroHoras, 2.5)
    
    def test_confirmar_compra_alquiler(self):
        alquiler = Alquiler.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10,0),
            horaFin=time(11,0)
        )

        alquiler.confirmarCompra()

        self.assertEqual(alquiler.estado, EstadoReserva.CONFIRMADA)
    
