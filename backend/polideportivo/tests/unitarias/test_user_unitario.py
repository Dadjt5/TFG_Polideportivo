from django.test import TestCase
from ...models import User, Administrador, RolAdministrador


class UserUnitariasTest(TestCase):

    def test_codigo_usuario_se_genera(self):
        user = User()
        self.assertEqual(len(user.codigo_usuario), 8)

    def test_is_usuario_final_false(self):
        user = User()
        self.assertFalse(user.is_usuario_final)

    def test_is_monitor_false(self):
        user = User()
        self.assertFalse(user.is_monitor)

    def test_is_administrador_false(self):
        user = User()
        self.assertFalse(user.is_administrador)

    def test_is_administrador_raiz_true(self):
        user = User.objects.create(username="admin1")

        admin = Administrador.objects.create(
            user=user,
            rol=RolAdministrador.RAIZ
        )

        self.assertTrue(user.is_administrador_raiz)

    def test_roles_administrador(self):
        user = User.objects.create(username="admin2")

        admin = Administrador.objects.create(
            user=user,
            rol=RolAdministrador.USUARIOS
        )

        self.assertTrue(user.is_administrador_usuarios)
    
        user2 = User.objects.create(username="admin3")
        admin = Administrador.objects.create(
            user=user2,
            rol=RolAdministrador.ESPACIOS
        )

        self.assertTrue(user2.is_administrador_espacios)

        user3 = User.objects.create(username="admin4")
        admin = Administrador.objects.create(
            user=user3,
            rol=RolAdministrador.TARIFAS
        )

        self.assertTrue(user3.is_administrador_tarifas)