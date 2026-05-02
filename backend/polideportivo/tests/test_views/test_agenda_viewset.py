from rest_framework.test import APITestCase
from rest_framework import status

from polideportivo.models import (
    Agenda,
    TipoReserva
)


class AgendaViewSetTests(APITestCase):

    def setUp(self):
        self.agenda = Agenda.objects.create(
            dia="Lunes"
        )

        self.sesion = Agenda.objects.create(
            dia="Lunes",
            calle=1,
            horaInicio="10:00",
            horaFin="11:00"
        )

        self.reserva_mapa = self.agenda.mapa_reservas.create(
            calle=1,
            horaInicio="10:00",
            estado=TipoReserva.ACTIVIDAD
        )

    def test_eliminar_sesion_libera_reservas_del_mapa(self):
        response = self.client.delete(f"/api/agenda/{self.sesion.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.reserva_mapa.refresh_from_db()
        self.assertEqual(self.reserva_mapa.estado, TipoReserva.LIBRE)

        self.assertFalse(
            Agenda.objects.filter(id=self.sesion.id).exists()
        )