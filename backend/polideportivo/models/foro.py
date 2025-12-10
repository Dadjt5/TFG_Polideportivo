from django.db import models
from django.utils.translation import gettext_lazy as _

from .constantes import Tematica


class Foro(models.Model):
    """Modelo para representar el foro"""

    numeroParticipantes = models.IntegerField(default=1)

    def __str__(self):
        return f'Foro con {self.numeroParticipantes}'


class Canal(models.Model):
    """Modelo para representar un canal"""

    titulo = models.CharField(max_length=256, blank=True)
    numeroParticipantes = models.IntegerField(default=1)
    oculto = models.BooleanField(default=False)
    secreto = models.BooleanField(default=False)
    
    foro = models.ForeignKey(Foro, on_delete=models.RESTRICT)

    tema = models.CharField(default=Tematica.CHAT, choices=Tematica.choices)

    def __str__(self):
        return f'Canal para {self.titulo} con {self.numeroParticipantes} participantes'