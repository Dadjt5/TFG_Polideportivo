from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model

from ...models import (
    Foro, Canal, UsuarioCanal, Mensaje, UsuarioFinal,
    Administrador
)

User = get_user_model()

class ForoIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user1", password="1234")

        self.usuario = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user)

        self.foro = Foro.objects.create(titulo="Foro principal")

    def test_nuevo_canal_crea_canales_y_usuarios(self):
        resultado = self.foro.nuevoCanal(
            titulo="Canal 1",
            tema="General",
            secreto=False,
            oculto=False
        )

        self.assertTrue(resultado)
        self.assertEqual(Canal.objects.count(), 1)
    
    def test_nuevo_canal_crea_canales_fallo(self):
        resultado = self.foro.nuevoCanal(
            titulo=None,
            tema=None,
            secreto=None,
            oculto=None
        )

        self.assertFalse(resultado)


class CanalIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="1234")
        self.user2 = User.objects.create(username="admin", password="1234", )

        self.admin = Administrador.objects.create(user=self.user2)
        self.usuario = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user)
        self.foro = Foro.objects.create(titulo="Foro")

        self.canal = Canal.objects.create(
            titulo="Chat",
            tema="General",
            foro=self.foro
        )

    def test_añadir_usuario(self):
        resultado = self.canal.añadirUsuario(self.usuario)

        self.assertTrue(resultado)
        self.assertEqual(UsuarioCanal.objects.count(), 1)

    def test_nuevo_mensaje_usuario_valido(self):
        self.canal.añadirUsuario(self.usuario)

        resultado = self.canal.nuevoMensaje(
            usuario=self.user,
            texto="Hola"
        )

        self.assertTrue(resultado)
        self.assertEqual(Mensaje.objects.count(), 1)

    def test_nuevo_mensaje_usuario_no_miembro(self):
        resultado = self.canal.nuevoMensaje(
            usuario=self.user,
            texto="Hola"
        )

        self.assertFalse(resultado)
    
    def test_nuevo_mensaje_usuario_administrador(self):
        resultado = self.canal.nuevoMensaje(
            usuario=self.user2,
            texto="Hola"
        )

        self.assertTrue(resultado)
    
    def test_nuevo_mensaje_no_usuario(self):
            resultado = self.canal.nuevoMensaje(
                texto="Hola",
                usuario=None
            )

            self.assertFalse(resultado)

    def test_cambiar_silencio(self):
        self.canal.añadirUsuario(self.usuario)

        resultado = self.canal.cambiarSilencioUsuario(self.usuario)

        self.assertTrue(resultado)
    
    def test_cambiar_silencio_fallo(self):
        self.canal.añadirUsuario(self.usuario)

        resultado = self.canal.cambiarSilencioUsuario(None)

        self.assertFalse(resultado)

    def test_cambiar_expulsion(self):
        self.canal.añadirUsuario(self.usuario)

        resultado = self.canal.cambiarExpulsionUsuario(self.usuario)
        self.assertTrue(resultado)

        resultado = self.canal.cambiarExpulsionUsuario(self.usuario)
        self.assertTrue(resultado)
    
    def test_cambiar_expulsion_fallo(self):
        self.canal.añadirUsuario(self.usuario)

        resultado = self.canal.cambiarExpulsionUsuario(None)

        self.assertFalse(resultado)