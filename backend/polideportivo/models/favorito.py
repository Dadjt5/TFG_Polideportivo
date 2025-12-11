from django.db import models
from django.utils.translation import gettext_lazy as _
import math

from .instalacion import Instalacion
from .actividad import Actividad
from .usuario_final import UsuarioFinal


class Favorito(models.Model):
    """Modelo para representar las instalaciones y actividades marcadas como favoritas por un usuario final"""

    usuario = models.ForeignKey(UsuarioFinal, on_delete=models.RESTRICT)    
    actividad = models.ForeignKey(Actividad, on_delete=models.RESTRICT, null=True)
    instalacion = models.ForeignKey(Instalacion, on_delete=models.RESTRICT, null=True)

    class Meta:
        unique_together = ('usuario', 'actividad', 'instalacion')
        
    def __str__(self):
        if self.actividad:
            return f"{self.usuario} tiene como actividad favorita: {self.actividad}"
        elif self.instalacion:
            return f"{self.usuario} tiene como instalación favorita: {self.instalacion}"
        return f"{self.usuario} sin favoritos"
