from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta, datetime
from django.utils import timezone
import stripe
from django.conf import settings

from .abono import CompraAbono
from .bono import CompraBono
from .reserva import ReservaActividad
from .tda import TDA
from .configuracion import Configuracion
from .constantes import EstadoPago, TipoPago

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

    # Relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="pago")
    object_id = models.PositiveIntegerField()
    objeto = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f'Pago {self.concepto}, de coste {self.coste} en estado {self.estadoPago}'
    
    def confirmarPago(self):
        self.objeto.confirmarCompra()
        self.estadoPago = EstadoPago.PAGADO
        self.save()
        return True
    
    def cancelarPago(self):
        self.objeto.cancelarCompra()
        self.estadoPago = EstadoPago.CANCELADO
        self.stripe_payment_intent = None
        self.stripe_price_id = None
        self.stripe_subscription_id = None
        self.save()
        return True

    @classmethod
    def contar(cls):
        return cls.objects.count()

    @classmethod
    def contarDinero(cls):
        return cls.objects.filter(
            estadoPago=EstadoPago.PAGADO
        ).aggregate(total=models.Sum('costeFinal'))['total'] or 0

    @classmethod
    def nuevoPago(cls, concepto, usuario, tipo, objeto, complementos=None):
        porcentaje = 0
        if not isinstance(objeto, (CompraBono, CompraAbono, TDA)):
            porcentaje = objeto.calcularDescuento()

        if isinstance(objeto, CompraAbono):
            coste = objeto.calcular_precio(
                usuario,
                forma=complementos["forma"],
                familiar=complementos["familiar"]
            )

        elif isinstance(objeto, ReservaActividad):
            coste = objeto.calcular_precio()

            if usuario.tieneAbono:
                compraAbono = usuario.abono.filter(abonoVerano=None).first()

                if compraAbono and compraAbono.abonoDeportivo:
                    if usuario.actividadesRealizadas == 0:
                        porcentaje += compraAbono.abonoDeportivo.descuentoPrimeraActividad
                    else:
                        porcentaje += compraAbono.abonoDeportivo.descuentoRestoActividades
                    
                    if objeto.actividad.exterior:
                        porcentaje += compraAbono.abonoDeportivo.descuentoActividadesExteriores

        else:
            coste = objeto.calcular_precio()

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
            usuarioFinal=usuario
        )
    
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

    def aplicarSubscripcion(self, usuario):
        hoy = datetime.now(timezone.utc)
        if hoy.month == 12:
            primer_dia_mes = datetime(hoy.year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            primer_dia_mes = datetime(hoy.year, hoy.month + 1, 1, tzinfo=timezone.utc)

        primer_dia_mes_timestamp = int(primer_dia_mes.timestamp())

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

        # Crear customer
        if not usuario.stripe_customer_id:
            customer = stripe.Customer.create(
                email=usuario.user.email
            )
            usuario.stripe_customer_id = customer.id
            usuario.save()

        # Crear precio
        if not self.stripe_price_id:
            precio = stripe.Price.create(
                unit_amount=int(self.costeFinal * 100),
                currency="eur",
                recurring={"interval": tipo, "interval_count": intervalo},
                product_data={
                    "name": self.concepto
                }
            )
            self.stripe_price_id = precio.id
            self.save()

        # Crear suscripción
        subscription = stripe.Subscription.create(
            customer=usuario.stripe_customer_id,
            items=[{
                "price": self.stripe_price_id
            }],
            payment_behavior="default_incomplete",
            collection_method="charge_automatically",
            payment_settings={
                "save_default_payment_method": "on_subscription"
            },
            expand=["latest_invoice.confirmation_secret"],
        )

        self.stripe_subscription_id = subscription.id
        self.save()

        return subscription