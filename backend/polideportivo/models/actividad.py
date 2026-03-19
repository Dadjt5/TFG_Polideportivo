from django.db import models
from django.utils.translation import gettext_lazy as _
import math
from django.utils import timezone
from datetime import time
from django.http import Http404
from datetime import time, datetime, timedelta

from .notificacion import Notificacion
from .constantes import TipoActividad, FormaReserva, Terreno, Estado, Periodo, Dia


class Actividad(models.Model):
    """Modelo para representar una actividad"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    imagenURL = models.ImageField(upload_to="actividades/", blank=True, null=True)
    edadMinima = models.PositiveIntegerField(default=18)
    plazasMaximas = models.PositiveIntegerField(default=50)
    plazasReservadas = models.PositiveIntegerField(default=0)
    año = models.PositiveIntegerField()
    numeroCreditos = models.PositiveIntegerField(default=0)
    nivel = models.CharField(max_length=64, blank=True)
    material = models.CharField(max_length=1024, blank=True)
    exterior = models.BooleanField(default=False)

    deportes = models.ForeignKey('Deporte', on_delete=models.RESTRICT, related_name="actividades", null=True, blank=True)
    instalacion = models.ForeignKey('Instalacion', on_delete=models.RESTRICT, related_name="actividad")
    monitor = models.ForeignKey('Monitor', on_delete=models.RESTRICT, related_name="actividades")
    tarifa = models.ForeignKey('TarifaActividad', on_delete=models.RESTRICT, blank=True, null=True)

    tipoActividad = models.CharField(default=TipoActividad.OTROS, choices=TipoActividad.choices)
    tipoReserva = models.CharField(default=FormaReserva.NINGUNA, choices=FormaReserva.choices)
    terreno = models.CharField(default=Terreno.PISTA, choices=Terreno.choices)
    estado = models.CharField(default=Estado.INDEFINIDO, choices=Estado.choices)
    periodo = models.CharField(default=Periodo.ANUAL, choices=Periodo.choices)

    def __str__(self):
        return f'{self.nombre}, en la instalacion {self.instalacion}'

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
        elif self.tipoActividad == TipoActividad.FISIOTERAPIA:
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

        raise Http404("Tipo de actividad no válido")
    
    def _calcular_precio_base(self, usuario, numeroHorasSemana=0, numeroPersonas=0, tipoPago='', tipoSesion=''):
        """Devuelve el precio base según tipo de actividad y parámetros"""
        if self.tipoActividad == TipoActividad.OTROS:
            if self.tarifa.actividadcomun.numeroHorasSemana == 0:
                raise ValueError("El número de horas no puede ser 0")

            precio = self.tarifa.actividadcomun.precioOtros
            if usuario.esUAM:
                precio = self.tarifa.actividadcomun.precioUAM

            return precio * (self.calcularHorasSemanales()/self.tarifa.actividadcomun.numeroHorasSemana)

        elif self.tipoActividad == TipoActividad.GRUPOS_REDUCIDOS:
            if self.tarifa.gruporeducido.numeroHoras == 0 or self.tarifa.gruporeducido.numeroPersonas == 0:
                raise ValueError("Ni el número de horas ni el número de personas puede ser 0")

            precio = self.tarifa.gruporeducido.precio
            if tipoPago.lower() == "mensual":
                precio = self.tarifa.gruporeducido.precioMensual
            elif tipoPago.lower() == "cuatrimestral":
                precio = self.tarifa.gruporeducido.precioCuatrimestre

            precio = precio * (numeroHorasSemana/self.tarifa.gruporeducido.numeroHoras)
            return precio * (numeroPersonas/self.tarifa.gruporeducido.numeroPersonas)

        elif self.tipoActividad == TipoActividad.FISIOTERAPIA:
            precio = self.tarifa.fisioterapia.precioConsultaOtros
            if usuario.tieneTDA:
                if tipoSesion.lower() == "consulta":
                    precio = self.tarifa.fisioterapia.precioConsultaTDA
                elif tipoSesion.lower() == "sesiones1_5":
                    precio = self.tarifa.fisioterapia.precioSesiones1_5TDA
                elif tipoSesion.lower() == "sesiones6":
                    precio = self.tarifa.fisioterapia.precioSesiones6TDA

            elif usuario.esUAM:
                if tipoSesion.lower() == "consulta":
                    precio = self.tarifa.fisioterapia.precioConsultaUAM
                elif tipoSesion.lower() == "sesiones1_5":
                    precio = self.tarifa.fisioterapia.precioSesiones1_5UAM
                elif tipoSesion.lower() == "sesiones6":
                    precio = self.tarifa.fisioterapia.precioSesiones6UAM

            else:
                if tipoSesion.lower() == "sesiones1_5":
                    precio = self.tarifa.fisioterapia.precioSesiones1_5Otros
                elif tipoSesion.lower() == "sesiones6":
                    precio = self.tarifa.fisioterapia.precioSesiones6Otros

            return precio

        raise ValueError("Tipo de actividad no válido")

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
            horas += sesion.numeroHoras

        return math.ceil(horas)

    def getDias(self):
        return ",".join(sesion.dia for sesion in self.sesiones.all()),
    
    def getHorario(self):
        horario = []
        
        for sesion in self.sesiones.all():
            horario.append({
                "dia": sesion.dia,
                "horaInicio": sesion.horaInicio.strftime("%H:%M"),
                "horaFin": sesion.horaFin.strftime("%H:%M")
            })
        
        return horario
    
    def nuevaSesion(self, dia, horaInicio, horaFin, calle=None):
        if isinstance(horaInicio, str):
            h, m = map(int, horaInicio.split(":"))
            horaInicio = time(h, m)
        if isinstance(horaFin, str):
            h, m = map(int, horaFin.split(":"))
            horaFin = time(h, m)

        sesion = Sesion.objects.create(dia=dia, horaInicio=horaInicio, horaFin=horaFin, actividad=self, calle=calle, numeroHoras=0.0)
        return sesion
    
    def modificarInformacion(self, actividad_data, tarifa, instalacion, monitor, imagen):
        campos_simples = [
            "nombre",
            "edadMinima",
            "año",
            "numeroCreditos",
            "nivel",
            "material",
            "exterior",
            "tipoReserva",
            "terreno",
            "periodo",
            "estado",
        ]

        # Validaciones especiales
        nuevas_plazas_max = actividad_data.get("plazasMaximas", self.plazasMaximas)
        nuevas_plazas_res = actividad_data.get("plazasReservadas", self.plazasReservadas)

        if nuevas_plazas_res > nuevas_plazas_max:
            return False

        if nuevas_plazas_max < self.plazasReservadas:
            return False

        for campo in campos_simples:
            if campo in actividad_data:
                setattr(self, campo, actividad_data[campo])
                
                if campo == "material" and actividad_data[campo] != self.material:
                    Notificacion.notificarNuevoMaterial(actividad=self)

        self.plazasMaximas = nuevas_plazas_max
        self.plazasReservadas = nuevas_plazas_res

        self.tarifa = tarifa
        self.instalacion = instalacion
        self.monitor = monitor
        self.imagenURL = imagen

        self.save()
        return True

    @classmethod
    def contar(cls):
        return cls.objects.count()

    @classmethod
    def buscar(cls, nombre=None, tipo=None, horaInicio=None, horaFin=None, dias=None):
        res = cls.objects.all()

        print(res, nombre, tipo, horaInicio, horaFin, dias)
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

        print(res)
        return res.distinct()


class Sesion(models.Model):
    """Modelo para representar una sesion de una actividad"""

    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="sesiones")
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    numeroHoras = models.FloatField(default=0.0)

    calle = models.ForeignKey('Calle', null=True, blank=True, on_delete=models.SET_NULL)

    dia = models.CharField(default=Dia.SABADO, choices=Dia.choices)
    
    class Meta:
        ordering = [
            models.Case(
                models.When(dia='lunes', then=0),
                models.When(dia='martes', then=1),
                models.When(dia='miercoles', then=2),
                models.When(dia='jueves', then=3),
                models.When(dia='viernes', then=4),
                models.When(dia='sabado', then=5),
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
            
            if Asistencia.objects.filter(usuarioFinal=usuarioFinal, sesion=self, presente=False).count() > 10:
                Notificacion.notificarAusencias(usuario=usuarioFinal, actividad=self.actividad)
            return True
        except:
            return False
        
    def save(self, *args, **kwargs):
        if isinstance(self.horaInicio, str):
            h, m = map(int, self.horaInicio.split(":"))
            self.horaInicio = time(h, m)

        if isinstance(self.horaFin, str):
            h, m = map(int, self.horaFin.split(":"))
            self.horaFin = time(h, m)

        if self.horaInicio and self.horaFin:
            inicio = datetime.combine(datetime.today(), self.horaInicio)
            fin = datetime.combine(datetime.today(), self.horaFin)

            if fin <= inicio:
                raise ValueError("horaFin debe ser mayor que horaInicio")

            self.numeroHoras = (fin - inicio).total_seconds() / 3600

        super().save(*args, **kwargs)

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