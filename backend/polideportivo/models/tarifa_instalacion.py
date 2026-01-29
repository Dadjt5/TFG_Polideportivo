from django.db import models
from django.utils.translation import gettext_lazy as _

from .tarifa import Tarifa

class TarifaInstalacion(Tarifa):
    """Modelo para representar una tarifa sobre una instalacion"""

    precioAbonado = models.FloatField(default=0.0)
    precioUAM = models.FloatField(default=0.0)
    precioTDA = models.FloatField(default=0.0)
    precioOtros = models.FloatField(default=0.0)
    por_defecto = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[],
                condition=models.Q(por_defecto=True),
                name="unique_tarifa_instalacion_por_defecto"
            )
        ]

    def __str__(self):
        return f'Tarifa para una instalación, con precio para comunidad UAM de {self.precioUAM}'
