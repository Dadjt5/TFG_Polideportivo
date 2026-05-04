from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date

from polideportivo.models import Notificacion, Administrador, RolAdministrador, UsuarioFinal, Pabellon, Monitor, Actividad, Instalacion

User = get_user_model()


class AccionNotificacionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

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
            plazasReservadas=10,
            instalacion=self.instalacion,
            nombre="Actividad test"
        )

    def test_aceptar_notificacion(self):
        self.client.force_authenticate(user=self.user)

        notificacion = Notificacion.objects.create(
            usuario=self.user,
            actividad=self.actividad,
            titulo="Test"
        )

        response = self.client.post(
            f"/api/v1/notificaciones/{notificacion.id}/responder/",
            {"aceptar": True}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_no_aceptar_procesa_lista_espera(self):
        self.client.force_authenticate(user=self.user)

        notificacion = Notificacion.objects.create(
            usuario=self.user,
            actividad=self.actividad,
            titulo="Test lista espera"
        )

        response = self.client.post(
            f"/api/v1/notificaciones/{notificacion.id}/responder/",
            {"aceptar": False}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NuevaNotificacionTests(APITestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        Administrador.objects.create(user=self.admin, rol=RolAdministrador.RAIZ)

    def test_crear_notificacion(self):
        self.client.force_authenticate(user=self.admin)

        datos = {
            "titulo": "Aviso",
            "descripcion": "Mensaje",
            "usuarios": "TODOS"
        }

        response = self.client.post("/api/v1/notificaciones/nueva/", datos)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

class GuardarNotificacionTests(APITestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

    def test_obtener_notificaciones(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/v1/notificaciones/guardar/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_actualizar_notificaciones(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/api/v1/notificaciones/guardar/", {"id": 1, "leido": True, "fijado": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)