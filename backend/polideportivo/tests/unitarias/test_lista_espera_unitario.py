from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from ...models import (
    Actividad, ListaEspera, EntradaListaEspera, Pabellon,
    Instalacion, Monitor, UsuarioFinal
)


class ListaEsperaUnitTest(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user1 = User.objects.create_user(username="u1", password="123")
        self.user2 = User.objects.create_user(username="u2", password="123")

        self.usuario1 = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user1)
        self.usuario2 = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user2)

        self.user3 = User.objects.create_user(username="monitor", password="123")

        self.monitor = Monitor.objects.create(user=self.user3)

        self.pabellon = Pabellon.objects.create(
            nombre="Principal"
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Sala 1",
            pabellon=self.pabellon
        )

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            instalacion=self.instalacion,
            monitor=self.monitor
        )

        self.lista = ListaEspera.objects.create(actividad=self.actividad)

    def test_str(self):
        self.assertIn("Yoga", str(self.lista))

    def test_nueva_entrada(self):
        resultado = self.lista.nuevaEntrada(self.usuario1)

        self.assertEqual(resultado, 1)
        self.assertEqual(self.lista.registro.count(), 1)

    def test_nueva_entrada_duplicada(self):
        self.lista.nuevaEntrada(self.usuario1)
        resultado = self.lista.nuevaEntrada(self.usuario1)

        self.assertIsNone(resultado)

    def test_salir_lista(self):
        self.lista.nuevaEntrada(self.usuario1)
        self.lista.salirLista(self.usuario1)

        self.assertEqual(self.lista.registro.count(), 0)

    def test_siguiente_usuario(self):
        self.lista.nuevaEntrada(self.usuario1)
        self.lista.nuevaEntrada(self.usuario2)

        siguiente = self.lista.siguienteUsuario()

        self.assertIsNotNone(siguiente)
        self.assertEqual(siguiente.usuarioFinal, self.usuario1)
    
    def test_siguiente_usuario_fallo(self):
        siguiente = self.lista.siguienteUsuario()

        self.assertIsNone(siguiente)


class EntradaListaEsperaUnitTest(TestCase):

    def test_str(self):
        User = get_user_model()

        user = User.objects.create_user(username="u", password="123")
        usuario1 = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=user)

        pabellon = Pabellon.objects.create(
            nombre="Principal"
        )

        instalacion = Instalacion.objects.create(
            nombre="Sala 1",
            pabellon=pabellon
        )

        user3 = User.objects.create_user(username="monitor", password="123")

        monitor = Monitor.objects.create(user=user3)
        
        actividad = Actividad.objects.create(nombre="Pilates", instalacion=instalacion, monitor=monitor)
        lista = ListaEspera.objects.create(actividad=actividad)

        entrada = EntradaListaEspera.objects.create(
            usuarioFinal=usuario1,
            listaEspera=lista
        )

        self.assertIn("Fecha", str(entrada))

    def test_contar(self):
        self.assertEqual(EntradaListaEspera.contar(), 0)