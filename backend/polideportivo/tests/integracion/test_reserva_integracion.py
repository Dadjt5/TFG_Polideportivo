from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time, timedelta

from ...models import (
    Actividad, ReservaActividad, UsuarioFinal, Monitor, 
    Deporte, Instalacion, Pabellon, EstadoReserva, 
    FormaReserva, Descuento, Alquiler
)

User = get_user_model()


class ReservaIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="12345678A",
            email="test@test.com",
            password="test"
        )

        self.user2 = User.objects.create(
            username="monitor",
            password="test"
        )

        self.deporte = Deporte.objects.create(titulo="Fútbol")
        self.pabellon = Pabellon.objects.create(nombre="Pabellón")

        self.instalacion = Instalacion.objects.create(
            nombre="Instalación",
            pabellon=self.pabellon
        )

        self.monitor = Monitor.objects.create(user=self.user2)
        self.usuarioFinal = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.actividad = Actividad.objects.create(
            nombre="Actividad",
            instalacion=self.instalacion,
            deportes=self.deporte,
            plazasMaximas=10,
            plazasReservadas=0,
            tipoReserva=FormaReserva.AMBAS,
            monitor=self.monitor
        )

    def test_nueva_reserva_actividad(self):
        reserva = ReservaActividad.nuevaReserva(
            usuario=self.usuarioFinal,
            actividad=self.actividad,
            complementos={"personas": 0, "tipoSesion": "", "forma": ""}
        )

        self.assertIsNotNone(reserva)
        self.assertEqual(reserva.estado, EstadoReserva.PENDIENTE)

    def test_reserva_no_duplicada(self):
        primera = ReservaActividad.nuevaReserva(self.usuarioFinal, self.actividad, {"personas": 0, "tipoSesion": "", "forma": ""})
        primera.estado = EstadoReserva.CONFIRMADA
        primera.save()

        segunda = ReservaActividad.nuevaReserva(self.usuarioFinal, self.actividad, {"personas": 0, "tipoSesion": "", "forma": ""})

        self.assertIsNone(segunda)

    def test_cancelar_reserva_actualiza_plazas(self):
        reserva = ReservaActividad.nuevaReserva(self.usuarioFinal, self.actividad, {"personas": 0, "tipoSesion": "", "forma": ""})

        self.actividad.refresh_from_db()
        plazas_antes = self.actividad.plazasReservadas

        reserva.cancelarCompra()

        self.actividad.refresh_from_db()

        self.assertEqual(reserva.estado, EstadoReserva.CANCELADO)
    
    def test_nueva_reserva_sin_plazas(self):
        self.actividad.plazasReservadas = 10
        self.actividad.save()

        reserva = ReservaActividad.nuevaReserva(
            self.usuarioFinal,
            self.actividad,
            {"personas": 0, "tipoSesion": "", "forma": ""}
        )

        self.assertIsNone(reserva)
    
    def test_nueva_reserva_tipo_no_permitido(self):
        self.actividad.tipoReserva = FormaReserva.PRESENCIAL
        self.actividad.save()

        reserva = ReservaActividad.nuevaReserva(
            self.usuarioFinal,
            self.actividad,
            {"personas": 0, "tipoSesion": "", "forma": ""}
        )

        self.assertIsNone(reserva)
    
    def test_confirmar_reserva_incrementa_actividades(self):
        reserva = ReservaActividad.nuevaReserva(
            self.usuarioFinal,
            self.actividad,
            {"personas": 0, "tipoSesion": "", "forma": ""}
        )

        reserva.confirmarCompra()
        self.usuarioFinal.refresh_from_db()

        self.assertEqual(self.usuarioFinal.actividadesRealizadas, 1)
    
    def test_cancelar_reserva_actualiza_plazas(self):
        reserva = ReservaActividad.nuevaReserva(
            self.usuarioFinal,
            self.actividad,
            {"personas": 0, "tipoSesion": "", "forma": ""}
        )

        reserva.confirmarCompra()
        self.actividad.refresh_from_db()
        plazas_antes = self.actividad.plazasReservadas

        reserva.cancelarCompra()
        self.actividad.refresh_from_db()

        self.assertEqual(reserva.estado, EstadoReserva.CANCELADO)
        self.assertLess(self.actividad.plazasReservadas, plazas_antes)
    
    def test_nueva_reserva_con_descuentos(self):
        descuento = Descuento.objects.create(
            nombre="D1",
            porcentaje=10,
            fechaInicio=date.today(),
            fechaFinValidez=date.today(),
        )

        descuento.deportes.set([self.deporte])

        reserva = ReservaActividad.nuevaReserva(
            self.usuarioFinal,
            self.actividad,
            {"personas": 0, "tipoSesion": "", "forma": ""}
        )

        reserva.descuentos.add(descuento)

        self.assertTrue(reserva.descuentos.exists())
    
    def test_nueva_reserva_alquiler(self):
        self.instalacion.controlarAlquiler = lambda *args, **kwargs: True

        alquiler = Alquiler.nuevaReserva(
            usuario=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today() + timedelta(days=1),
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            luz=False,
        )

        self.assertIsNotNone(alquiler)
        self.assertEqual(alquiler.estado, EstadoReserva.PENDIENTE)
    
    def test_alquiler_conflicto_horario(self):
        Alquiler.objects.create(
            usuarioFinal=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10,0),
            horaFin=time(11,0),
            estado=EstadoReserva.CONFIRMADA
        )

        alquiler = Alquiler.nuevaReserva(
            usuario=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10,30),
            horaFin=time(11,30),
            luz=False
        )

        self.assertIsNone(alquiler)
    
    def test_nueva_reserva_cancela_pendiente_anterior(self):
        self.actividad.plazasReservadas = 1
        self.actividad.save()

        anterior = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad,
            estado=EstadoReserva.PENDIENTE
        )

        nueva = ReservaActividad.nuevaReserva(
            self.usuarioFinal,
            self.actividad,
            {"personas": 0, "tipoSesion": "", "forma": ""}
        )

        anterior.refresh_from_db()

        self.assertEqual(anterior.estado, EstadoReserva.CANCELADO)
        self.assertIsNotNone(nueva)
        
    def test_alquiler_con_descuentos(self):
        self.instalacion.controlarAlquiler = lambda *args, **kwargs: True

        descuento = Descuento.objects.create(
            nombre="D1",
            porcentaje=10,
            fechaInicio=date.today(),
            fechaFinValidez=date.today(),
            tiposInstalacion=self.instalacion.tipoInstalacion
        )

        reserva = Alquiler.nuevaReserva(
            usuario=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10,0),
            horaFin=time(11,0),
            luz=False
        )

        self.assertTrue(reserva.descuentos.exists())
    
    def test_cancelar_reserva_activa_lista_espera(self):
        user3 = User.objects.create(username="otro", password="test")
        usuario_espera = UsuarioFinal.objects.create(
            user=user3,
            fechaNacimiento=date(2000, 1, 1)
        )

        from ...models import ListaEspera

        lista = ListaEspera.objects.create(actividad=self.actividad)
        lista.nuevaEntrada(usuario_espera)

        self.usuarioFinal.actividadesRealizadas = 1
        self.usuarioFinal.save()

        self.actividad.plazasMaximas = 2
        self.actividad.plazasReservadas = 1
        self.actividad.save()

        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad,
            estado=EstadoReserva.CONFIRMADA
        )

        reserva.cancelarCompra()

        self.actividad.refresh_from_db()

        self.assertEqual(self.actividad.plazasReservadas, 1)
    
    def test_nueva_reserva_existente_confirmada(self):
        ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad,
            estado=EstadoReserva.CONFIRMADA
        )

        reserva = ReservaActividad.nuevaReserva(
            self.usuarioFinal,
            self.actividad,
            {"personas": 0, "tipoSesion": "", "forma": ""}
        )

        self.assertIsNone(reserva)
    
    def test_contar_alquileres(self):
        Alquiler.objects.create(
            usuarioFinal=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today(),
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertEqual(Alquiler.contar(), 1)
    
    def test_nueva_reserva_piscina_filtra_por_calle(self):
        from ...models import Calle, TipoInstalacion

        calle = Calle.objects.create(numero=1, instalacion=self.instalacion)

        self.instalacion.tipoInstalacion = TipoInstalacion.PISCINA
        self.instalacion.save()

        self.instalacion.controlarAlquiler = lambda *args, **kwargs: True

        alquiler = Alquiler.nuevaReserva(
            usuario=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today() + timedelta(days=1),
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            luz=False,
            calle=calle
        )

        self.assertIsNotNone(alquiler)
    
    def test_nueva_reserva_alquiler_fuera_horario(self):
        self.instalacion.controlarAlquiler = lambda *args, **kwargs: False

        alquiler = Alquiler.nuevaReserva(
            usuario=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today() + timedelta(days=1),
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            luz=False
        )

        self.assertIsNone(alquiler)
    
    def test_nueva_reserva_alquiler_cancela_pendiente_previo(self):
        self.instalacion.controlarAlquiler = lambda *args, **kwargs: True

        anterior = Alquiler.objects.create(
            usuarioFinal=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today() + timedelta(days=1),
            horaInicio=time(8, 0),
            horaFin=time(9, 0),
            estado=EstadoReserva.PENDIENTE
        )

        nuevo = Alquiler.nuevaReserva(
            usuario=self.usuarioFinal,
            instalacion=self.instalacion,
            fecha=date.today() + timedelta(days=1),
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            luz=False
        )

        anterior.refresh_from_db()

        self.assertEqual(anterior.estado, EstadoReserva.CANCELADO)
        self.assertIsNotNone(nuevo)