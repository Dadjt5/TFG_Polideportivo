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
    prioritario = models.BooleanField(default=False)
    fechaInicio = models.DateField(auto_now_add=True)
    fechaFinValidez = models.DateField(auto_now_add=True)

    tiposInstalacion = MultiSelectField(choices=TipoInstalacion.choices, max_length=512)

    deportes = models.ManyToManyField("Deporte", blank=True)

    def __str__(self):
        return f'{self.nombre} del {self.porcentaje}% para {self.tiposInstalacion}'

    @classmethod
    def contar(cls):
        return cls.objects.count()

    @classmethod
    def obtener_descuentos(cls, actividad=None, instalacion=None):
        hoy = now().date()

        if actividad:
            descuentos = cls.objects.filter(
                deportes__in=actividad.deportes.all(),
                fechaInicio__lte=hoy,
                fechaFinValidez__gte=hoy
            ).distinct()
            
            return cls._filtrar_descuentos(descuentos)

        if instalacion:
            descuentos = cls.objects.filter(
                tiposInstalacion__contains=instalacion.tipoInstalacion,
                fechaInicio__lte=hoy,
                fechaFinValidez__gte=hoy
            ).distinct()
            
            return cls._filtrar_descuentos(descuentos)

    @staticmethod
    def _filtrar_descuentos(descuentos):
        if not descuentos.exists():
            return None

        prioritarios = descuentos.filter(prioritario=True)
        if prioritarios.exists():
            descuentos = prioritarios

        combinables = descuentos.filter(combinable=True)
        no_combinable = descuentos.filter(combinable=False).order_by("-porcentaje").first()

        total_combinables = Descuento._calcular_porcentaje(combinables)

        if no_combinable and no_combinable.porcentaje >= total_combinables:
            return {
                "porcentaje_total": no_combinable.porcentaje,
                "descuentos": [no_combinable]
            }

        return {
            "porcentaje_total": total_combinables,
            "descuentos": list(combinables)
        }


    @staticmethod
    def _calcular_porcentaje(descuentos):
        porcentaje = 0

        for descuento in descuentos:
            porcentaje += descuento.porcentaje

        return porcentaje