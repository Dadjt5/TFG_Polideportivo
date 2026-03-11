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
    fechaExpiracion = models.DateField()
    _codigo_secreto_hash = models.CharField(max_length=128, blank=True)
    codigo_secreto = models.CharField(max_length=128, blank=True)

    estado = models.CharField(default=EstadoReserva.PENDIENTE, choices=EstadoReserva.choices)

    tarifa = models.ForeignKey('TarifaTDA', on_delete=models.PROTECT, blank=True, null=True)
    usuarioFinal = models.ForeignKey(UsuarioFinal, on_delete=models.CASCADE, related_name="tda", blank=True, null=True)

    def __str__(self):
        return f'Tarjeta deportiva anual con fecha de inicio: {self.fechaInicio} y fecha de expiracion: {self.fechaExpiracion}'

    def nuevo_codigo_secreto(self, codigo: str):
        self._codigo_secreto_hash = make_password(codigo)

    def comprobar_codigo_secreto(self, codigo: str):
        return check_password(codigo, self._codigo_secreto_hash)

    def asignar_usuario(self, usuario_final):
        if self.usuarioFinal:
            return False

        self.usuarioFinal = usuario_final
        self._codigo_secreto_hash = ""
        self.save()
        
        usuario_final.tieneTDA = True
        usuario_final.save()

        return True
    
    @classmethod
    def compraTDA(cls, usuario):
        with transaction.atomic():
            hoy = now().date()
            if cls.objects.filter(usuarioFinal=usuario, estado=EstadoReserva.CONFIRMADA, fechaExpiracion__gte=hoy).exists():
                return None
            
            if not TarifaTDA.objects.exists():
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
    
    def calcular_precio(self):
        precio = self.tarifa.precioOtros
        if self.usuarioFinal.esUAM:
            precio = self.tarifa.precioUAM

        return precio
    
    def confirmarCompra(self):
        self.usuarioFinal.tieneTDA = True
        self.usuarioFinal.save()

        self.estado = EstadoReserva.CONFIRMADA
        self.save()
    
    def cancelarCompra(self):
        self.usuarioFinal.tieneTDA = False
        self.usuarioFinal.save()

        self.delete()

    @classmethod
    def contar(cls):
        return cls.objects.count()