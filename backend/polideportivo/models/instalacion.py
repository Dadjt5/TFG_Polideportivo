from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import time

from .agenda import Agenda
from .constantes import TipoInstalacion
from .actividad import Sesion


class Pabellon(models.Model):
    """Modelo para representar un pabellon"""

    nombre = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=1024, blank=True)
    imagenURL = models.CharField(max_length=2048, blank=True)
    direccion = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f'{self.nombre}, localizado en {self.direccion}'
    
    @classmethod
    def contar(cls):
        return cls.objects.count()


class Instalacion(models.Model):
    """Modelo para representar una instalacion"""

    nombre = models.CharField(max_length=256, blank=True)
    imagenURL = models.CharField(max_length=2048, blank=True)
    aforoMaximo = models.PositiveIntegerField(default=50)
    luz = models.BooleanField(default=False)
    porcentajeTDA = models.FloatField(default=0.0)

    pabellon = models.ForeignKey(Pabellon, on_delete=models.RESTRICT)
    tarifa = models.ForeignKey('TarifaInstalacion', on_delete=models.PROTECT, blank=True, null=True)

    tipoInstalacion = models.CharField(default=TipoInstalacion.SALA_MULTIUSOS, choices=TipoInstalacion.choices)

    def __str__(self):
        return f'{self.nombre}, ubicado en el {self.pabellon}'
    
    def obtener_precios(self):
        return {
            "precioAbonado": self.tarifa.precioAbonado,
            "precioUAM": self.tarifa.precioUAM,
            "precioTDA": self.tarifa.precioTDA,
            "precioOtros": self.tarifa.precioOtros
        }
        
    def calcular_precio(self, usuario):
        precio = self.tarifa.precioOtros
        if usuario.tieneAbono:
            precio = self.tarifa.precioAbonado
        elif usuario.esUAM:
            precio = self.tarifa.precioUAM
        elif usuario.tieneTDA:
            precio = self.tarifa.precioTDA
        
        return precio

    def controlarHorarioActividad(self, dia, hora_inicio, hora_fin, sesion_id=None):
        if isinstance(hora_inicio, str):
            h, m = map(int, hora_inicio.split(":"))
            hora_inicio = time(h, m)
        if isinstance(hora_fin, str):
            h, m = map(int, hora_fin.split(":"))
            hora_fin = time(h, m)

        agenda = self.agenda.filter(dia__iexact=dia).first()
        if not agenda or not agenda.abierto:
            return False

        if agenda.horaApertura > hora_inicio or agenda.horaCierre < hora_fin:
            return False

        conflictos = Sesion.objects.filter(
            actividad__instalacion=self,
            dia=dia,
            horaInicio__lt=hora_fin,
            horaFin__gt=hora_inicio
        )

        if sesion_id and sesion_id != -1:
            conflictos = conflictos.exclude(id=sesion_id)
        
        if conflictos.exists():
            return False

        return True

    def controlarCambioHorario(self, dia, horaInicio, horaFin, abierto):
        conflictos = self.actividad.filter(
            sesiones__dia=dia,
            sesiones__horaInicio__lt=horaFin,
            sesiones__horaFin__gt=horaInicio
        )

        if conflictos.exists():
            return False
        
        return True

    def nuevoHorario(self, dia, horaApertura, horaCierre, abierto):
        if isinstance(horaApertura, str):
            h, m = map(int, horaApertura.split(":")[:2])
            horaApertura = time(h, m)

        if isinstance(horaCierre, str):
            h, m = map(int, horaCierre.split(":")[:2])
            horaCierre = time(h, m)

        agenda = Agenda.objects.filter(instalacion=self, dia=dia, fecha__isnull=True).first()

        if not abierto:
            if agenda:
                agenda.abierto = False
                agenda.horaApertura = None
                agenda.horaCierre = None
                agenda.save()
            else:
                Agenda.objects.create(instalacion=self, dia=dia, abierto=False)
            return True

        if not horaApertura or not horaCierre or horaCierre <= horaApertura:
            return False

        if agenda:
            agenda.abierto = True
            agenda.horaApertura = horaApertura
            agenda.horaCierre = horaCierre
            agenda.save()
        else:
            agenda = Agenda.objects.create(
                instalacion=self,
                dia=dia,
                horaApertura=horaApertura,
                horaCierre=horaCierre,
                abierto=True
            )

        agenda.generarMapa()
        return True

    def nuevoHorarioEspecial(self, fecha, horaApertura, horaCierre, abierto):
        if isinstance(horaApertura, str):
            h, m = map(int, horaApertura.split(":")[:2])
            horaApertura = time(h, m)

        if isinstance(horaCierre, str):
            h, m = map(int, horaCierre.split(":")[:2])
            horaCierre = time(h, m)

        if not abierto:
            Agenda.objects.create(instalacion=self, fecha=fecha, abierto=False)
            return True

        if not horaApertura or not horaCierre or horaCierre <= horaApertura:
            return False

        agenda = Agenda.objects.create(instalacion=self, fecha=fecha, horaApertura=horaApertura, horaCierre=horaCierre)
        agenda.generarMapa()

        return True

    def get_horario(self, fecha):
        agenda = Agenda.objects.filter(instalacion=self, fecha=fecha).first()

        if agenda and agenda.abierto:
            return agenda.horaApertura, agenda.horaCierre

        return None, None

    def get_reservas(self, fecha):
        if not fecha:
            return []

        agenda = Agenda.objects.filter(instalacion=self, fecha=fecha, abierto=True).first()

        if not agenda:
            return []

        reservas = []
        for mapa in agenda.mapa_reservas.all():
            reservas.append({
                "horaInicio": mapa.horaInicio.strftime("%H:%M"),
                "horaFin": mapa.horaFin.strftime("%H:%M"),
                "estado": mapa.estado
            })

        return reservas

    @classmethod
    def contar(cls):
        return cls.objects.count()

    @classmethod
    def buscar(cls, nombre=None, tipo=None, horaInicio=None, horaFin=None):
        res = cls.objects.all()

        if nombre:
            res = res.filter(nombre__icontains=nombre)

        if tipo:
            res = res.filter(tipoInstalacion__in=tipo)

        if horaInicio:
            res = res.filter(agenda__horaApertura__lte=horaInicio)

        if horaFin:
            res = res.filter(agenda__horaCierre__gte=horaFin)

        return res.distinct()
