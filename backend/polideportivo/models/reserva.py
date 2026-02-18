from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .constantes import EstadoReserva
from .descuento import Descuento


class Reserva(models.Model):
    """Modelo para representar una reserva"""

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)
    descuentos = models.ManyToManyField('Descuento', blank=True)

    estado = models.CharField(default=EstadoReserva.PENDIENTE, choices=EstadoReserva.choices)

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
    
    @classmethod
    def nuevaReserva(cls, usuario, actividad):
        if actividad.plazasReservadas >= actividad.plazasMaximas:
            raise ValueError("No hay plazas disponibles") # Lista de espera

        descuentos = Descuento.obtener_descuentos(actividad=actividad)

        reserva = cls.objects.create(
            usuarioFinal=usuario,
            actividad=actividad,
            estadoReserva=EstadoReserva.PENDIENTE
        )

        reserva.descuentos.set(descuentos["descuento"]["aplicados"])

        actividad.plazasReservadas += 1
        actividad.save()

        return reserva


class Alquiler(Reserva):
    """Modelo para representar un alquiler en una instalacion"""

    fecha = models.TimeField(default=timezone.now)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    numeroHoras = models.FloatField(default=0.0)

    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE)

    def __str__(self):
        return f'Alquiler de {self.instalacion}, en {self.fecha} de {self.horaInicio} a {self.horaFin}'

    @classmethod
    def contar(cls):
        return cls.objects.count()

    def save(self, *args, **kwargs):
        t1 = self.horaInicio.hour*3600 + self.horaInicio.minute*60 + self.horaInicio.second
        t2 = self.horaFin.hour*3600 + self.horaFin.minute*60 + self.horaFin.second
        horas = (t2-t1)/3600
        self.numeroHoras = horas
        
        super().save(*args, **kwargs)

    @property
    def valido(self):
        t1 = self.horaInicio.hour*3600 + self.horaInicio.minute*60 + self.horaInicio.second
        t2 = self.horaFin.hour*3600 + self.horaFin.minute*60 + self.horaFin.second
        
        horas = (t1-t2)/3600
        if horas > 2.0:
            return False

        return True