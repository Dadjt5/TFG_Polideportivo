from django.db import models
from django.utils.translation import gettext_lazy as _

from .actividad import Actividad
from .instalacion import Instalacion
from .pabellon import Pabellon
from .usuario import Usuario

class Notificacion(models.Model):
    """Modelo para representar a las notificaciones"""

    título = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    
    actividad = models.ForeignKey(Actividad, on_delete=models.RESTRICT)
    instalacion = models.ForeignKey(Instalacion, on_delete=models.RESTRICT)
    pabellon = models.ForeignKey(Pabellon, on_delete=models.RESTRICT)
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.titulo}'
