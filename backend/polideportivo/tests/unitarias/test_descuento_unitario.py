from django.test import TestCase

from ...models import Descuento


class DescuentoUnitTest(TestCase):

    def test_str(self):
        d = Descuento.objects.create(
            nombre="Promo verano",
            porcentaje=10,
            fechaInicio="2024-01-01",
            fechaFinValidez="2026-12-31"
        )

        self.assertEqual(str(d), "Promo verano del 10%")

    def test_contar(self):
        Descuento.objects.create(
            nombre="D1",
            porcentaje=5,
            fechaInicio="2024-01-01",
            fechaFinValidez="2026-12-31"
        )

        self.assertEqual(Descuento.contar(), 1)

    def test_calcular_porcentaje(self):
        d1 = Descuento(porcentaje=10)
        d2 = Descuento(porcentaje=20)

        total = Descuento._calcular_porcentaje([d1, d2])

        self.assertEqual(total, 30)
    
    def test_filtrar_descuentos_combinables(self):
        d1 = Descuento.objects.create(
            nombre="A",
            porcentaje=5,
            combinable=True,
            fechaInicio="2024-01-01",
            fechaFinValidez="2026-12-31"
        )

        d2 = Descuento.objects.create(
            nombre="B",
            porcentaje=10,
            combinable=True,
            fechaInicio="2024-01-01",
            fechaFinValidez="2026-12-31"
        )

        descuentos = Descuento.objects.filter(id__in=[d1.id, d2.id])

        resultado = Descuento._filtrar_descuentos(descuentos)

        self.assertEqual(resultado["porcentaje_total"], 15)
        self.assertEqual(len(resultado["descuentos"]), 2)
    
    def test_filtrar_prioritario(self):
        d1 = Descuento.objects.create(
            nombre="A",
            porcentaje=5,
            combinable=True,
            fechaInicio="2024-01-01",
            fechaFinValidez="2026-12-31"
        )

        d2 = Descuento.objects.create(
            nombre="B",
            porcentaje=50,
            prioritario=True,
            combinable=False,
            fechaInicio="2024-01-01",
            fechaFinValidez="2026-12-31"
        )

        descuentos = Descuento.objects.filter(id__in=[d1.id, d2.id])

        resultado = Descuento._filtrar_descuentos(descuentos)

        self.assertEqual(resultado["descuentos"][0].nombre, "B")