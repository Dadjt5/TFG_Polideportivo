from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import time, date
from django.contrib.auth import get_user_model


from polideportivo.models import (
    Instalacion, Alquiler, EstadoReserva, Pabellon, UsuarioFinal
)


class InstalacionViewSetTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(
            nombre="Pista 1",
            pabellon=self.pabellon
        )

        self.alquiler = Alquiler.objects.create(
            instalacion=self.instalacion,
            horaInicio=time(10,0),
            horaFin=time(12,0),
            usuarioFinal=self.usuario,
            estado=EstadoReserva.CONFIRMADA
        )

    @patch("polideportivo.models.Pago.objects.get")
    @patch("polideportivo.models.Notificacion.notificarEliminacionInstalacion")
    def test_eliminar_instalacion_cancela_pagos_y_notifica(
        self,
        mock_notificacion,
        mock_pago_get
    ):
        pago_mock = MagicMock()
        mock_pago_get.return_value = pago_mock

        response = self.client.delete(
            f"/api/v1/instalaciones/{self.instalacion.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)