from django.test import TestCase
from unittest.mock import patch, MagicMock, PropertyMock
from django.contrib.auth import get_user_model
from datetime import date, time, datetime, timezone

from ...models import (
    Pago, EstadoPago, TipoPago, Configuracion, Alquiler,
    Instalacion, Pabellon, UsuarioFinal, TarifaInstalacion,
    AbonoVerano, CompraAbono, ReservaActividad, Monitor,
    Actividad, AbonoDeportivo, EstadoReserva, Periodo
)


class PagoIntegracionTest(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create(
            username="usuario_test",
            password="1234"
        )

        self.usuarioFinal = UsuarioFinal.objects.create(
            fechaNacimiento=date(2001,1,1),
            user=self.user
        )

        self.configuracion = Configuracion.objects.create()

        self.pabellon = Pabellon.objects.create()
        self.tarifa = TarifaInstalacion.objects.create(costeIluminacion=10)
        self.instalacion = Instalacion.objects.create(pabellon=self.pabellon, tarifa=self.tarifa)

        self.user2 = User.objects.create(username="monitor", password="1234")
        self.monitor = Monitor.objects.create(user=self.user2)

        self.actividad = Actividad.objects.create(monitor=self.monitor, instalacion=self.instalacion)

        self.objeto = Alquiler.objects.create(
            instalacion=self.instalacion,
            usuarioFinal=self.usuarioFinal,
            horaInicio=time(10,0),
            horaFin=time(11,0)
        )

    @patch("stripe.PaymentIntent.create")
    def test_creacion_y_confirmacion_pago_unico(self, mock_stripe):
        mock_stripe.return_value = MagicMock(id="pi_test")

        pago = Pago.nuevoPago(
            concepto="integracion test",
            usuario=self.usuarioFinal,
            tipo=TipoPago.UNICO,
            objeto=self.objeto
        )

        self.assertEqual(pago.estadoPago, EstadoPago.PENDIENTE)

        pago.confirmarPago()

        self.assertEqual(pago.estadoPago, EstadoPago.PAGADO)

    @patch("polideportivo.models.pago.datetime")
    @patch("stripe.Subscription.create")
    def test_pago_suscripcion_flujo_completo(self, mock_sub, mock_datetime):
        mock_sub.return_value = MagicMock(id="sub_test")
        mock_datetime.now.return_value = datetime(2025, 12, 15, tzinfo=timezone.utc)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)


        pago = Pago.nuevoPago(
            concepto="subscripcion test",
            usuario=self.usuarioFinal,
            tipo=TipoPago.MENSUAL,
            objeto=self.objeto
        )

        subscription = pago.aplicarSubscripcion(self.usuarioFinal)

        self.assertEqual(subscription.id, "sub_test")

    @patch("stripe.Refund.create")
    def test_cancelacion_pago_integrado(self, mock_refund):
        mock_refund.return_value = MagicMock(id="re_123")

        pago = Pago.nuevoPago(
            concepto="cancel test",
            usuario=self.usuarioFinal,
            tipo=TipoPago.UNICO,
            objeto=self.objeto
        )

        pago.stripe_payment_intent = "pi_123"

        pago.cancelarPago(tipo="unico")

        self.assertEqual(pago.estadoPago, EstadoPago.CANCELADO)
    
    @patch("stripe.PaymentIntent.create")
    def test_aplicar_pago_unico_integracion(self, mock_stripe):
        mock_stripe.return_value = MagicMock(id="pi_123")

        pago = Pago.objects.create(
            concepto="test",
            costeFinal=100,
            usuarioFinal=self.usuarioFinal,
            objeto=self.objeto,
            content_type_id=1,
            object_id=1,
            tipoPago=TipoPago.UNICO
        )

        intent = pago.aplicarPagoUnico(self.usuarioFinal)

        self.assertEqual(intent.id, "pi_123")
        self.assertEqual(pago.stripe_payment_intent, "pi_123")
    
    @patch("stripe.PaymentIntent.retrieve")
    def test_comprobar_pago_ok(self, mock_retrieve):
        mock_retrieve.return_value = MagicMock(status="succeeded")

        pago = Pago(
            tipoPago=TipoPago.UNICO,
            stripe_payment_intent="pi_123"
        )

        self.assertTrue(pago.comprobarPago())
    
    @patch("stripe.Subscription.retrieve")
    def test_comprobar_pago_subscripcion(self, mock_retrieve):
        mock_retrieve.return_value = MagicMock(status="active")

        pago = Pago(
            tipoPago=TipoPago.ANUAL,
            stripe_subscription_id="sub_123"
        )

        self.assertTrue(pago.comprobarPago())

    def test_confirmar_pago_integracion(self):
        pago = Pago(
            concepto="test",
            estadoPago=EstadoPago.PENDIENTE
        )

        mock_objeto = MagicMock()

        with patch.object(Pago, "objeto", new_callable=PropertyMock) as mock_objeto_prop:
            mock_objeto_prop.return_value = mock_objeto

            with patch.object(pago, "save") as mock_save:
                pago.confirmarPago()

                mock_objeto.confirmarCompra.assert_called_once()
                self.assertEqual(pago.estadoPago, EstadoPago.PAGADO)
                mock_save.assert_called_once()
    
    @patch("stripe.Refund.create")
    def test_cancelar_pago_unico_integracion(self, mock_refund):
        pago = Pago(
            concepto="test",
            stripe_payment_intent="pi_123"
        )

        mock_objeto = MagicMock()

        with patch.object(Pago, "objeto", new_callable=PropertyMock) as mock_objeto_prop:
            mock_objeto_prop.return_value = mock_objeto

            with patch.object(pago, "save") as mock_save:
                pago.cancelarPago(tipo="unico")

                mock_refund.assert_called_once()
                mock_objeto.cancelarCompra.assert_called_once()
                self.assertEqual(pago.estadoPago, EstadoPago.CANCELADO)
                mock_save.assert_called_once()
    
    @patch("stripe.PaymentIntent.retrieve")
    def test_comprobar_pago_fail(self, mock_retrieve):
        mock_retrieve.return_value = MagicMock(status="failed")

        pago = Pago(
            tipoPago=TipoPago.UNICO,
            stripe_payment_intent="pi_123"
        )

        self.assertFalse(pago.comprobarPago())
    
    @patch("stripe.Subscription.create")
    def test_aplicar_subscripcion_integracion(self, mock_sub):
        mock_sub.return_value = MagicMock(id="sub_123")

        pago = Pago(
            concepto="test",
            costeFinal=50,
            usuarioFinal=self.usuarioFinal,
            tipoPago=TipoPago.MENSUAL,
            objeto=self.objeto
        )

        sub = pago.aplicarSubscripcion(self.usuarioFinal)

        self.assertEqual(sub.id, "sub_123")
        self.assertEqual(pago.stripe_subscription_id, "sub_123")
    
    @patch("django.contrib.contenttypes.models.ContentType.objects.get_for_model")
    @patch("polideportivo.models.Pago.objects.create")
    @patch("polideportivo.models.Configuracion.objects.first")
    def test_nuevo_pago_sin_descuentos(self, mock_configuracion, mock_create, mock_content_type):
        mock_configuracion.return_value = self.configuracion
        mock_content_type.return_value = MagicMock()

        self.objeto.calcularPrecio = MagicMock(return_value=100)
        self.objeto.calcularDescuento = MagicMock(return_value={})

        Pago.nuevoPago(
            concepto="test",
            usuario=self.usuarioFinal,
            tipo=TipoPago.UNICO,
            objeto=self.objeto
        )

        self.objeto.calcularPrecio.assert_called_once()
        self.objeto.calcularDescuento.assert_called_once()
    
    @patch("django.contrib.contenttypes.models.ContentType.objects.get_for_model")
    @patch("polideportivo.models.Pago.objects.create")
    @patch("polideportivo.models.Configuracion.objects.first")
    def test_nuevo_pago_respeta_porcentaje_maximo(self, mock_configuracion, mock_create, mock_content_type):

        self.objeto.calcularDescuento = MagicMock(return_value={"desc": 200})
        self.objeto.calcularPrecio = MagicMock(return_value=100)

        mock_configuracion.return_value = self.configuracion
        self.configuracion.porcentaje_maximo = 10
        mock_content_type.return_value = MagicMock()

        Pago.nuevoPago(
            concepto="test",
            usuario=self.usuarioFinal,
            tipo=TipoPago.UNICO,
            objeto=self.objeto
        )

        mock_create.assert_called_once()

        datos_pago = mock_create.call_args.kwargs
        self.assertEqual(datos_pago["descuentoAplicado"], 10)

    def test_nuevo_pago_compra_abono(self):
        abonoVerano = AbonoVerano.objects.create()
        objeto = CompraAbono.objects.create(
            abonoVerano=abonoVerano,
            usuarioFinal=self.usuarioFinal
        )

        objeto.calcularPrecio = MagicMock(return_value=120)

        Pago.nuevoPago(
            concepto="abono",
            usuario=self.usuarioFinal,
            tipo=TipoPago.UNICO,
            objeto=objeto,
            complementos={
                "forma": "mensual",
                "familiar": True
            }
        )

        objeto.calcularPrecio.assert_called_once_with(
            self.usuarioFinal,
            forma="mensual",
            familiar=True
        )

    @patch("django.contrib.contenttypes.models.ContentType.objects.get_for_model")
    @patch("polideportivo.models.Pago.objects.create")
    @patch("polideportivo.models.Configuracion.objects.first")
    def test_nuevo_pago_reserva_actividad_con_abono(
        self,
        mock_configuracion,
        mock_create,
        mock_content_type
    ):
        objeto = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad
        )

        objeto.calcularPrecio = MagicMock(return_value=100)
        objeto.calcularDescuento = MagicMock(return_value={})
        objeto.actividad.exterior = True
        objeto.id = 1

        mock_configuracion.return_value = self.configuracion
        mock_content_type.return_value = MagicMock()

        self.usuarioFinal.tieneAbono = True
        self.usuarioFinal.actividadesRealizadas = 0

        abono_deportivo = AbonoDeportivo.objects.create(descuentoPrimeraActividad=25)
        compra_abono = CompraAbono.objects.create(abonoDeportivo=abono_deportivo, usuarioFinal=self.usuarioFinal, estado=EstadoReserva.CONFIRMADA)

        Pago.nuevoPago(
            concepto="actividad",
            usuario=self.usuarioFinal,
            tipo=TipoPago.UNICO,
            objeto=objeto,
            complementos={"forma": TipoPago.MENSUAL, "familiar": False}
        )

        datos = mock_create.call_args.kwargs

        self.assertEqual(datos["descuentoAplicado"], 25)
        self.assertIn("Descuento por abono deportivo", datos["descripcionPorcentajes"])
    
    @patch("django.contrib.contenttypes.models.ContentType.objects.get_for_model")
    @patch("polideportivo.models.Pago.objects.create")
    @patch("polideportivo.models.Configuracion.objects.first")
    def test_nuevo_pago_reserva_actividad_con_abono_segunda_actividad(
        self,
        mock_configuracion,
        mock_create,
        mock_content_type
    ):
        objeto = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad
        )

        objeto.calcularPrecio = MagicMock(return_value=100)
        objeto.calcularDescuento = MagicMock(return_value={})
        objeto.actividad.exterior = True
        objeto.id = 1

        mock_configuracion.return_value = self.configuracion
        mock_content_type.return_value = MagicMock()

        self.usuarioFinal.tieneAbono = True
        self.usuarioFinal.actividadesRealizadas = 1

        abono_deportivo = AbonoDeportivo.objects.create(descuentoRestoActividades=10)
        compra_abono = CompraAbono.objects.create(abonoDeportivo=abono_deportivo, usuarioFinal=self.usuarioFinal, estado=EstadoReserva.CONFIRMADA)

        Pago.nuevoPago(
            concepto="actividad",
            usuario=self.usuarioFinal,
            tipo=TipoPago.UNICO,
            objeto=objeto,
            complementos={"forma": TipoPago.MENSUAL, "familiar": False}
        )

        datos = mock_create.call_args.kwargs

        self.assertEqual(datos["descuentoAplicado"], 10)
        self.assertIn("Descuento por abono deportivo", datos["descripcionPorcentajes"])
    
    @patch("django.contrib.contenttypes.models.ContentType.objects.get_for_model")
    @patch("polideportivo.models.Pago.objects.create")
    @patch("polideportivo.models.Configuracion.objects.first")
    def test_nuevo_pago_alquiler_con_abono(
        self,
        mock_configuracion,
        mock_create,
        mock_content_type
    ):
        objeto = Alquiler.objects.create(
            usuarioFinal=self.usuarioFinal,
            instalacion=self.instalacion,
            horaInicio=time(9,0),
            horaFin=time(11,0)
        )

        objeto.calcularPrecio = MagicMock(return_value=100)
        objeto.calcularDescuento = MagicMock(return_value={})
        objeto.id = 1

        mock_configuracion.return_value = self.configuracion
        mock_content_type.return_value = MagicMock()

        self.usuarioFinal.tieneAbono = True

        abono_deportivo = AbonoDeportivo.objects.create(descuentoAlquileres=25)
        compra_abono = CompraAbono.objects.create(abonoDeportivo=abono_deportivo, usuarioFinal=self.usuarioFinal, estado=EstadoReserva.CONFIRMADA)

        Pago.nuevoPago(
            concepto="instalacion",
            usuario=self.usuarioFinal,
            tipo=TipoPago.UNICO,
            objeto=objeto,
            complementos={"forma": TipoPago.MENSUAL, "familiar": False}
        )

        datos = mock_create.call_args.kwargs

        self.assertEqual(datos["descuentoAplicado"], 25)
        self.assertIn("Descuento por abono deportivo", datos["descripcionPorcentajes"])

    @patch("stripe.Subscription.create")
    def test_aplicar_subscripcion_primer_cuatrimestre(self, mock_create):

        mock_create.return_value = MagicMock(id="sub_1")

        self.actividad.periodo = Periodo.PRIMER_CUATRIMESTRE

        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad
        )

        pago = Pago(
            objeto=reserva,
            tipoPago=TipoPago.MENSUAL,
            concepto="actividad",
            usuarioFinal=self.usuarioFinal,
        )

        res = pago.aplicarSubscripcion(self.usuarioFinal)

        self.assertIsNotNone(res)
        mock_create.assert_called_once()
    
    @patch("stripe.Subscription.create")
    def test_aplicar_subscripcion_segundo_cuatrimestre(self, mock_create):

        mock_create.return_value = MagicMock(id="sub_2")

        self.actividad.periodo = Periodo.SEGUNDO_CUATRIMESTRE

        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad
        )

        pago = Pago(
            objeto=reserva,
            tipoPago=TipoPago.MENSUAL,
            concepto="actividad",
            usuarioFinal=self.usuarioFinal,
        )

        res = pago.aplicarSubscripcion(self.usuarioFinal)

        self.assertIsNotNone(res)
        mock_create.assert_called_once()
    
    @patch("polideportivo.models.pago.datetime")
    @patch("stripe.Subscription.create")
    def test_aplicar_subscripcion_tercer_cuatrimestre(self, mock_create, mock_datetime):
        mock_create.return_value = MagicMock(id="sub_3")

        mock_datetime.now.return_value = datetime(2025, 12, 15, tzinfo=timezone.utc)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        self.actividad.periodo = Periodo.TERCER_CUATRIMESTRE

        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad
        )

        pago = Pago(
            objeto=reserva,
            tipoPago=TipoPago.CUATRIMESTRAL,
            concepto="actividad",
            usuarioFinal=self.usuarioFinal,
        )

        res = pago.aplicarSubscripcion(self.usuarioFinal)

        self.assertIsNotNone(res)
        mock_create.assert_called_once()

    @patch("stripe.Subscription.create")
    def test_aplicar_subscripcion_anual(self, mock_create):

        mock_create.return_value = MagicMock(id="sub_123")

        self.actividad.periodo = Periodo.ANUAL

        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad
        )

        pago = Pago(
            objeto=reserva,
            tipoPago=TipoPago.ANUAL,
            concepto="actividad",
            usuarioFinal=self.usuarioFinal,
        )

        res = pago.aplicarSubscripcion(self.usuarioFinal)

        self.assertIsNotNone(res)
        mock_create.assert_called_once()
    
    @patch("stripe.Subscription.create")
    def test_aplicar_subscripcion_invalido(self, mock_create):

        mock_create.return_value = MagicMock(id="sub_123")

        self.actividad.periodo = Periodo.ANUAL

        reserva = ReservaActividad.objects.create(
            usuarioFinal=self.usuarioFinal,
            actividad=self.actividad
        )

        pago = Pago(
            objeto=reserva,
            tipoPago="invalido",
            concepto="actividad",
            usuarioFinal=self.usuarioFinal,
        )

        res = pago.aplicarSubscripcion(self.usuarioFinal)

        self.assertIsNone(res)