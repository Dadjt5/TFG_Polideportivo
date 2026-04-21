from django.test import TestCase
from datetime import date
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model

from ...models import UsuarioFinal, Sexo, Rol


class UsuarioFinalUnitTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.auth_user = User.objects.create_user(
            username="juan123",
            email="juan@test.com",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(
            user=self.auth_user,
            nombre="Juan",
            apellidos="Pérez",
            fechaNacimiento=date(2000, 1, 1),
            DNI="12345678A",
            sexo=Sexo.NINGUNO,
            esUAM=False
        )

    # ----------------- STR -----------------

    def test_str(self):
        texto = str(self.usuario)

        self.assertIn("Usuario:", texto)
        self.assertIn("2000-01-01", texto)

    # ----------------- SAVE -----------------

    def test_save_esUAM_false(self):
        self.usuario.esUAM = False
        self.usuario.save()

        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.rol, Rol.EXTERNO)

    def test_save_esUAM_true(self):
        self.usuario.esUAM = True
        self.usuario.save()

        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.rol, Rol.ESTUDIANTE)

    # ----------------- ABONO -----------------

    def test_marcar_abono(self):
        self.usuario.marcarAbono(True)

        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.tieneAbono)

    @patch("polideportivo.models.usuario_final.UsuarioFinal.abono")
    def test_comprobar_abono_true(self, mock_abono):
        mock_abono.exists.return_value = True

        self.usuario.comprobarAbono()

        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.tieneAbono)

    @patch("polideportivo.models.usuario_final.UsuarioFinal.abono")
    def test_comprobar_abono_false(self, mock_abono):
        mock_abono.exists.return_value = False

        self.usuario.comprobarAbono()

        self.usuario.refresh_from_db()
        self.assertFalse(self.usuario.tieneAbono)

    # ----------------- CONTAR -----------------

    def test_contar(self):
        self.assertEqual(UsuarioFinal.contar(), 1)