from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, Mock
from datetime import datetime, time, date

from ..models import (
    Notificacion, UsuarioFinal, Monitor, Administrador, 
    Configuracion, Instalacion, Pabellon, Actividad, Sesion,
    Deporte, ReservaActividad
)

class NotificacionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username="user1", email="user1@test.com", password="1234")
        self.user2 = User.objects.create_user(username="user2", email="user2@test.com", password="1234")

        self.usuario_final = UsuarioFinal.objects.create(user=self.user1, fechaNacimiento=date(2000, 1, 1))
        self.monitor = Monitor.objects.create(user=self.user2, nombre="Mon", apellidos="Test", DNI="dni123")

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)

        self.actividad = Actividad.objects.create(nombre="Yoga", monitor=self.monitor, instalacion=instalacion)
        self.sesion = Sesion.objects.create(actividad=self.actividad, dia="Lunes", horaInicio=time(10,0), horaFin=time(11,0))

        # Debemos crear una reserva para que algunas de las notificaciones se pueden enviar correctamente
        ReservaActividad.objects.create(usuarioFinal=self.usuario_final, actividad=self.actividad)

        # Configuración de prueba
        Configuracion.objects.create(
            titulo_aviso_devolucion_dinero_alquiler="Devolucion",
            texto_aviso_devolucion_dinero_alquiler="Se devolvio dinero",
            titulo_avisos_sobre_actividades_usuarios="Actividad próxima",
            texto_avisos_sobre_actividades_usuarios="Tu actividad empieza pronto",
            titulo_avisos_sobre_actividades_monitores="Actividad próxima monitor",
            texto_avisos_sobre_actividades_monitores="Revisa tu actividad",
            titulo_avisos_actividades="Nueva actividad",
            texto_avisos_actividades="Actividad añadida",
            titulo_material_especial="Material especial",
            texto_material_especial="Nuevo material disponible",
            titulo_cambios_sesiones="Cambio de sesiones",
            texto_cambios_sesiones="Sesión modificada",
            titulo_cambios_cancelaciones="Cancelación",
            texto_cambios_cancelaciones="Se ha cancelado",
            titulo_ausencias="Ausencia",
            texto_ausencias="Has faltado",
            titulo_problemas_pago="Pago",
            texto_problemas_pago="Problema con el pago",
            titulo_salida_lista_espera="Salida lista espera",
            texto_salida_lista_espera="Has salido de la lista de espera"
        )


    # ----------------- STR -----------------

    def test_str(self):
        noti = Notificacion.objects.create(titulo="Prueba", usuario=self.user1)
        self.assertEqual(str(noti), "Prueba")


    # ----------------- CONTAR -----------------

    def test_contar(self):
        Notificacion.objects.create(titulo="N1", usuario=self.user1)
        Notificacion.objects.create(titulo="N2", usuario=self.user2)

        self.assertEqual(Notificacion.contar(), 2)


    # ----------------- CAMBIAR ESTADO -----------------

    def test_cambiarEstado(self):
        n = Notificacion.objects.create(titulo="Estado", usuario=self.user1, leido=False, fijado=False)
        Notificacion.cambiarEstado(self.user1, n.id, leido=True, fijado=True)
        n.refresh_from_db()

        self.assertTrue(n.leido)
        self.assertTrue(n.fijado)


    # ----------------- NUEVA NOTIFICACION -----------------

    def test_nuevaNotificacion_todos(self):
        Notificacion.nuevaNotificacion("Test", "Desc", "TODOS", None)
        self.assertEqual(Notificacion.contar(), 2)

    @patch("polideportivo.models.notificacion.Notificacion.objects.bulk_create")
    def test_nuevaNotificacion_mock_bulk(self, bulk_create_mock):
        Notificacion.nuevaNotificacion("Test", "Desc", "USUARIOS_FINALES", None)
        bulk_create_mock.assert_called_once()


    # ----------------- NOTIFICACIONES AUTOMATICAS -----------------

    def test_notificarActividadUsuarioFinal(self):
        Notificacion.notificarActividadUsuarioFinal(self.actividad, self.sesion)
        n = Notificacion.objects.first()

        self.assertEqual(n.actividad, self.actividad)
        self.assertEqual(n.sesion, self.sesion)

    def test_notificarActividadMonitor(self):
        Notificacion.notificarActividadMonitor(self.actividad, self.sesion)
        n = Notificacion.objects.first()

        self.assertEqual(n.actividad, self.actividad)
        self.assertEqual(n.sesion, self.sesion)
        self.assertEqual(n.usuario, self.monitor.user)

    def test_notificarProblemasPago(self):
        Notificacion.notificarProblemasPago(self.user1)
        n = Notificacion.objects.first()

        self.assertEqual(n.usuario, self.user1)
        self.assertIn("Pago", n.titulo)

    def test_notificarNuevaActividad(self):
        yoga = Deporte.objects.create(titulo="Yoga")
        self.actividad.deportes = yoga
        self.usuario_final.deportesFavoritos.set([yoga])
        self.usuario_final.save()

        Notificacion.notificarNuevaActividad(self.actividad)
        n = Notificacion.objects.first()

        self.assertEqual(n.titulo, "Nueva actividad")
        self.assertEqual(n.actividad, self.actividad)
        self.assertEqual(n.usuario, self.usuario_final.user)

    def test_notificarCambioSesiones(self):
        Notificacion.notificarCambioSesiones(self.actividad)
        n = Notificacion.objects.first()

        self.assertEqual(n.titulo, "Cambio de sesiones")
        self.assertEqual(n.actividad, self.actividad)

    def test_notificarCambioCancelacion(self):
        Notificacion.notificarCambioCancelacion()
        n = Notificacion.objects.first()

        self.assertEqual(n.titulo, "Cancelación")

    def test_notificarAusencias(self):
        Notificacion.notificarAusencias(self.usuario_final, self.actividad)
        n = Notificacion.objects.first()

        self.assertEqual(n.titulo, "Ausencia")
        self.assertEqual(n.actividad, self.actividad)
        self.assertEqual(n.usuario, self.usuario_final.user)

    def test_notificarSalidaListaDeEspera(self):
        Notificacion.notificarSalidaListaDeEspera(self.usuario_final, self.actividad)
        n = Notificacion.objects.first()

        self.assertEqual(n.titulo, "Salida lista espera")
        self.assertTrue(n.debeMarcar)
        self.assertEqual(n.actividad, self.actividad)
        self.assertEqual(n.usuario, self.usuario_final.user)

    def test_notificarNuevoMaterial(self):
        Notificacion.notificarNuevoMaterial(self.actividad)
        n = Notificacion.objects.first()

        self.assertEqual(n.titulo, "Material especial")
        self.assertEqual(n.actividad, self.actividad)
        self.assertEqual(n.usuario, self.usuario_final.user)