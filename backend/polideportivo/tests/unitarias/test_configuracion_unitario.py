from django.test import TestCase

from ...models import Configuracion


class ConfiguracionUnitTest(TestCase):

    def test_str(self):
        config = Configuracion.objects.create()

        self.assertEqual(
            str(config),
            "Configuración global de la aplicación"
        )

    def test_solo_una_configuracion(self):
        Configuracion.objects.create()

        with self.assertRaises(ValueError):
            Configuracion.objects.create()

    def test_editar_campos(self):
        config = Configuracion.objects.create()

        resultado = config.editar({
            "max_deportes_por_usuario": 8,
            "dias_maximo_alquiler": 10
        })

        config.refresh_from_db()

        self.assertTrue(resultado)
        self.assertEqual(config.max_deportes_por_usuario, 8)
        self.assertEqual(config.dias_maximo_alquiler, 10)

    def test_editar_ignora_campos_invalidos(self):
        config = Configuracion.objects.create()

        config.editar({
            "campo_inexistente": 123,
            "dias_minimo_alquiler": 2
        })

        config.refresh_from_db()

        self.assertEqual(config.dias_minimo_alquiler, 2)