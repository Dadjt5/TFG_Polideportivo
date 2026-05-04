from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

from polideportivo.models import (
    Foro, Canal, UsuarioFinal, Administrador, UsuarioCanal
)

class ForoViewTests(APITestCase):

    def setUp(self):
        self.user_final = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user_final, fechaNacimiento=date(2001,1,1))

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.administrador = Administrador.objects.create(user=self.admin)

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

        self.administrador = Administrador.objects.create(user=self.admin)

    def test_ver_canal_admin(self):
        self.client.force_authenticate(user=self.admin)

        self.foro = Foro.objects.create()
        canal = Canal.objects.create(titulo="Test", foro=self.foro, numeroParticipantes=10)

        response = self.client.get(f"/api/v1/canales/{canal.id}/admin/")

        self.assertEqual(response.status_code, 200)


class NuevoCanalViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        
        self.administrador = Administrador.objects.create(user=self.admin)

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
            f"/api/v1/foros/{self.foro.id}/canal/",
            datos
        )

        self.assertEqual(response.status_code, 200)


class MensajesCanalViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.foro = Foro.objects.create()
        self.canal = Canal.objects.create(titulo="Canal test", foro=self.foro, numeroParticipantes=10)

        UsuarioCanal.objects.create(canal=self.canal, usuarioFinal=self.usuario)

    def test_ver_mensajes(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/v1/canales/{self.canal.id}/mensajes/")

        self.assertEqual(response.status_code, 200)

    def test_enviar_mensaje(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f"/api/v1/canales/{self.canal.id}/mensajes/",
            {"texto": "Hola"}
        )

        self.assertEqual(response.status_code, 201)



class GestionarUsuarioCanalTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.administrador = Administrador.objects.create(user=self.admin)

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.foro = Foro.objects.create()
        self.canal = Canal.objects.create(titulo="Canal test", foro=self.foro, numeroParticipantes=10)

        UsuarioCanal.objects.create(canal=self.canal, usuarioFinal=self.usuario_final)

    def test_silenciar_usuario(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/v1/canales/{self.canal.id}/modificar/{self.usuario_final.id}/",
            "silenciar",
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_expulsar_usuario(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/v1/canales/{self.canal.id}/modificar/{self.usuario_final.id}/",
            "expulsar",
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_accion_invalida(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/v1/canales/{self.canal.id}/modificar/{self.usuario_final.id}/",
            "loquesea",
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)