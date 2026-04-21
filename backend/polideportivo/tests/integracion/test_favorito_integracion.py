from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model

from ...models import (
    Favorito, UsuarioFinal, Actividad, Instalacion, Monitor,
    Pabellon
)

User = get_user_model()


class FavoritoIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user1", password="1234")
        self.user2 = User.objects.create(username="monitor1", password="1234")

        self.usuario = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user)
        self.monitor = Monitor.objects.create(user=self.user2)

        self.pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(nombre="Pista 1", pabellon=self.pabellon)

        self.actividad = Actividad.objects.create(nombre="Tenis", instalacion=self.instalacion, monitor=self.monitor)

    def test_unico_favorito_actividad(self):
        Favorito.objects.create(
            usuarioFinal=self.usuario,
            actividad=self.actividad
        )

        with self.assertRaises(Exception):
            Favorito.objects.create(
                usuarioFinal=self.usuario,
                actividad=self.actividad
            )

    def test_unico_favorito_instalacion(self):
        Favorito.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion
        )

        with self.assertRaises(Exception):
            Favorito.objects.create(
                usuarioFinal=self.usuario,
                instalacion=self.instalacion
            )

    def test_favorito_diferente_permitido(self):
        Favorito.objects.create(
            usuarioFinal=self.usuario,
            actividad=self.actividad
        )

        fav2 = Favorito.objects.create(
            usuarioFinal=self.usuario,
            instalacion=self.instalacion
        )

        self.assertIsNotNone(fav2)