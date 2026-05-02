from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from polideportivo.models import Monitor

User = get_user_model()

class MonitorViewSetTests(APITestCase):

    def setUp(self):
        self.usuario_monitor = User.objects.create_user(
            username="monitor",
            email="monitor@test.com",
            password="1234"
        )
        self.usuario_monitor.is_monitor = True
        self.usuario_monitor.save()

        self.monitor = Monitor.objects.create(
            user=self.usuario_monitor,
            nombre="Monitor 1"
        )

    def test_monitor_solo_ve_su_perfil(self):
        self.client.force_authenticate(user=self.usuario_monitor)

        response = self.client.get("/api/monitor/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_admin_ve_todos_los_monitores(self):
        admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        admin.is_administrador = True
        admin.save()

        Monitor.objects.create(user=admin, nombre="Monitor 2")

        self.client.force_authenticate(user=admin)

        response = self.client.get("/api/monitor/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)
    

    def test_actualizar_monitor(self):
        self.client.force_authenticate(user=self.usuario_monitor)

        datos = {
            "nombre": "Monitor actualizado"
        }

        response = self.client.patch(
            f"/api/monitor/{self.monitor.id}/",
            datos
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.monitor.refresh_from_db()
        self.assertEqual(self.monitor.nombre, "Monitor actualizado")