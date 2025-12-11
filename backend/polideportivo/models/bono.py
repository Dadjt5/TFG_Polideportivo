from django.db import models
from django.utils.translation import gettext_lazy as _

from .usuario_final import UsuarioFinal
from .constantes import TipoBono


class Bono(models.Model):
    """Modelo para representar un bono"""

    usos = models.PositiveIntegerField(default=10)
    añosValidez = models.PositiveIntegerField(default=1)
    precioTDA = models.FloatField(default=0.0)
    precioUAM = models.FloatField(default=0.0)
    precioAbono = models.FloatField(default=0.0)
    precioOtros = models.FloatField(default=0.0)
    
    UsuarioFinal = models.ForeignKey(UsuarioFinal, on_delete=models.RESTRICT)
    tipoBono = models.CharField(default=TipoBono.PISCINA, choices=TipoBono.choices)

    def __str__(self):
        return f'Bono para {self.tipoBono} de {self.usos} usos en un máximo de {self.añosValidez} años'
