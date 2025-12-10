from django.db import models
from django.utils.translation import gettext_lazy as _

from .instalacion import Instalacion
from .deporte import Deporte
from .monitor import Monitor
from .horario import Horario
from .constantes import TipoActividad, TipoReserva, Terreno, Estado, Periodo, Dia

class Actividad(models.Model):
    """Modelo para representar una actividad"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    imagenURL = models.CharField(max_length=2048, blank=True)
    edadMinima = models.IntegerField(default=18)
    plazasMaximas = models.IntegerField(default=50)
    plazasReservadas = models.IntegerField(default=0)
    año = models.IntegerField()
    numeroCreditos = models.IntegerField(default=0)
    nivel = models.CharField(max_length=64, blank=True)
    material = models.CharField(max_length=1024, blank=True)
    exterior = models.BooleanField(default=False)
    
    deportes = models.ManyToManyField(Deporte, related_name="actividades")
    instalacion = models.ForeignKey(Instalacion, on_delete=models.RESTRICT)
    monitor = models.ForeignKey(Monitor, on_delete=models.RESTRICT)
    
    tipoActividad = models.CharField(default=TipoActividad.OTROS, choices=TipoActividad.choices)
    tipoReserva = models.CharField(default=TipoReserva.NINGUNA, choices=TipoReserva.choices)
    terreno = models.CharField(default=Terreno.PISTA, choices=Terreno.choices)
    estado = models.CharField(default=Estado.INDEFINIDO, choices=Estado.choices)
    periodo = models.CharField(default=Periodo.ANUAL, choices=Periodo.choices)

    def __str__(self):
        return f'{self.nombre}, en la instalacion {self.instalacion}'


class Sesion(models.Model):
    """Modelo para representar una sesion de una actividad"""
    
    actividad = models.ForeignKey(Actividad, on_delete=models.RESTRICT)
    monitor = models.ForeignKey(Monitor, on_delete=models.RESTRICT)
    horario = models.ForeignKey(Horario, on_delete=models.RESTRICT)    

    dia = models.CharField(default=Dia.SABADO, choices=Dia.choices)

    def __str__(self):
        return f'Sesion el {self.dia} de {self.actividad}'