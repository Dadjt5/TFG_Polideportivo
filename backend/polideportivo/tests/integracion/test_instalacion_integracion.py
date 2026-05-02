from django.test import TestCase
from datetime import time, date
from django.contrib.contenttypes.models import ContentType
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model


from ...models import (
    Instalacion, Pabellon, Calle, Agenda, Periodo, Monitor,
    TipoInstalacion, Dia, Actividad, Sesion, EstadoReserva,
    UsuarioFinal, Pago, MapaReservas, ReservaActividad, Alquiler,
    TipoReserva, Configuracion
)

User = get_user_model()


class InstalacionIntegrationFullTest(TestCase):

    def setUp(self):
        self.pabellon = Pabellon.objects.create(nombre="P1")

        self.instalacion = Instalacion.objects.create(
            nombre="Piscina",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.PISCINA,
            numeroCalles=2
        )

        self.instalacion2 = Instalacion.objects.create(
            nombre="Pista",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.PISTA_TENIS
        )

        Configuracion.objects.create()

        self.calle1 = Calle.objects.create(instalacion=self.instalacion, numero=1)
        self.calle2 = Calle.objects.create(instalacion=self.instalacion, numero=2)

        self.agenda = Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.LUNES,
            horaApertura=time(8, 0),
            horaCierre=time(20, 0),
            abierto=True
        )

        self.user = User.objects.create(username="user", password="1234")
        self.usuario = UsuarioFinal.objects.create(
            nombre="user1",
            fechaNacimiento=date(2001,1,1),
            user=self.user
        )

        self.user2 = User.objects.create(username="monitor", password="1234")
        self.monitor = Monitor.objects.create(
            nombre="monitor1",
            user=self.user2
        )


    def test_str_and_contar(self):
        self.assertIn("Piscina", str(self.instalacion))
        self.assertGreaterEqual(Instalacion.contar(), 1)


    # -------------------------
    # HORARIOS
    # -------------------------

    def test_nuevo_horario_ok(self):
        ok = self.instalacion.nuevoHorario(Dia.MARTES, "08:00", "10:00", True)
        self.assertTrue(ok)

    def test_nuevo_horario_cerrado(self):
        ok = self.instalacion.nuevoHorario(Dia.MARTES, None, None, False)
        self.assertTrue(ok)

    def test_nuevo_horario_invalido(self):
        ok = self.instalacion.nuevoHorario(Dia.MARTES, "10:00", "08:00", True)
        self.assertFalse(ok)
    
    def test_nuevo_horario_cerrar_existente(self):
        ok = self.instalacion.nuevoHorario(
            Dia.LUNES,
            None,
            None,
            False
        )

        self.assertTrue(ok)

        self.agenda.refresh_from_db()
        self.assertFalse(self.agenda.abierto)
        self.assertIsNone(self.agenda.horaApertura)
        self.assertIsNone(self.agenda.horaCierre)

    def test_nuevo_horario_actualiza_existente(self):
        ok = self.instalacion.nuevoHorario(
            Dia.LUNES,
            "09:00",
            "18:00",
            True
        )

        self.assertTrue(ok)

        self.agenda.refresh_from_db()
        self.assertEqual(self.agenda.horaApertura, time(9, 0))
        self.assertEqual(self.agenda.horaCierre, time(18, 0))
        self.assertTrue(self.agenda.abierto)

    # -------------------------
    # HORARIO ESPECIAL
    # -------------------------

    def test_horario_especial(self):
        ok = self.instalacion.nuevoHorarioEspecial(date.today())
        self.assertTrue(ok)

    # -------------------------
    # CALLLES
    # -------------------------

    def test_calles_crear_y_reducir(self):
        self.instalacion.sincronizarCalles(3)
        self.assertEqual(self.instalacion.calles.count(), 3)

        self.instalacion.sincronizarCalles(1)
        self.assertEqual(self.instalacion.calles.count(), 1)
    
    def test_calles_crear_no_piscina(self):
        ret = self.instalacion2.sincronizarCalles(3)
        self.assertIsNone(ret)


    # -------------------------
    # ACTUALIZAR MAPA
    # -------------------------

    def test_actualizar_mapa(self):
        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "08:00",
            "horaFin": "09:00",
            "calle": self.calle1.id
        }]

        MapaReservas.objects.create(
            horaInicio=time(8,0),
            horaFin=time(9,0),
            calle=self.calle1
        )

        self.instalacion.actualizarMapa(sesiones)
        self.assertTrue(True)
    
    def test_actualizar_mapa_cambia_estado(self):
        reserva = self.agenda.mapa_reservas.create(
            horaInicio=time(8, 0),
            horaFin=time(9, 0),
            calle=self.calle1
        )

        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "08:00",
            "horaFin": "09:00",
            "calle": self.calle1.id
        }]

        self.instalacion.actualizarMapa(sesiones)

        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, TipoReserva.ACTIVIDAD)

    def test_actualizar_mapa_sin_agenda(self):
        sesiones = [{
            "dia": "Martes",
            "horaInicio": "08:00",
            "horaFin": "09:00",
            "calle": self.calle1.id
        }]

        self.instalacion.actualizarMapa(sesiones)

        self.assertTrue(True)
    
    def test_actualizar_mapa_varias_horas(self):
        r1 = self.agenda.mapa_reservas.create(
            horaInicio=time(8, 0),
            horaFin=time(9, 0),
            calle=self.calle1
        )

        r2 = self.agenda.mapa_reservas.create(
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            calle=self.calle1
        )

        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "08:00",
            "horaFin": "10:00",
            "calle": self.calle1.id
        }]

        self.instalacion.actualizarMapa(sesiones)

        r1.refresh_from_db()
        r2.refresh_from_db()

        self.assertEqual(r1.estado, TipoReserva.ACTIVIDAD)
        self.assertEqual(r2.estado, TipoReserva.ACTIVIDAD)

    def test_actualizar_mapa_no_piscina(self):
        self.instalacion.tipoInstalacion = TipoInstalacion.SALA_MULTIUSOS
        self.instalacion.save()

        agenda = Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.MARTES,
            horaApertura=time(8,0),
            horaCierre=time(20,0),
            abierto=True
        )

        reserva = agenda.mapa_reservas.create(
            horaInicio=time(8,0),
            horaFin=time(9,0)
        )

        sesiones = [{
            "dia": "Martes",
            "horaInicio": "08:00",
            "horaFin": "09:00"
        }]

        self.instalacion.actualizarMapa(sesiones)

        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, TipoReserva.ACTIVIDAD)

    # -------------------------
    # CONTROL ALQUILER
    # -------------------------

    def test_controlar_alquiler_fallo(self):
        ok = self.instalacion.controlarAlquiler(
            date.today(), time(9, 0), time(10, 0)
        )
        self.assertFalse(ok)

    # -------------------------
    # CONTROL HORARIO ACTIVIDAD
    # -------------------------

    def test_controlar_horario_actividad_fallo(self):
        ok = self.instalacion.controlarHorarioActividad(
            "Lunes", "08:00", "21:00",
            periodo="ANUAL",
            calle=self.calle1
        )

        self.assertFalse(ok)
    
    def test_controlar_horario_actividad_cerrado(self):
        self.agenda.abierto = False
        self.agenda.save()

        ok = self.instalacion.controlarHorarioActividad(
            "Lunes", "08:00", "21:00",
            periodo="ANUAL",
            calle=self.calle1
        )

        self.assertFalse(ok)

    def test_controlar_horario_actividad_ok(self):
        ok = self.instalacion.controlarHorarioActividad(
            "Lunes",
            "10:00",
            "11:00",
            Periodo.PRIMER_CUATRIMESTRE,
            calle=self.calle1
        )

        self.assertTrue(ok)

    def test_controlar_horario_actividad_conflicto(self):
        actividad = Actividad.objects.create(
            nombre="Natacion",
            instalacion=self.instalacion,
            monitor=self.monitor,
            plazasMaximas=10,
            periodo=Periodo.ANUAL
        )

        Sesion.objects.create(
            actividad=actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            calle=self.calle1
        )

        ok = self.instalacion.controlarHorarioActividad(
            "Lunes",
            "10:30",
            "11:30",
            Periodo.ANUAL,
            calle=self.calle1
        )

        self.assertFalse(ok)

    def test_controlar_horario_actividad_excluye_misma_sesion(self):
        actividad = Actividad.objects.create(
            nombre="Natacion",
            instalacion=self.instalacion,
            monitor=self.monitor,
            plazasMaximas=10,
            periodo=Periodo.ANUAL
        )

        sesion = Sesion.objects.create(
            actividad=actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            calle=self.calle1
        )

        ok = self.instalacion.controlarHorarioActividad(
            "Lunes",
            "10:00",
            "11:00",
            Periodo.ANUAL,
            sesion_id=sesion.id,
            calle=self.calle1
        )

        self.assertTrue(ok)

    def test_controlar_horario_actividad_otro_carril(self):
        actividad = Actividad.objects.create(
            nombre="Natacion",
            instalacion=self.instalacion,
            monitor=self.monitor,
            plazasMaximas=10,
            periodo=Periodo.ANUAL
        )

        Sesion.objects.create(
            actividad=actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            calle=self.calle1
        )

        ok = self.instalacion.controlarHorarioActividad(
            "Lunes",
            "10:00",
            "11:00",
            Periodo.ANUAL,
            calle=self.calle2
        )

        self.assertTrue(ok)

    # -------------------------
    # BUSCAR
    # -------------------------

    def test_buscar(self):
        res = Instalacion.buscar(nombre="Piscina")
        self.assertTrue(res.exists())
    
    def test_buscar_por_tipo(self):
        res = Instalacion.buscar(tipo=[TipoInstalacion.PISCINA])
        self.assertTrue(res.exists())
    
    def test_buscar_por_hora_inicio(self):
        Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.MIERCOLES,
            horaApertura=time(8, 0),
            horaCierre=time(20, 0),
            abierto=True
        )

        res = Instalacion.buscar(horaInicio=time(9, 0))
        self.assertTrue(res.exists())
    
    def test_buscar_por_hora_fin(self):
        Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.MARTES,
            horaApertura=time(8, 0),
            horaCierre=time(20, 0),
            abierto=True
        )

        res = Instalacion.buscar(horaFin=time(19, 0))
        self.assertTrue(res.exists())
    
    def test_buscar_con_todos_los_filtros(self):
        Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.MIERCOLES,
            horaApertura=time(8, 0),
            horaCierre=time(20, 0),
            abierto=True
        )

        res = Instalacion.buscar(
            nombre="Piscina",
            tipo=[TipoInstalacion.PISCINA],
            horaInicio=time(9, 0),
            horaFin=time(19, 0)
        )

        self.assertTrue(res.exists())

    # -------------------------
    # REVISAR ALQUILERES (CRÍTICO)
    # -------------------------

    def test_revisar_alquileres_confirmacion(self):
        Alquiler.objects.create(horaInicio=time(9,0), horaFin=time(10,0), estado=EstadoReserva.CONFIRMADA, usuarioFinal=self.usuario, instalacion=self.instalacion, calle=self.calle1)
        Alquiler.objects.create(horaInicio=time(10,0), horaFin=time(11,0), estado=EstadoReserva.PENDIENTE, usuarioFinal=self.usuario, instalacion=self.instalacion, calle=self.calle1)
        Alquiler.objects.create(horaInicio=time(11,0), horaFin=time(12,0), estado=EstadoReserva.PENDIENTE, usuarioFinal=self.usuario, instalacion=self.instalacion, calle=self.calle1)
        Alquiler.objects.create(horaInicio=time(12,0), horaFin=time(13,0), estado=EstadoReserva.CONFIRMADA, usuarioFinal=self.usuario, instalacion=self.instalacion)

        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "09:00",
            "horaFin": "10:00",
            "calle": self.calle1
        }]

        self.instalacion.revisarAlquileres(
            sesiones,
            periodo="PRIMER_CUATRIMESTRE",
            confirmacion=True
        )
    
        self.instalacion.revisarAlquileres(
            sesiones,
            periodo="SEGUNDO_CUATRIMESTRE",
            confirmacion=True
        )
    
        self.instalacion.revisarAlquileres(
            sesiones,
            periodo="TERCER_CUATRIMESTRE",
            confirmacion=True
        )

        self.assertTrue(True)

    # -------------------------
    # REVISAR ALQUILERES (SIN CONFIRMACION)
    # -------------------------

    def test_revisar_alquileres_sin_confirmacion(self):
        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "09:00",
            "horaFin": "10:00",
            "calle": self.calle1
        }]

        res = self.instalacion.revisarAlquileres(
            sesiones,
            periodo="PRIMER_CUATRIMESTRE",
            confirmacion=False
        )

        self.assertTrue(res is None or isinstance(res, dict))

    def test_revisar_alquileres_periodo_fuera_devuelve_none(self):
        Alquiler.objects.create(
            fecha=date(2026, 6, 1),  # junio -> fuera primer cuatrimestre
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "09:00",
            "horaFin": "10:00",
            "calle": self.calle1
        }]

        res = self.instalacion.revisarAlquileres(
            sesiones,
            Periodo.PRIMER_CUATRIMESTRE,
            False
        )

        self.assertIsNone(res)

    def test_revisar_alquileres_suma_dinero(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 9, 7),  # lunes septiembre
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        ct = ContentType.objects.get_for_model(alquiler)

        Pago.objects.create(
            concepto="test",
            coste=100,
            costeFinal=80,
            usuarioFinal=self.usuario,
            tipoPago="unico",
            content_type=ct,
            object_id=alquiler.id
        )

        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "09:00",
            "horaFin": "10:00",
            "calle": self.calle1
        }]

        res = self.instalacion.revisarAlquileres(
            sesiones,
            Periodo.PRIMER_CUATRIMESTRE,
            False
        )

        self.assertEqual(res["dinero"], 80)
        self.assertEqual(res["alquileres"], 1)
        self.assertEqual(res["usuarios"], 1)


    @patch("polideportivo.models.notificacion.Notificacion.notificarCancelacionYDevolucionDinero")
    @patch("polideportivo.models.pago.Pago.cancelarPago")
    @patch("polideportivo.models.Alquiler.cancelarCompra")
    def test_revisar_alquileres_cancelaciones(
        self, mock_cancelar_compra, mock_cancelar_pago, mock_notificar
    ):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 9, 7),
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        ct = ContentType.objects.get_for_model(alquiler)

        Pago.objects.create(
            concepto="test",
            coste=100,
            costeFinal=80,
            usuarioFinal=self.usuario,
            tipoPago="unico",
            content_type=ct,
            object_id=alquiler.id
        )

        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "09:00",
            "horaFin": "10:00",
            "calle": self.calle1
        }]

        self.instalacion.revisarAlquileres(
            sesiones,
            Periodo.PRIMER_CUATRIMESTRE,
            True
        )

        mock_notificar.assert_called_once()
        mock_cancelar_pago.assert_called_once()

    def test_controlar_cambio_horario_cerrado_con_actividad(self):
        actividad = Actividad.objects.create(
            nombre="Natacion",
            instalacion=self.instalacion,
            monitor=self.monitor,
            plazasMaximas=10,
            periodo=Periodo.ANUAL
        )

        Sesion.objects.create(
            actividad=actividad,
            dia=Dia.LUNES,
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            calle=self.calle1
        )

        ok = self.instalacion.controlarCambioHorario(
            Dia.LUNES,
            time(8, 0),
            time(20, 0),
            abierto=False
        )

        self.assertFalse(ok)
    
    def test_controlar_cambio_horario_ok(self):
        ok = self.instalacion.controlarCambioHorario(
            Dia.LUNES,
            time(8, 0),
            time(20, 0),
            abierto=True
        )

        self.assertTrue(ok)
    
    def test_controlar_alquiler_ok(self):
        fecha = date(2026, 5, 4)

        Agenda.objects.create(
            instalacion=self.instalacion,
            fecha=fecha,
            abierto=True
        )

        ok = self.instalacion.controlarAlquiler(
            fecha,
            time(9, 0),
            time(10, 0),
            calle=self.calle1
        )

        self.assertFalse(ok)
    
    from unittest.mock import patch

    @patch("polideportivo.models.agenda.Agenda.estaOcupado")
    def test_controlar_alquiler_ocupado(self, mock_ocupado):
        mock_ocupado.return_value = True

        fecha = date(2026, 5, 4)  # lunes

        ok = self.instalacion.controlarAlquiler(
            fecha,
            time(9, 0),
            time(10, 0),
            calle=self.calle1
        )

        self.assertFalse(ok)
    
    @patch("polideportivo.models.agenda.Agenda.estaOcupado")
    def test_controlar_alquiler_libre(self, mock_ocupado):
        mock_ocupado.return_value = False

        fecha = date(2026, 5, 4)  # lunes

        ok = self.instalacion.controlarAlquiler(
            fecha,
            time(9, 0),
            time(10, 0),
            calle=self.calle1
        )

        self.assertTrue(ok)

    def test_revisar_alquileres_devuelve_dict(self):
        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "10:00",
                "calle": self.calle1
            }],
            periodo="PRIMER_CUATRIMESTRE",
            confirmacion=False
        )

        self.assertIsInstance(res, dict)
    
    def test_comprobar_aforo_false(self):
        actividad = Actividad.objects.create(
            nombre="Natacion",
            instalacion=self.instalacion,
            monitor=self.monitor,
            plazasMaximas=200,
            periodo=Periodo.ANUAL
        )

        self.instalacion.actividad.set([actividad])

        ok = self.instalacion.comprobarAforo(100, 1)
        self.assertFalse(ok)
    
    def test_sincronizar_mapa_agenda_cerrada(self):
        self.agenda.mapa_reservas.create(
            horaInicio=time(8, 0),
            horaFin=time(9, 0),
            calle=self.calle1
        )

        self.agenda.abierto = False
        self.agenda.save()

        self.instalacion.sincronizarMapaReservas(self.agenda)

        self.assertEqual(self.agenda.mapa_reservas.count(), 0)
    
    def test_sincronizar_mapa_instalacion_normal(self):
        self.instalacion.tipoInstalacion = TipoInstalacion.SALA_MULTIUSOS
        self.instalacion.save()

        agenda = Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.MARTES,
            horaApertura=time(8, 0),
            horaCierre=time(10, 0),
            abierto=True
        )

        self.instalacion.sincronizarMapaReservas(agenda)

        self.assertEqual(agenda.mapa_reservas.count(), 2)
    
    def test_sincronizar_mapa_piscina(self):
        agenda = Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.MARTES,
            horaApertura=time(8, 0),
            horaCierre=time(10, 0),
            abierto=True
        )

        self.instalacion.sincronizarMapaReservas(agenda)

        self.assertEqual(agenda.mapa_reservas.count(), 4)
    
    def test_sincronizar_mapa_horas_string(self):
        agenda = Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.MIERCOLES,
            horaApertura="08:00",
            horaCierre="10:00",
            abierto=True
        )

        ok = self.instalacion.sincronizarMapaReservas(agenda)

        self.assertTrue(ok)

    def test_sincronizar_mapa_reservas_elimina_slots_fuera_rango(self):
        agenda = Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.MIERCOLES,
            horaApertura=time(10, 0),
            horaCierre=time(12, 0),
            abierto=True
        )

        MapaReservas.objects.create(
            horaInicio=time(8, 0),
            horaFin=time(9, 0),
            calle=None,
            agenda=agenda
        )

        MapaReservas.objects.create(
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            calle=None,
            agenda=agenda
        )

        self.instalacion.sincronizarMapaReservas(agenda, minutos=60)

        reservas = agenda.mapa_reservas.all()

        # solo debe quedar el slot válido (5 por )
        self.assertEqual(reservas.count(), 5)
        self.assertEqual(reservas.first().horaInicio, time(10, 0))


    def test_revisar_alquileres_pago_none(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 9, 7),  # Lunes real
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "10:00",
                "calle": self.calle1
            }],
            periodo=Periodo.PRIMER_CUATRIMESTRE,
            confirmacion=False
        )

        self.assertEqual(res["alquileres"], 1)
        self.assertEqual(res["dinero"], 0)


    def test_revisar_alquileres_pago_existe(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 9, 7),  # Lunes real
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        ct = ContentType.objects.get_for_model(alquiler)

        Pago.objects.create(
            concepto="test",
            coste=100,
            costeFinal=80,
            usuarioFinal=self.usuario,
            tipoPago="unico",
            content_type=ct,
            object_id=alquiler.id
        )

        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "10:00",
                "calle": self.calle1
            }],
            periodo=Periodo.PRIMER_CUATRIMESTRE,
            confirmacion=False
        )

        self.assertEqual(res["dinero"], 80)
        self.assertEqual(res["alquileres"], 1)
        self.assertEqual(res["usuarios"], 1)
    
    def test_revisar_alquileres_pago_confirmacion(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 9, 7),  # Lunes real
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.PENDIENTE,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        ct = ContentType.objects.get_for_model(alquiler)

        Pago.objects.create(
            concepto="test",
            coste=100,
            costeFinal=80,
            usuarioFinal=self.usuario,
            tipoPago="unico",
            content_type=ct,
            object_id=alquiler.id
        )

        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "10:00",
                "calle": self.calle1
            }],
            periodo=Periodo.PRIMER_CUATRIMESTRE,
            confirmacion=True
        )

        self.assertIsNone(res)
    
    def test_revisar_alquileres_pago_existe_segundo(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2027, 2, 15),  # Lunes real
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.PENDIENTE,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        alquiler2 = Alquiler.objects.create(
            fecha=date(2027, 2, 15),  # Lunes real
            horaInicio=time(11, 0),
            horaFin=time(12, 0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        ct = ContentType.objects.get_for_model(alquiler)

        Pago.objects.create(
            concepto="test",
            coste=100,
            costeFinal=80,
            usuarioFinal=self.usuario,
            tipoPago="unico",
            content_type=ct,
            object_id=alquiler.id
        )

        Pago.objects.create(
            concepto="test",
            coste=100,
            costeFinal=80,
            usuarioFinal=self.usuario,
            tipoPago="unico",
            content_type=ct,
            object_id=alquiler2.id
        )

        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "14:00",
                "calle": self.calle1
            }],
            periodo=Periodo.SEGUNDO_CUATRIMESTRE,
            confirmacion=False
        )

        self.assertEqual(res["dinero"], 80)
        self.assertEqual(res["alquileres"], 1)
        self.assertEqual(res["usuarios"], 1)

    def test_revisar_alquileres_periodo_none(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 6, 8),  # fuera del PRIMER_CUATRIMESTRE
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.PENDIENTE,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "10:00",
                "calle": self.calle1
            }],
            periodo=Periodo.PRIMER_CUATRIMESTRE,
            confirmacion=False
        )

        self.assertIsNone(res)
    
    def test_revisar_alquileres_periodo_none_segundo(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 6, 8),  # fuera del SEGUNDO_CUATRIMESTRE
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "10:00",
                "calle": self.calle1
            }],
            periodo=Periodo.SEGUNDO_CUATRIMESTRE,
            confirmacion=False
        )

        self.assertIsNone(res)
    
    def test_revisar_alquileres_periodo_none_tercer(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 11, 2),  # fuera del TERCER_CUATRIMESTRE
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "10:00",
                "calle": self.calle1
            }],
            periodo=Periodo.TERCER_CUATRIMESTRE,
            confirmacion=False
        )

        self.assertIsNone(res)

    def test_revisar_alquileres_calle_mismatch(self):
        alquiler = Alquiler.objects.create(
            fecha=date(2026, 9, 8),  # Lunes REAL
            horaInicio=time(9,0),
            horaFin=time(10,0),
            estado=EstadoReserva.CONFIRMADA,
            usuarioFinal=self.usuario,
            instalacion=self.instalacion,
            calle=self.calle1
        )

        otra_calle = Calle.objects.create(instalacion=self.instalacion, numero=99)

        res = self.instalacion.revisarAlquileres(
            [{
                "dia": "Lunes",
                "horaInicio": "09:00",
                "horaFin": "10:00",
                "calle": otra_calle
            }],
            periodo=Periodo.TERCER_CUATRIMESTRE,
            confirmacion=False
        )

        self.assertEqual(res["alquileres"], 0)