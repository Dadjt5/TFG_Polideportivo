from django.test import TestCase
from datetime import date
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models import (
    AbonoDeportivo, AbonoVerano, CompraAbono, EstadoReserva,
    TipoPago, UsuarioFinal
)

User = get_user_model()


class AbonoTest(TestCase):

    # ----------------- HERENCIA -----------------

    def test_herencia_nombre_en_abono_deportivo(self):
        abono = AbonoDeportivo.objects.create(
            nombre="Abono Gym",
            meses=3
        )
        self.assertEqual(abono.nombre, "Abono Gym")

    def test_herencia_nombre_en_abono_verano(self):
        abono = AbonoVerano.objects.create(
            nombre="Abono Verano"
        )
        self.assertEqual(abono.nombre, "Abono Verano")


class AbonoDeportivoTest(TestCase):
    def setUp(self):
        self.abono = AbonoDeportivo.objects.create(
            nombre="Abono Premium",
            meses=6,
            descuentoPrimeraActividad=10.0,
            descuentoRestoActividades=5.0,
            descuentoActividadesExteriores=3.0,
            descuentoAlquileres=2.0,
            precioTotalMensual=50.0,
            precioPagoUnicoUAM=270.0,
            precioFamiliar=200.0,
            precioTotalMensualOtros=60.0,
            precioPagoUnicoOtros=300.0
        )


    # ----------------- CREACION -----------------

    def test_creacion_abono_deportivo(self):
        """Se crea correctamente en base de datos"""
        self.assertEqual(self.abono.nombre, "Abono Premium")
        self.assertEqual(self.abono.meses, 6)
        self.assertEqual(self.abono.precioTotalMensual, 50.0)

    def test_str(self):
        """Representación en string"""
        texto = str(self.abono)
        self.assertIn("Abono deportivo de 6", texto)
        self.assertIn("comienza el", texto)


    # ----------------- PRECIOS Y MESES -----------------

    def test_valores_por_defecto(self):
        """Comprueba valores por defecto"""
        abono = AbonoDeportivo.objects.create(nombre="Basico")

        self.assertEqual(abono.meses, 1)
        self.assertEqual(abono.descuentoPrimeraActividad, 0.0)
        self.assertEqual(abono.precioTotalMensual, 0.0)

    def test_fecha_inicio_auto(self):
        """fechaInicio se asigna automáticamente"""
        hoy = timezone.now().date()
        self.assertEqual(self.abono.fechaInicio, hoy)

    def test_campos_tipo_float(self):
        """Verifica que los campos numéricos guardan correctamente floats"""
        self.assertIsInstance(self.abono.precioTotalMensual, float)
        self.assertIsInstance(self.abono.descuentoPrimeraActividad, float)

    def test_meses_es_positivo(self):
        """meses debe ser positivo"""
        abono = AbonoDeportivo.objects.create(nombre="Test", meses=3)
        self.assertGreater(abono.meses, 0)


class AbonoVeranoTest(TestCase):
    def setUp(self):
        self.abono = AbonoVerano.objects.create(
            nombre="Abono Verano 2026",
            precioTDA=30.0,
            precioUAM=25.0,
            precioOtros=40.0
        )

    # ----------------- CREACION Y STR -----------------

    def test_creacion_abono_verano(self):
        """Se crea correctamente"""
        self.assertEqual(self.abono.nombre, "Abono Verano 2026")
        self.assertEqual(self.abono.precioUAM, 25.0)

    def test_str(self):
        """Representación en string"""
        texto = str(self.abono)

        self.assertIn("Abono de verano", texto)
        self.assertIn("coste 25.0", texto)


    # ----------------- PRECIOS -----------------

    def test_valores_por_defecto(self):
        """Valores por defecto en precios"""
        abono = AbonoVerano.objects.create(nombre="Basico")

        self.assertEqual(abono.precioTDA, 0.0)
        self.assertEqual(abono.precioUAM, 0.0)
        self.assertEqual(abono.precioOtros, 0.0)

    def test_tipos_de_precios(self):
        """Verifica que los precios son floats"""
        self.assertIsInstance(self.abono.precioTDA, float)
        self.assertIsInstance(self.abono.precioUAM, float)
        self.assertIsInstance(self.abono.precioOtros, float)

    def test_precio_no_negativo(self):
        """Los precios deberían ser >= 0 (control básico)"""
        self.assertGreaterEqual(self.abono.precioTDA, 0)
        self.assertGreaterEqual(self.abono.precioUAM, 0)
        self.assertGreaterEqual(self.abono.precioOtros, 0)



class CompraAbonoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1", password="1234")
        self.usuario = UsuarioFinal.objects.create(nombre="user1", user=self.user, fechaNacimiento=date(2001,1,1), esUAM=True, tieneTDA=True)

        self.abono_dep = AbonoDeportivo.objects.create(
            nombre="Premium",
            precioTotalMensual=50,
            precioPagoUnicoUAM=200,
            precioFamiliar=150,
            precioTotalMensualOtros=60,
            precioPagoUnicoOtros=250
        )

        self.abono_ver = AbonoVerano.objects.create(
            nombre="Verano",
            precioTDA=20,
            precioUAM=15,
            precioOtros=30
        )
    
    # ----------------- CREACION -----------------

    def test_creacion_compra(self):
        compra = CompraAbono.objects.create(
            usuarioFinal=None,
            abonoDeportivo=self.abono_dep
        )
        self.assertIsNotNone(compra.id)


    # ----------------- CONTAR -----------------

    def test_contar(self):
        CompraAbono.objects.create(abonoDeportivo=self.abono_dep)
        CompraAbono.objects.create(abonoVerano=self.abono_ver)

        self.assertEqual(CompraAbono.contar(), 2)


    # ----------------- CALCULAR PRECIO -----------------

    def test_precio_abono_deportivo_uam_mensual(self):
        compra = CompraAbono(abonoDeportivo=self.abono_dep)
        precio = compra.calcularPrecio(self.usuario, TipoPago.MENSUAL)

        self.assertEqual(precio, 50)

    def test_precio_abono_deportivo_uam_unico(self):
        compra = CompraAbono(abonoDeportivo=self.abono_dep)
        precio = compra.calcularPrecio(self.usuario, TipoPago.UNICO)

        self.assertEqual(precio, 200)

    def test_precio_abono_deportivo_familiar(self):
        compra = CompraAbono(abonoDeportivo=self.abono_dep)
        precio = compra.calcularPrecio(self.usuario, familiar=True)

        self.assertEqual(precio, 150)

    def test_precio_abono_verano_uam(self):
        compra = CompraAbono(abonoVerano=self.abono_ver)
        precio = compra.calcularPrecio(self.usuario)

        self.assertEqual(precio, 15)

    def test_precio_abono_verano_tda(self):
        user = User.objects.create(username="user2", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user2", user=user, fechaNacimiento=date(2001,1,1), esUAM=False, tieneTDA=True)

        compra = CompraAbono(abonoVerano=self.abono_ver)

        precio = compra.calcularPrecio(usuario)
        self.assertEqual(precio, 20)


    # ----------------- CONFIRMAR COMPRA -----------------

    def test_confirmar_compra(self):
        user = User.objects.create(username="user3", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user3", user=user, fechaNacimiento=date(2001,1,1))

        compra = CompraAbono.objects.create(
            usuarioFinal=usuario,
            abonoDeportivo=self.abono_dep
        )

        compra.confirmarCompra()

        self.assertEqual(compra.estado, EstadoReserva.CONFIRMADA)
        self.assertTrue(usuario.tieneAbono)


    # ----------------- CANCELAR COMPRA -----------------

    def test_cancelar_compra_confirmada(self):
        user = User.objects.create(username="user4", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user4", user=user, fechaNacimiento=date(2001,1,1))

        compra = CompraAbono.objects.create(
            usuarioFinal=usuario,
            abonoDeportivo=self.abono_dep,
            estado=EstadoReserva.CONFIRMADA
        )

        compra.cancelarCompra()

        self.assertEqual(compra.estado, EstadoReserva.CANCELADO)
        self.assertIsNone(compra.usuarioFinal)


    # ----------------- COMPRA ABONO ----------------- 

    def test_compra_abono_nueva(self):
        compra = CompraAbono.compraAbono(
            self.abono_dep,
            self.usuario,
            "abono_deportivo"
        )

        self.assertIsNotNone(compra)
        self.assertEqual(compra.estado, EstadoReserva.PENDIENTE)

    def test_no_duplica_compra_confirmada(self):
        CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoDeportivo=self.abono_dep,
            estado=EstadoReserva.CONFIRMADA
        )

        compra = CompraAbono.compraAbono(
            self.abono_dep,
            self.usuario,
            "abono_deportivo"
        )

        self.assertIsNone(compra)

    def test_elimina_pendientes_anteriores(self):
        CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoDeportivo=self.abono_dep,
            estado=EstadoReserva.PENDIENTE
        )

        nueva = CompraAbono.compraAbono(
            self.abono_dep,
            self.usuario,
            "abono_deportivo"
        )

        pendientes = CompraAbono.objects.filter(
            usuarioFinal=self.usuario,
            estado=EstadoReserva.PENDIENTE
        )

        self.assertEqual(pendientes.count(), 1)
        self.assertEqual(pendientes.first().id, nueva.id)