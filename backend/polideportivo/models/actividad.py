from django.db import models
from django.utils.translation import gettext_lazy as _
import math
from django.utils import timezone
from django.core.exceptions import ValidationError

from .constantes import TipoActividad, TipoReserva, Terreno, Estado, Periodo, Dia
from .tarifa_actividad import Fisioterapia, GrupoReducido, ActividadComun

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
    monitor = models.ForeignKey('Monitor', on_delete=models.RESTRICT, related_name="actividades")
    tarifa = models.ForeignKey('TarifaActividad', on_delete=models.PROTECT, blank=True, null=True)

    tipoActividad = models.CharField(default=TipoActividad.OTROS, choices=TipoActividad.choices)
    tipoReserva = models.CharField(default=TipoReserva.NINGUNA, choices=TipoReserva.choices)
    terreno = models.CharField(default=Terreno.PISTA, choices=Terreno.choices)
    estado = models.CharField(default=Estado.INDEFINIDO, choices=Estado.choices)
    periodo = models.CharField(default=Periodo.ANUAL, choices=Periodo.choices)

    def __str__(self):
        return f'{self.nombre}, en la instalacion {self.instalacion}'

    def save(self, *args, **kwargs):
        if not self.tarifa:
            if self.tipoActividad == TipoActividad.OTROS:
                tarifa = ActividadComun.objects.filter(por_defecto=True).first()
            elif self.tipoActividad == TipoActividad.FISIOTERAPIA:
                tarifa = Fisioterapia.objects.filter(por_defecto=True).first()
            else:
                tarifa = GrupoReducido.objects.filter(por_defecto=True).first()

            if not tarifa:
                raise ValidationError("No existe una tarifa por defecto para este tipo de actividad")

            self.tarifa = tarifa
        super().save(*args, **kwargs)

    def obtener_precios(self):
        if self.tipoActividad == TipoActividad.OTROS:
            return {
                "precioUAM": self.tarifa.actividadcomun.precioUAM,
                "precioOtros": self.tarifa.actividadcomun.precioOtros,
                "numeroHorasSemana": self.tarifa.actividadcomun.numeroHorasSemana
            }
        elif self.tipoActividad == TipoActividad.GRUPOS_REDUCIDOS:
            return {
                "numeroHoras": self.tarifa.gruporeducido.numeroHoras,
                "numeroPersonas": self.tarifa.gruporeducido.numeroPersonas,
                "precio": self.tarifa.gruporeducido.precio,
                "precioCuatrimestre": self.tarifa.gruporeducido.precioCuatrimestre,
                "precioMensual": self.tarifa.gruporeducido.precioMensual
            }
        else:
            return {
                "precioConsultaTDA": self.tarifa.fisioterapia.precioConsultaTDA,
                "precioConsultaUAM": self.tarifa.fisioterapia.precioConsultaUAM,
                "precioConsultaOtros": self.tarifa.fisioterapia.precioConsultaOtros,
                "precioSesiones1_5TDA": self.tarifa.fisioterapia.precioSesiones1_5TDA,
                "precioSesiones1_5UAM": self.tarifa.fisioterapia.precioSesiones1_5UAM,
                "precioSesiones1_5Otros": self.tarifa.fisioterapia.precioSesiones1_5Otros,
                "precioSesiones6TDA": self.tarifa.fisioterapia.precioSesiones6TDA,
                "precioSesiones6UAM": self.tarifa.fisioterapia.precioSesiones6UAM,
                "precioSesiones6Otros": self.tarifa.fisioterapia.precioSesiones6Otros
            }

    @property
    def activa(self):
        if self.periodo == Periodo.ANUAL:
            return True

        now = timezone.now()

        if self.periodo == Periodo.PRIMER_CUATRIMESTRE:
            return now.month in [9,10,11,12,1]

        if self.periodo == Periodo.SEGUNDO_CUATRIMESTRE:
            return now.month in [2,3,4,5]

        return False

    def calcularHorasSemanales(self):
        horas = 0.0
        for sesion in self.sesiones.all():
            horas += sesion.horario.numeroHoras

        return math.ceil(horas)

    def getDias(self):
        return ",".join(sesion.dia for sesion in self.sesiones.all()),
    
    def getHorario(self):
        horario = []
        
        for sesion in self.sesiones.all():
            horario.append({
                "dia": sesion.dia,
                "horaInicio": sesion.horario.horaInicio.strftime("%H:%M"),
                "horaFin": sesion.horario.horaFin.strftime("%H:%M")
            })
        
        return horario

    @classmethod
    def contar(cls):
        return cls.objects.count()

    @classmethod
    def buscar(cls, nombre=None, tipo=None, horaInicio=None, horaFin=None, dias=None):
        res = cls.objects.all()

        if nombre:
            res = res.filter(nombre__icontains=nombre)

        if tipo:
            res = res.filter(tipoActividad__in=tipo)

        if horaInicio:
            res = res.filter(sesiones__horario__horaInicio__lte=horaInicio)

        if horaFin:
            res = res.filter(sesiones__horario__horaFin__gte=horaFin)

        if dias:
            res = res.filter(sesiones__dia__in=dias)

        return res.distinct()


class Sesion(models.Model):
    """Modelo para representar una sesion de una actividad"""

    actividad = models.ForeignKey(Actividad, on_delete=models.RESTRICT, related_name="sesiones")
    horario = models.ForeignKey('Horario', on_delete=models.RESTRICT)    

    dia = models.CharField(default=Dia.SABADO, choices=Dia.choices)
    
    class Meta:
        ordering = [
            models.Case(
                models.When(dia='lunes', then=0),
                models.When(dia='martes', then=1),
                models.When(dia='miércoles', then=2),
                models.When(dia='jueves', then=3),
                models.When(dia='viernes', then=4),
                models.When(dia='sábado', then=5),
                models.When(dia='domingo', then=6),
                output_field=models.IntegerField(),
            )
        ]

    def __str__(self):
        return f'Sesion el {self.dia} de {self.actividad}'
    
    def cambiarFalta(self, usuarioFinal, falta):
        try:
            asistencia = Asistencia.objects.get(usuarioFinal=usuarioFinal, sesion=self)

            if asistencia.presente != falta:
                asistencia.presente = falta
                asistencia.save(update_fields=["presente"])
            return True
        except:
            return False

    @classmethod
    def contar(cls):
        return cls.objects.count()


class Asistencia(models.Model):
    """Modelo para representar la relación entre sesion y usuario"""

    presente = models.BooleanField(default=False)

    usuarioFinal = models.ForeignKey('UsuarioFinal', on_delete=models.RESTRICT)
    sesion = models.ForeignKey(Sesion, on_delete=models.RESTRICT, related_name="asistencias")

    class Meta:
        unique_together = ('usuarioFinal', 'sesion')