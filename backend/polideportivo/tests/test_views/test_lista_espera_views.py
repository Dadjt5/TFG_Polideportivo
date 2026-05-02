from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from polideportivo.models import (
    Actividad,
    UsuarioFinal
)

class PasarListaEsperaViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(nombre="UF1")

        self.actividad = Actividad.objects.create(nombre="Actividad test")

        self.user.usuario_final = self.usuario_final
        self.user.save()

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

    def test_salir_lista_espera_error(self):
        self.client.force_authenticate(user=self.user)

        self.actividad.salirListaEspera = lambda uf: None

        response = self.client.delete(
            f"/api/v1/actividades/{self.actividad.id}/esperar/"
        )

        self.assertEqual(response.status_code, 404)

    def test_sin_auth(self):
        response_post = self.client.post(
            f"/api/v1/actividades/{self.actividad.id}/esperar/"
        )

        response_delete = self.client.delete(
            f"/api/v1/actividades/{self.actividad.id}/esperar/"
        )

        self.assertEqual(response_post.status_code, 403)
        self.assertEqual(response_delete.status_code, 403)