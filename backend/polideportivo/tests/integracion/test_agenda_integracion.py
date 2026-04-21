from datetime import time
from django.test import TestCase

from ...models import (
    Agenda, MapaReservas, Instalacion, Dia, TipoReserva,
    Pabellon, TipoInstalacion, Calle
)


class AgendaIntegrationTest(TestCase):
    def setUp(self):
        self.pabellon = Pabellon.objects.create(
            nombre="Pabellón central"
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Pista tenis",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.PISCINA,
            numeroCalles=1
        )

        self.agenda = Agenda.objects.create(
            dia=Dia.LUNES,
            instalacion=self.instalacion
        )

    def test_agenda_recupera_slots_relacionados(self):
        MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(9, 0),
            horaFin=time(10, 0),
            estado=TipoReserva.LIBRE
        )

        MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(10, 0),
            horaFin=time(11, 0),
            estado=TipoReserva.ACTIVIDAD
        )

        self.assertEqual(
            self.agenda.mapa_reservas.count(),
            2
        )

    def test_esta_ocupado_consulta_relacion_bd(self):
        MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(12, 0),
            horaFin=time(13, 0),
            estado=TipoReserva.LIBRE
        )

        disponible = self.agenda.estaOcupado(
            horaInicio=time(12, 0),
            horaFin=time(13, 0),
        )

        self.assertFalse(disponible)

    def test_esta_ocupado_consulta_por_calle(self):
        self.instalacion.crearCalles()

        MapaReservas.objects.create(
            agenda=self.agenda,
            horaInicio=time(12, 0),
            horaFin=time(13, 0),
            estado=TipoReserva.LIBRE,
            calle=Calle.objects.create(instalacion=self.instalacion, numero=10)
        )

        disponible = self.agenda.estaOcupado(
            horaInicio=time(12, 0),
            horaFin=time(13, 0),
            calle=self.instalacion.calles.first()
        )

        self.assertTrue(disponible)