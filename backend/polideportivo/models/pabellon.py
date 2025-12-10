from django.db import models
from django.utils.translation import gettext_lazy as _

class Pabellon(models.Model):
    """Modelo para representar un pabellon"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=1024, blank=True)
    direccion = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.nombre}, localizado en {self.direccion}'
