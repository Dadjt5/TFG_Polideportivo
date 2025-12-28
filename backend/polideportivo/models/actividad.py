from django.db import models
from django.utils.translation import gettext_lazy as _
import math
from django.db.models import Q

from .constantes import TipoActividad, TipoReserva, Terreno, Estado, Periodo, Dia

class Actividad(models.Model):
    """Modelo para representar una actividad"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    imagenURL = models.CharField(max_length=2048, blank=True)
    edadMinima = models.PositiveIntegerField(default=18)
    plazasMaximas = models.PositiveIntegerField(default=50)
    plazasReservadas = models.PositiveIntegerField(default=0)
    año = models.PositiveIntegerField()
    numeroCreditos = models.PositiveIntegerField(default=0)
    nivel = models.CharField(max_length=64, blank=True)
    material = models.CharField(max_length=1024, blank=True)
    exterior = models.BooleanField(default=False)
    
    deportes = models.ManyToManyField('Deporte', related_name="actividades")
    instalacion = models.ForeignKey('Instalacion', on_delete=models.RESTRICT)
    monitor = models.ForeignKey('Monitor', on_delete=models.RESTRICT)
    
    tipoActividad = models.CharField(default=TipoActividad.OTROS, choices=TipoActividad.choices)
    tipoReserva = models.CharField(default=TipoReserva.NINGUNA, choices=TipoReserva.choices)
    terreno = models.CharField(default=Terreno.PISTA, choices=Terreno.choices)
    estado = models.CharField(default=Estado.INDEFINIDO, choices=Estado.choices)
    periodo = models.CharField(default=Periodo.ANUAL, choices=Periodo.choices)

    def __str__(self):
        return f'{self.nombre}, en la instalacion {self.instalacion}'
    
    def calcularHorasSemanales(self):
        horas = 0.0
        for sesion in self.sesion_set.all():
            horas += sesion.horario.numeroHoras

        return math.ceil(horas)
    
    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    @classmethod
    def buscar(cls, nombre=None, tipo=None, horaInicio=None, horaFin=None, dias=None):
        res = cls.objects.all()

        if nombre:
            res = res.filter(nombre__icontains=nombre)

        if tipo:
            tipo = tipo.split(',')
            res = res.filter(tipoActividad__in=tipo)

        if horaInicio:
            res = res.filter(sesion__horario__horaInicio__lte=horaInicio)

        if horaFin:
            res = res.filter(sesion__horario__horaFin__gte=horaFin)

        if dias:
            dias = dias.split(',')
            res = res.filter(sesion__dia__in=dias)

        return res.distinct()


class Sesion(models.Model):
    """Modelo para representar una sesion de una actividad"""

    actividad = models.ForeignKey(Actividad, related_name="sesion", on_delete=models.RESTRICT)
    monitor = models.ForeignKey('Monitor', on_delete=models.RESTRICT)
    horario = models.ForeignKey('Horario', on_delete=models.RESTRICT)    

    dia = models.CharField(default=Dia.SABADO, choices=Dia.choices)

    def __str__(self):
        return f'Sesion el {self.dia} de {self.actividad}'
    
    def ponerFalta(self, usuarioFinal):
        try:
            asistencia = Asistencia.objects.get(usuarioFinal=usuarioFinal, sesion=self)
            asistencia.presente = False
            asistencia.save(update_fields=["presente"])
            return True
        except:
            return False

    @classmethod
    def contar(cls):
        return cls.objects.count()


class Asistencia(models.Model):
    """Modelo para representar la relación entre sesion y usuario"""
    
    presente = models.BooleanField(default=True)
    
    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)
    sesion = models.ForeignKey(Sesion, on_delete=models.RESTRICT)
    
    class Meta:
        unique_together = ('usuarioFinal', 'sesion')