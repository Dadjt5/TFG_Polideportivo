from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Notificacion(models.Model):
    """Modelo para representar una notificacion"""

    titulo = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    leido = models.BooleanField(default=False)

    actividad = models.ForeignKey('Actividad', on_delete=models.RESTRICT, blank=True, null=True)
    instalacion = models.ForeignKey('Instalacion', on_delete=models.RESTRICT, blank=True, null=True)
    pabellon = models.ForeignKey('Pabellon', on_delete=models.RESTRICT, blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.titulo}'

    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    @classmethod
    def contar_no_leidas(cls, usuario):
        return cls.objects.filter(usuario=usuario, leido=False).count()