from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, PropertyMock
from datetime import date

from ..models import RolAdministrador, UsuarioFinal, Monitor


class UserTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="juan123", email="juan@test.com", password="1234"
        )


    # ----------------- CODIGO USUARIO -----------------

    def test_codigo_usuario_generado(self):
        self.assertIsNotNone(self.user.codigo_usuario)
        self.assertEqual(len(self.user.codigo_usuario), 8)

    def test_codigo_usuario_unico(self):
        User = get_user_model()
        otro_user = User.objects.create_user(
            username="maria123", email="maria@test.com", password="1234"
        )
        self.assertNotEqual(self.user.codigo_usuario, otro_user.codigo_usuario)


    # ----------------- PROPIEDADES -----------------

    def test_is_usuario_final(self):
        with patch.object(type(self.user), 'is_usuario_final', new_callable=PropertyMock) as mock_prop:
            mock_prop.return_value = True
            self.assertTrue(self.user.is_usuario_final)
    
    def test_is_usuario_final(self):
        self.assertFalse(self.user.is_usuario_final)

        UsuarioFinal.objects.create(
            user=self.user,
            nombre="Juan",
            apellidos="Test",
            DNI="12345678A",
            fechaNacimiento=date(2001,1,1)
        )

        self.assertTrue(self.user.is_usuario_final)

    def test_is_monitor(self):
        with patch.object(type(self.user), 'is_monitor', new_callable=PropertyMock) as mock_prop:
            mock_prop.return_value = True
            self.assertTrue(self.user.is_monitor)
    
    def test_is_monitor(self):
        self.assertFalse(self.user.is_monitor)

        Monitor.objects.create(
            user=self.user,
            nombre="Juan",
            apellidos="Test",
            DNI="12345678A"
        )

        self.assertTrue(self.user.is_monitor)

    def test_is_administrador(self):
        with patch.object(type(self.user), 'is_administrador', new_callable=PropertyMock) as mock_prop:
            mock_prop.return_value = True
            self.assertTrue(self.user.is_administrador)

    def test_is_administrador_raiz(self):
        with patch.object(type(self.user), 'administrador', new_callable=PropertyMock) as mock_admin:
            mock_admin.return_value = type('AdminMock', (), {'rol': RolAdministrador.RAIZ})()
            self.assertTrue(self.user.is_administrador_raiz)

            mock_admin.return_value.rol = RolAdministrador.ESPACIOS
            self.assertFalse(self.user.is_administrador_raiz)

    def test_is_administrador_espacios(self):
        with patch.object(type(self.user), 'administrador', new_callable=PropertyMock) as mock_admin:
            mock_admin.return_value = type('AdminMock', (), {'rol': RolAdministrador.ESPACIOS})()
            self.assertTrue(self.user.is_administrador_espacios)

            mock_admin.return_value.rol = RolAdministrador.USUARIOS
            self.assertFalse(self.user.is_administrador_espacios)

    def test_is_administrador_usuarios(self):
        with patch.object(type(self.user), 'administrador', new_callable=PropertyMock) as mock_admin:
            mock_admin.return_value = type('AdminMock', (), {'rol': RolAdministrador.USUARIOS})()
            self.assertTrue(self.user.is_administrador_usuarios)

            mock_admin.return_value.rol = RolAdministrador.TARIFAS
            self.assertFalse(self.user.is_administrador_usuarios)

    def test_is_administrador_tarifas(self):
        with patch.object(type(self.user), 'administrador', new_callable=PropertyMock) as mock_admin:
            mock_admin.return_value = type('AdminMock', (), {'rol': RolAdministrador.TARIFAS})()
            self.assertTrue(self.user.is_administrador_tarifas)

            mock_admin.return_value.rol = RolAdministrador.RAIZ
            self.assertFalse(self.user.is_administrador_tarifas)