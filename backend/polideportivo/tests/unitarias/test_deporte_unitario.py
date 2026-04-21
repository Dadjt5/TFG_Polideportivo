from django.test import TestCase

from ...models import Deporte


class DeporteUnitTest(TestCase):

    def test_str(self):
        deporte = Deporte.objects.create(
            titulo="Tenis"
        )

        self.assertEqual(
            str(deporte),
            "Tenis"
        )

    def test_contar(self):
        Deporte.objects.create(titulo="Tenis")
        Deporte.objects.create(titulo="Natación")

        self.assertEqual(
            Deporte.contar(),
            2
        )