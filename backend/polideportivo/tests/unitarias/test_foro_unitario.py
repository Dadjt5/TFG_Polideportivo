from django.test import TestCase

from ...models import Foro, Canal, Mensaje


class ForoUnitTest(TestCase):

    def test_str(self):
        foro = Foro.objects.create(numeroParticipantes=5)
        self.assertIn("5", str(foro))


class CanalUnitTest(TestCase):

    def test_str(self):
        canal = Canal.objects.create(
            titulo="General",
            tema="Deportes",
            foro=Foro.objects.create(titulo="Foro")
        )

        self.assertIn("General", str(canal))

    def test_contar(self):
        foro = Foro.objects.create(titulo="F")
        Canal.objects.create(titulo="C1", tema="T", foro=foro)

        self.assertEqual(Canal.contar(), 1)

    def test_get_mensajes(self):
        foro = Foro.objects.create(titulo="F")
        canal = Canal.objects.create(titulo="C1", tema="T", foro=foro)

        self.assertEqual(canal.getMensajes().count(), 0)


class MensajeUnitTest(TestCase):

    def test_str(self):
        foro = Foro.objects.create(titulo="F")
        canal = Canal.objects.create(titulo="C", tema="T", foro=foro)

        mensaje = Mensaje.objects.create(
            canal=canal,
            texto="Hola"
        )

        self.assertEqual("Mensaje en C", str(mensaje))