from unittest.mock import patch

from django.test import TestCase
from django.db.utils import IntegrityError
from datetime import date, timedelta
from django.contrib.auth import get_user_model


from ..models import TDA, UsuarioFinal, TarifaTDA, EstadoReserva

User = get_user_model()


class TDATests(TestCase):
    def setUp(self):
        user = User.objects.create(username="user0", password="1234")
        self.usuario = UsuarioFinal.objects.create(nombre="user0", user=user, fechaNacimiento=date(2001,1,1))

        self.tarifa = TarifaTDA.objects.create(precioUAM=10, precioOtros=20)


    # ----------------- STR -----------------

    def test_str(self):
        tda = TDA(fechaInicio=date(2024, 1, 1), fechaExpiracion=date(2025, 1, 1))

        self.assertIn("2024-01-01", str(tda))
        self.assertIn("2025-01-01", str(tda))


    # ----------------- CODIGO SECRETO -----------------

    def test_codigo_secreto(self):
        tda = TDA()
        tda.nuevoCodigoSecreto("1234")

        self.assertTrue(tda.comprobarCodigoSecreto("1234"))
        self.assertFalse(tda.comprobarCodigoSecreto("0000"))


    # ----------------- COMPRA -----------------

    def test_compra_tda_ok(self):
        user = User.objects.create_user(username="user1", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user1", user=user, fechaNacimiento=date(2001,1,1))
        TarifaTDA.objects.create(precioUAM=5, precioOtros=10)

        tda = TDA.compraTDA(usuario)

        self.assertIsNotNone(tda)
        self.assertEqual(tda.usuarioFinal, usuario)
        self.assertEqual(tda.estado, EstadoReserva.PENDIENTE)

    def test_compra_tda_ya_confirmada(self):
        user = User.objects.create_user(username="user3", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user3", user=user, fechaNacimiento=date(2001,1,1))
        tarifa = TarifaTDA.objects.create(precioUAM=5, precioOtros=10)

        TDA.objects.create(
            usuarioFinal=usuario,
            estado=EstadoReserva.CONFIRMADA,
            fechaExpiracion=date.today() + timedelta(days=10),
            tarifa=tarifa
        )

        tda = TDA.compraTDA(usuario)
        self.assertIsNone(tda)

    def test_compra_tda_elimina_pendientes(self):
        user = User.objects.create_user(username="user4", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user4", user=user, fechaNacimiento=date(2001,1,1))
        tarifa = TarifaTDA.objects.create(precioUAM=5, precioOtros=10)

        TDA.objects.create(usuarioFinal=usuario, estado=EstadoReserva.PENDIENTE, tarifa=tarifa)

        tda = TDA.compraTDA(usuario)

        self.assertEqual(TDA.objects.filter(usuarioFinal=usuario).count(), 1)
        self.assertEqual(tda.estado, EstadoReserva.PENDIENTE)


    # ----------------- CALCULAR PRECIO -----------------

    def test_calcular_precio_no_uam(self):
        tda = TDA(usuarioFinal=self.usuario, tarifa=self.tarifa)
        self.assertEqual(tda.calcularPrecio(), 20)

    def test_calcular_precio_uam(self):
        self.usuario.esUAM = True
        tda = TDA(usuarioFinal=self.usuario, tarifa=self.tarifa)
        self.assertEqual(tda.calcularPrecio(), 10)


    # ----------------- CONFIRMAR -----------------

    def test_confirmar_compra(self):
        user = User.objects.create_user(username="user5", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user5", tieneTDA=False, user=user, fechaNacimiento=date(2001,1,1))
        tarifa = TarifaTDA.objects.create(precioUAM=5, precioOtros=10)

        tda = TDA.objects.create(usuarioFinal=usuario, tarifa=tarifa)

        tda.confirmarCompra()

        usuario.refresh_from_db()
        tda.refresh_from_db()

        self.assertTrue(usuario.tieneTDA)
        self.assertEqual(tda.estado, EstadoReserva.CONFIRMADA)


    # ----------------- CANCELAR -----------------

    def test_cancelar_compra(self):
        user = User.objects.create_user(username="user6", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user6", tieneTDA=True, user=user, fechaNacimiento=date(2001,1,1))
        tarifa = TarifaTDA.objects.create(precioUAM=5, precioOtros=10)

        tda = TDA.objects.create(usuarioFinal=usuario, tarifa=tarifa)

        tda.cancelarCompra()

        usuario.refresh_from_db()

        self.assertFalse(usuario.tieneTDA)
        self.assertEqual(TDA.objects.count(), 0)


    # ----------------- CONTAR -----------------

    def test_contar(self):
        user = User.objects.create_user(username="user7", password="1234")
        usuario = UsuarioFinal.objects.create(nombre="user7", user=user, fechaNacimiento=date(2001,1,1))
        tarifa = TarifaTDA.objects.create(precioUAM=5, precioOtros=10)

        TDA.objects.create(usuarioFinal=usuario, tarifa=tarifa)
        TDA.objects.create(usuarioFinal=usuario, tarifa=tarifa)

        self.assertEqual(TDA.contar(), 2)


    # ----------------- COMPRAR TDA -----------------

    def test_compra_tda_sin_tarifa_devuelve_none(self):
        TarifaTDA.objects.all().delete()

        tda = TDA.compraTDA(self.usuario)

        self.assertIsNone(tda)
    
    @patch("polideportivo.models.tda.TarifaTDA.objects.exists")
    @patch("polideportivo.models.tda.TarifaTDA.objects.first")
    def test_compra_tda_tarifa_exists_false(self, mock_first, mock_exists):
        mock_first.return_value = object()
        mock_exists.return_value = False

        tda = TDA.compraTDA(self.usuario)

        self.assertIsNone(tda)

    def test_compra_tda_elimina_tda_caducada(self):
        tda_vencida = TDA.objects.create(
            usuarioFinal=self.usuario,
            estado=EstadoReserva.CONFIRMADA,
            fechaExpiracion=date.today() - timedelta(days=1),
            tarifa=self.tarifa
        )

        tda_nueva = TDA.compraTDA(self.usuario)

        self.assertFalse(
            TDA.objects.filter(id=tda_vencida.id).exists()
        )

        self.assertIsNotNone(tda_nueva)