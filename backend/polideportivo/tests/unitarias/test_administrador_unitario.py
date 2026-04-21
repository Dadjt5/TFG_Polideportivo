from django.test import TestCase
from django.contrib.auth import get_user_model

from ...models import Administrador, RolAdministrador


class AdministradorUnitTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="12345678A",
            email="admin@test.com",
            password="123456"
        )

        self.admin = Administrador.objects.create(
            user=self.user,
            nombre="David",
            DNI="12345678A",
            rol=RolAdministrador.USUARIOS
        )

    def test_str(self):
        texto = str(self.admin)

        self.assertIn("David", texto)
        self.assertIn(RolAdministrador.USUARIOS, texto)

    def test_delete_elimina_user_asociado(self):
        user_id = self.user.id

        self.admin.delete()

        User = get_user_model()

        self.assertFalse(
            User.objects.filter(id=user_id).exists()
        )