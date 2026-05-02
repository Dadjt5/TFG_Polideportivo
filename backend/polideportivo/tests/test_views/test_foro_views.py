from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

from polideportivo.models import (
    Foro,
    Canal,
    Mensaje,
    UsuarioFinal
)

class ForoViewTests(APITestCase):

    def setUp(self):
        self.user_final = User.objects.create_user(
            username="user",
            password="1234"
        )
        self.user_final.is_usuario_final = True
        self.user_final.save()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador = True
        self.admin.save()

    def test_foro_usuario_final(self):
        self.client.force_authenticate(user=self.user_final)

        response = self.client.get("/api/v1/foro/")

        self.assertEqual(response.status_code, 200)


class CanalAdministradorViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador = True
        self.admin.save()

    def test_ver_canal_admin(self):
        self.client.force_authenticate(user=self.admin)

        canal = Canal.objects.create(titulo="Test")

        response = self.client.get(f"/api/v1/canal/{canal.id}/admin/")

        self.assertEqual(response.status_code, 200)


class NuevoCanalViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador = True
        self.admin.save()

        self.foro = Foro.objects.create()

    def test_crear_canal(self):
        self.client.force_authenticate(user=self.admin)

        datos = {
            "titulo": "Canal prueba",
            "tema": "General",
            "secreto": False,
            "oculto": False
        }

        response = self.client.post(
            f"/api/v1/foro/{self.foro.id}/canal/",
            datos
        )

        self.assertEqual(response.status_code, 200)


class MensajesCanalViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.canal = Canal.objects.create(titulo="Canal test")

    def test_ver_mensajes(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/v1/canal/{self.canal.id}/mensajes/")

        self.assertEqual(response.status_code, 200)

    def test_enviar_mensaje(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f"/api/v1/canal/{self.canal.id}/mensajes/",
            {"texto": "Hola"}
        )

        self.assertEqual(response.status_code, 201)



class GestionarUsuarioCanalTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador = True
        self.admin.save()

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user)

        self.canal = Canal.objects.create(titulo="Canal test")

    def test_silenciar_usuario(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/v1/canal/{self.canal.id}/usuario/{self.usuario_final.id}/",
            {"accion": "silenciar"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_expulsar_usuario(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/v1/canal/{self.canal.id}/usuario/{self.usuario_final.id}/",
            {"accion": "expulsar"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_accion_invalida(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/v1/canal/{self.canal.id}/usuario/{self.usuario_final.id}/",
            {"accion": "loquesea"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)