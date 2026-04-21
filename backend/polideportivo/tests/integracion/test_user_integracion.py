from django.test import TestCase

from ...models import User


class UserIntegracionTest(TestCase):

    def test_creacion_usuario_db(self):
        user = User.objects.create_user(
            username="testuser",
            password="1234"
        )

        self.assertIsNotNone(user.id)
        self.assertEqual(len(user.codigo_usuario), 8)

    def test_recuperacion_usuario_db(self):
        User.objects.create_user(
            username="testuser2",
            password="1234"
        )

        user = User.objects.first()

        self.assertEqual(user.username, "testuser2")