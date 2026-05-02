from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from multiselectfield import MultiSelectField

from .constantes import TipoInstalacion


class Descuento(models.Model):
    """Modelo para representar un descuento"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    porcentaje = models.FloatField(default=0.0)
    combinable = models.BooleanField(default=False)
    prioritario = models.BooleanField(default=False)
    fechaInicio = models.DateField()
    fechaFinValidez = models.DateField()

    tiposInstalacion = MultiSelectField(choices=TipoInstalacion.choices, max_length=512)

    deportes = models.ManyToManyField("Deporte", blank=True)

    def __str__(self):
        return f'{self.nombre} del {self.porcentaje}%'

    # Función para contar el número de descuento en el sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()

    # Función para obtener todos los descuentos de una actividad o instalacion
    @classmethod
    def obtenerDescuentos(cls, actividad=None, instalacion=None):
        hoy = now().date()

        if actividad:
            descuentos = cls.objects.filter(
                Q(deportes=actividad.deportes) |
                Q(tiposInstalacion__contains=actividad.instalacion.tipoInstalacion),
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

    # Función auxiliar para extraer los descuentos de unos dados atendiendo a campos como prioritario y combinable
    @staticmethod
    def _filtrar_descuentos(descuentos):
        if not descuentos.exists():
            return None

        combinables = descuentos.filter(combinable=True)
        esPrioritarioCombinables = combinables.filter(prioritario=True).exists()

        no_combinables = descuentos.filter(combinable=False).order_by("-porcentaje")
        if no_combinables.filter(prioritario=True).exists():
            no_combinable = no_combinables.filter(prioritario=True).order_by("-porcentaje").first()
            esPrioritarioNoCombinables = True
        else:
            no_combinable = no_combinables.first()
            esPrioritarioNoCombinables = False
        
        total_combinables = Descuento._calcular_porcentaje(combinables)

        if no_combinable and no_combinable.porcentaje >= total_combinables:
            # En caso de que el no combinable sea mayor revisamos con cuidado que la prioridad sea igual o mayor
            if esPrioritarioCombinables and esPrioritarioNoCombinables or not esPrioritarioCombinables:
                return {
                    "porcentaje_total": no_combinable.porcentaje,
                    "descuentos": [no_combinable]
                }

        return {
            "porcentaje_total": total_combinables,
            "descuentos": list(combinables)
        }

    # Función auxiliar para calcular el total del porcentaje dada una lista de porcentajes
    @staticmethod
    def _calcular_porcentaje(descuentos):
        porcentaje = 0

        for descuento in descuentos:
            porcentaje += descuento.porcentaje

        return porcentaje