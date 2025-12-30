from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import time

class Agenda(models.Model):
    """Modelo para representar la agenda de las instalaciones"""

    fecha = models.DateField()
    horaApertura = models.TimeField(default=time(8, 0))
    horaCierre = models.TimeField(default=time(20, 0))
    abierto = models.BooleanField(default=True)
    
    instalacion = models.ForeignKey('Instalacion', related_name="agenda", on_delete=models.RESTRICT)

    class Meta:
        unique_together = ('fecha', 'instalacion')

    def __str__(self):
        return f'Agenda para el día {self.fecha} para la instalacion: {self.instalacion.nombre}'
