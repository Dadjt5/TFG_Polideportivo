from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Notificacion(models.Model):
    """Modelo para representar una notificacion"""

    título = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)

    actividad = models.ForeignKey('Actividad', on_delete=models.RESTRICT)
    instalacion = models.ForeignKey('Instalacion', on_delete=models.RESTRICT)
    pabellon = models.ForeignKey('Pabellon', on_delete=models.RESTRICT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.titulo}'

    @classmethod
    def contar(cls):
        return cls.objects.count()