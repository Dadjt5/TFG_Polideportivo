from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from polideportivo.models import Deporte, Actividad, Pabellon, Instalacion, Monitor

User = get_user_model()


class DeporteViewSetTests(APITestCase):

    def setUp(self):
        self.deporte = Deporte.objects.create(
            titulo="Fútbol"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234"
        )

        self.pabellon = Pabellon.objects.create()

        self.instalacion = Instalacion.objects.create(
            id=1,
            pabellon=self.pabellon,
            nombre="Instalacion test"
        )

        self.monitor = Monitor.objects.create(user=self.user2)

    def test_eliminar_deporte_correctamente(self):
        response = self.client.delete(f"/api/v1/deportes/{self.deporte.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Deporte.objects.filter(id=self.deporte.id).exists())
    
    def test_no_se_puede_eliminar_deporte_si_esta_en_uso(self):
        # deporte
        deporte = Deporte.objects.create(titulo="Baloncesto")

        # actividad que lo usa (clave para bloquear borrado)
        actividad = Actividad.objects.create(
            nombre="Entrenamiento",
            instalacion=self.instalacion,
            monitor=self.monitor,
            deportes=deporte
        )

        response = self.client.delete(f"/api/v1/deportes/{deporte.id}/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Deporte.objects.filter(id=deporte.id).exists())