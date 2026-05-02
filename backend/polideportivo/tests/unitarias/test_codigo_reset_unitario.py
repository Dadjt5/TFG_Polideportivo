from django.test import TestCase

from ...models import CodigoResetPassword


class CodigoResetUnitTest(TestCase):
    def test_isValid(self):
        codigo_reset = CodigoResetPassword.objects.create(
            email="user@user.com",
            codigo="ABC123"
        )

        self.assertTrue(codigo_reset.isValid())
