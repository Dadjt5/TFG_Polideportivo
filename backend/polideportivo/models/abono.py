from django.db import models
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.utils import timezone
from datetime import datetime

from .constantes import EstadoReserva, TipoPago


class Abono(models.Model):
    """Modelo para representar un abono (clase abstracta)"""
    nombre = models.CharField(max_length=256)

    class Meta:
        abstract = True


class AbonoDeportivo(Abono):
    """Modelo para representar un abono deportivo"""

    meses = models.PositiveIntegerField(default=1)
    descuentoPrimeraActividad = models.FloatField(default=0.0)
    descuentoRestoActividades = models.FloatField(default=0.0)
    descuentoActividadesExteriores = models.FloatField(default=0.0)
    descuentoAlquileres = models.FloatField(default=0.0)
    precioTotalMensual = models.FloatField(default=0.0)
    precioPagoUnicoUAM = models.FloatField(default=0.0)
    precioFamiliar = models.FloatField(default=0.0)
    precioTotalMensualOtros = models.FloatField(default=0.0)
    precioPagoUnicoOtros = models.FloatField(default=0.0)
    fechaInicio = models.DateField(auto_now=True)

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

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.CASCADE, related_name="abono", null=True, blank=True)
    abonoDeportivo = models.ForeignKey('AbonoDeportivo', on_delete=models.RESTRICT, related_name="compras_deportivo", blank=True, null=True)
    abonoVerano = models.ForeignKey('AbonoVerano', on_delete=models.RESTRICT, related_name="compras_verano", blank=True, null=True)

    estado = models.CharField(default=EstadoReserva.PENDIENTE, choices=EstadoReserva.choices)

    # Función de la clase para contar el numero de compras de abonos
    @classmethod
    def contar(cls):
        return cls.objects.count()

    # Función para calcular el precio del abono en funcion de su tarifa y de la forma de pago y el tipo de abono
    def calcularPrecio(self, usuario, forma="", familiar=False):
        if self.abonoDeportivo:
            precio = self.abonoDeportivo.precioPagoUnicoOtros

            if forma == TipoPago.MENSUAL:
                precio = self.abonoDeportivo.precioTotalMensualOtros

            if usuario.esUAM:
                if forma == TipoPago.MENSUAL:
                    precio = self.abonoDeportivo.precioTotalMensual
                elif forma == TipoPago.UNICO:
                    precio = self.abonoDeportivo.precioPagoUnicoUAM

            if familiar:
                precio = self.abonoDeportivo.precioFamiliar
            
        elif self.abonoVerano:
            precio = self.abonoVerano.precioOtros
            if usuario.esUAM:
                precio = self.abonoVerano.precioUAM
            elif usuario.tieneTDA:
                precio = self.abonoVerano.precioTDA

        return precio

    # Función para confirmar la compra de un abono    
    def confirmarCompra(self):
        self.usuarioFinal.tieneAbono = True
        self.usuarioFinal.save()

        self.estado = EstadoReserva.CONFIRMADA
        self.save()

    # Función para cancelar la compra de un abono
    def cancelarCompra(self):
        if self.estado == EstadoReserva.CONFIRMADA:
            usuario = self.usuarioFinal

            self.usuarioFinal = None
            self.save(update_fields=["usuarioFinal"])

            if usuario:
                usuario.marcarAbono(abono=self)

        self.estado = EstadoReserva.CANCELADO
        self.save(update_fields=["estado"])

    # Función de la clase para ejecutar la compra de un abono (aún sin pagar)
    @classmethod
    def compraAbono(cls, abono, usuario, tipoAbono):
        with transaction.atomic():
            abono.refresh_from_db()

            if tipoAbono == "abono_deportivo":
                if cls.objects.filter(usuarioFinal=usuario, abonoDeportivo=abono, estado=EstadoReserva.CONFIRMADA).exists():
                    return None
                
                for comAbono in cls.objects.filter(usuarioFinal=usuario, abonoDeportivo=abono, estado=EstadoReserva.PENDIENTE):
                    comAbono.cancelarCompra()

                compra = cls.objects.create(
                    usuarioFinal=usuario,
                    abonoDeportivo=abono,
                    estado=EstadoReserva.PENDIENTE
                )

            elif tipoAbono == "abono_verano":
                if cls.objects.filter(usuarioFinal=usuario, abonoVerano=abono, estado=EstadoReserva.CONFIRMADA).exists():
                    return None

                for comAbono in cls.objects.filter(usuarioFinal=usuario, abonoVerano=abono, estado=EstadoReserva.PENDIENTE):
                    comAbono.cancelarCompra()
        
                compra = cls.objects.create(
                    usuarioFinal=usuario,
                    abonoVerano=abono,
                    estado=EstadoReserva.PENDIENTE
                )

            return compra