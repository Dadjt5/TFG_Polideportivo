from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone



class Reserva(models.Model):
    """Modelo para representar una reserva"""

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)
    descuento = models.ForeignKey('Descuento', on_delete=models.RESTRICT)
    
    pago = models.OneToOneField('Pago', on_delete=models.RESTRICT)

    class Meta:
        abstract = True


class ReservaActividad(Reserva):
    """Modelo para representar una reserva en una actividad"""

    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE)

    def __str__(self):
        return f'Reserva de {self.actividad}'

    @classmethod
    def contar(cls):
        return cls.objects.count()


class Alquiler(Reserva):
    """Modelo para representar un alquiler en una instalacion"""

    fecha = models.TimeField(default=timezone.now)
    
    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE)
    horario = models.ForeignKey('Horario', on_delete=models.RESTRICT)

    def __str__(self):
        return f'Alquiler de {self.instalacion}, en {self.fecha}'
    
    @classmethod
    def contar(cls):
        return cls.objects.count()