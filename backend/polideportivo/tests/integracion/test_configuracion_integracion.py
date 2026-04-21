from django.test import TestCase
from unittest.mock import patch

from ...models import Configuracion


class ConfiguracionIntegrationTest(TestCase):

    @patch("polideportivo.models.Notificacion.notificarCambioCancelacion")
    def test_editar_lanza_notificacion_si_cambia_cancelacion(self, mock_notificacion):
        config = Configuracion.objects.create(
            dias_minimo_cancelacion=1
        )

        config.editar({
            "dias_minimo_cancelacion": 3
        })

        mock_notificacion.assert_called_once()

    @patch("polideportivo.models.Notificacion.notificarCambioCancelacion")
    def test_editar_no_lanza_notificacion_si_no_cambia(self, mock_notificacion):
        config = Configuracion.objects.create(
            dias_minimo_cancelacion=2
        )

        config.editar({
            "dias_minimo_cancelacion": 2
        })

        mock_notificacion.assert_not_called()