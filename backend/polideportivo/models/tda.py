from django.db import models, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password, check_password

from .usuario_final import UsuarioFinal
from .tarifa import TarifaTDA
from .constantes import EstadoReserva


class TDA(models.Model):
    """Modelo para representar una actividad"""

    fechaInicio = models.DateField(auto_now_add=True)
    fechaExpiracion = models.DateField(blank=True, null=True)
    codigo_secreto = models.CharField(max_length=128, blank=True)

    estado = models.CharField(default=EstadoReserva.PENDIENTE, choices=EstadoReserva.choices)

    tarifa = models.ForeignKey('TarifaTDA', on_delete=models.RESTRICT, blank=True, null=True)
    usuarioFinal = models.ForeignKey(UsuarioFinal, on_delete=models.CASCADE, related_name="tda", blank=True, null=True)

    def __str__(self):
        return f'Tarjeta deportiva anual con fecha de inicio: {self.fechaInicio} y fecha de expiracion: {self.fechaExpiracion}'

    # Función apra generar un nuevo código secreto
    def nuevoCodigoSecreto(self, codigo: str):
        self._codigo_secreto_hash = make_password(codigo)

    # FUnción para comprobar el codigo secreto
    def comprobarCodigoSecreto(self, codigo: str):
        return check_password(codigo, self._codigo_secreto_hash)

    # Función para comprar una TDA    
    @classmethod
    def compraTDA(cls, usuario):
        with transaction.atomic():
            hoy = now().date()
            if not TarifaTDA.objects.first():
                return None

            if cls.objects.filter(usuarioFinal=usuario, estado=EstadoReserva.CONFIRMADA, fechaExpiracion__gte=hoy).exists():
                return None

            for tda in cls.objects.filter(usuarioFinal=usuario, estado=EstadoReserva.PENDIENTE):
                tda.delete()
            
            for tda in cls.objects.filter(usuarioFinal=usuario, fechaExpiracion__lte=hoy):
                tda.delete()

            tda = cls.objects.create(
                usuarioFinal=usuario,
                estado=EstadoReserva.PENDIENTE,
                tarifa=TarifaTDA.objects.first()
            )

            tda.fechaExpiracion = tda.fechaInicio + relativedelta(years=1)
            tda.save()

            return tda
    
    # Función para calcular el precio de compra basandose en la tarifa
    def calcularPrecio(self):
        precio = self.tarifa.precioOtros
        if self.usuarioFinal.esUAM:
            precio = self.tarifa.precioUAM

        return precio
    
    # Función para confirmar la compra de la TDA
    def confirmarCompra(self):
        self.usuarioFinal.tieneTDA = True
        self.usuarioFinal.save()

        self.estado = EstadoReserva.CONFIRMADA
        self.save()
    
    # Función para cancelar la compra de la TDA
    def cancelarCompra(self):
        self.usuarioFinal.tieneTDA = False
        self.usuarioFinal.save()

        self.delete()

    # Función para contar el número de TDAs del sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()