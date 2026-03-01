from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import time
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

from .constantes import TipoReserva, Dia


class Agenda(models.Model):
    """Modelo para representar la agenda de las instalaciones"""

    fecha = models.DateField(blank=True, null=True)
    dia = models.CharField(max_length=10, choices=Dia.choices, blank=True, null=True)

    horaApertura = models.TimeField(default=time(8, 0))
    horaCierre = models.TimeField(default=time(20, 0))
    abierto = models.BooleanField(default=True)

    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE, related_name="agenda")

    class Meta:
        unique_together = [('dia', 'instalacion'), ('fecha', 'instalacion')]

    def __str__(self):
        if self.dia:
            return f'Agenda para {self.dia} de {self.instalacion.nombre}'
        return f'Agenda para {self.fecha} de {self.instalacion.nombre}'

    def generarMapa(self, minutos=60):
        if not self.abierto:
            return

        inicio = datetime.combine(datetime.today(), self.horaApertura)
        fin = datetime.combine(datetime.today(), self.horaCierre)

        while inicio < fin:
            siguiente = inicio + timedelta(minutes=minutos)

            MapaReservas.objects.get_or_create(
                agenda=self,
                horaInicio=inicio.time(),
                horaFin=siguiente.time(),
            )

            inicio = siguiente


class MapaReservas(models.Model):
    """Modelo para representar el mapa de reservas de un dia"""

    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    estado = models.CharField(max_length=40, default=TipoReserva.LIBRE, choices=TipoReserva.choices)

    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, related_name="mapa_reservas")

    class Meta:
        ordering = ['horaInicio']
        unique_together = ('agenda', 'horaInicio', 'horaFin')

    def clean(self):
        if self.horaInicio >= self.horaFin:
            raise ValidationError("La hora de inicio debe ser menor que la hora de fin")

    def __str__(self):
        return f'{self.agenda.fecha} {self.horaInicio}-{self.horaFin}'