from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from .constantes import TipoInstalacion


class Descuento(models.Model):
    """Modelo para representar un descuento"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    porcentaje = models.FloatField(default=0.0)
    combinable = models.BooleanField(default=False)
    fechaInicio = models.DateField(auto_now_add=True)
    fechFinValidez = models.DateField(auto_now_add=True)

    tiposInstalacion = MultiSelectField(choices=TipoInstalacion.choices, max_length=512)
    
    deporte = models.ForeignKey("Deporte", on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} del {self.porcentaje}% para {self.tiposInstalacion}'

    @classmethod
    def contar(cls):
        return cls.objects.count()

    def obtener_descuentos(cls, actividad):
        hoy = now().date()

        return cls.objects.filter(
            deportes__in=actividad.deportes.all(),
            fechaInicio__lte=hoy,
            fechaFinValidez__gte=hoy
        ).distinct()