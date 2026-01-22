from django.db import models
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Bono(models.Model):
    """Modelo para representar un bono"""

    usos = models.PositiveIntegerField(default=10)
    validez = models.PositiveIntegerField(default=1)
    precioTDA = models.FloatField(default=0.0)
    precioUAM = models.FloatField(default=0.0)
    precioAbono = models.FloatField(default=0.0)
    precioOtros = models.FloatField(default=0.0)

    instalacion = models.ForeignKey('Instalacion', on_delete=models.RESTRICT, blank=True, null=True)
    deporte = models.ForeignKey('Deporte', on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return f'Bono de {self.usos} usos en un máximo de {self.validez} años'


class CompraBono(models.Model):
    """Modelo para representar la compra de un bono"""
    
    fecha = models.DateTimeField(default=timezone.now)
    vecesUsado = models.PositiveIntegerField(default=0)
    fechaExpiracion = models.DateTimeField(blank=True, null=True)

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)
    bono = models.ForeignKey('Bono', on_delete=models.RESTRICT, related_name="compras_bono")
    pago = models.OneToOneField('Pago', on_delete=models.RESTRICT)

    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    def save(self, *args, **kwargs):
        if not self.fechaExpiracion:
            self.fechaExpiracion = self.fecha + relativedelta(
                years=self.bono.validez
            )
        super().save(*args, **kwargs)
        
    @property
    def usosRestantes(self):
        return max(0, self.bono.usos - self.vecesUsado)

    @property
    def activo(self):
        return self.fechaExpiracion > timezone.now()