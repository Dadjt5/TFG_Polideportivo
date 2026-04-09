from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Administrador, RolAdministrador

User = get_user_model()


class AdministradorTests(TestCase):

    # ---------------- REGISTRO ----------------

    def test_registrar_administrador_exitoso(self):
        result = Administrador.registrarAdministrador(
            nombre="Juan Perez",
            dni="12345678A",
            rol=RolAdministrador.USUARIOS,
            email="juan@example.com",
            password="1234abcd"
        )

        self.assertFalse(result["error"])
        admin = result["respuesta"]
        self.assertEqual(admin.nombre, "Juan Perez")
        self.assertEqual(admin.DNI, "12345678A")
        self.assertEqual(admin.rol, RolAdministrador.USUARIOS)
        self.assertTrue(User.objects.filter(username="12345678A").exists())

    def test_registrar_administrador_dni_existente(self):
        User.objects.create_user(username="12345678A", email="otro@example.com", password="pass")
        result = Administrador.registrarAdministrador(
            nombre="Juan Perez",
            dni="12345678A",
            rol=RolAdministrador.USUARIOS,
            email="juan@example.com",
            password="1234abcd"
        )

        self.assertTrue(result["error"])
        self.assertEqual(result["respuesta"], "Ya existe un usuario con ese DNI")

    def test_registrar_administrador_email_existente(self):
        User.objects.create_user(username="98765432B", email="juan@example.com", password="pass")
        result = Administrador.registrarAdministrador(
            nombre="Juan Perez",
            dni="12345678A",
            rol=RolAdministrador.USUARIOS,
            email="juan@example.com",
            password="1234abcd"
        )

        self.assertTrue(result["error"])
        self.assertEqual(result["respuesta"], "Ya existe un usuario con ese email")

    def test_registrar_administrador_rol_invalido(self):
        result = Administrador.registrarAdministrador(
            nombre="Juan Perez",
            dni="12345678A",
            rol="ROL_INVALIDO",
            email="juan@example.com",
            password="1234abcd"
        )

        self.assertTrue(result["error"])
        self.assertEqual(result["respuesta"], "Rol de administrador inválido")


    # ---------------- STR ----------------

    def test_str_administrador(self):
        result = Administrador.registrarAdministrador(
            nombre="Juan Perez",
            dni="12345678A",
            rol=RolAdministrador.USUARIOS,
            email="juan@example.com",
            password="1234abcd"
        )

        admin = result["respuesta"]
        self.assertEqual(str(admin), "Juan Perez, rol: Administrador de usuarios")


    # ---------------- ELIMINACION ----------------

    def test_delete_elimina_usuario_django(self):
        result = Administrador.registrarAdministrador(
            nombre="Juan Perez",
            dni="12345678A",
            rol=RolAdministrador.USUARIOS,
            email="juan@example.com",
            password="1234abcd"
        )

        admin = result["respuesta"]
        user_id = admin.user.id
        admin.delete()
        self.assertFalse(Administrador.objects.filter(id=admin.id).exists())
        self.assertFalse(User.objects.filter(id=user_id).exists())