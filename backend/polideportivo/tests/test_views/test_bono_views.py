from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta

from polideportivo.models import (
    UsuarioFinal,
    CompraBono,
    EstadoReserva,
    Bono,
    Administrador
)

class BonosUsuarioFinalViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )

        self.administrador = Administrador.objects.create(user=self.admin)

        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.bono_unico = Bono.objects.create()
        self.usuario_final = UsuarioFinal.objects.create(nombre="UF1", fechaNacimiento=date(2001,1,1), user=self.user)

        self.bono = CompraBono.objects.create(
            usuarioFinal=self.usuario_final,
            estado=EstadoReserva.CONFIRMADA,
            bono=self.bono_unico,
            fechaExpiracion=date.today() + timedelta(days=365)
        )

    def test_get_bonos_ok(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(
            f"/api/v1/usuariosFinales/{self.usuario_final.id}/bonos/"
        )

        self.assertEqual(response.status_code, 200)

    def test_post_incrementar_bono_ok(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "bono_id": self.bono.id,
            "cantidad": 2
        }

        response = self.client.post(
            f"/api/v1/usuariosFinales/{self.usuario_final.id}/bonos/",
            data
        )

        self.assertEqual(response.status_code, 200)

    def test_post_bono_inactivo_lo_cancela(self):
        self.client.force_authenticate(user=self.admin)

        self.bono.fechaExpiracion = date.today() - timedelta(days=1)
        self.bono.save()

        data = {
            "bono_id": self.bono.id,
            "cantidad": 1
        }

        response = self.client.post(
            f"/api/v1/usuariosFinales/{self.usuario_final.id}/bonos/",
            data
        )

        self.assertEqual(response.status_code, 200)

        self.bono.refresh_from_db()
        self.assertEqual(self.bono.estado, EstadoReserva.CANCELADO)

    def test_post_sin_auth(self):
        data = {
            "bono_id": self.bono.id,
            "cantidad": 1
        }

        response = self.client.post(
            f"/api/v1/usuariosFinales/{self.usuario_final.id}/bonos/",
            data
        )

        self.assertEqual(response.status_code, 401)