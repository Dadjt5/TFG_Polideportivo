from datetime import time
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from unittest.mock import patch

from ...models import (
    Actividad, Sesion, Asistencia, Dia, UsuarioFinal,
    Pabellon, Instalacion, Monitor, ListaEspera, ReservaActividad
)

User = get_user_model()


class ActividadIntegrationTest(TestCase):

    def setUp(self):
        self.pabellon = Pabellon.objects.create(
            nombre="Pabellón central"
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Pista tenis",
            pabellon=self.pabellon
        )

        self.user = User.objects.create(username="user1", password="1234")
        self.user2 = User.objects.create(username="user2", password="1234")

        self.usuario = UsuarioFinal.objects.create(fechaNacimiento=date(2001,1,1), user=self.user)
        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(
            nombre="Natación",
            instalacion=self.instalacion,
            monitor=self.monitor
        )

        self.sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio=time(10, 0),
            horaFin=time(11, 0),   
        )
    
    def test_activar_asistencia(self):
        self.actividad.activarAsistencia(self.usuario)

        self.assertTrue(
            Asistencia.objects.filter(
                usuarioFinal=self.usuario,
                sesion=self.sesion
            ).exists()
        )

    def test_eliminar_asistencia(self):
        Asistencia.objects.create(
            usuarioFinal=self.usuario,
            sesion=self.sesion
        )

        self.actividad.eliminarAsistencia(self.usuario)

        self.assertFalse(
            Asistencia.objects.filter(
                usuarioFinal=self.usuario,
                sesion=self.sesion
            ).exists()
        )

    def test_nueva_sesion(self):
        sesion = self.actividad.nuevaSesion(
            dia=Dia.MARTES,
            horaInicio="12:00",
            horaFin="13:00"
        )

        self.assertEqual(sesion.actividad, self.actividad)

    def test_cambiar_falta(self):
        asistencia = Asistencia.objects.create(
            usuarioFinal=self.usuario,
            sesion=self.sesion,
            presente=True
        )

        resultado = self.sesion.cambiarFalta(
            self.usuario,
            False
        )

        asistencia.refresh_from_db()

        self.assertTrue(resultado)
        self.assertFalse(asistencia.presente)
    
    def test_pasar_a_espera(self):
        ListaEspera.objects.create(actividad=self.actividad)

        resultado = self.actividad.pasarAEspera(self.usuario)
        self.assertIsNotNone(resultado)

    def test_pasar_a_espera_usuario_inscrito(self):
        Asistencia.objects.create(
            sesion=self.sesion,
            usuarioFinal=self.usuario
        )

        resultado = self.actividad.pasarAEspera(self.usuario)
        self.assertFalse(resultado)
    
    def test_salir_lista_espera(self):
        ListaEspera.objects.create(actividad=self.actividad)

        self.actividad.pasarAEspera(self.usuario)
        resultado = self.actividad.salirListaEspera(self.usuario)

        self.assertTrue(resultado)
    
    def test_salir_lista_espera_usuario_inscrito(self):
        Asistencia.objects.create(
            sesion=self.sesion,
            usuarioFinal=self.usuario
        )

        resultado = self.actividad.salirListaEspera(self.usuario)
        self.assertFalse(resultado)
    
    def test_modificar_informacion_cambia_material_y_notifica(self):
        self.actividad.material = "viejo material"
        self.actividad.save()

        data = {
            "material": "material"
        }

        with patch("polideportivo.models.actividad.Notificacion.notificarNuevoMaterial") as mock_notif:
            self.actividad.modificarInformacion(
                actividad_data=data,
                tarifa=self.actividad.tarifa,
                instalacion=self.instalacion,
                monitor=self.monitor,
                imagen=None
            )

            self.actividad.refresh_from_db()

            self.assertEqual(self.actividad.material, "material")
            mock_notif.assert_called_once_with(actividad=self.actividad)

    def test_cambiar_falta_notificacion_ausencias(self):
        Asistencia.objects.create(
            usuarioFinal=self.usuario,
            sesion=self.sesion,
            presente=True
        )

        # crear 11 faltas para activar el if
        for _ in range(11):
            sesion = Sesion.objects.create(
                actividad=self.actividad,
                dia=Dia.LUNES,
                horaInicio=time(10, 0),
                horaFin=time(11, 0)
            )

            Asistencia.objects.create(
                usuarioFinal=self.usuario,
                sesion=sesion,
                presente=False
            )

        with patch("polideportivo.models.actividad.Notificacion.notificarAusencias") as mock:
            self.sesion.cambiarFalta(self.usuario, False)

            mock.assert_called_once()