from django.test import TestCase

from ..models import Usuario

# Mock de usuario
class UsuarioMock(Usuario):
    class Meta:
        app_label = 'polideportivo'


class UsuarioTests(TestCase):
    def setUp(self):
        self.usuario = UsuarioMock(
            nombre="Juan",
            apellidos="Pérez",
            DNI="12345678A"
        )


    # ----------------- STR -----------------

    def test_str_completo(self):
        self.assertEqual(str(self.usuario), "Juan Pérez")

    def test_str_sin_apellidos(self):
        usuario = UsuarioMock(nombre="Juan", apellidos=None)
        self.assertEqual(str(usuario), "Juan None")

    def test_str_vacio(self):
        usuario = UsuarioMock()
        self.assertEqual(str(usuario), " None")