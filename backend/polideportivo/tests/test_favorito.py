from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from datetime import date

from ..models import (
    Favorito, UsuarioFinal, Actividad, Instalacion, Monitor,
    Pabellon
)

User = get_user_model()


class FavoritoTests(TestCase):
    def setUp(self):
        user = User.objects.create(username="user0", password="1234")
        self.usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1))

        monitor_user = User.objects.create(username="monitor0", password="1234")
        monitor = Monitor.objects.create(nombre="monitor0", user=monitor_user)
        pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(pabellon=pabellon)
        self.actividad = Actividad.objects.create(nombre="Yoga", instalacion=self.instalacion, monitor=monitor)


    # ----------------- STR -----------------

    def test_str_actividad(self):
        favorito = Favorito(usuarioFinal=self.usuario, actividad=self.actividad)
        self.assertEqual(str(favorito), f"Usuario: {self.usuario.id}, nacido el 2001-01-01 tiene como actividad favorita: Yoga, en la instalacion , ubicado en el , localizado en ")

    def test_str_instalacion(self):
        favorito = Favorito(usuarioFinal=self.usuario, instalacion=self.instalacion)
        self.assertEqual(str(favorito), f"Usuario: {self.usuario.id}, nacido el 2001-01-01 tiene como instalación favorita: , ubicado en el , localizado en ")

    def test_str_sin_favorito(self):
        favorito = Favorito(usuarioFinal=self.usuario)
        self.assertEqual(str(favorito), f"Usuario: {self.usuario.id}, nacido el 2001-01-01 sin favoritos")


    # ----------------- CONTAR -----------------

    def test_contar_favoritos(self):
        # Usamos objetos reales para poder contar correctamente
        user = User.objects.create_user(username="user2", password="1234")
        usuario_real = UsuarioFinal.objects.create(user=user, nombre="user1", fechaNacimiento=date(2001,1,1))
        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)
        user = User.objects.create_user(username="monitor1", password="1234")
        monitor = Monitor.objects.create(user=user)
        actividad_real = Actividad.objects.create(nombre="Yoga", instalacion=instalacion, monitor=monitor)

        instalacion_real = Instalacion.objects.create(nombre="Piscina", pabellon=pabellon)

        Favorito.objects.create(usuarioFinal=usuario_real, actividad=actividad_real)
        Favorito.objects.create(usuarioFinal=usuario_real, instalacion=instalacion_real)

        self.assertEqual(Favorito.contar(), 2)


    # ----------------- UNICO -----------------

    def test_unique_together(self):
        user = User.objects.create_user(username="user2", password="1234")
        usuario_real = UsuarioFinal.objects.create(user=user, nombre="user2", fechaNacimiento=date(2001,1,1))

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)

        user = User.objects.create_user(username="monitor2", password="1234")
        monitor = Monitor.objects.create(user=user)

        actividad_real = Actividad.objects.create(nombre="Pilates", instalacion=instalacion, monitor=monitor)

        Favorito.objects.create(usuarioFinal=usuario_real, actividad=actividad_real)

        with self.assertRaises(IntegrityError):
            Favorito.objects.create(usuarioFinal=usuario_real, actividad=actividad_real)