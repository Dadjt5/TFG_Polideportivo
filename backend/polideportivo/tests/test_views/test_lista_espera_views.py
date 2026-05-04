from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from datetime import date

from polideportivo.models import (
    Actividad, Instalacion, Pabellon, Monitor, ListaEspera,
    UsuarioFinal, EntradaListaEspera
)

class PasarListaEsperaViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(nombre="UF1", fechaNacimiento=date(2001,1,1), user=self.user)

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Instalacion test"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            id=1,
            monitor=self.monitor,
            instalacion=self.instalacion,
            nombre="Actividad test"
        )

        self.lista_espera = ListaEspera.objects.create(actividad=self.actividad)


    def test_entrar_lista_espera_ok(self):
        self.client.force_authenticate(user=self.user)

        self.actividad.pasarAEspera = lambda uf: 1

        response = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/esperar/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["posicion"], 1)

    def test_ya_en_lista_espera(self):
        self.client.force_authenticate(user=self.user)

        self.actividad.pasarAEspera = lambda uf: None
        self.entrada = EntradaListaEspera.objects.create(listaEspera=self.lista_espera, usuarioFinal=self.usuario_final)

        response = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/esperar/"
        )

        self.assertEqual(response.status_code, 404)

    def test_salir_lista_espera_ok(self):
        self.client.force_authenticate(user=self.user)

        self.actividad.salirListaEspera = lambda uf: True

        response = self.client.delete(
            f"/api/v1/actividades/{self.actividad.id}/esperar/"
        )

        self.assertEqual(response.status_code, 200)

    def test_sin_auth(self):
        response_post = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/esperar/"
        )

        response_delete = self.client.delete(
            f"/api/v1/actividades/{self.actividad.id}/esperar/"
        )

        self.assertEqual(response_post.status_code, 401)
        self.assertEqual(response_delete.status_code, 401)