from django.test import TestCase
from datetime import time
from unittest.mock import MagicMock

from ...models import (
    Pabellon, Instalacion, Calle, TipoInstalacion, TarifaInstalacion, Dia
)


class PabellonUnitTest(TestCase):

    def test_str(self):
        p = Pabellon.objects.create(nombre="Central", direccion="Madrid")
        self.assertIn("Central", str(p))

    def test_contar(self):
        Pabellon.objects.create(nombre="A")
        Pabellon.objects.create(nombre="B")
        self.assertEqual(Pabellon.contar(), 2)


class InstalacionUnitTest(TestCase):

    def setUp(self):
        self.pabellon = Pabellon.objects.create(nombre="P1")

        self.tarifa = TarifaInstalacion.objects.create(
            precioAbonado=10,
            precioUAM=20,
            precioTDA=30,
            precioOtros=40,
            costeIluminacion=5
        )

        self.instalacion = Instalacion.objects.create(
            nombre="Piscina",
            pabellon=self.pabellon,
            tipoInstalacion=TipoInstalacion.SALA_MULTIUSOS,
            tarifa=self.tarifa,
            numeroCalles=0
        )

    def test_str(self):
        self.assertIn("Piscina", str(self.instalacion))

    def test_contar(self):
        self.assertGreaterEqual(Instalacion.contar(), 1)

    def test_obtener_precios(self):
        precios = self.instalacion.obtenerPrecios()
        self.assertEqual(precios["precioAbonado"], 10)

    def test_calcular_precio_base(self):
        class U:
            tieneAbono = True
            esUAM = False
            tieneTDA = False

        self.assertEqual(self.instalacion._calcular_precio_base(U()), 10)

    def test_comprobar_aforo_piscina(self):
        self.instalacion.tipoInstalacion = TipoInstalacion.PISCINA
        self.instalacion.numeroCalles = 2
        self.instalacion.save()

        ok = self.instalacion.comprobarAforo(100, 2)
        self.assertTrue(ok)

    def test_buscar(self):
        res = Instalacion.buscar(nombre="Piscina")
        self.assertTrue(res.exists())

    def test_modificar_informacion(self):
        self.instalacion.modificarInformacion(
            {"nombre": "Nueva"},
            self.pabellon,
            self.tarifa,
            "img.png"
        )
        self.assertEqual(self.instalacion.nombre, "Nueva")
    
    def test_crear_calles_no_piscina(self):
        self.instalacion.tipoInstalacion = TipoInstalacion.SALA_MULTIUSOS
        self.instalacion.numeroCalles = 3
        self.instalacion.save()

        self.instalacion.crearCalles()

        self.assertEqual(self.instalacion.calles.count(), 0)
    
    def test_crear_calles_piscina(self):
        self.instalacion.tipoInstalacion = TipoInstalacion.PISCINA
        self.instalacion.numeroCalles = 3
        self.instalacion.save()

        self.instalacion.crearCalles()

        self.assertEqual(self.instalacion.calles.count(), 3)
    
    def test_calcular_precio_base_uam(self):
        class U:
            tieneAbono = False
            esUAM = True
            tieneTDA = False

        self.assertEqual(self.instalacion._calcular_precio_base(U()), 20)
    
    def test_calcular_precio_base_tda(self):
        class U:
            tieneAbono = False
            esUAM = False
            tieneTDA = True

        self.assertEqual(self.instalacion._calcular_precio_base(U()), 30)
    
    def test_calcular_precio_base_otros(self):
        class U:
            tieneAbono = False
            esUAM = False
            tieneTDA = False

        self.assertEqual(self.instalacion._calcular_precio_base(U()), 40)