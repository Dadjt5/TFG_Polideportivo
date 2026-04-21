from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import Deporte


class DeporteTests(TestCase):
    def setUp(self):
        self.deporte1 = Deporte.objects.create(titulo="Fútbol")
        self.deporte2 = Deporte.objects.create(titulo="Baloncesto")


    # ----------------- STR -----------------

    def test_str_deporte(self):
        self.assertEqual(str(self.deporte1), "Fútbol")
        self.assertEqual(str(self.deporte2), "Baloncesto")


    # ----------------- CONTAR -----------------

    def test_contar_deportes(self):
        self.assertEqual(Deporte.contar(), 2)


    # ----------------- UNICO -----------------

    def test_unicidad_titulo(self):
        with self.assertRaises(IntegrityError):
            Deporte.objects.create(titulo="Fútbol")