from django.test import TestCase
from django.utils import timezone
from datetime import date
from django.contrib.auth import get_user_model

from ...models import (
    CompraAbono, AbonoDeportivo, AbonoVerano, UsuarioFinal, 
    EstadoReserva, TipoPago, Rol
)

User = get_user_model()


class CompraAbonoUnitTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="123456"
        )

        self.usuario = UsuarioFinal.objects.create(
            user=self.user,
            esUAM=True,
            tieneTDA=False,
            tieneAbono=False,
            fechaNacimiento=date(2001,1,1)
        )

        self.abono_deportivo = AbonoDeportivo.objects.create(
            nombre="Abono anual",
            meses=12,
            precioTotalMensual=20,
            precioPagoUnicoUAM=200,
            precioFamiliar=150,
            precioTotalMensualOtros=30,
            precioPagoUnicoOtros=300
        )

        self.abono_verano = AbonoVerano.objects.create(
            nombre="Verano",
            precioTDA=25,
            precioUAM=30,
            precioOtros=40
        )

    def test_str_abono_deportivo(self):
        self.assertIn("Abono deportivo", str(self.abono_deportivo))

    def test_str_abono_verano(self):
        self.assertIn("Abono de verano", str(self.abono_verano))

    def test_contar_compras(self):
        CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoDeportivo=self.abono_deportivo
        )

        self.assertEqual(CompraAbono.contar(), 1)

    def test_calcular_precio_deportivo_uam_mensual(self):
        compra = CompraAbono(abonoDeportivo=self.abono_deportivo)

        precio = compra.calcularPrecio(
            usuario=self.usuario,
            forma=TipoPago.MENSUAL
        )

        self.assertEqual(precio, 20)

    def test_calcular_precio_deportivo_uam_unico(self):
        compra = CompraAbono(abonoDeportivo=self.abono_deportivo)

        precio = compra.calcularPrecio(
            usuario=self.usuario,
            forma=TipoPago.UNICO
        )

        self.assertEqual(precio, 200)

    def test_calcular_precio_deportivo_familiar(self):
        compra = CompraAbono(abonoDeportivo=self.abono_deportivo)

        precio = compra.calcularPrecio(
            usuario=self.usuario,
            familiar=True
        )

        self.assertEqual(precio, 150)

    def test_calcular_precio_verano_uam(self):
        compra = CompraAbono(abonoVerano=self.abono_verano)

        precio = compra.calcularPrecio(usuario=self.usuario)

        self.assertEqual(precio, 30)

    def test_calcular_precio_verano_tda(self):
        compra = CompraAbono(abonoVerano=self.abono_verano)

        self.usuario.tieneTDA = True
        self.usuario.esUAM = False
        self.usuario.rol = Rol.EXTERNO
        self.usuario.save()

        precio = compra.calcularPrecio(usuario=self.usuario)

        self.assertEqual(precio, 25)


    def test_confirmar_compra(self):
        compra = CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoDeportivo=self.abono_deportivo,
            estado=EstadoReserva.PENDIENTE
        )

        compra.confirmarCompra()

        compra.refresh_from_db()
        self.usuario.refresh_from_db()

        self.assertEqual(compra.estado, EstadoReserva.CONFIRMADA)
        self.assertTrue(self.usuario.tieneAbono)

    def test_cancelar_compra(self):
        compra = CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoDeportivo=self.abono_deportivo,
            estado=EstadoReserva.PENDIENTE
        )

        compra.cancelarCompra()

        compra.refresh_from_db()

        self.assertEqual(compra.estado, EstadoReserva.CANCELADO)
    
    def test_cancelar_compra_confirmada(self):
        compra = CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoDeportivo=self.abono_deportivo,
            estado=EstadoReserva.CONFIRMADA
        )

        compra.cancelarCompra()

        compra.refresh_from_db()

        self.assertEqual(compra.estado, EstadoReserva.CANCELADO)