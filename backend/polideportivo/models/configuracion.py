from django.db import models
from django.utils.translation import gettext_lazy as _


class Configuracion(models.Model):
    """Modelo para representar la configuracion interna de la aplicacion"""
    
    max_deportes_por_usuario = models.PositiveIntegerField(default=5)
    max_horas_alquiler = models.PositiveIntegerField(default=120)  # minutos
    otro_parametro = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciones"

    def save(self, *args, **kwargs):
        """Obligamos a que solo haya una configuracion"""
        if not self.pk and Configuracion.objects.exists():
            raise ValueError("Solo puede existir una configuración")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Configuración global de la aplicación"
