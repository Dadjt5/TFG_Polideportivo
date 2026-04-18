from django.test import TestCase
from unittest.mock import patch, MagicMock
from datetime import date, datetime, time, timedelta
from django.utils import timezone

from django.utils.timezone import now, make_aware
from django.contrib.auth import get_user_model

from ..models import (
    UsuarioFinal, Rol, Sexo, Sesion, Asistencia, Instalacion,
    Pabellon, Monitor, Actividad, Dia, Foro, Canal
)


# Mocks simples
class UserMock:
    def __init__(self, username="user", email="user@test.com"):
        self.username = username
        self.email = email

    def delete(self):
        pass

class SesionMock:
    def __init__(self, dia="Lunes", horaInicio=time(12,0), actividad="Yoga"):
        self.dia = dia
        self.horaInicio = horaInicio
        self.actividad = actividad

    def comprobarPeriodo(self, mes):
        self.periodo_comprobado = mes

class AsistenciaMock:
    def __init__(self, sesion):
        self.sesion = sesion



class UsuarioFinalTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.auth_user = User.objects.create_user(username="juan123", email="juan@test.com", password="1234")
        self.usuario = UsuarioFinal.objects.create(
            user=self.auth_user,
            nombre="Juan",
            apellidos="Pérez",
            fechaNacimiento=date(2000, 1, 1),
            DNI="12345678A",
            sexo=Sexo.NINGUNO,
            esUAM=False
        )

        foro = Foro.objects.create(
            titulo = "Foro",
            numeroParticipantes = 0
       )
    
        Canal.objects.create(
            titulo = "Buzón de sugerencias",
            tema = "Buzón",
            numeroParticipantes = 0,
            secreto=True,
            foro=foro
        )

        user = User.objects.create(username="monitor1", password="1234")
        monitor = Monitor.objects.create(user=user)
        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)

        self.actividad = Actividad.objects.create(nombre="Yoga", instalacion=instalacion, monitor=monitor)

        self.usuario.asistencias.set([])


    # ----------------- STR -----------------

    def test_str(self):
        self.assertIn("Usuario: ", str(self.usuario))
        self.assertIn("2000-01-01", str(self.usuario))


    # ----------------- ROL -----------------

    def test_save_esUAM_false(self):
        self.usuario.esUAM = False
        self.usuario.save()

        self.assertEqual(self.usuario.rol, Rol.EXTERNO)

    def test_save_esUAM_true(self):
        self.usuario.esUAM = True
        self.usuario.save()

        self.assertEqual(self.usuario.rol, Rol.ESTUDIANTE)


    # ----------------- ABONO -----------------

    def test_marcar_abono(self):
        self.usuario.marcarAbono(True)
        self.usuario.refresh_from_db()

        self.assertTrue(self.usuario.tieneAbono)

    def test_comprobar_abono_false(self):
        self.usuario.comprobarAbono()
        self.assertFalse(self.usuario.tieneAbono)


    # ----------------- FAVORITOS -----------------

    def test_cambiar_favorito_actividad(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)
        user = User.objects.create_user(username="monitor2", password="1234")
        monitor = Monitor.objects.create(user=user)
        actividad = Actividad.objects.create(nombre="Yoga", instalacion=instalacion, monitor=monitor)

        res = self.usuario.cambiarFavorito(actividad=actividad)
        self.assertTrue(res)

        res2 = self.usuario.cambiarFavorito(actividad=actividad)
        self.assertFalse(res2)

    def test_cambiar_favorito_error_ambos(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)
        user = User.objects.create_user(username="monitor3", password="1234")
        monitor = Monitor.objects.create(user=user)
        actividad = Actividad.objects.create(nombre="Yoga", instalacion=instalacion, monitor=monitor)

        with self.assertRaises(ValueError):
            self.usuario.cambiarFavorito(actividad=actividad, instalacion=instalacion)


    # ----------------- CONTAR -----------------

    def test_contar(self):
        self.assertEqual(UsuarioFinal.contar(), 1)


    # ----------------- REGISTRAR USUARIO -----------------

    def test_registrar_usuario_ok(self):
        result = UsuarioFinal.registrarUsuario(
            nombre="Ana",
            apellidos="Gomez",
            sexo=Sexo.NINGUNO,
            fechaNacimiento=date(1995,1,1),
            dni="87654321B",
            telefono="123456789",
            email="ana@test.com",
            provincia="Madrid",
            municipio="Madrid",
            localidad="Centro",
            codigoPostal="28001",
            password="pass1234",
            esUAM=False
        )

        self.assertFalse(result["error"])
        self.assertEqual(result["respuesta"].nombre, "Ana")

    def test_registrar_usuario_duplicado_dni(self):
        User = get_user_model()
        User.objects.create_user(username="12345678A", email="otro@test.com", password="1234")
        result = UsuarioFinal.registrarUsuario(
            nombre="Juan",
            apellidos="Perez",
            sexo=Sexo.NINGUNO,
            fechaNacimiento=date(2000,1,1),
            dni="12345678A",
            telefono="123",
            email="nuevo@test.com",
            provincia="X",
            municipio="X",
            localidad="X",
            codigoPostal="X",
            password="1234",
            esUAM=False
        )

        self.assertTrue(result["error"])
        self.assertIn("Ya existe un usuario con ese DNI", result["respuesta"])

    def test_registrar_usuario_duplicado_email(self):
        User = get_user_model()
        User.objects.create_user(username="nuevo", email="juan@test.com", password="1234")
        result = UsuarioFinal.registrarUsuario(
            nombre="Juan",
            apellidos="Perez",
            sexo=Sexo.NINGUNO,
            fechaNacimiento=date(2000,1,1),
            dni="99999999X",
            telefono="123",
            email="juan@test.com",
            provincia="X",
            municipio="X",
            localidad="X",
            codigoPostal="X",
            password="1234",
            esUAM=False
        )

        self.assertTrue(result["error"])
        self.assertIn("Ya existe un usuario con ese email", result["respuesta"])


    # ----------------- REVISAR ACTIVIDADES -----------------

    @patch("polideportivo.models.Notificacion.notificarActividadUsuarioFinal")
    @patch("polideportivo.models.Notificacion.objects.filter")
    def test_revisar_actividades_notificar(self, mock_filter, mock_notificar):
        ahora = timezone.now()
        dia_hoy = ahora.weekday()

        mapa_dias_reverse = {
            0: "Lunes",
            1: "Martes",
            2: "Miercoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sabado",
            6: "Domingo",
        }

        sesion = Sesion.objects.create(
            dia=mapa_dias_reverse[dia_hoy],
            horaInicio=(ahora + timedelta(minutes=30)).time(),
            horaFin=(ahora + timedelta(minutes=90)).time(),
            actividad=self.actividad
        )

        asistencia_real = Asistencia.objects.create(usuarioFinal=self.usuario, sesion=sesion)
        self.usuario.asistencias.set([asistencia_real])

        mock_filter.return_value.exists.return_value = False

        with patch("polideportivo.models.usuario_final.now") as now_mock:
            now_mock.return_value = ahora
            self.usuario.revisarActividades()

        mock_notificar.assert_called_once_with(sesion.actividad, sesion)

    @patch("polideportivo.models.Notificacion.objects.filter")
    @patch("polideportivo.models.Notificacion.notificarActividadUsuarioFinal")
    def test_revisar_actividades_no_notificar_existente(self, mock_notificar, mock_filter):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        pabellon = Pabellon.objects.create()
        instalacion = Instalacion.objects.create(pabellon=pabellon)
        user = User.objects.create_user(username="monitor4", password="1234")
        monitor = Monitor.objects.create(user=user)
        actividad = Actividad.objects.create(nombre="Yoga", instalacion=instalacion, monitor=monitor)

        sesion = Sesion.objects.create(
            dia=Dia.LUNES,
            horaInicio=time(hour=14, minute=0),
            horaFin=time(hour=15, minute=0),
            actividad=actividad
        )

        asistencia_real = Asistencia.objects.create(usuarioFinal=self.usuario, sesion=sesion)
        self.usuario.asistencias.set([asistencia_real])
        mock_filter.return_value.exists.return_value = True

        self.usuario.revisarActividades()
        mock_notificar.assert_not_called()
    
    def test_delete_elimina_usuario_auth(self):
        auth_id = self.auth_user.id

        self.usuario.delete()

        User = get_user_model()

        self.assertFalse(
            User.objects.filter(id=auth_id).exists()
        )