from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from ...models import (
    Actividad, ListaEspera, Pabellon, Instalacion, Monitor,
    UsuarioFinal
)


class ListaEsperaIntegrationTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user1 = User.objects.create(username="u1", password="123")
        self.user2 = User.objects.create(username="u2", password="123")

        self.usuario1 = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user1)
        self.usuario2 = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user2)

        self.user = User.objects.create(username="monitor", password="1234")
        self.monitor = Monitor.objects.create(user=self.user)

        self.pabellon = Pabellon.objects.create(nombre="Gran pabellon")
        self.instalacion = Instalacion.objects.create(nombre="Campo 1", pabellon=self.pabellon)
        self.actividad = Actividad.objects.create(nombre="Crossfit", instalacion=self.instalacion, monitor=self.monitor)

        self.lista = ListaEspera.objects.create(actividad=self.actividad)

    def test_flujo_completo_lista_espera(self):
        # Añadir usuarios
        self.lista.nuevaEntrada(self.usuario1)
        self.lista.nuevaEntrada(self.usuario2)

        self.assertEqual(self.lista.registro.count(), 2)

        # Siguiente usuario
        siguiente = self.lista.siguienteUsuario()
        self.assertEqual(siguiente.usuarioFinal, self.usuario1)

        # Salir de lista
        self.lista.salirLista(self.usuario1)
        self.assertEqual(self.lista.registro.count(), 1)

    def test_no_duplicados(self):
        self.lista.nuevaEntrada(self.usuario1)
        self.lista.nuevaEntrada(self.usuario1)

        self.assertEqual(self.lista.registro.count(), 1)