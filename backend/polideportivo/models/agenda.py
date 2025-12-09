from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import time

from .instalacion import Instalacion

class Instalacion(models.Model):
    """Modelo para representar las agendas de las instalaciones"""

    fecha = models.DateField(auto_now_add=True)
    horaApertura = models.TimeField(default=time(8, 0))
    horaCierre = models.TimeField(default=time(20, 0))
    abierto = models.BooleanField(default=True)
    
    instalacion = models.ForeignKey(Instalacion, on_delete=models.RESTRICT)

    def __str__(self):
        return f''
