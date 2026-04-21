from django.test import TestCase

from ...models import Usuario


class UsuarioAbstractoUnitariasTest(TestCase):

    def test_campos_existen_en_subclase(self):
        self.assertTrue(hasattr(Usuario, "nombre"))
        self.assertTrue(hasattr(Usuario, "apellidos"))
        self.assertTrue(hasattr(Usuario, "DNI"))

    def test_str_logic_conceptual(self):
        class FakeUsuario(Usuario):
            class Meta:
                app_label = "app"

        u = FakeUsuario(nombre="Ana", apellidos="García")

        self.assertEqual(str(u), "Ana García")