from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

from polideportivo.models import (
    TDA,
    UsuarioFinal,
    TarifaTDA,
    EstadoReserva
)

User = get_user_model()

class TDAViewSetTests(APITestCase):

    def setUp(self):
        self.usuario_login = User.objects.create_user(
            username="usuario",
            email="usuario@test.com",
            password="1234"
        )

        self.usuario_final = UsuarioFinal.objects.create(user=self.usuario_login)

        self.tarifa = TarifaTDA.objects.create(
            nombre="Tarifa base",
            precio=100
        )

    def test_crear_tda_asigna_campos_correctamente(self):
        self.client.force_authenticate(user=self.usuario_login)

        datos = {
            "usuario_id": self.usuario_final.id
        }

        response = self.client.post("/api/v1/tdas/", datos)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tda = TDA.objects.first()

        self.assertEqual(tda.usuarioFinal, self.usuario_final)
        self.assertEqual(tda.estado, EstadoReserva.CONFIRMADA)
        self.assertIsNotNone(tda.tarifa)


        def test_usuario_queda_marcado_con_tda(self):
            self.client.force_authenticate(user=self.usuario_login)

            self.client.post("/api/v1/tda/", {
                "usuario_id": self.usuario_final.id
            })

            self.usuario_final.refresh_from_db()

            self.assertTrue(self.usuario_final.tieneTDA)
        
        def test_eliminar_tda_desmarca_usuario(self):
            tda = TDA.objects.create(
                usuarioFinal=self.usuario_final,
                tarifa=self.tarifa,
                estado=EstadoReserva.CONFIRMADA,
                fechaExpiracion=now().date()
            )

            self.usuario_final.tieneTDA = True
            self.usuario_final.save()

            self.client.force_authenticate(user=self.usuario_login)

            response = self.client.delete(f"/api/v1/tdas/{tda.id}/")

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            self.usuario_final.refresh_from_db()

            self.assertFalse(self.usuario_final.tieneTDA)