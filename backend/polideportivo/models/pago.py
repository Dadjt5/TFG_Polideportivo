from django.db import models
from django.utils.translation import gettext_lazy as _


from .constantes import EstadoPago


class Pago(models.Model):
    """Modelo para representar el pago"""

    concepto = models.CharField(max_length=256, blank=True)
    coste = models.FloatField(default=0.0)
    fecha = models.DateField(auto_now_add=True)

    reservaActividad = models.OneToOneField('ReservaActividad', on_delete=models.RESTRICT, null=True, blank=True)
    alquiler = models.OneToOneField('alquiler', on_delete=models.RESTRICT, null=True, blank=True)
    abonoDeportivo = models.OneToOneField('AbonoDeportivo', on_delete=models.RESTRICT, null=True, blank=True)
    abonoVerano = models.OneToOneField('AbonoVerano', on_delete=models.RESTRICT, null=True, blank=True)
    bono = models.OneToOneField('Bono', on_delete=models.RESTRICT, null=True, blank=True)

    estadoPago = models.CharField(default=EstadoPago.PENDIENTE, choices=EstadoPago.choices)

    def __str__(self):
        return f'Pago {self.concepto}, de coste {self.coste} en estado {self.estadoPago}'
