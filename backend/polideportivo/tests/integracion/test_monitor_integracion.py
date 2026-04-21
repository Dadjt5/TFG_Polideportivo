from django.test import TestCase
from unittest.mock import patch
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from ...models import (
    Monitor, Actividad, Sesion, Dia, Periodo, Pabellon, 
    Instalacion, Notificacion, Configuracion
)

class MonitorIntegrationTest(TestCase):
    def setUp(self):
        self.data = {
            "nombre": "Ana",
            "apellidos": "Lopez",
            "dni": "87654321B",
            "email": "ana@test.com",
            "password": "1234"
        }

        Configuracion.objects.create()
        self.monitor = Monitor.registrarMonitor(**self.data)["respuesta"]

        self.pabellon = Pabellon.objects.create(nombre="Gran pabellon")
        self.instalacion = Instalacion.objects.create(nombre="Campo 1", pabellon=self.pabellon)

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            monitor=self.monitor,
            instalacion=self.instalacion,
            periodo=Periodo.ANUAL
        )

        self.sesion = Sesion.objects.create(
            actividad=self.actividad,
            dia=Dia.LUNES,
            horaInicio="08:00",
            horaFin="10:00"
        )


    def test_comprobar_disponibilidad_conflicto(self):
        sesiones = [{
            "dia": Dia.LUNES,
            "horaInicio": "09:00",
            "horaFin": "11:00"
        }]

        resultado = self.monitor.comprobarDisponibilidad(
            sesiones,
            Periodo.ANUAL,
        )

        self.assertFalse(resultado)
    
    def test_comprobar_disponibilidad_conflicto_exlusion(self):
        sesiones = [{
            "dia": Dia.LUNES,
            "horaInicio": "09:00",
            "horaFin": "11:00"
        }]

        resultado = self.monitor.comprobarDisponibilidad(
            sesiones,
            Periodo.ANUAL,
            actividad_id=self.actividad.id
        )

        self.assertTrue(resultado)

    def test_comprobar_disponibilidad_sin_conflicto(self):
        sesiones = [{
            "dia": Dia.MARTES,
            "horaInicio": "10:00",
            "horaFin": "11:00"
        }]

        resultado = self.monitor.comprobarDisponibilidad(
            sesiones,
            Periodo.ANUAL
        )

        self.assertTrue(resultado)
    
    @patch("polideportivo.models.monitor.now")
    def test_revisar_actividades_crea_notificacion(self, mock_now):
        fecha_actual = make_aware(datetime(2026, 4, 20, 7, 30))  # lunes 07:30
        mock_now.return_value = fecha_actual

        self.sesion.horaInicio = "08:00"
        self.sesion.horaFin = "09:00"
        self.sesion.save()

        self.monitor.revisarActividades()

        existe = Notificacion.objects.filter(
            usuario=self.monitor.user,
            actividad=self.actividad,
            sesion=self.sesion
        ).exists()

        self.assertTrue(existe)
    
    def test_revisar_actividades_no_duplica_notificacion(self):
        Notificacion.objects.create(
            usuario=self.monitor.user,
            actividad=self.actividad,
            sesion=self.sesion,
        )

        self.monitor.revisarActividades()

        total = Notificacion.objects.filter(
            usuario=self.monitor.user,
            actividad=self.actividad,
            sesion=self.sesion
        ).count()

        self.assertEqual(total, 1)
    
    @patch("polideportivo.models.monitor.now")
    def test_revisar_actividades_no_crea_si_lejos(self, mock_now):
        fecha_actual = make_aware(datetime(2026, 4, 20, 5, 0))  # faltan más de 1h
        mock_now.return_value = fecha_actual

        self.monitor.revisarActividades()

        existe = Notificacion.objects.filter(
            usuario=self.monitor.user,
            actividad=self.actividad,
            sesion=self.sesion
        ).exists()

        self.assertFalse(existe)
    
    def test_delete_elimina_monitor_y_usuario(self):
        user_id = self.monitor.user.id
        monitor_id = self.monitor.id

        self.actividad.delete()
        self.monitor.delete()

        self.assertFalse(Monitor.objects.filter(id=monitor_id).exists())
        self.assertFalse(get_user_model().objects.filter(id=user_id).exists())