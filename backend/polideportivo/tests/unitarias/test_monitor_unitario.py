from django.test import TestCase
from django.contrib.auth import get_user_model

from ...models import Monitor, Actividad, Sesion, Periodo, Dia


class MonitorUnitTest(TestCase):

    def setUp(self):
        self.data = {
            "nombre": "Juan",
            "apellidos": "Perez",
            "dni": "12345678A",
            "email": "test@test.com",
            "password": "1234"
        }

        self.data2 = {
            "nombre": "Juan",
            "apellidos": "Perez",
            "dni": "12345678N",
            "email": "test@test.com",
            "password": "1234"
        }

    def test_registrar_monitor_ok(self):
        result = Monitor.registrarMonitor(**self.data)

        self.assertFalse(result["error"])
        self.assertIsNotNone(result["respuesta"])
    
    def test_registrar_monitor_email_duplicado(self):
        Monitor.registrarMonitor(**self.data)

        result = Monitor.registrarMonitor(**self.data2)

        self.assertTrue(result["error"])

    def test_registrar_monitor_dni_duplicado(self):
        Monitor.registrarMonitor(**self.data)

        result = Monitor.registrarMonitor(**self.data)

        self.assertTrue(result["error"])

    def test_contar(self):
        Monitor.registrarMonitor(**self.data)
        self.assertGreaterEqual(Monitor.contar(), 1)

    def test_comprobar_disponibilidad_true(self):
        monitor = Monitor.registrarMonitor(**self.data)["respuesta"]

        sesiones = [{
            "dia": Dia.LUNES,
            "horaInicio": "08:00",
            "horaFin": "09:00"
        }]

        resultado = monitor.comprobarDisponibilidad(
            sesiones,
            Periodo.ANUAL
        )

        self.assertTrue(resultado)