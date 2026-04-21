from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


from ..models import (
    Canal, Foro, UsuarioFinal, UsuarioCanal, Mensaje,
    Administrador
)



class ForoTests(TestCase):
    def setUp(self):
        self.foro = Foro.objects.create(titulo="Foro Test")


    # ----------------- STR -----------------

    def test_str(self):
        self.assertEqual(str(self.foro), "Foro con 0")


    # ----------------- CREACION DE CANAL -----------------

    def test_nuevo_canal_exitoso(self):
        canal_creado = self.foro.nuevoCanal(
            titulo="Canal 1",
            tema="Tema Test",
            secreto=False,
            oculto=False
        )

        self.assertTrue(canal_creado)
        self.assertEqual(self.foro.canal.count(), 1)

        canal = self.foro.canal.first()

        self.assertEqual(canal.titulo, "Canal 1")
        self.assertEqual(canal.numeroParticipantes, 0)

    def test_nuevo_canal_fallo(self):
        canal_original_count = self.foro.canal.count()
        result = self.foro.nuevoCanal(
            titulo=None,
            tema="Tema Test",
            secreto=False,
            oculto=False
        )

        self.assertFalse(result)
        self.assertEqual(self.foro.canal.count(), canal_original_count)


    # ----------------- CONTAR PARTICIPANTES -----------------

    def test_numero_participantes_actualiza_correctamente(self):
        canal = Canal.objects.create(
            titulo="Canal 2",
            tema="Tema Test",
            foro=self.foro
        )

        user = User.objects.create_user(username="user1", password="1234")
        user2 = User.objects.create_user(username="user2", password="1234")

        usuario1 = UsuarioFinal.objects.create(user=user, nombre="user1", fechaNacimiento=date(2001,1,1))
        usuario2 = UsuarioFinal.objects.create(user=user2, nombre="user2", fechaNacimiento=date(2001,1,1))

        canal.añadirUsuario(usuario1)
        canal.añadirUsuario(usuario2)

        self.assertEqual(canal.numeroParticipantes, 2)
        self.assertEqual(self.foro.numeroParticipantes, 2)



class CanalTests(TestCase):
    def setUp(self):
        self.foro = Foro.objects.create(titulo="Foro Test")
        self.canal = Canal.objects.create(
            titulo="Canal Test",
            tema="Tema Test",
            foro=self.foro
        )

        user = User.objects.create_user(username="user1", password="1234")
        user2 = User.objects.create_user(username="user2", password="1234")

        self.usuario1 = UsuarioFinal.objects.create(user=user, nombre="user1", fechaNacimiento=date(2001,1,1))
        self.usuario2 = UsuarioFinal.objects.create(user=user2, nombre="user2", fechaNacimiento=date(2001,1,1))
        self.admin = User.objects.create(username="admin", password="1234")


    # ----------------- STR -----------------

    def test_str(self):
        self.assertEqual(str(self.canal), "Canal para Canal Test con 0 participantes")


    # ----------------- CONTAR -----------------

    def test_contar(self):
        Canal.objects.create(titulo="Canal2", tema="Tema2", foro=self.foro)
        self.assertEqual(Canal.contar(), 2)


    # ----------------- AÑADIR USUARIO -----------------

    def test_añadir_usuario(self):
        result = self.canal.añadirUsuario(self.usuario1)

        self.assertTrue(result)
        self.assertEqual(self.canal.numeroParticipantes, 1)
        self.assertEqual(self.foro.numeroParticipantes, 1)

        result2 = self.canal.añadirUsuario(self.usuario1)

        self.assertFalse(result2)
        self.assertEqual(self.canal.numeroParticipantes, 1)


    # ----------------- CAMBIAR EXPULSION -----------------

    def test_cambiar_expulsion_usuario(self):
        self.canal.añadirUsuario(self.usuario1)
        result = self.canal.cambiarExpulsionUsuario(self.usuario1)

        self.assertTrue(result)
        self.assertEqual(self.canal.numeroParticipantes, 0)

        result2 = self.canal.cambiarExpulsionUsuario(self.usuario1)

        self.assertTrue(result2)
        self.assertEqual(self.canal.numeroParticipantes, 1)


    # ----------------- CAMBIAR SILENCIO -----------------

    def test_cambiar_silencio_usuario(self):
        self.canal.añadirUsuario(self.usuario1)
        result = self.canal.cambiarSilencioUsuario(self.usuario1)

        self.assertTrue(result)

        relacion = UsuarioCanal.objects.get(usuarioFinal=self.usuario1, canal=self.canal)

        self.assertTrue(relacion.silenciado)

        result2 = self.canal.cambiarSilencioUsuario(self.usuario1)
        relacion.refresh_from_db()

        self.assertTrue(result2)
        self.assertFalse(relacion.silenciado)


    # ----------------- NUEVO MENSAJE -----------------

    def test_nuevo_mensaje_administrador(self):
        administrador = Administrador.objects.create(nombre="admin23", user=self.admin)
        self.admin.administrador = administrador

        result = self.canal.nuevoMensaje(self.admin, "Mensaje admin")

        self.assertTrue(result)
        self.assertEqual(self.canal.mensajes.count(), 1)

        mensaje = self.canal.mensajes.first()

        self.assertEqual(mensaje.texto, "Mensaje admin")

    def test_nuevo_mensaje_usuario_normal(self):
        self.canal.añadirUsuario(self.usuario1)
        usuario_mock = User.objects.create(username="admin2", password="1234")

        usuario_mock.usuario_final = self.usuario1

        result = self.canal.nuevoMensaje(usuario_mock, "Hola")

        self.assertTrue(result)
        self.assertEqual(self.canal.mensajes.count(), 1)

        self.canal.cambiarExpulsionUsuario(self.usuario1)
        result2 = self.canal.nuevoMensaje(usuario_mock, "Otro mensaje")

        self.assertFalse(result2)
        self.assertEqual(self.canal.mensajes.count(), 1)
    

    # ----------------- OBTENER MENSAJES -----------------

    def test_get_mensajes(self):
        administrador = Administrador.objects.create(nombre="admin23", user=self.admin)
        self.admin.administrador = administrador

        self.canal.nuevoMensaje(self.admin, "Mensaje 1")
        self.canal.nuevoMensaje(self.admin, "Mensaje 2")

        mensajes = self.canal.getMensajes()

        self.assertEqual(mensajes.count(), 2)
        self.assertEqual(mensajes[0].texto, "Mensaje 1")
        self.assertEqual(mensajes[1].texto, "Mensaje 2")



