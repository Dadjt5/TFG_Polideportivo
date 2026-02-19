from django.db import models
from django.utils.translation import gettext_lazy as _

from .constantes import TipoInstalacion

from .agenda import Agenda

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
