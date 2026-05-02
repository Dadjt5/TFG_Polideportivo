from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.contenttypes.models import ContentType

from polideportivo.models import (
    Instalacion,
    Alquiler,
    EstadoReserva
)


class InstalacionViewSetTests(APITestCase):

    def setUp(self):
        self.instalacion = Instalacion.objects.create(
            nombre="Pista 1"
        )

        self.alquiler = Alquiler.objects.create(
            instalacion=self.instalacion,
            estado=EstadoReserva.CONFIRMADA
        )

    @patch("polideportivo.views.Pago.objects.get")
    @patch("polideportivo.views.Notificacion.notificarEliminacionInstalacion")
    def test_eliminar_instalacion_cancela_pagos_y_notifica(
        self,
        mock_notificacion,
        mock_pago_get
    ):
        pago_mock = MagicMock()
        mock_pago_get.return_value = pago_mock

        response = self.client.delete(
            f"/api/instalacion/{self.instalacion.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        mock_notificacion.assert_called_once_with(self.instalacion)
        pago_mock.cancelarPago.assert_called_once()

        self.assertFalse(
            Instalacion.objects.filter(id=self.instalacion.id).exists()
        )