class UsuarioCanalTests(TestCase):
    def setUp(self):
        self.foro = Foro.objects.create(titulo="Foro Test")
        self.canal = Canal.objects.create(titulo="Canal Test", tema="Tema Test", foro=self.foro)

        user = User.objects.create_user(username="user1", password="1234")
        user2 = User.objects.create_user(username="user2", password="1234")
        
        self.usuario1 = UsuarioFinal.objects.create(user=user, nombre="user1", fechaNacimiento=date(2001,1,1))
        self.usuario2 = UsuarioFinal.objects.create(user=user2, nombre="user2", fechaNacimiento=date(2001,1,1))


    # ----------------- CREACION -----------------

    def test_crear_usuario_canal(self):
        relacion = UsuarioCanal.objects.create(usuarioFinal=self.usuario1, canal=self.canal)

        self.assertEqual(relacion.usuarioFinal, self.usuario1)
        self.assertEqual(relacion.canal, self.canal)
        self.assertFalse(relacion.silenciado)
        self.assertFalse(relacion.expulsado)


    # ----------------- UNICO -----------------

    def test_unique_together_usuario_canal(self):
        UsuarioCanal.objects.create(usuarioFinal=self.usuario1, canal=self.canal)

        with self.assertRaises(IntegrityError):
            UsuarioCanal.objects.create(usuarioFinal=self.usuario1, canal=self.canal)


    # ----------------- MULTIPLES USUARIOS -----------------

    def test_multiples_usuarios_en_mismo_canal(self):
        UsuarioCanal.objects.create(usuarioFinal=self.usuario1, canal=self.canal)
        relacion2 = UsuarioCanal.objects.create(usuarioFinal=self.usuario2, canal=self.canal)

        self.assertEqual(self.canal.usuarioFinal.count(), 2)
        self.assertIn(relacion2, self.canal.usuarioFinal.all())



class MensajeTests(TestCase):
    def setUp(self):
        self.foro = Foro.objects.create(titulo="Foro Test")
        self.canal = Canal.objects.create(titulo="Canal Test", tema="Tema Test", foro=self.foro)
        self.usuario = User.objects.create_user(username="user1", password="pass123")


    # ----------------- STR -----------------

    def test_str(self):
        mensaje = Mensaje.objects.create(canal=self.canal, usuario=self.usuario, texto="Hola mundo")
        self.assertEqual(str(mensaje), f"Mensaje en {self.canal.titulo}")


    # ----------------- CREACION Y ASOCIACION CON USUARIO -----------------

    def test_creacion_mensaje_usuario(self):
        mensaje = Mensaje.objects.create(canal=self.canal, usuario=self.usuario, texto="Mensaje 1")
        
        self.assertEqual(mensaje.canal, self.canal)
        self.assertEqual(mensaje.usuario, self.usuario)
        self.assertEqual(mensaje.texto, "Mensaje 1")
        self.assertIsNotNone(mensaje.fechaEnvio)

    def test_creacion_mensaje_sin_usuario(self):
        mensaje = Mensaje.objects.create(canal=self.canal, texto="Mensaje anónimo")
        
        self.assertIsNone(mensaje.usuario)
        self.assertEqual(mensaje.texto, "Mensaje anónimo")


    # ----------------- ORDEN POR FECHA -----------------

    def test_orden_mensajes_por_fecha(self):
        mensaje1 = Mensaje.objects.create(canal=self.canal, usuario=self.usuario, texto="Primer mensaje")
        mensaje2 = Mensaje.objects.create(canal=self.canal, usuario=self.usuario, texto="Segundo mensaje")

        mensajes = self.canal.mensajes.all()

        self.assertEqual(list(mensajes), [mensaje1, mensaje2])