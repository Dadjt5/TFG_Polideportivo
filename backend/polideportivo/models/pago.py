from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .abono import CompraAbono
from .bono import CompraBono
from .reserva import ReservaActividad
from .constantes import EstadoPago


class Pago(models.Model):
    """Modelo para representar el pago"""

    concepto = models.CharField(max_length=256, blank=True)
    coste = models.FloatField(default=0.0)
    costeFinal = models.FloatField(default=0.0)
    descuentoAplicado = models.FloatField(default=0.0)
    fecha = models.DateField(auto_now_add=True)
    
    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)

    estadoPago = models.CharField(default=EstadoPago.PENDIENTE, choices=EstadoPago.choices)
    
    stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True)

    # Relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    objeto = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f'Pago {self.concepto}, de coste {self.coste} en estado {self.estadoPago}'
    
    def confirmarPago(self):
        if not self.objeto.confirmarCompra():
            return False

        self.estado = EstadoPago.PAGADO
        self.save()
        return True
    
    def cancelarPago(self):
        if not self.objeto.cancelarCompra():
            return False

        self.estado = EstadoPago.CANCELADO
        self.save()
        return True

    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    @classmethod
    def nuevoPago(cls, concepto, usuario, objeto, complementos=None):
        porcentaje = 0
        if not isinstance(objeto, (CompraBono, CompraAbono)):
            porcentaje = objeto.calcularDescuento()

        if isinstance(objeto, CompraAbono):
            coste = objeto.calcular_precio(
                usuario,
                forma=complementos["forma"],
                familiar=complementos["familiar"]
            )

        elif isinstance(objeto, ReservaActividad):
            coste = objeto.calcular_precio(
                usuario,
                numeroHorasSemana=complementos["numeroHorasSemana"],
                numeroPersonas=complementos["numeroPersonas"],
                tipoPago=complementos["tipoPago"],
                tipoSesion=complementos["tipoSesion"]
            )
        else:
            coste = objeto.calcular_precio(usuario)

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
            usuarioFinal=usuario
        )