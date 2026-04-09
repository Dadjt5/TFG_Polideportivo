from django.test import TestCase
from django.core.exceptions import ValidationError
from unittest.mock import patch

from ..models import Configuracion


class ConfiguracionTests(TestCase):
    def setUp(self):
        self.config = Configuracion.objects.create(
            max_deportes_por_usuario=5,
            dias_minimo_alquiler=0,
            dias_maximo_alquiler=7,
            dias_minimo_cancelacion=1,
            horas_alquiler_consecutivas=2,
            porcentaje_maximo=100
        )


    # ----------------- STR -----------------

    def test_str_configuracion(self):
        self.assertEqual(str(self.config), "Configuración global de la aplicación")


    # ----------------- CONFIGURACION UNICA -----------------

    def test_unica_configuracion(self):
        from django.db import IntegrityError
        with self.assertRaises(ValueError):
            Configuracion.objects.create(
                max_deportes_por_usuario=10
            )


    # ----------------- MODIFICAR CAMPOS -----------------

    def test_editar_campos(self):
        data = {
            "max_deportes_por_usuario": 8,
            "dias_minimo_alquiler": 2
        }
        resultado = self.config.editar(data)
        self.assertTrue(resultado)
        self.config.refresh_from_db()
        self.assertEqual(self.config.max_deportes_por_usuario, 8)
        self.assertEqual(self.config.dias_minimo_alquiler, 2)

    @patch('polideportivo.models.Notificacion.notificarCambioCancelacion')
    def test_editar_cambio_dias_minimo_cancelacion(self, mock_notificar):
        data = {"dias_minimo_cancelacion": 5}
        resultado = self.config.editar(data)
        self.assertTrue(resultado)
        self.config.refresh_from_db()
        self.assertEqual(self.config.dias_minimo_cancelacion, 5)
        mock_notificar.assert_called_once()

    def test_editar_campo_inexistente(self):
        data = {"campo_inexistente": 123}
        resultado = self.config.editar(data)
        self.assertTrue(resultado)