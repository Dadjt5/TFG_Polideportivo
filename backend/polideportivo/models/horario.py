from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Horario(models.Model):
    """Modelo para representar el horario de una sesion o un alquiler"""

    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    numeroHoras = models.FloatField(default=0.0)

    def __str__(self):
        return f'Horario: {self.horaInicio}-{self.horaFin}'
    
    def save(self, *args, **kwargs):
        t1 = self.horaInicio.hour*3600 + self.horaInicio.minute*60 + self.horaInicio.second
        t2 = self.horaFin.hour*3600 + self.horaFin.minute*60 + self.horaFin.second
        horas = (t2-t1)/3600
        self.numeroHoras = horas
        
        super().save(*args, **kwargs)

    @property
    def valido(self):
        t1 = self.horaInicio.hour*3600 + self.horaInicio.minute*60 + self.horaInicio.second
        t2 = self.horaFin.hour*3600 + self.horaFin.minute*60 + self.horaFin.second
        
        horas = (t1-t2)/3600
        if horas > 2.0:
            return False

        return True