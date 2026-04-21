from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth import get_user_model

from ..models import Bono, CompraBono, UsuarioFinal, EstadoReserva

User = get_user_model()

class BonoTests(TestCase):
    def setUp(self):
        self.bono = Bono.objects.create(
            usos=5,
            validez=2,
            precioTDA=10,
            precioUAM=15,
            precioAbono=12,
            precioOtros=20
        )


    # ----------------- CREACION -----------------

    def test_crear_bono(self):
        self.assertEqual(self.bono.usos, 5)
        self.assertEqual(self.bono.validez, 2)
        self.assertEqual(self.bono.precioTDA, 10)
        self.assertEqual(self.bono.precioUAM, 15)
        self.assertEqual(self.bono.precioAbono, 12)
        self.assertEqual(self.bono.precioOtros, 20)


    # ----------------- STR -----------------

    def test_str_bono(self):
        self.assertEqual(str(self.bono), "Bono de 5 usos en un máximo de 2 años")



class CompraBonoTests(TestCase):
    def setUp(self):
        user = User.objects.create(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1))

        self.bono = Bono.objects.create(
            usos=5,
            validez=2,
            precioTDA=10,
            precioUAM=15,
            precioAbono=12,
            precioOtros=20
        )

    # ----------------- CREAR COMPRA -----------------

    def test_compra_bono_crea_compra(self):
        compra = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)

        self.assertIsNotNone(compra)
        self.assertEqual(compra.usuarioFinal, self.usuario)
        self.assertEqual(compra.bono, self.bono)
        self.assertEqual(compra.estado, EstadoReserva.PENDIENTE)
        self.assertEqual(compra.fechaExpiracion.year, compra.fecha.year + self.bono.validez)


    # ----------------- CONTAR -----------------

    def test_contar_compras(self):
        self.assertEqual(CompraBono.contar(), 0)
        CompraBono.compraBono(bono=self.bono, usuario=self.usuario)
        self.assertEqual(CompraBono.contar(), 1)


    # ----------------- DUPLICADO -----------------

    def test_no_permite_compra_confirmada_duplicada(self):
        compra1 = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)
        compra1.confirmarCompra()
        compra2 = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)

        self.assertIsNone(compra2)


    # ----------------- CANCELAR PENDIENTES -----------------

    def test_cancelar_compras_pendientes(self):
        compra1 = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)
        compra2 = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)
        compra1.refresh_from_db()

        self.assertEqual(compra1.estado, EstadoReserva.CANCELADO)
        self.assertEqual(compra2.estado, EstadoReserva.PENDIENTE)


    # ----------------- CALCULAR PRECIO -----------------

    def test_calcular_precio(self):
        compra = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)

        self.assertEqual(compra.calcularPrecio(), self.bono.precioOtros)

        self.usuario.tieneAbono = True
        self.usuario.save()

        self.assertEqual(compra.calcularPrecio(), self.bono.precioAbono)

        self.usuario.tieneAbono = False
        self.usuario.esUAM = True
        self.usuario.save()

        self.assertEqual(compra.calcularPrecio(), self.bono.precioUAM)

        self.usuario.esUAM = False
        self.usuario.tieneTDA = True
        self.usuario.save()

        self.assertEqual(compra.calcularPrecio(), self.bono.precioTDA)


    # ----------------- CONFIRMAR Y CANCELAR -----------------

    def test_confirmar_y_cancelar_compra(self):
        compra = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)
        compra.confirmarCompra()
        compra.refresh_from_db()

        self.assertEqual(compra.estado, EstadoReserva.CONFIRMADA)

        compra.cancelarCompra()
        compra.refresh_from_db()

        self.assertEqual(compra.estado, EstadoReserva.CANCELADO)


    # ----------------- ATRIBUTOS DEL BONO -----------------

    def test_usos_restantes(self):
        compra = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)
        compra.vecesUsado = 2
        compra.save()

        self.assertEqual(compra.usosRestantes, self.bono.usos - 2)

    def test_activo_propiedad(self):
        compra = CompraBono.compraBono(bono=self.bono, usuario=self.usuario)
        compra.fechaExpiracion = timezone.now() + timedelta(days=1)
        compra.save()

        self.assertTrue(compra.activo)

        compra.fechaExpiracion = timezone.now() - timedelta(days=1)
        compra.save()

        self.assertFalse(compra.activo)