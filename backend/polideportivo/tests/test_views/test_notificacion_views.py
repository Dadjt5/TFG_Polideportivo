from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from polideportivo.models import Notificacion

User = get_user_model()


class AccionNotificacionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

    def test_aceptar_notificacion(self):
        self.client.force_authenticate(user=self.user)

        # aquí necesitarías una notificación real creada en setUp
        notificacion = Notificacion.objects.create(
            usuario=self.user,
            titulo="Test"
        )

        response = self.client.post(
            f"/api/v1/notificacion/{notificacion.id}/accion/",
            {"aceptar": True}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_no_aceptar_procesa_lista_espera(self):
        self.client.force_authenticate(user=self.user)

        notificacion = Notificacion.objects.create(
            usuario=self.user,
            titulo="Test lista espera"
        )

        response = self.client.post(
            f"/api/v1/notificacion/{notificacion.id}/accion/",
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
        self.admin.is_administrador = True
        self.admin.save()

    def test_crear_notificacion(self):
        self.client.force_authenticate(user=self.admin)

        datos = {
            "titulo": "Aviso",
            "descripcion": "Mensaje",
            "usuarios": "GENERAL"
        }

        response = self.client.post("/api/v1/notificacion/", datos)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

class GuardarNotificacionTests(APITestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

    def test_obtener_notificaciones(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/v1/notificacion/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        def test_actualizar_notificaciones(self):
            self.client.force_authenticate(user=self.user)

            datos = {
                "notificaciones": [
                    {
                        "id": 1,
                        "leido": True,
                        "fijado": False
                    }
                ]
            }

            response = self.client.post("/api/v1/notificacion/", datos)

            self.assertEqual(response.status_code, status.HTTP_200_OK)