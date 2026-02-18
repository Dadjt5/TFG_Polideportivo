from django.db import models
from django.utils.translation import gettext_lazy as _

from .constantes import EstadoPago


class Pago(models.Model):
    """Modelo para representar el pago"""

    concepto = models.CharField(max_length=256, blank=True)
    coste = models.FloatField(default=0.0)
    fecha = models.DateField(auto_now_add=True)

    estadoPago = models.CharField(default=EstadoPago.PENDIENTE, choices=EstadoPago.choices)
    
    reservaActividad = models.OneToOneField("ReservaActividad", on_delete=models.CASCADE, null=True, blank=True)
    alquiler = models.OneToOneField("Alquiler", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Pago {self.concepto}, de coste {self.coste} en estado {self.estadoPago}'

    @classmethod
    def contar(cls):
        return cls.objects.count()