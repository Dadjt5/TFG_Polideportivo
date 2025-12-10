from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from .constantes import TipoInstalacion


class Descuento(models.Model):
    """Modelo para representar un descuento"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    porcentaje = models.FloatField(default=0.0)
    deporte = models.CharField(max_length=64, blank=True)
    combinable = models.BooleanField(default=False)
    fechaInicio = models.DateField(auto_now_add=True)
    fechFinValidez = models.DateField(auto_now_add=True)

    tiposInstalacion = MultiSelectField(choices=TipoInstalacion.choices, max_length=512)

    def __str__(self):
        return f'{self.nombre} del {self.porcentaje}% para {self.tipoInstalacion}'
