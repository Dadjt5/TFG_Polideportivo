from django.test import TestCase
from unittest.mock import Mock, patch
from datetime import date, time
from django.contrib.auth import get_user_model

from ..models import (
    ReservaActividad, UsuarioFinal, Descuento,
    Actividad, EstadoReserva, FormaReserva, ListaEspera,
    Instalacion, TipoInstalacion, Alquiler, Pabellon, Monitor,
    TarifaInstalacion
)

User = get_user_model()


class ReservaBaseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2000, 1, 1))

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)
        user = User.objects.create_user(username="monitor1", password="1234")
        monitor = Monitor.objects.create(user=user)
        self.actividad = Actividad.objects.create(nombre="Yoga", instalacion=instalacion, monitor=monitor)

        self.reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuario,
            actividad=self.actividad
        )


    # ----------------- CALCULAR DESCUENTO -----------------

    def test_calcularDescuento_sin_descuentos(self):
        self.assertEqual(self.reserva.calcularDescuento(), 0.0)

    def test_calcularDescuento_un_descuento(self):
        d = Descuento.objects.create(nombre="D1", porcentaje=10, fechaInicio=date(2000, 1, 1), fechaFinValidez=date(2000, 1, 1))
        self.reserva.descuentos.add(d)

        self.assertEqual(self.reserva.calcularDescuento(), 10)

    def test_calcularDescuento_varios_descuentos(self):
        d1 = Descuento.objects.create(nombre="D1", porcentaje=10, fechaInicio=date(2000, 1, 1), fechaFinValidez=date(2000, 1, 1))
        d2 = Descuento.objects.create(nombre="D2", porcentaje=15, fechaInicio=date(2000, 1, 1), fechaFinValidez=date(2000, 1, 1))

        self.reserva.descuentos.add(d1, d2)

        self.assertEqual(self.reserva.calcularDescuento(), 25)



class ReservaActividadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(user=self.user, actividadesRealizadas=0, fechaNacimiento=date(2000, 1, 1))

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)
        user = User.objects.create_user(username="monitor1", password="1234")
        monitor = Monitor.objects.create(user=user)

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            plazasMaximas=2,
            plazasReservadas=0,
            tipoReserva=FormaReserva.ONLINE,
            instalacion=instalacion,
            monitor=monitor
        )

        self.lista = ListaEspera.objects.create(actividad=self.actividad)


    # ----------------- STR -----------------

    def test_str(self):
        reserva = ReservaActividad.objects.create(usuarioFinal=self.usuario, actividad=self.actividad)
        self.assertIn("Reserva de", str(reserva))


    # ----------------- CALCULAR PRECIO -----------------

    def test_calcularPrecio(self):
        reserva = ReservaActividad.objects.create(usuarioFinal=self.usuario, actividad=self.actividad)

        self.actividad._calcularPrecio_base = Mock(return_value=50)

        precio = reserva.calcularPrecio()
        self.assertEqual(precio, 50)


    # ----------------- CONFIRMAR -----------------

    def test_confirmarCompra(self):
        reserva = ReservaActividad.objects.create(usuarioFinal=self.usuario, actividad=self.actividad)

        reserva.confirmarCompra()

        reserva.refresh_from_db()
        self.usuario.refresh_from_db()

        self.assertEqual(reserva.estado, EstadoReserva.CONFIRMADA)
        self.assertEqual(self.usuario.actividadesRealizadas, 1)


    # ----------------- CANCELAR -----------------

    @patch("polideportivo.models.reserva.Notificacion.notificarSalidaListaDeEspera")
    def test_cancelarCompra(self, noti_mock):
        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuario,
            actividad=self.actividad,
            estado=EstadoReserva.CONFIRMADA
        )

        self.usuario.actividadesRealizadas = 1
        self.usuario.save()

        self.actividad.plazasReservadas = 1
        self.actividad.save()

        self.actividad.eliminarAsistencia = Mock()

        reserva.cancelarCompra()

        reserva.refresh_from_db()
        self.usuario.refresh_from_db()

        self.assertEqual(reserva.estado, EstadoReserva.CANCELADO)
        self.assertEqual(self.usuario.actividadesRealizadas, 0)


    # ----------------- CONTAR -----------------

    def test_contar(self):
        ReservaActividad.objects.create(usuarioFinal=self.usuario, actividad=self.actividad)
        ReservaActividad.objects.create(usuarioFinal=self.usuario, actividad=self.actividad)

        self.assertEqual(ReservaActividad.contar(), 2)


    # ----------------- NUEVA RESERVA -----------------

    def test_nuevaReserva_ok(self):
        self.actividad.activarAsistencia = Mock()

        reserva = ReservaActividad.nuevaReserva(self.usuario, self.actividad)

        self.assertIsNotNone(reserva)
        self.assertEqual(reserva.estado, EstadoReserva.PENDIENTE)

    def test_nuevaReserva_sin_plazas(self):
        self.actividad.plazasReservadas = 2
        self.actividad.plazasMaximas = 2
        self.actividad.save()

        reserva = ReservaActividad.nuevaReserva(self.usuario, self.actividad)

        self.assertIsNone(reserva)

    def test_nuevaReserva_duplicada(self):
        ReservaActividad.objects.create(
            usuarioFinal=self.usuario,
            actividad=self.actividad,
            estado=EstadoReserva.CONFIRMADA
        )

        reserva = ReservaActividad.nuevaReserva(self.usuario, self.actividad)

        self.assertIsNone(reserva)

    def test_nuevaReserva_tipo_no_permitido(self):
        self.actividad.tipoReserva = FormaReserva.PRESENCIAL
        self.actividad.save()

        reserva = ReservaActividad.nuevaReserva(self.usuario, self.actividad)

        self.assertIsNone(reserva)

    @patch("polideportivo.models.reserva.Descuento.obtenerDescuentos")
    def test_nuevaReserva_con_descuentos(self, descuento_mock):
        self.actividad.activarAsistencia = Mock()

        descuento = Descuento.objects.create(
            nombre="D1",
            porcentaje=10,
            fechaInicio=date.today(),
            fechaFinValidez=date.today()
        )

        descuento_mock.return_value = {
            "descuento": {
                "aplicados": [descuento]
            }
        }

        reserva = ReservaActividad.nuevaReserva(self.usuario, self.actividad)

        self.assertIsNotNone(reserva)



class AlquilerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2000, 1, 1))
        pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            nombre="Pista",
            pabellon=pabellon
        )

        self.instalacion.tarifa = TarifaInstalacion()
        self.instalacion.tarifa.costeIluminacion = 10

        self.instalacion._calcularPrecio_base = Mock(return_value=20)
        self.instalacion.controlarAlquiler = Mock(return_value=True)


    # ----------------- STR -----------------

    def test_str(self):
        alquiler = Alquiler.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertIn("Alquiler de", str(alquiler))


    # ----------------- CALCULAR PRECIO -----------------

    def test_calcularPrecio_con_luz(self):
        alquiler = Alquiler(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            horaInicio=time(8, 0),
            horaFin=time(10, 0)
        )

        precio = alquiler.calcularPrecio()

        self.assertTrue(alquiler.luz)
        self.assertEqual(precio, 10 + (20 * alquiler.numeroHoras))

    def test_calcularPrecio_sin_luz(self):
        alquiler = Alquiler(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            horaInicio=time(7, 0),
            horaFin=time(8, 0)
        )

        precio = alquiler.calcularPrecio()

        self.assertFalse(alquiler.luz)
        self.assertEqual(precio, 20 * alquiler.numeroHoras)


    # ----------------- SAVE PARA EL NUMERO DE HORAS -----------------

    def test_save_calcula_numeroHoras(self):
        alquiler = Alquiler.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(12, 0)
        )

        self.assertEqual(alquiler.numeroHoras, 2)


    # ----------------- CONFIRMAR Y CANCELAR -----------------

    def test_confirmarCompra(self):
        alquiler = Alquiler.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        alquiler.confirmarCompra()
        self.assertEqual(alquiler.estado, EstadoReserva.CONFIRMADA)

    def test_cancelarCompra(self):
        alquiler = Alquiler.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        alquiler.cancelarCompra()
        self.assertEqual(alquiler.estado, EstadoReserva.CANCELADO)


    # ----------------- CONTAR -----------------

    def test_contar(self):
        Alquiler.objects.create(usuarioFinal=self.usuario, instalacion=self.instalacion, fecha=date.today(), horaInicio=time(10,0), horaFin=time(11,0))
        Alquiler.objects.create(usuarioFinal=self.usuario, instalacion=self.instalacion, fecha=date.today(), horaInicio=time(12,0), horaFin=time(13,0))

        self.assertEqual(Alquiler.contar(), 2)


    # ----------------- NUEVA RESERVA -----------------

    def test_nuevaReserva_ok(self):
        reserva = Alquiler.nuevaReserva(
            usuario=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            luz=False
        )

        self.assertIsNotNone(reserva)
        self.assertEqual(reserva.estado, EstadoReserva.PENDIENTE)

    def test_nuevaReserva_conflicto(self):
        Alquiler.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            estado=EstadoReserva.CONFIRMADA
        )

        reserva = Alquiler.nuevaReserva(
            usuario=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 30),
            horaFin=time(11, 30),
            luz=False
        )

        self.assertIsNone(reserva)

    def test_nuevaReserva_control_instalacion(self):
        self.instalacion.controlarAlquiler = Mock(return_value=False)

        reserva = Alquiler.nuevaReserva(
            usuario=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            luz=False
        )

        self.assertIsNone(reserva)

    @patch("polideportivo.models.reserva.Descuento.obtenerDescuentos")
    def test_nuevaReserva_con_descuentos(self, descuento_mock):
        descuento = Descuento.objects.create(
            nombre="D1",
            porcentaje=10,
            fechaInicio=date.today(),
            fechaFinValidez=date.today()
        )

        descuento_mock.return_value = {
            "descuento": {
                "aplicados": [descuento]
            }
        }

        reserva = Alquiler.nuevaReserva(
            usuario=self.usuario,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            luz=False
        )

        self.assertIsNotNone(reserva)