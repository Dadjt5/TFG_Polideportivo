from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Horario(models.Model):
    """Modelo para representar el horario de una sesion o un alquiler"""
    
    horaInicio = models.TimeField(auto_now_add=True)
    horaFin = models.TimeField(auto_now_add=True)
    numeroHorasInstalacion = models.TimeField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])
    
    def __str__(self):
        return f'Horario: {self.horaInicio}-{self.horaFin}'
