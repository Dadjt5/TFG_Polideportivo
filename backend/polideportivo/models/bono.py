from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .constantes import EstadoReserva


class Bono(models.Model):
    """Modelo para representar un bono"""

    usos = models.PositiveIntegerField(default=10)
    validez = models.PositiveIntegerField(default=1)
    precioTDA = models.FloatField(default=0.0)
    precioUAM = models.FloatField(default=0.0)
    precioAbono = models.FloatField(default=0.0)
    precioOtros = models.FloatField(default=0.0)

    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Bono de {self.usos} usos en un máximo de {self.validez} años'


class CompraBono(models.Model):
    """Modelo para representar la compra de un bono"""

    fecha = models.DateTimeField(default=timezone.now)
    vecesUsado = models.PositiveIntegerField(default=0)
    fechaExpiracion = models.DateTimeField(blank=True, null=True)

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)
    bono = models.ForeignKey('Bono', on_delete=models.RESTRICT, related_name="compras_bono")

    estado = models.CharField(default=EstadoReserva.PENDIENTE, choices=EstadoReserva.choices)

    @classmethod
    def contar(cls):
        return cls.objects.count()

    @classmethod
    def compraBono(cls, bono, usuario):
        with transaction.atomic():
            bono.refresh_from_db()

            if cls.objects.filter(usuarioFinal=usuario, bono=bono, estado=EstadoReserva.CONFIRMADA).exists():
                return None

            for comBono in cls.objects.filter(usuarioFinal=usuario, bono=bono, estado=EstadoReserva.PENDIENTE):
                comBono.cancelarCompra()

            compra = cls.objects.create(
                usuarioFinal=usuario,
                bono=bono,
                estado=EstadoReserva.PENDIENTE
            )

            compra.fechaExpiracion = compra.fecha + relativedelta(years=bono.validez)
            compra.save()

            return compra
    
    def calcular_precio(self):
        precio = self.bono.precioOtros
        if self.usuarioFinal.tieneAbono:
            precio = self.bono.precioAbono
        elif self.usuarioFinal.esUAM:
            precio = self.bono.precioUAM
        elif self.usuarioFinal.tieneTDA:
            precio = self.bono.precioTDA

        return precio
    
    def confirmarCompra(self):
        self.estado = EstadoReserva.CONFIRMADA
        self.save()
    
    def cancelarCompra(self):
        self.estado = EstadoReserva.CANCELADO
        self.save()

    @property
    def usosRestantes(self):
        return max(0, self.bono.usos - self.vecesUsado)

    @property
    def activo(self):
        return self.fechaExpiracion > timezone.now()