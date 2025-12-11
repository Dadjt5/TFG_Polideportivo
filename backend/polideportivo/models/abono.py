from django.db import models
from django.utils.translation import gettext_lazy as _

from .usuario_final import UsuarioFinal


class Abono(models.Model):
    """Modelo para representar un abono (clase abstracta)"""

    UsuarioFinal = models.ForeignKey(UsuarioFinal, on_delete=models.RESTRICT)

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
    fechaInicio = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Abono deportivo de {self.meses} que comienza el {self.fechaInicio}'


class AbonoVerano(Abono):
    """Modelo para representar un abono de verano"""

    precioTDA = models.FloatField(default=0.0)
    precioUAM = models.FloatField(default=0.0)
    precioOtros = models.FloatField(default=0.0)


    def __str__(self):
        return f'Abono de verano para junio, julio y agosto de coste {self.precioUAM} para la comunidad UAM'