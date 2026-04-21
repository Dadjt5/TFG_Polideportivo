from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from ...models import (
    Favorito, UsuarioFinal, Actividad, Instalacion, Pabellon,
    Monitor
)


class FavoritoUnitTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create(
            username="testuser",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(
            user=self.user,
            fechaNacimiento=date(2001,1,1)
        )

        self.user2 = User.objects.create(
            username="monitor",
            password="1234"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.pabellon = Pabellon.objects.create(
            nombre="Principal"
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Piscina",
            pabellon=self.pabellon
        )

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            instalacion=self.instalacion,
            monitor=self.monitor
        )


    def test_contar(self):
        Favorito.objects.create(usuarioFinal=self.usuario)

        self.assertEqual(Favorito.contar(), 1)

    def test_str_con_actividad(self):
        fav = Favorito(
            usuarioFinal=self.usuario,
            actividad=self.actividad
        )

        self.assertIn("actividad favorita", str(fav))

    def test_str_con_instalacion(self):
        fav = Favorito(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion
        )

        self.assertIn("instalación favorita", str(fav))

    def test_str_sin_relaciones(self):
        fav = Favorito(usuarioFinal=self.usuario)

        self.assertIn("sin favoritos", str(fav))