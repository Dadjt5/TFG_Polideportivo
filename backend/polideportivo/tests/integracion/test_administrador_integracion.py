from django.test import TestCase
from django.contrib.auth import get_user_model

from ...models import Administrador, RolAdministrador


class AdministradorIntegrationTest(TestCase):

    def test_registrar_administrador_correcto(self):
        resultado = Administrador.registrarAdministrador(
            nombre="Admin Uno",
            dni="11111111A",
            rol=RolAdministrador.USUARIOS,
            email="admin1@test.com",
            password="123456"
        )

        self.assertFalse(resultado["error"])
        self.assertIsInstance(resultado["respuesta"], Administrador)

        admin = resultado["respuesta"]

        self.assertEqual(admin.rol, RolAdministrador.USUARIOS)
        self.assertEqual(admin.nombre, "Admin Uno")
        self.assertEqual(admin.DNI, "11111111A")
    
    def test_registrar_administrador_correcto_espacios(self):
        resultado = Administrador.registrarAdministrador(
            nombre="Admin Uno",
            dni="11111111A",
            rol=RolAdministrador.ESPACIOS,
            email="admin1@test.com",
            password="123456"
        )

        self.assertFalse(resultado["error"])
        self.assertIsInstance(resultado["respuesta"], Administrador)

        admin = resultado["respuesta"]

        self.assertEqual(admin.rol, RolAdministrador.ESPACIOS)
        self.assertEqual(admin.nombre, "Admin Uno")
        self.assertEqual(admin.DNI, "11111111A")
    
    def test_registrar_administrador_correcto_tarifas(self):
        resultado = Administrador.registrarAdministrador(
            nombre="Admin Uno",
            dni="11111111A",
            rol=RolAdministrador.TARIFAS,
            email="admin1@test.com",
            password="123456"
        )

        self.assertFalse(resultado["error"])
        self.assertIsInstance(resultado["respuesta"], Administrador)

        admin = resultado["respuesta"]

        self.assertEqual(admin.rol, RolAdministrador.TARIFAS)
        self.assertEqual(admin.nombre, "Admin Uno")
        self.assertEqual(admin.DNI, "11111111A")

    def test_registrar_administrador_correcto_raiz(self):
        resultado = Administrador.registrarAdministrador(
            nombre="Admin Uno",
            dni="11111111A",
            rol=RolAdministrador.RAIZ,
            email="admin1@test.com",
            password="123456"
        )

        self.assertFalse(resultado["error"])
        self.assertIsInstance(resultado["respuesta"], Administrador)

        admin = resultado["respuesta"]

        self.assertEqual(admin.rol, RolAdministrador.RAIZ)
        self.assertEqual(admin.nombre, "Admin Uno")
        self.assertEqual(admin.DNI, "11111111A")

    def test_registrar_administrador_dni_duplicado(self):
        User = get_user_model()

        user = User.objects.create_user(
            username="22222222B",
            email="existente@test.com",
            password="123456"
        )

        Administrador.objects.create(
            user=user,
            nombre="Existente",
            DNI="22222222B",
            rol=RolAdministrador.USUARIOS
        )

        resultado = Administrador.registrarAdministrador(
            nombre="Nuevo",
            dni="22222222B",
            rol=RolAdministrador.USUARIOS,
            email="nuevo@test.com",
            password="123456"
        )

        self.assertTrue(resultado["error"])
        self.assertEqual(
            resultado["respuesta"],
            "Ya existe un usuario con ese DNI"
        )

    def test_registrar_administrador_email_duplicado(self):
        User = get_user_model()

        user = User.objects.create_user(
            username="33333333C",
            email="duplicado@test.com",
            password="123456"
        )

        Administrador.objects.create(
            user=user,
            nombre="Existente",
            DNI="33333333C",
            rol=RolAdministrador.USUARIOS
        )

        resultado = Administrador.registrarAdministrador(
            nombre="Nuevo",
            dni="44444444D",
            rol=RolAdministrador.USUARIOS,
            email="duplicado@test.com",
            password="123456"
        )

        self.assertTrue(resultado["error"])
        self.assertEqual(
            resultado["respuesta"],
            "Ya existe un usuario con ese email"
        )

    def test_registrar_administrador_rol_invalido(self):
        resultado = Administrador.registrarAdministrador(
            nombre="Admin",
            dni="55555555E",
            rol="rol_invalido",
            email="admin@test.com",
            password="123456"
        )

        self.assertTrue(resultado["error"])
        self.assertEqual(
            resultado["respuesta"],
            "Rol de administrador inválido"
        )