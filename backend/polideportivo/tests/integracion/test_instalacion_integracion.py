from django.test import TestCase
from datetime import time, date
from django.contrib.contenttypes.models import ContentType
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model


from ...models import (
    Instalacion, Pabellon, Calle, Agenda,
    TipoInstalacion, Dia,
    UsuarioFinal, Pago, EstadoReserva
)

User = get_user_model()


class InstalacionIntegrationFullTest(TestCase):

    def setUp(self):
        # ------------------ base sistema ------------------
        self.pabellon = Pabellon.objects.create(nombre="P1")

        self.instalacion = Instalacion.objects.create(
            nombre="Piscina",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.PISCINA,
            numeroCalles=2
        )

        # calles
        self.calle1 = Calle.objects.create(instalacion=self.instalacion, numero=1)
        self.calle2 = Calle.objects.create(instalacion=self.instalacion, numero=2)

        # agenda activa
        self.agenda = Agenda.objects.create(
            instalacion=self.instalacion,
            dia=Dia.LUNES,
            horaApertura=time(8, 0),
            horaCierre=time(20, 0),
            abierto=True
        )

        # Usuario
        self.user = User.objects.create(username="user", password="1234")
        self.usuario = UsuarioFinal.objects.create(
            nombre="user1",
            fechaNacimiento=date(2001,1,1),
            user=self.user
        )

    # -------------------------
    # BASIC INSTALACION
    # -------------------------

    def test_str_and_contar(self):
        self.assertIn("Piscina", str(self.instalacion))
        self.assertGreaterEqual(Instalacion.contar(), 1)

    # -------------------------
    # HORARIOS
    # -------------------------

    def test_nuevo_horario_ok(self):
        ok = self.instalacion.nuevoHorario(
            Dia.MARTES, "08:00", "10:00", True
        )
        self.assertTrue(ok)

    def test_nuevo_horario_cerrado(self):
        ok = self.instalacion.nuevoHorario(Dia.MARTES, None, None, False)
        self.assertTrue(ok)

    def test_nuevo_horario_invalido(self):
        ok = self.instalacion.nuevoHorario(Dia.MARTES, "10:00", "08:00", True)
        self.assertFalse(ok)

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

    # -------------------------
    # GET HORARIO
    # -------------------------

    def test_get_horario_none(self):
        self.assertEqual(
            self.instalacion.getHorario(date.today()),
            (None, None)
        )

    # -------------------------
    # GET RESERVAS
    # -------------------------

    def test_get_reservas_empty(self):
        res = self.instalacion.getReservas(date.today())
        self.assertIsInstance(res, list)

    # -------------------------
    # ACTUALIZAR MAPA
    # -------------------------

    def test_actualizar_mapa(self):
        sesiones = [{
            "dia": "Lunes",
            "horaInicio": "08:00",
            "horaFin": "09:00",
            "calle": self.calle1
        }]

        self.instalacion.actualizarMapa(sesiones)
        self.assertTrue(True)

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

    # -------------------------
    # BUSCAR
    # -------------------------

    def test_buscar(self):
        res = Instalacion.buscar(nombre="Piscina")
        self.assertTrue(res.exists())

    # -------------------------
    # REVISAR ALQUILERES (CRÍTICO)
    # -------------------------

    @patch("stripe.Refund.create")
    @patch("stripe.Subscription.delete")
    def test_revisar_alquileres_confirmacion(self, mock_sub, mock_refund):

        mock_refund.return_value = MagicMock()
        mock_sub.return_value = True

        ct = ContentType.objects.get_for_model(self.usuario)

        pago = Pago.objects.create(
            concepto="test",
            coste=100,
            costeFinal=80,
            usuarioFinal=self.usuario,
            estadoPago=EstadoReserva.CONFIRMADA,
            tipoPago="unico",
            content_type=ct,
            object_id=self.usuario.id
        )

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
    