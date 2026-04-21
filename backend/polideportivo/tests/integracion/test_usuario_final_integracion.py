from django.test import TestCase
from unittest.mock import patch
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

from ...models import (
    UsuarioFinal,
    Sexo,
    Monitor,
    Instalacion,
    Pabellon,
    Actividad,
    Sesion,
    Asistencia,
    Dia,
    Canal,
    Foro
)


class UsuarioFinalIntegrationTests(TestCase):
    def setUp(self):
        User = get_user_model()

        self.auth_user = User.objects.create_user(
            username="juan123",
            email="juan@test.com",
            password="1234"
        )

        self.usuario = UsuarioFinal.objects.create(
            user=self.auth_user,
            nombre="Juan",
            apellidos="Pérez",
            fechaNacimiento=date(2000, 1, 1),
            DNI="12345678A",
            sexo=Sexo.NINGUNO,
            esUAM=False
        )

        monitor_user = User.objects.create_user(
            username="monitor1",
            password="1234"
        )

        self.monitor = Monitor.objects.create(user=monitor_user)
        self.pabellon = Pabellon.objects.create()
        self.instalacion = Instalacion.objects.create(pabellon=self.pabellon)

        self.actividad = Actividad.objects.create(
            nombre="Yoga",
            instalacion=self.instalacion,
            monitor=self.monitor
        )

    # ----------------- FAVORITOS -----------------

    def test_cambiar_favorito_crear_y_eliminar(self):
        resultado = self.usuario.cambiarFavorito(actividad=self.actividad)
        self.assertTrue(resultado)

        resultado2 = self.usuario.cambiarFavorito(actividad=self.actividad)
        self.assertFalse(resultado2)

    def test_cambiar_favorito_error(self):
        with self.assertRaises(ValueError):
            self.usuario.cambiarFavorito(
                actividad=self.actividad,
                instalacion=self.instalacion
            )

    # ----------------- REGISTRAR USUARIO -----------------

    def test_registrar_usuario_ok(self):
        self.foro = Foro.objects.create()
        Canal.objects.create(
            titulo="General",
            tema="General",
            numeroParticipantes=0,
            foro=self.foro
        )

        resultado = UsuarioFinal.registrarUsuario(
            nombre="Ana",
            apellidos="Gomez",
            sexo=Sexo.NINGUNO,
            fechaNacimiento=date(1995, 1, 1),
            dni="87654321B",
            telefono="123456789",
            email="ana@test.com",
            provincia="Madrid",
            municipio="Madrid",
            localidad="Centro",
            codigoPostal="28001",
            password="1234",
            esUAM=False
        )

        self.assertFalse(resultado["error"])
        self.assertEqual(resultado["respuesta"].nombre, "Ana")
    
    def test_registrar_usuario_error_dni_duplicado(self):
        User = get_user_model()

        User.objects.create_user(
            username="12345678A",
            email="otro@test.com",
            password="1234"
        )

        resultado = UsuarioFinal.registrarUsuario(
            nombre="Juan",
            apellidos="Pérez",
            sexo="H",
            fechaNacimiento=date(2000, 1, 1),
            dni="12345678A",
            telefono="600000000",
            email="nuevo@test.com",
            provincia="Madrid",
            municipio="Madrid",
            localidad="Madrid",
            codigoPostal="28001",
            password="1234",
            esUAM=True
        )

        self.assertTrue(resultado["error"])
        self.assertEqual(
            resultado["respuesta"],
            "Ya existe un usuario con ese DNI"
        )

    def test_registrar_usuario_error_email_duplicado(self):
        User = get_user_model()

        User.objects.create_user(
            username="99999999Z",
            email="test@test.com",
            password="1234"
        )

        resultado = UsuarioFinal.registrarUsuario(
            nombre="Juan",
            apellidos="Pérez",
            sexo="H",
            fechaNacimiento=date(2000, 1, 1),
            dni="12345678A",
            telefono="600000000",
            email="test@test.com",
            provincia="Madrid",
            municipio="Madrid",
            localidad="Madrid",
            codigoPostal="28001",
            password="1234",
            esUAM=True
        )

        self.assertTrue(resultado["error"])
        self.assertEqual(
            resultado["respuesta"],
            "Ya existe un usuario con ese email"
        )

    # ----------------- REVISAR ACTIVIDADES -----------------

    @patch("polideportivo.models.Notificacion.notificarActividadUsuarioFinal")
    @patch("polideportivo.models.Notificacion.objects.filter")
    def test_revisar_actividades_notifica(self, mock_filter, mock_notificar):
        ahora = timezone.now()

        mapa_dias = {
            0: Dia.LUNES,
            1: Dia.MARTES,
            2: Dia.MIERCOLES,
            3: Dia.JUEVES,
            4: Dia.VIERNES,
            5: Dia.SABADO,
            6: Dia.DOMINGO
        }

        sesion = Sesion.objects.create(
            dia=mapa_dias[ahora.weekday()],
            horaInicio=(ahora + timedelta(minutes=30)).time(),
            horaFin=(ahora + timedelta(minutes=90)).time(),
            actividad=self.actividad
        )

        Asistencia.objects.create(
            usuarioFinal=self.usuario,
            sesion=sesion
        )

        mock_filter.return_value.exists.return_value = False

        with patch("polideportivo.models.usuario_final.now") as mock_now:
            mock_now.return_value = ahora
            self.usuario.revisarActividades()

        mock_notificar.assert_called_once()

    # ----------------- DELETE -----------------

    def test_delete_elimina_usuario_auth(self):
        auth_id = self.auth_user.id

        self.usuario.delete()

        User = get_user_model()

        self.assertFalse(
            User.objects.filter(id=auth_id).exists()
        )