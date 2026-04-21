from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from ...models import Notificacion, Configuracion

User = get_user_model()


class NotificacionUnitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="12345678A",
            email="test@test.com",
            password="test"
        )

        self.config = Configuracion.objects.create(
            titulo_avisos_actividades="titulo",
            texto_avisos_actividades="texto",
            titulo_cambios_cancelaciones="titulo",
            texto_cambios_cancelaciones="texto",
            titulo_problemas_pago="titulo",
            texto_problemas_pago="texto",
            titulo_salida_lista_espera="titulo",
            texto_salida_lista_espera="texto",
            titulo_ausencias="titulo",
            texto_ausencias="texto",
            titulo_material_especial="titulo",
            texto_material_especial="texto",
            titulo_cambios_sesiones="titulo",
            texto_cambios_sesiones="texto",
            titulo_avisos_sobre_actividades_usuarios="titulo",
            texto_avisos_sobre_actividades_usuarios="texto",
            titulo_avisos_sobre_actividades_monitores="titulo",
            texto_avisos_sobre_actividades_monitores="texto",
            titulo_aviso_devolucion_dinero_alquiler="titulo",
            texto_aviso_devolucion_dinero_alquiler="texto",
        )

    def test_contar_notificaciones(self):
        Notificacion.objects.create(titulo="t", descripcion="d", usuario=self.user)
        Notificacion.objects.create(titulo="t2", descripcion="d2", usuario=self.user)

        self.assertEqual(Notificacion.contar(), 2)

    def test_cambiar_estado(self):
        notif = Notificacion.objects.create(
            titulo="t",
            descripcion="d",
            usuario=self.user
        )

        Notificacion.cambiarEstado(
            usuario=self.user,
            id=notif.id,
            leido=True,
            fijado=True
        )

        notif.refresh_from_db()
        self.assertTrue(notif.leido)
        self.assertTrue(notif.fijado)

    @patch("polideportivo.models.notificacion")
    def test_nueva_notificacion_todos(self, mock_user):
        mock_user.objects.all.return_value = [self.user]

        Notificacion.nuevaNotificacion(
            titulo="t",
            descripcion="d",
            tipoUsuarios="TODOS",
            complemento=None
        )

        self.assertEqual(Notificacion.objects.count(), 1)

    def test_notificacion_problemas_pago(self):
        Notificacion.notificarProblemasPago(self.user)

        self.assertEqual(Notificacion.objects.count(), 1)
        self.assertEqual(Notificacion.objects.first().usuario, self.user)