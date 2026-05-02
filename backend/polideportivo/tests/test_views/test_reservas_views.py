from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
import json

from polideportivo.models import (
    Alquiler,
    ReservaActividad,
    EntradaListaEspera,
    EstadoReserva,
    Instalacion,
    TipoInstalacion
)

User = get_user_model()

class ReservasViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario",
            password="1234"
        )

    def test_obtener_reservas(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/v1/reservas/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_sin_reservas(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/v1/reservas/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
    
class ComprobarAlquileresViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador = True
        self.admin.save()

        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion test",
            tipoInstalacion=TipoInstalacion.PISTA,
            aforoMaximo=100
        )

    def test_sin_conflictos_alquileres(self):
        self.client.force_authenticate(user=self.admin)

        self.instalacion.revisarAlquileres = lambda sesiones, periodo, flag: {
            "alquileres": 0
        }

        data = {
            "sesiones": json.dumps([]),
            "periodo": "2026"
        }

        response = self.client.post(
            f"/api/v1/instalaciones/{self.instalacion.id}/comprobar/alquiler/",
            data
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["conflicto"])

    def test_con_conflictos_alquileres(self):
        self.client.force_authenticate(user=self.admin)

        self.instalacion.revisarAlquileres = lambda sesiones, periodo, flag: {
            "alquileres": 2,
            "usuarios": 3,
            "dinero": 50
        }

        data = {
            "sesiones": json.dumps([]),
            "periodo": "2026"
        }

        response = self.client.post(
            f"/api/v1/instalaciones/{self.instalacion.id}/comprobar/alquiler/",
            data
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["conflicto"])
        self.assertEqual(response.data["alquileres_afectados"], 2)

    def test_sin_auth(self):
        data = {
            "sesiones": json.dumps([]),
            "periodo": "2026"
        }

        response = self.client.post(
            f"/api/v1/instalaciones/{self.instalacion.id}/comprobar/alquiler/",
            data
        )

        self.assertEqual(response.status_code, 403)