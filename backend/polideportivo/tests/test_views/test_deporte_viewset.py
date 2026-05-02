from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from polideportivo.models import Deporte, Actividad

User = get_user_model()


class DeporteViewSetTests(APITestCase):

    def setUp(self):
        self.deporte = Deporte.objects.create(
            nombre="Fútbol"
        )

    def test_eliminar_deporte_correctamente(self):
        response = self.client.delete(f"/api/deporte/{self.deporte.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Deporte.objects.filter(id=self.deporte.id).exists())
    
    def test_no_se_puede_eliminar_deporte_si_esta_en_uso(self):
        # deporte
        deporte = Deporte.objects.create(nombre="Baloncesto")

        # actividad que lo usa (clave para bloquear borrado)
        Actividad.objects.create(
            nombre="Entrenamiento",
            deporte=deporte
        )

        response = self.client.delete(f"/api/deporte/{deporte.id}/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Deporte.objects.filter(id=deporte.id).exists())