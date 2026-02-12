from django.db import models
from django.utils.translation import gettext_lazy as _


class Tarifa(models.Model):
    """Modelo para representar la clase abstracta tarifa"""

    titulo = models.CharField(max_length=256, blank=True)

    class Meta:
        abstract = True


class TarifaTDA(Tarifa):
    """Modelo para representar una tarifa para la TDA"""
    
    precioUAM = models.FloatField(default=0.0)
    precioOtros = models.FloatField(default=0.0)
    precioReposicion = models.FloatField(default=0.0)
    por_defecto = models.BooleanField(default=False)

    def __str__(self):
        return f'Tarifa para TDA de precio: {self.precioUAM} para comunidad UAM y precio {self.precioOtros} para externos'