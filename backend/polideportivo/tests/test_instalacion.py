from django.test import TestCase
from unittest.mock import MagicMock, patch
from datetime import time, datetime, timedelta, date
from django.contrib.auth import get_user_model


from polideportivo.models import (
    Instalacion, Pabellon, TipoInstalacion, Calle, 
    TarifaInstalacion, Agenda, Sesion, UsuarioFinal, 
    TipoReserva, EstadoReserva, Periodo, Dia, Alquiler,
    Monitor, Actividad
)

User = get_user_model()


class InstalacionTests(TestCase):
    def setUp(self):
        self.pabellon = Pabellon.objects.create(nombre="Pabellon Test", direccion="Calle Falsa 123")
        self.tarifa = TarifaInstalacion.objects.create(
            precioAbonado=10.0,
            precioUAM=8.0,
            precioTDA=6.0,
            precioOtros=12.0,
            costeIluminacion=2.0
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Piscina Test",
            pabellon=self.pabellon,
            tarifa=self.tarifa,
            tipoInstalacion=TipoInstalacion.PISCINA,
            numeroCalles=3
        )

        self.instalacion.crearCalles()

        user = User.objects.create_user(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(nombre="Usuario Test", tieneAbono=True, fechaNacimiento=date(2000, 1, 1), user=user)


    # ----------------- STR -----------------

    def test_str(self):
        self.assertEqual(str(self.instalacion), f'{self.instalacion.nombre}, ubicado en el {self.instalacion.pabellon}')


    # ----------------- PRECIOS -----------------

    def test_calcular_precio_base(self):
        precio = self.instalacion._calcular_precio_base(self.usuario)
        self.assertEqual(precio, 10.0)  # precioAbonado

    def test_obtenerPrecios(self):
        precios = self.instalacion.obtenerPrecios()
        self.assertEqual(precios['precioAbonado'], 10.0)


    # ----------------- AFORO -----------------

    def test_comprobarAforo(self):
        user = User.objects.create(username="monitor1", password="1234")
        monitor = Monitor.objects.create(nombre="monitor", user=user)
        Actividad.objects.create(instalacion=self.instalacion, nombre="yoga", monitor=monitor, plazasMaximas=2)

        self.assertTrue(self.instalacion.comprobarAforo({"aforoMaximo": 50}))


    # ----------------- MODIFICAR INFORMACION -----------------

    def test_modificarInformacion(self):
        nueva_data = {"nombre":"Nueva","aforoMaximo":100,"luz":True,"porcentajeTDA":5.0,"numeroCalles":4}
        pab_nueva = Pabellon.objects.create(nombre="Pab2", direccion="Calle 2")
        tarifa_nueva = TarifaInstalacion.objects.create(precioOtros=20)
        res = self.instalacion.modificarInformacion(nueva_data, pab_nueva, tarifa_nueva, "imagen.jpg")

        self.assertTrue(res)

        self.instalacion.refresh_from_db()

        self.assertEqual(self.instalacion.nombre,"Nueva")
        self.assertEqual(self.instalacion.pabellon, pab_nueva)


    # ----------------- CALLES -----------------

    def test_crearCalles(self):
        self.instalacion.numeroCalles = 5
        self.instalacion.crearCalles()

        self.assertEqual(self.instalacion.calles.count(), 5)


    def test_sincronizarCalles_aumenta_disminuye(self):
        self.instalacion.sincronizarCalles(5)
        self.assertEqual(self.instalacion.calles.count(),5)

        self.instalacion.sincronizarCalles(2)
        self.assertEqual(self.instalacion.calles.count(),2)


    # ----------------- MAPA RESERVAS -----------------

    @patch('polideportivo.models.Agenda.objects.filter')
    def test_actualizarMapa(self, mock_agenda_filter):
        agenda_mock = MagicMock()
        mapa_mock = MagicMock()

        agenda_mock.mapa_reservas.filter.return_value.first.return_value = mapa_mock
        mock_agenda_filter.return_value.first.return_value = agenda_mock
        sesiones = [{"dia":"Lunes","horaInicio":"09:00","horaFin":"11:00","calle":1}]

        self.instalacion.actualizarMapa(sesiones)
        self.assertEqual(mapa_mock.estado, TipoReserva.ACTIVIDAD)

    def test_sincronizarMapaReservas_no_abierto(self):
        agenda_mock = Agenda(instalacion=self.instalacion, abierto=False)
        agenda_mock.save()

        res = self.instalacion.sincronizarMapaReservas(agenda_mock)
        self.assertTrue(res)


    # ----------------- ALQUILERES -----------------

    @patch('polideportivo.models.Notificacion.notificarCancelacionYDevolucionDinero')
    @patch('polideportivo.models.Pago.objects.filter')
    def test_revisarAlquileres(self, mock_pago_filter, mock_notif):
        alquiler = Alquiler.objects.create(usuarioFinal=self.usuario, instalacion=self.instalacion, calle=self.instalacion.calles.first(), estado=EstadoReserva.CONFIRMADA, horaInicio=time(12), horaFin=time(13), fecha=date(2026,4,13))

        mock_pago = MagicMock()
        mock_pago_filter.return_value.first.return_value = mock_pago

        self.instalacion.revisarAlquileres([{"dia": Dia.LUNES, "horaInicio":"12:00","horaFin":"13:00","calle":1}], Periodo.ANUAL, confirmacion=True)
        mock_notif.assert_called()

    @patch('polideportivo.models.Agenda.objects.filter')
    def test_controlarAlquiler(self,mock_agenda):
        agenda_mock = MagicMock()
        agenda_mock.estaOcupado.return_value=False
        mock_agenda.return_value.first.return_value=agenda_mock

        self.assertTrue(self.instalacion.controlarAlquiler(date.today(),time(9),time(10),calle=1))


    # ----------------- MANEJAR HORARIO -----------------

    @patch('polideportivo.models.Sesion.objects.filter')
    def test_controlarHorarioActividad(self, mock_ses):
        mock_ses.return_value.exists.return_value=False
        self.assertTrue(self.instalacion.controlarHorarioActividad("Lunes",time(9),time(10)))

    @patch('polideportivo.models.Sesion.objects.filter')
    def test_controlarCambioHorario(self,mock_ses):
        mock_ses.return_value.exists.return_value=False

        self.assertTrue(self.instalacion.controlarCambioHorario("Lunes",time(9),time(10),True))
        self.assertTrue(self.instalacion.controlarCambioHorario("Lunes",time(9),time(10),False))

    @patch.object(Instalacion,'sincronizarMapaReservas',return_value=True)
    def test_nuevoHorario(self, mock_sync):
        res=self.instalacion.nuevoHorario("Lunes",time(9),time(18),True)
        self.assertTrue(res)

        res_inv=self.instalacion.nuevoHorario("Lunes",time(18),time(9),True)
        self.assertFalse(res_inv)

    @patch.object(Instalacion,'sincronizarMapaReservas',return_value=True)
    def test_nuevoHorarioEspecial(self, mock_sync):
        res=self.instalacion.nuevoHorarioEspecial(date.today(),time(9),time(18),True)
        self.assertTrue(res)

        res_inv=self.instalacion.nuevoHorarioEspecial(date.today(),time(18),time(9),True)
        self.assertFalse(res_inv)

    def test_getHorario_none(self):
        apertura,cierre=self.instalacion.getHorario(date.today())

        self.assertIsNone(apertura)
        self.assertIsNone(cierre)


    # ----------------- RESERVAS -----------------

    @patch('polideportivo.models.Agenda.objects.filter')
    def test_getReservas(self, mock_agenda):
        mock_agenda.return_value.first.return_value=None

        self.assertEqual(self.instalacion.getReservas(date.today()),[])


    # ----------------- CONTAR -----------------

    def test_contar(self):
        self.assertEqual(Instalacion.contar(),1)


    # ----------------- BUSCAR -----------------

    def test_buscar(self):
        self.assertIn(self.instalacion,Instalacion.buscar(nombre="Piscina"))
        self.assertIn(self.instalacion,Instalacion.buscar(tipo=[TipoInstalacion.PISCINA]))



class CalleTests(TestCase):
    def setUp(self):
        self.pabellon = Pabellon.objects.create(nombre="Pabellon Test", direccion="Calle Falsa 123")
        self.instalacion = Instalacion.objects.create(
            nombre="Piscina Test",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.PISCINA
        )


    # ----------------- CREACION -----------------

    def test_crear_calle(self):
        calle = Calle.objects.create(instalacion=self.instalacion, numero=1)

        self.assertEqual(calle.numero, 1)
        self.assertEqual(calle.instalacion, self.instalacion)


    # ----------------- STR -----------------

    def test_str(self):
        calle = Calle.objects.create(instalacion=self.instalacion, numero=2)
        self.assertEqual(str(calle), f"Calle 2 - {self.instalacion.nombre}")