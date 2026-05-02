from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta, datetime, date
from django.utils import timezone
import stripe
from django.conf import settings

from .abono import CompraAbono
from .bono import CompraBono
from .reserva import ReservaActividad, Alquiler
from .tda import TDA
from .configuracion import Configuracion
from .constantes import EstadoPago, TipoPago, Periodo, EstadoReserva


stripe.api_key = settings.STRIPE_SECRET_KEY

class Pago(models.Model):
    """Modelo para representar el pago"""

    concepto = models.CharField(max_length=256, blank=True)
    coste = models.FloatField(default=0.0)
    costeFinal = models.FloatField(default=0.0)
    descuentoAplicado = models.FloatField(default=0.0)
    fecha = models.DateField(auto_now_add=True)

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.CASCADE)

    estadoPago = models.CharField(default=EstadoPago.PENDIENTE, choices=EstadoPago.choices)
    tipoPago = models.CharField(default=TipoPago.UNICO, choices=TipoPago.choices)
    
    stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)

    descripcionPorcentajes = models.JSONField(default=dict, blank=True)

    # Relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="pago")
    object_id = models.PositiveIntegerField()
    objeto = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f'Pago {self.concepto}, de coste {self.coste} en estado {self.estadoPago}'
    
    # Función para confirmar un pago
    def confirmarPago(self):
        self.objeto.confirmarCompra()
        self.estadoPago = EstadoPago.PAGADO
        self.save()
        return True
    
    # Función para cancelar un pago
    def cancelarPago(self, tipo="unico"):
        if tipo == "unico":
            refund = stripe.Refund.create(payment_intent=self.stripe_payment_intent)
        elif tipo == "subscripcion":
            if self.stripe_subscription_id:
                stripe.Subscription.delete(self.stripe_subscription_id)
        
        self.objeto.cancelarCompra()
        self.estadoPago = EstadoPago.CANCELADO
        self.stripe_payment_intent = None
        self.stripe_price_id = None
        self.stripe_subscription_id = None
        self.save()
        return True

    # Función para contar el número de pagos del sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()

    # Función para contar el dinero total conseguido
    @classmethod
    def contarDinero(cls):
        return cls.objects.filter(
            estadoPago=EstadoPago.PAGADO
        ).aggregate(total=models.Sum('costeFinal'))['total'] or 0

    # Función para crear nuevos pagos
    @classmethod
    def nuevoPago(cls, concepto, usuario, tipo, objeto, complementos=None):
        porcentaje = 0
        descripcionPorcentajes = {}

        if not isinstance(objeto, (CompraBono, CompraAbono, TDA)):
            infoDescuento = objeto.calcularDescuento()

            for nombre, porcent in infoDescuento.items():
                descripcionPorcentajes[nombre] = porcent
                porcentaje += porcent

        if isinstance(objeto, CompraAbono):
            coste = objeto.calcularPrecio(
                usuario,
                forma=complementos["forma"],
                familiar=complementos["familiar"]
            )

        elif isinstance(objeto, ReservaActividad):
            numeroSesiones = ReservaActividad.objects.filter(actividad=objeto.actividad, usuarioFinal=usuario).exclude(tipoSesion="consulta").count()
            coste = objeto.calcularPrecio(numeroSesiones)
            porcentajeExtra = 0.0

            if usuario.tieneAbono:
                compraAbono = usuario.abono.filter(abonoVerano__isnull=True, estado=EstadoReserva.CONFIRMADA).first()
                if compraAbono and compraAbono.abonoDeportivo:
                    descripcionPorcentajes["Descuento por abono deportivo"] = {}
                    if usuario.actividadesRealizadas == 0:
                        porcentajeExtra += compraAbono.abonoDeportivo.descuentoPrimeraActividad
                        if porcentajeExtra > 0.0:
                            descripcionPorcentajes["Descuento por abono deportivo"]["Primera actividad"] = porcentajeExtra
                    else:
                        porcentajeExtra += compraAbono.abonoDeportivo.descuentoRestoActividades
                        if porcentajeExtra > 0.0:
                            descripcionPorcentajes["Descuento por abono deportivo"]["Inscripcion en actividad"] = porcentajeExtra

                    if objeto.actividad.exterior:
                        porcentajeExtra += compraAbono.abonoDeportivo.descuentoActividadesExteriores
                        if porcentajeExtra > 0.0:
                            descripcionPorcentajes["Descuento por abono deportivo"]["Actividad en exteriores"] = porcentajeExtra
            
            porcentaje += porcentajeExtra

        elif isinstance(objeto, Alquiler):
            coste = objeto.calcularPrecio()
            porcentajeExtra = 0.0

            if usuario.tieneAbono:
                compraAbono = usuario.abono.filter(abonoVerano__isnull=True, estado=EstadoReserva.CONFIRMADA).first()

                if compraAbono and compraAbono.abonoDeportivo:
                    descripcionPorcentajes["Descuento por abono deportivo"] = {}

                    porcentajeExtra += compraAbono.abonoDeportivo.descuentoAlquileres
                    if porcentajeExtra > 0.0:
                            descripcionPorcentajes["Descuento por abono deportivo"]["Alquiler instalaciones"] = porcentajeExtra
                
            porcentaje += porcentajeExtra

        else:
            coste = objeto.calcularPrecio()

        config = Configuracion.objects.first()
        porcentaje = min(porcentaje, config.porcentaje_maximo)

        costeFinal = coste - (coste * porcentaje / 100)
        content_type = ContentType.objects.get_for_model(objeto)

        return cls.objects.create(
            concepto=concepto,
            coste=coste,
            costeFinal=costeFinal,
            descuentoAplicado=porcentaje,
            estadoPago=EstadoPago.PENDIENTE,
            content_type=content_type,
            object_id=objeto.id,
            tipoPago=tipo,
            usuarioFinal=usuario,
            descripcionPorcentajes=descripcionPorcentajes
        )
    
    # Función para comprobar si el pago se ha realizado en stripe
    def comprobarPago(self):
        if self.tipoPago == TipoPago.UNICO:
            intent = stripe.PaymentIntent.retrieve(self.stripe_payment_intent)

            if intent.status == "succeeded":
                return True
        else:
            subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)

            if subscription.status in ["active", "trialing"]:
                return True
        
        return False

    # Función para aplicar un pago único en stripe
    def aplicarPagoUnico(self, usuario):
        intent = stripe.PaymentIntent.create(
            amount=int(self.costeFinal * 100), # En centimos
            currency="eur",
            metadata={
                "pago_id": self.id,
                "usuario_id": usuario.id
            }
        )

        self.stripe_payment_intent = intent.id
        self.save()

        return intent

    # Función para aplicar una subcscripción en stripe
    def aplicarSubscripcion(self, usuario):
        hoy = datetime.now(timezone.utc)

        if isinstance(self.objeto, ReservaActividad):
            año = hoy.year

            # Los pagos de actividades comienzan y finalizan mientras se desarrolla la actividad
            if self.objeto.actividad.periodo == Periodo.PRIMER_CUATRIMESTRE:
                inicio = datetime(año, 9, 1, tzinfo=timezone.utc)
                fin = datetime(año + 1, 1, 31, tzinfo=timezone.utc)
            elif self.objeto.actividad.periodo == Periodo.SEGUNDO_CUATRIMESTRE:
                inicio = datetime(año, 2, 1, tzinfo=timezone.utc)
                fin = datetime(año, 5, 31, tzinfo=timezone.utc)
            elif self.objeto.actividad.periodo == Periodo.TERCER_CUATRIMESTRE:
                inicio = datetime(año, 6, 1, tzinfo=timezone.utc)
                fin = datetime(año, 8, 31, tzinfo=timezone.utc)
            elif self.objeto.actividad.periodo == Periodo.ANUAL:
                inicio = datetime(año, 1, 1, tzinfo=timezone.utc)
                fin = datetime(año, 12, 31, tzinfo=timezone.utc)
        else:
            # Si no es actividad empieza día 1 del mes siguiente al actual
            if hoy.month == 12:
                inicio = datetime(hoy.year + 1, 1, 1, tzinfo=timezone.utc)
            else:
                inicio = datetime(hoy.year, hoy.month + 1, 1, tzinfo=timezone.utc)

            fin = None

        inicio_ts = int(inicio.timestamp())

        if self.tipoPago == TipoPago.MENSUAL:
            tipo = "month"
            intervalo = 1
        elif self.tipoPago == TipoPago.CUATRIMESTRAL:
            tipo = "month"
            intervalo = 4
        elif self.tipoPago == TipoPago.ANUAL:
            tipo = "year"
            intervalo = 1
        else:
            return None

        if not usuario.stripe_customer_id:
            customer = stripe.Customer.create(email=usuario.user.email)
            usuario.stripe_customer_id = customer.id
            usuario.save()

        if not self.stripe_price_id:
            precio = stripe.Price.create(
                unit_amount=int(self.costeFinal * 100),
                currency="eur",
                recurring={"interval": tipo, "interval_count": intervalo},
                product_data={"name": self.concepto}
            )
            self.stripe_price_id = precio.id
            self.save()

        subscription_data = {
            "customer": usuario.stripe_customer_id,
            "items": [{"price": self.stripe_price_id}],
            "payment_behavior": "default_incomplete",
            "collection_method": "charge_automatically",
            "payment_settings": {
                "save_default_payment_method": "on_subscription"
            },
            "proration_behavior": "create_prorations",
            "expand": ["latest_invoice.confirmation_secret"],
        }

        # Esto esta pensado para cuando las TDAs eran de pago anual y no unico, para manejar que solo las reservas de actividades comiencen a principio de mes
        if isinstance(self.objeto, ReservaActividad):
            subscription_data["billing_cycle_anchor"] = inicio_ts
            subscription_data["trial_end"] = inicio_ts

        if fin:
            subscription_data["cancel_at"] = int(fin.timestamp())

        subscription = stripe.Subscription.create(**subscription_data)

        self.stripe_subscription_id = subscription.id
        self.save()

        return subscription