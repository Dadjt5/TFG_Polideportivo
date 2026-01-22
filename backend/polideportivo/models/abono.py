from django.db import models
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import datetime


class Abono(models.Model):
    """Modelo para representar un abono (clase abstracta)"""

    class Meta:
        abstract = True


class AbonoDeportivo(Abono):
    """Modelo para representar un abono deportivo"""

    meses = models.PositiveIntegerField(default=1)
    descuentoPrimeraActividad = models.FloatField(default=0.0)
    descuentoRestoActividades = models.FloatField(default=0.0)
    descuentoActividadesExteriores = models.FloatField(default=0.0)
    precioTotalMensual = models.FloatField(default=0.0)
    precioPagoUnicoUAM = models.FloatField(default=0.0)
    precioFamiliar = models.FloatField(default=0.0)
    precioTotalMensualOtros = models.FloatField(default=0.0)
    precioPagoUnicoOtros = models.FloatField(default=0.0)

    def __str__(self):
        return f'Abono deportivo de {self.meses} que comienza el {self.fechaInicio}'


class AbonoVerano(Abono):
    """Modelo para representar un abono de verano"""
    precioTDA = models.FloatField(default=0.0)
    precioUAM = models.FloatField(default=0.0)
    precioOtros = models.FloatField(default=0.0)
    
    def __str__(self):
        return f'Abono de verano para junio, julio y agosto de coste {self.precioUAM} para la comunidad UAM'


class CompraAbono(models.Model):
    """Modelo para representar la compra de un abono"""
    
    fecha = models.DateTimeField(default=timezone.now)

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT, related_name="abono")
    abonoDeportivo = models.ForeignKey('AbonoDeportivo', on_delete=models.RESTRICT, related_name="compras_deportivo", blank=True, null=True)
    abonoVerano = models.ForeignKey('AbonoVerano', on_delete=models.RESTRICT, related_name="compras_verano", blank=True, null=True)
    pago = models.OneToOneField('Pago', on_delete=models.RESTRICT)

    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    @property
    def fechaInicio(self):
        if self.abonoDeportivo:
            return self.fecha

        if self.abonoVerano:
            year = timezone.now().year
            return timezone.make_aware(datetime(year, 6, 1))

        return None
    
    @property
    def fechaExpiracion(self):
        if self.abonoDeportivo:
            return self.fechaInicio + relativedelta(
                months=self.abonoDeportivo.meses
            )

        if self.abonoVerano:
            year = timezone.now().year
            return timezone.make_aware(datetime(year, 8, 31, 23, 59, 59))

        return None

    @property
    def diasRestantes(self):
        fechaExpiracion = self.fechaExpiracion
        if not fechaExpiracion:
            return 0

        dias = (fechaExpiracion.date() - timezone.now().date()).days
        return max(0, dias)
    
    @property
    def valido(self):
        return self.diasRestantes > 0