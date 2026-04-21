from django.test import TestCase
from django.db.utils import IntegrityError
from datetime import date, time, timedelta
from django.contrib.auth import get_user_model


from ..models import ListaEspera, EntradaListaEspera, UsuarioFinal, Actividad, Pabellon, Instalacion, Monitor

User = get_user_model()


class ListaEsperaTests(TestCase):
    def setUp(self):
        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)
        user = User.objects.create_user(username="monitor1", password="1234")
        monitor = Monitor.objects.create(user=user)
        self.actividad = Actividad.objects.create(nombre="Yoga", instalacion=instalacion, monitor=monitor)

        self.usuario = UsuarioFinal.objects.create(user=user, nombre="user_real", fechaNacimiento=date(2000, 1, 1))

        self.lista = ListaEspera.objects.create(actividad=self.actividad)


    # ----------------- STR -----------------

    def test_str(self):
        self.assertEqual(str(self.lista), f'Lista de espera para {self.actividad}')


    # ----------------- NUEVA ENTRADA -----------------

    def test_nuevaEntrada_retorna_contador(self):
        contador = self.lista.nuevaEntrada(self.usuario)
        self.assertEqual(contador, 1)

        contador_dup = self.lista.nuevaEntrada(self.usuario)
        self.assertIsNone(contador_dup)


    # ----------------- SALIR DE LISTA -----------------

    def test_salirLista_elimina_usuario(self):
        self.lista.nuevaEntrada(self.usuario)
        self.assertEqual(self.lista.registro.count(), 1)

        self.lista.salirLista(self.usuario)
        self.assertEqual(self.lista.registro.count(), 0)


    # ----------------- SIGUIENTE USUARIO -----------------

    def test_siguienteUsuario_devuelve_primero(self):
        user = User.objects.create_user(username="user1", password="1234")
        usuario2 = UsuarioFinal.objects.create(user=user, nombre="user2", fechaNacimiento=date(2000, 1, 1))
        self.lista.nuevaEntrada(self.usuario)
        self.lista.nuevaEntrada(usuario2)

        primero = self.lista.siguienteUsuario()
        self.assertEqual(primero.usuarioFinal, self.usuario)


    # ----------------- CONTAR ENTRADAS -----------------

    def test_contar_entradas(self):
        user = User.objects.create_user(username="user1", password="1234")
        self.lista.nuevaEntrada(self.usuario)
        usuario2 = UsuarioFinal.objects.create(user=user, nombre="user2", fechaNacimiento=date(2000, 1, 1))
        self.lista.nuevaEntrada(usuario2)

        self.assertEqual(EntradaListaEspera.contar(), 2)


    # ----------------- UNICO -----------------

    def test_unique_together(self):
        self.lista.nuevaEntrada(self.usuario)
        with self.assertRaises(IntegrityError):
            EntradaListaEspera.objects.create(listaEspera=self.lista, usuarioFinal=self.usuario)



class EntradaListaEsperaTests(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1", password="1234")
        user2 = User.objects.create_user(username="user2", password="1234")
        user = User.objects.create_user(username="monitor1", password="1234")

        self.usuario1 = UsuarioFinal.objects.create(user=user1, nombre="user1", fechaNacimiento=date(2000, 1, 1))
        self.usuario2 = UsuarioFinal.objects.create(user=user2, nombre="user2", fechaNacimiento=date(2000, 1, 1))

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)
        monitor = Monitor.objects.create(user=user)
        self.actividad = Actividad.objects.create(nombre="Yoga", instalacion=instalacion, monitor=monitor)
        
        self.lista = ListaEspera.objects.create(actividad=self.actividad)


    # ----------------- STR -----------------

    def test_str(self):
        entrada = EntradaListaEspera.objects.create(listaEspera=self.lista, usuarioFinal=self.usuario1)
        expected_str = f'Fecha: {entrada.fechaEntrada}, Hora: {entrada.horaEntrada}'

        self.assertEqual(str(entrada), expected_str)


    # ----------------- CONTAR -----------------

    def test_contar(self):
        EntradaListaEspera.objects.create(listaEspera=self.lista, usuarioFinal=self.usuario1)
        EntradaListaEspera.objects.create(listaEspera=self.lista, usuarioFinal=self.usuario2)

        self.assertEqual(EntradaListaEspera.contar(), 2)


    # ----------------- UNICO -----------------

    def test_unique_together(self):
        EntradaListaEspera.objects.create(listaEspera=self.lista, usuarioFinal=self.usuario1)

        with self.assertRaises(IntegrityError):
            EntradaListaEspera.objects.create(listaEspera=self.lista, usuarioFinal=self.usuario1)


    # ----------------- ORDEN POR FECHA/HORA -----------------

    def test_ordering_fecha_hora(self):
        entrada1 = EntradaListaEspera.objects.create(listaEspera=self.lista, usuarioFinal=self.usuario1)
        
        entrada2 = EntradaListaEspera.objects.create(listaEspera=self.lista, usuarioFinal=self.usuario2)
        entrada2.fechaEntrada = entrada1.fechaEntrada + timedelta(days=1)
        entrada2.horaEntrada = (entrada1.horaEntrada.replace(minute=entrada1.horaEntrada.minute + 1)
                                if entrada1.horaEntrada.minute < 59 else entrada1.horaEntrada)
        entrada2.save()

        entradas = list(EntradaListaEspera.objects.all())

        self.assertEqual(entradas[0], entrada1)
        self.assertEqual(entradas[1], entrada2)