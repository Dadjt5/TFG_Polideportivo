from django.db import models
from django.utils.translation import gettext_lazy as _

from .constantes import EstadoPago


class Pago(models.Model):
    """Modelo para representar el pago"""

    concepto = models.CharField(max_length=256, blank=True)
    coste = models.FloatField(default=0.0)
    costeFinal = models.FloatField(default=0.0)
    descuentoAplicado = models.FloatField(default=0.0)
    fecha = models.DateField(auto_now_add=True)

    estadoPago = models.CharField(default=EstadoPago.PENDIENTE, choices=EstadoPago.choices)
    
    reservaActividad = models.OneToOneField("ReservaActividad", on_delete=models.CASCADE, null=True, blank=True, related_name="pago")
    alquiler = models.OneToOneField("Alquiler", on_delete=models.CASCADE, null=True, blank=True, related_name="pago")

    def __str__(self):
        return f'Pago {self.concepto}, de coste {self.coste} en estado {self.estadoPago}'

    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    @classmethod
    def nuevoPago(cls, concepto, usuario, reservaActividad=None, alquiler=None):
        if reservaActividad:
            porcentaje = reservaActividad.calcularDescuento()
            coste = reservaActividad.actividad.calcular_precio(usuario)

            costeFinal = coste - (coste*porcentaje/100)

            pago = cls.objects.create(concepto=concepto, coste=coste, costeFinal=costeFinal, descuentoAplicado=porcentaje, estadoPago=EstadoPago.PENDIENTE, reservaActividad=reservaActividad)
            return pago

        if alquiler:
            porcentaje = alquiler.calcularDescuento()
            coste = alquiler.instalacion.calcular_precio(usuario)

            costeFinal = coste - (coste*porcentaje/100)

            pago = cls.objects.create(concepto=concepto, coste=coste, costeFinal=costeFinal, descuentoAplicado=porcentaje, estadoPago=EstadoPago.PENDIENTE, alquiler=alquiler)
            return pago

        return None