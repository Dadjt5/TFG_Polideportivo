from django.db import models
from django.utils.translation import gettext_lazy as _

from .usuario_final import UsuarioFinal


class TDA(models.Model):
    """Modelo para representar una actividad"""

    fechaInicio = models.DateField(auto_now_add=True)
    fechaExpiracion = models.DateField()
    enRegla = models.BooleanField(default=False)
    
    usuarioFinal = models.ForeignKey(UsuarioFinal, on_delete=models.RESTRICT, related_name="tda", null=True)

    def __str__(self):
        return f'Tarjeta deportiva anual con fecha de inicio: {self.fechaInicio} y fecha de expiracion: {self.fechaExpiracion}'

    @classmethod
    def contar(cls):
        return cls.objects.count()