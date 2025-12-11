from django.db import models
from django.utils.translation import gettext_lazy as _

from .pabellon import Pabellon
from .constantes import TipoInstalacion

class Instalacion(models.Model):
    """Modelo para representar una instalacion"""

    nombre = models.CharField(max_length=256, blank=True)
    imagenURL = models.CharField(max_length=2048, blank=True)
    aforoMaximo = models.PositiveIntegerField(default=50)
    luz = models.BooleanField(default=False)
    porcentajeTDA = models.FloatField(default=0.0)
    
    pabellon = models.ForeignKey(Pabellon, on_delete=models.RESTRICT)
    
    tipoInstalacion = models.CharField(default=TipoInstalacion.SALA_MULTIUSOS, choices=TipoInstalacion.choices)

    def __str__(self):
        return f'{self.nombre}, ubicado en el {self.pabellon}'
