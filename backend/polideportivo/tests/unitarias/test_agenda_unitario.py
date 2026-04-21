from datetime import date, time
from django.test import TestCase

from ...models import (
    Agenda, MapaReservas, Instalacion, Dia, TipoReserva,
    Pabellon, Calle
)


class AgendaUnitTest(TestCase):

    def setUp(self):
        self.pabellon = Pabellon.objects.create(
            nombre="Pabellón central"
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Pista central",
            pabellon=self.pabellon
        )

    def test_save_no_permite_fecha_y_dia(self):
        agenda = Agenda(
            fecha=date.today(),
            dia=Dia.LUNES,
            instalacion=self.instalacion
        )

        with self.assertRaises(ValueError):
            agenda.save()

    def test_save_fecha_cierra_instalacion(self):
        agenda = Agenda.objects.create(
            fecha=date.today(),
            instalacion=self.instalacion
        )

        self.assertFalse(agenda.abierto)
        self.assertIsNone(agenda.horaApertura)
        self.assertIsNone(agenda.horaCierre)

    def test_str_con_dia(self):
        agenda = Agenda.objects.create(
            dia=Dia.LUNES,
            instalacion=self.instalacion
        )

        self.assertIn("Agenda para", str(agenda))

    def test_str_con_fecha(self):
        agenda = Agenda.objects.create(
            fecha=date.today(),
            instalacion=self.instalacion
        )

        self.assertIn(str(date.today()), str(agenda))
    

    def test_esta_ocupado_agenda_cerrada(self):
        agenda = Agenda.objects.create(
            dia=Dia.LUNES,
            abierto=False,
            instalacion=self.instalacion
        )

        ocupado = agenda.estaOcupado(
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertTrue(ocupado)

    def test_esta_ocupado_slot_libre(self):
        agenda = Agenda.objects.create(
            dia=Dia.LUNES,
            instalacion=self.instalacion
        )

        MapaReservas.objects.create(
            agenda=agenda,
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            estado=TipoReserva.LIBRE
        )

        ocupado = agenda.estaOcupado(
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertFalse(ocupado)

    def test_esta_ocupado_slot_ocupado(self):
        agenda = Agenda.objects.create(
            dia=Dia.LUNES,
            instalacion=self.instalacion
        )

        MapaReservas.objects.create(
            agenda=agenda,
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            estado=TipoReserva.ACTIVIDAD
        )

        ocupado = agenda.estaOcupado(
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertTrue(ocupado)


class MapaReservasUnitTest(TestCase):
    def setUp(self):
        self.pabellon = Pabellon.objects.create(
            nombre="Pabellón central"
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Pista central",
            pabellon=self.pabellon
        )

        self.instalacion2 = Instalacion.objects.create(
            nombre="piscina",
            pabellon=self.pabellon
        )

        self.agenda = Agenda.objects.create(
            dia=Dia.LUNES,
            instalacion=self.instalacion
        )

    def test_str_mapa_reservas(self):
        mapa = MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertIn("10:00:00", str(mapa))
    
    def test_str_con_calle(self):
        mapa = MapaReservas.objects.create(
            calle = Calle.objects.create(numero=5, instalacion=self.instalacion2),
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )

        self.assertIn(str(time(10,0)), str(mapa))