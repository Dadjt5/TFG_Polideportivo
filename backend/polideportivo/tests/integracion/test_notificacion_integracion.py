from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time

from ...models import (
    Notificacion, UsuarioFinal, Actividad, Sesion, Deporte, 
    Monitor, Instalacion, Pabellon, Configuracion, Alquiler,
    TipoActividad, Periodo, ReservaActividad, Administrador
)

User = get_user_model()


class NotificacionIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="12345678A",
            email="test@test.com",
            password="test"
        )

        self.user2 = User.objects.create(
            username="12345678M",
            password="test"
        )

        self.monitor = Monitor.objects.create(nombre="monitor", user=self.user2)

        self.usuarioFinal = UsuarioFinal.objects.create(user=self.user, fechaNacimiento=date(2001,1,1))

        self.config = Configuracion.objects.create(
            titulo_avisos_actividades="titulo",
            texto_avisos_actividades="texto",
            titulo_avisos_sobre_actividades_usuarios="t",
            texto_avisos_sobre_actividades_usuarios="t",
            titulo_avisos_sobre_actividades_monitores="t",
            texto_avisos_sobre_actividades_monitores="t",
            titulo_material_especial="t",
            texto_material_especial="t",
            titulo_cambios_sesiones="t",
            texto_cambios_sesiones="t",
        )

        self.deporte = Deporte.objects.create(titulo="Fútbol")

        self.pabellon = Pabellon.objects.create(nombre="Pabellón 1")

        self.instalacion = Instalacion.objects.create(
            nombre="Instalación 1",
            pabellon=self.pabellon
        )

        self.actividad = Actividad.objects.create(
            nombre="Actividad 1",
            instalacion=self.instalacion,
            monitor=self.monitor,
            deportes=self.deporte,
            periodo=Periodo.ANUAL,
            tipoActividad=TipoActividad.OTROS
        )

        self.sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia="Lunes",
            horaInicio="10:00",
            horaFin="11:00"
        )

    def test_notificar_nueva_actividad_y_str(self):
        self.usuarioFinal.deportesFavoritos.set([self.deporte])
        self.usuarioFinal.save()
        notificacion = Notificacion.notificarNuevaActividad(self.actividad)

        self.assertTrue(Notificacion.objects.exists())
        notif = Notificacion.objects.first()
        self.assertTrue(str(notif), "titulo")
    
    def test_notificar_nueva_actividad_fallo(self):
        act = Actividad.objects.create(instalacion=self.instalacion, monitor=self.monitor)
        notificacion = Notificacion.notificarNuevaActividad(act)

        self.assertFalse(Notificacion.objects.exists())
    
    def test_notificar_material_cambia_con_usuarios(self):
        ReservaActividad.objects.create(usuarioFinal=self.usuarioFinal, actividad=self.actividad)
        Notificacion.notificarNuevoMaterial(self.actividad)

        self.assertTrue(Notificacion.objects.filter(actividad=self.actividad).exists())
    
    def test_notificarAusencias(self):
        Notificacion.notificarAusencias(self.usuarioFinal, self.actividad)
        n = Notificacion.objects.first()

        self.assertTrue(Notificacion.objects.exists())

    def test_notificarSalidaListaDeEspera(self):
        Notificacion.notificarSalidaListaDeEspera(self.usuarioFinal, self.actividad)
        n = Notificacion.objects.first()

        self.assertTrue(Notificacion.objects.exists())
        self.assertTrue(n.debeMarcar)
        self.assertEqual(n.actividad, self.actividad)

    def test_notificar_cambio_sesiones(self):
        ReservaActividad.objects.create(usuarioFinal=self.usuarioFinal, actividad=self.actividad)
        Notificacion.notificarCambioSesiones(self.actividad)

        self.assertTrue(Notificacion.objects.filter(actividad=self.actividad).exists())
    
    def test_notificarActividadUsuarioFinal(self):
        ReservaActividad.objects.create(usuarioFinal=self.usuarioFinal, actividad=self.actividad)
        Notificacion.notificarActividadUsuarioFinal(self.actividad, self.sesion)
        n = Notificacion.objects.first()

        self.assertEqual(n.actividad, self.actividad)
        self.assertEqual(n.sesion, self.sesion)

    def test_notificacion_monitor_actividad(self):
        Notificacion.notificarActividadMonitor(self.actividad, self.sesion)

        self.assertEqual(Notificacion.objects.count(), 1)
    
    def test_notificacion_cancelacion_devolucion(self):
        Notificacion.notificarCancelacionYDevolucionDinero([self.usuarioFinal], self.instalacion)

        self.assertEqual(Notificacion.objects.count(), 1)
    
    def test_notificarCambioCancelacion(self):
        Notificacion.notificarCambioCancelacion()
    
        self.assertTrue(Notificacion.objects.exists())


    # ---------------- Nuevas notificaciones ----------------

    def test_nueva_notificacion_tipo_invalido(self):
        Notificacion.nuevaNotificacion(
            titulo="titulo",
            descripcion="descripcion",
            tipoUsuarios="INVALIDO",
            complemento=None
        )

        self.assertEqual(Notificacion.objects.count(), 0)
    
    def test_nueva_notificacion_administradores(self):
        Administrador.objects.create(user=self.user)

        Notificacion.nuevaNotificacion(
            titulo="titulo",
            descripcion="descripcion",
            tipoUsuarios="ADMINISTRADORES",
            complemento=None
        )

        self.assertEqual(Notificacion.objects.count(), 1)
    
    def test_nueva_notificacion_monitores(self):
        Notificacion.nuevaNotificacion(
            titulo="titulo",
            descripcion="descripcion",
            tipoUsuarios="MONITORES",
            complemento=None
        )

        self.assertEqual(Notificacion.objects.count(), 1)
    
    def test_nueva_notificacion_usuarios_finales(self):
        Notificacion.nuevaNotificacion(
            titulo="titulo",
            descripcion="descripcion",
            tipoUsuarios="USUARIOS_FINALES",
            complemento=None
        )

        self.assertEqual(Notificacion.objects.count(), 1)
    
    def test_nueva_notificacion_actividad(self):
        ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad
        )

        Notificacion.nuevaNotificacion(
            titulo="titulo",
            descripcion="descripcion",
            tipoUsuarios="ACTIVIDAD",
            complemento=self.actividad.id
        )

        notif = Notificacion.objects.first()

        self.assertEqual(Notificacion.objects.count(), 1)
        self.assertEqual(notif.actividad, self.actividad)
    
    def test_nueva_notificacion_instalacion(self):
        Alquiler.objects.create(
            usuarioFinal=self.usuarioFinal,
            instalacion=self.instalacion,
            horaInicio=time(9,0),
            horaFin=time(10,0)
        )

        Notificacion.nuevaNotificacion(
            titulo="titulo",
            descripcion="descripcion",
            tipoUsuarios="INSTALACION",
            complemento=self.instalacion.id
        )

        notif = Notificacion.objects.first()

        self.assertEqual(Notificacion.objects.count(), 1)
        self.assertEqual(notif.instalacion, self.instalacion)
    
    def test_nueva_notificacion_pabellon(self):
        Alquiler.objects.create(
            usuarioFinal=self.usuarioFinal,
            instalacion=self.instalacion,
            horaInicio=time(9,0),
            horaFin=time(10,0)
        )

        Notificacion.nuevaNotificacion(
            titulo="titulo",
            descripcion="descripcion",
            tipoUsuarios="PABELLON",
            complemento=self.pabellon.id
        )

        notif = Notificacion.objects.first()

        self.assertEqual(Notificacion.objects.count(), 1)
        self.assertEqual(notif.pabellon, self.pabellon)