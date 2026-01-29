from django.db import models
from django.utils.translation import gettext_lazy as _

from .tarifa import Tarifa

class TarifaActividad(Tarifa):
    """Modelo para representar una tarifa de una actividad"""
    por_defecto = models.BooleanField(default=False)


class ActividadComun(TarifaActividad):
    """Modelo para representar una tarifa de una actividad comun"""

    precioUAM = models.FloatField(default=0.0)
    precioOtros = models.FloatField(default=0.0)
    numeroHorasSemana = models.PositiveIntegerField(default=0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[],
                condition=models.Q(por_defecto=True),
                name="unique_tarifa_comun_por_defecto"
            )
        ]

    def __str__(self):
        return f'Tarifa para actividad comun de precio: {self.precioUAM} para comunidad UAM y precio {self.precioOtros} para externos para {self.numeroHorasSemana} horas por semana'


class GrupoReducido(TarifaActividad):
    """Modelo para representar una tarifa de una actividad para grupos reducidos"""

    numeroHoras = models.PositiveIntegerField(default=0)
    numeroPersonas = models.PositiveIntegerField(default=0)
    precio = models.FloatField(default=0.0)
    precioCuatrimestre = models.FloatField(default=0.0)
    precioMensual = models.FloatField(default=0.0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[],
                condition=models.Q(por_defecto=True),
                name="unique_tarifa_grupo_reducido_por_defecto"
            )
        ]

    def __str__(self):
        return f'Tarifa para grupos reducidos de precio base: {self.precio}'


class Fisioterapia(TarifaActividad):
    """Modelo para representar una tarifa de fisioterapia"""

    precioConsultaTDA = models.FloatField(default=0.0)
    precioConsultaUAM = models.FloatField(default=0.0)
    precioConsultaOtros = models.FloatField(default=0.0)
    precioSesiones1_5TDA = models.FloatField(default=0.0)
    precioSesiones1_5UAM = models.FloatField(default=0.0)
    precioSesiones1_5Otros = models.FloatField(default=0.0)
    precioSesiones6TDA = models.FloatField(default=0.0)
    precioSesiones6UAM = models.FloatField(default=0.0)
    precioSesiones6Otros = models.FloatField(default=0.0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[],
                condition=models.Q(por_defecto=True),
                name="unique_tarifa_fisioterapia_por_defecto"
            )
        ]

    def __str__(self):
        return f'Tarifa de fisioterapia, para externos, un precio de consulta de {self.precioConsultaOtros} precio de primeras sesiones: {self.precioSesiones1_5Otros}, y a partir de la sexta sesion: {self.precioSesiones6Otros}'
