from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from datetime import date

from polideportivo.models import (
    TDA, UsuarioFinal, TarifaTDA, EstadoReserva, Administrador, RolAdministrador
)

User = get_user_model()

class TDAViewSetTests(APITestCase):

    def setUp(self):
        self.usuario_login = User.objects.create_user(
            username="usuario",
            email="usuario@test.com",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.usuario_login, fechaNacimiento=date(2001,1,1))

        self.tarifa = TarifaTDA.objects.create(
            precioOtros=100
        )

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        Administrador.objects.create(user=self.admin, rol=RolAdministrador.RAIZ)

    def test_crear_tda_asigna_campos_correctamente(self):
        self.client.force_authenticate(user=self.admin)

        datos = {
            "usuario_id": self.usuario_final.id
        }

        response = self.client.post("/api/v1/tdas/", datos)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tda = TDA.objects.first()

        self.assertEqual(tda.usuarioFinal, self.usuario_final)
        self.assertEqual(tda.estado, EstadoReserva.CONFIRMADA)
        self.assertIsNotNone(tda.tarifa)
        
    def test_eliminar_tda_desmarca_usuario(self):
        tda = TDA.objects.create(
            usuarioFinal=self.usuario_final,
            tarifa=self.tarifa,
            estado=EstadoReserva.CONFIRMADA,
            fechaExpiracion=now().date()
        )

        self.usuario_final.tieneTDA = True
        self.usuario_final.save()

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/api/v1/tdas/{tda.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.usuario_final.refresh_from_db()
        self.assertFalse(self.usuario_final.tieneTDA)