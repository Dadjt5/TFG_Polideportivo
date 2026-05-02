from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
import json

User = get_user_model()

from polideportivo.models import (
    Pabellon,
    TarifaInstalacion,
    Instalacion,
    Agenda,
    Sesion,
    TipoInstalacion
)

class NuevaInstalacionViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador = True
        self.admin.save()

        self.pabellon = Pabellon.objects.create(nombre="Pabellon 1")
        self.tarifa = TarifaInstalacion.objects.create(nombre="Tarifa 1", precio=10)

    def test_crear_instalacion_ok(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "instalacion": json.dumps({
                "nombre": "Piscina 1",
                "pabellon": self.pabellon.id,
                "tarifa": self.tarifa.id,
                "tipoInstalacion": TipoInstalacion.PISCINA,
                "numeroCalles": 4
            }),
            "agenda": json.dumps([]),
            "fechasEspeciales": json.dumps([])
        }

        response = self.client.post(
            "/api/v1/instalacion/nueva/",
            data
        )

        self.assertEqual(response.status_code, 201)

    def test_crear_instalacion_sin_datos_obligatorios(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "instalacion": json.dumps({
                "nombre": "Piscina 1"
            }),
            "agenda": json.dumps([]),
            "fechasEspeciales": json.dumps([])
        }

        response = self.client.post(
            "/api/v1/instalacion/nueva/",
            data
        )

        self.assertEqual(response.status_code, 400)

    def test_crear_instalacion_sin_auth(self):
        data = {
            "instalacion": json.dumps({
                "nombre": "Piscina 1"
            })
        }

        response = self.client.post(
            "/api/v1/instalacion/nueva/",
            data
        )

        self.assertEqual(response.status_code, 403)

class EditarInstalacionViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="1234"
        )
        self.admin.is_administrador = True
        self.admin.save()

        self.pabellon = Pabellon.objects.create(nombre="Pabellon 1")
        self.tarifa = TarifaInstalacion.objects.create(nombre="Tarifa 1", precio=10)

        self.instalacion = Instalacion.objects.create(
            nombre="Instalacion 1",
            pabellon=self.pabellon,
            tarifa=self.tarifa,
            aforoMaximo=100
        )

    def test_editar_instalacion_ok(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "instalacion": json.dumps({
                "nombre": "Instalacion editada",
                "pabellon": self.pabellon.id,
                "tarifa": self.tarifa.id,
                "aforoMaximo": 120
            }),
            "agenda": json.dumps([]),
            "fechasEspeciales": json.dumps([])
        }

        response = self.client.post(
            f"/api/v1/instalacion/{self.instalacion.id}/editar/",
            data
        )

        self.assertEqual(response.status_code, 200)

    def test_editar_instalacion_sin_auth(self):
        data = {
            "instalacion": json.dumps({
                "nombre": "Instalacion editada"
            }),
            "agenda": json.dumps([]),
            "fechasEspeciales": json.dumps([])
        }

        response = self.client.post(
            f"/api/v1/instalacion/{self.instalacion.id}/editar/",
            data
        )

        self.assertEqual(response.status_code, 403)

    def test_editar_instalacion_no_existe(self):
        self.client.force_authenticate(user=self.admin)

        data = {
            "instalacion": json.dumps({
                "nombre": "Instalacion editada"
            }),
            "agenda": json.dumps([]),
            "fechasEspeciales": json.dumps([])
        }

        response = self.client.post(
            "/api/v1/instalacion/999/editar/",
            data
        )

        self.assertEqual(response.status_code, 404)