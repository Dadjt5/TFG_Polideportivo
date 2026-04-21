from django.test import TestCase
from datetime import date
from ...models import CompraAbono, AbonoDeportivo, AbonoVerano, EstadoReserva, UsuarioFinal
from django.contrib.auth import get_user_model

User = get_user_model()


class CompraAbonoIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="123456"
        )

        self.usuario = UsuarioFinal.objects.create(
            user=self.user,
            esUAM=True,
            fechaNacimiento=date(2001,1,1)
        )

        self.abono_deportivo = AbonoDeportivo.objects.create(
            nombre="Abono anual"
        )

        self.abono_verano = AbonoVerano.objects.create(
            nombre="Abono verano"
        )

    def test_compra_abono_deportivo_crea_compra_pendiente(self):
        compra = CompraAbono.compraAbono(
            abono=self.abono_deportivo,
            usuario=self.usuario,
            tipoAbono="abono_deportivo"
        )

        self.assertIsNotNone(compra)
        self.assertEqual(compra.estado, EstadoReserva.PENDIENTE)
        self.assertEqual(compra.usuarioFinal, self.usuario)

    def test_compra_abono_verano_crea_compra_pendiente(self):
        compra = CompraAbono.compraAbono(
            abono=self.abono_verano,
            usuario=self.usuario,
            tipoAbono="abono_verano"
        )

        self.assertIsNotNone(compra)
        self.assertEqual(compra.estado, EstadoReserva.PENDIENTE)

    def test_no_permite_compra_confirmada_duplicada(self):
        CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoDeportivo=self.abono_deportivo,
            estado=EstadoReserva.CONFIRMADA
        )

        compra = CompraAbono.compraAbono(
            abono=self.abono_deportivo,
            usuario=self.usuario,
            tipoAbono="abono_deportivo"
        )

        self.assertIsNone(compra)
    
    def test_no_permite_compra_confirmada_duplicada_verano(self):
        CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoVerano=self.abono_verano,
            estado=EstadoReserva.CONFIRMADA
        )

        compra = CompraAbono.compraAbono(
            abono=self.abono_verano,
            usuario=self.usuario,
            tipoAbono="abono_verano"
        )

        self.assertIsNone(compra)

    def test_cancela_compra_pendiente_anterior(self):
        anterior = CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoDeportivo=self.abono_deportivo,
            estado=EstadoReserva.PENDIENTE
        )

        nueva = CompraAbono.compraAbono(
            abono=self.abono_deportivo,
            usuario=self.usuario,
            tipoAbono="abono_deportivo"
        )

        anterior.refresh_from_db()

        self.assertEqual(anterior.estado, EstadoReserva.CANCELADO)
        self.assertEqual(nueva.estado, EstadoReserva.PENDIENTE)
    
    def test_cancela_compra_pendiente_anterior_verano(self):
        anterior = CompraAbono.objects.create(
            usuarioFinal=self.usuario,
            abonoVerano=self.abono_verano,
            estado=EstadoReserva.PENDIENTE
        )

        nueva = CompraAbono.compraAbono(
            abono=self.abono_verano,
            usuario=self.usuario,
            tipoAbono="abono_verano"
        )

        anterior.refresh_from_db()

        self.assertEqual(anterior.estado, EstadoReserva.CANCELADO)
        self.assertEqual(nueva.estado, EstadoReserva.PENDIENTE)