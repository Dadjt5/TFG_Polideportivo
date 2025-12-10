from django.db import models
from django.utils.translation import gettext_lazy as _

from .reserva import Reserva
from .abono import Abono
from .bono import Bono
from .constantes import EstadoPago


class Pago(models.Model):
    """Modelo para representar el pago"""

    concepto = models.CharField(max_length=256, blank=True)
    coste = models.FloatField(default=0.0)
    fecha = models.DateField(auto_now_add=True)
    
    reserva = models.OneToOneField(Reserva, null=True, blank=True)
    abono = models.OneToOneField(Abono, null=True, blank=True)
    bono = models.OneToOneField(Bono, null=True, blank=True)
    
    estadoPago = models.CharField(default=EstadoPago.OTROS, choices=EstadoPago.choices)

    def __str__(self):
        return f'Pago {self.concepto}, de coste {self.coste} en estado {self.estadoPago}'
