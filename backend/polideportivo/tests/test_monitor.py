from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from unittest.mock import Mock, patch
from datetime import datetime, time, date, timedelta
from django.utils import timezone


from ..models import (
    Monitor, Usuario, Periodo, Actividad, Sesion, Instalacion,
    Pabellon, Asistencia
)


class MonitorTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.auth_user = User.objects.create_user(username="dni1", email="monitor1@test.com", password="pass123")
        self.monitor = Monitor.objects.create(user=self.auth_user, nombre="Test", apellidos="Monitor", DNI="dni1")

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)

        self.actividad = Actividad.objects.create(nombre="Yoga", periodo=Periodo.ANUAL, monitor=self.monitor, instalacion=instalacion)
        self.sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia="Lunes",
            horaInicio=time(10, 0),
            horaFin=time(11, 0)
        )


    # ----------------- REVISAR ACTIVIDADES -----------------
    
    @patch("polideportivo.models.Notificacion")
    def test_revisarActividades_notifica_correctamente(self, NotificacionMock):
        ahora = timezone.now()

        sesion = Sesion.objects.create(
            dia=ahora.weekday(),  # día de hoy
            horaInicio=(ahora + timedelta(minutes=30)).time(),
            horaFin=(ahora + timedelta(minutes=90)).time(),
            actividad=self.actividad
        )

        asistencia_real = Asistencia.objects.create(usuarioFinal=self.usuario, sesion=sesion)
        self.usuario.asistencias.set([asistencia_real])

        with patch("polideportivo.models.Monitor.timezone.now") as now_mock:
            now_mock.return_value = ahora
            self.monitor.revisarActividades()

        # Verificamos que se haya llamado a la notificación
        NotificacionMock.notificarActividadMonitor.assert_called_once_with(sesion.actividad, sesion)

    # ----------------- COMPROBAR DISPONIBILIDAD -----------------

    def test_comprobarDisponibilidad_true_false(self):
        sesiones_nueva = [
            {"dia": "Lunes", "horaInicio": time(12, 0), "horaFin": time(13, 0)},
            {"dia": "Lunes", "horaInicio": time(10, 30), "horaFin": time(11, 30)}
        ]

        self.assertFalse(self.monitor.comprobarDisponibilidad([sesiones_nueva[1]], Periodo.ANUAL))
        self.assertTrue(self.monitor.comprobarDisponibilidad([sesiones_nueva[0]], Periodo.ANUAL))


    # ----------------- REGISTRAR -----------------

    def test_registrarMonitor_crea_monitor_y_user(self):
        result = Monitor.registrarMonitor(
            nombre="Nuevo",
            apellidos="Monitor",
            dni="dni2",
            email="nuevo@test.com",
            password="1234"
        )

        self.assertFalse(result["error"])
        self.assertIsInstance(result["respuesta"], Monitor)

    def test_registrarMonitor_usuario_existente(self):
        result_dni = Monitor.registrarMonitor(
            nombre="Dup",
            apellidos="Monitor",
            dni="dni1",
            email="nuevo2@test.com",
            password="1234"
        )

        self.assertTrue(result_dni["error"])
        self.assertIn("DNI", result_dni["respuesta"])

        result_email = Monitor.registrarMonitor(
            nombre="Dup",
            apellidos="Monitor",
            dni="dni3",
            email="monitor1@test.com",
            password="1234"
        )

        self.assertTrue(result_email["error"])
        self.assertIn("email", result_email["respuesta"])


    # ----------------- CONTAR -----------------

    def test_contar(self):
        self.assertEqual(Monitor.contar(), 1)


    # ----------------- DELETE DJANGO USER-----------------

    def test_delete_elimina_usuario(self):
        user_id = self.monitor.user.id

        self.actividad.delete()

        self.monitor.delete()
        User = get_user_model()

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)