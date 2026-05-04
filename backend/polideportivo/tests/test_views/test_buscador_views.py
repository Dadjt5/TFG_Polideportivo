from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

from polideportivo.models import Instalacion, Actividad, UsuarioFinal, Monitor, Pabellon


class BuscarViewTests(APITestCase):

    def setUp(self):
        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Pista Central"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            id=1,
            monitor=self.monitor,
            instalacion=self.instalacion,
            nombre="Yoga"
        )

    def test_busqueda_devuelve_estructura_correcta(self):
        response = self.client.get("/api/v1/buscar/", {
            "busqueda": "Yoga"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("instalaciones", response.data)
        self.assertIn("actividades", response.data)
    
    def test_busqueda_con_filtros(self):
        response = self.client.get("/api/v1/buscar/", {
            "busqueda": "Pista",
            "dias": ["lunes", "martes"],
            "tiposActividad": ["deportiva"]
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ObtenerActividadesInstalacionesTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

        UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Pista 1"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            id=1,
            monitor=self.monitor,
            instalacion=self.instalacion,
            nombre="Actividad test"
        )

    def test_obtener_datos_correctamente(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/v1/obtener/favoritas/", {
            "actividad_ids": [self.actividad.id],
            "instalacion_ids": [self.instalacion.id]
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("actividades", response.data)
        self.assertIn("instalaciones", response.data)
    
    def test_listas_vacias(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/v1/obtener/favoritas/", {
            "actividad_ids": [],
            "instalacion_ids": []
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["actividades"]), 0)
        self.assertEqual(len(response.data["instalaciones"]), 0)


class AlterarFavoritosTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Pista 1"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            id=1,
            monitor=self.monitor,
            instalacion=self.instalacion,
            nombre="Yoga"
        )
    
    def test_marcar_favoritos(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/v1/marcar/favoritas/", {
            "actividad_ids": [self.actividad.id],
            "instalacion_ids": [self.instalacion.id]
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")
    
    def test_favoritos_vacios(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/v1/marcar/favoritas/", {
            "actividad_ids": [],
            "instalacion_ids": []
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "error")