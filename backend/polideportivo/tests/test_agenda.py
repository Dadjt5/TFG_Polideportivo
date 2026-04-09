from django.test import TestCase
from datetime import time

from ..models import (
    Agenda, MapaReservas, TipoReserva, Dia, TipoInstalacion,
    Instalacion, Calle, Pabellon
)


class AgendaTests(TestCase):
    def setUp(self):
        pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(nombre="Piscina Central", tipoInstalacion=TipoInstalacion.PISCINA, pabellon=pabellon)
        self.calle1 = Calle.objects.create(instalacion=self.instalacion, numero=1)
        self.calle2 = Calle.objects.create(instalacion=self.instalacion, numero=2)

        self.agenda = Agenda.objects.create(
            dia=Dia.LUNES,
            instalacion=self.instalacion,
            horaApertura=time(8, 0),
            horaCierre=time(20, 0),
            abierto=True
        )

    # ---------------- STR ----------------

    def test_str_agenda_dia(self):
        self.assertEqual(str(self.agenda), f'Agenda para {Dia.LUNES} de {self.instalacion.nombre}')

    def test_str_agenda_fecha(self):
        agenda_fecha = Agenda.objects.create(
            fecha="2026-04-08",
            instalacion=self.instalacion
        )
        self.assertEqual(str(agenda_fecha), f'Agenda para 2026-04-08 de {self.instalacion.nombre}')


    # ---------------- ESTA OCUPADO ----------------

    def test_esta_ocupado_sin_reservas(self):
        # Sin reservas un slot debe estar libre
        ocupado = self.agenda.estaOcupado(time(9,0), time(10,0))
        self.assertFalse(ocupado)

    def test_esta_ocupado_con_reserva_ocupada(self):
        # Creamos un mapa de reserva ocupada
        MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(9,0),
            horaFin=time(10,0),
            estado=TipoReserva.ACTIVIDAD
        )

        ocupado = self.agenda.estaOcupado(time(9,0), time(10,0))
        self.assertTrue(ocupado)

    def test_esta_ocupado_con_calle(self):
        MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(10,0),
            horaFin=time(11,0),
            estado=TipoReserva.LIBRE,
            calle=self.calle1
        )

        # En una calle diferente no debería estar ocupado
        ocupado = self.agenda.estaOcupado(time(10,0), time(11,0), calle=self.calle2)
        self.assertFalse(ocupado)

        # Pero en la misma calle si
        ocupado_calle1 = self.agenda.estaOcupado(time(10,0), time(11,0), calle=self.calle1)
        self.assertTrue(ocupado_calle1)

    def test_esta_ocupado_agenda_cerrada(self):
        self.agenda.abierto = False
        self.agenda.save()
        ocupado = self.agenda.estaOcupado(time(9,0), time(10,0))
        self.assertTrue(ocupado)



class MapaReservasTests(TestCase):
    def setUp(self):
        pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(nombre="Piscina Central", tipoInstalacion=TipoInstalacion.PISCINA, pabellon=pabellon)
        self.agenda = Agenda.objects.create(
            dia=Dia.LUNES,
            instalacion=self.instalacion,
            horaApertura=time(8,0),
            horaCierre=time(20,0),
            abierto=True
        )

        self.calle1 = Calle.objects.create(instalacion=self.instalacion, numero=1)
        self.calle2 = Calle.objects.create(instalacion=self.instalacion, numero=2)


    # ---------------- CREACION ----------------

    def test_crear_mapa_reserva(self):
        reserva = MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(9,0),
            horaFin=time(10,0),
            estado=TipoReserva.LIBRE,
            calle=self.calle1
        )
        self.assertEqual(reserva.agenda, self.agenda)
        self.assertEqual(reserva.calle, self.calle1)
        self.assertEqual(reserva.estado, TipoReserva.LIBRE)


    # ---------------- STR ----------------

    def test_str_mapa_reserva(self):
        reserva = MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(9,0),
            horaFin=time(10,0),
            estado=TipoReserva.LIBRE,
            calle=self.calle1
        )

        self.assertEqual(str(reserva), f'{Dia.LUNES} 09:00:00-10:00:00')


    # ---------------- ORDEN DE LAS RESERVAS ----------------

    def test_ordering_mapa_reservas(self):
        # Creamos do reservas desordenadas
        reserva1 = MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(11,0),
            horaFin=time(12,0)
        )

        reserva2 = MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(9,0),
            horaFin=time(10,0)
        )

        reservas = list(MapaReservas.objects.filter(agenda=self.agenda))

        # Deberian estar ordenadas por horaInicio
        self.assertEqual(reservas, [reserva2, reserva1])