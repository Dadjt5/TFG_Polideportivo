from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Configuracion(models.Model):
    """Modelo para representar la configuracion interna de la aplicacion"""
    
    max_deportes_por_usuario = models.PositiveIntegerField(default=5)
    dias_minimo_reserva_actividad = models.PositiveIntegerField(default=1)
    dias_maximo_reserva_actividad = models.PositiveIntegerField(default=7)
    dias_maximo_alquiler = models.PositiveIntegerField(default=7)
    dias_minimo_cancelacion = models.PositiveIntegerField(default=1)
    horas_previas_notificacion = models.PositiveIntegerField(default=1)
    horas_alquiler_consecutivas = models.PositiveIntegerField(default=2)
    porcentaje_maximo = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])

    titulo_cambios_cancelaciones = models.CharField(max_length=1024, blank=True)
    titulo_avisos_actividades = models.CharField(max_length=1024, blank=True)
    titulo_problemas_pago = models.CharField(max_length=1024, blank=True)
    titulo_salida_lista_espera = models.CharField(max_length=1024, blank=True)
    titulo_ausencias = models.CharField(max_length=1024, blank=True)
    titulo_material_especial = models.CharField(max_length=1024, blank=True)

    texto_cambios_cancelaciones = models.CharField(max_length=1024, blank=True)
    texto_avisos_actividades = models.CharField(max_length=1024, blank=True)
    texto_problemas_pago = models.CharField(max_length=1024, blank=True)
    texto_salida_lista_espera = models.CharField(max_length=1024, blank=True)
    texto_ausencias = models.CharField(max_length=1024, blank=True)
    texto_material_especial = models.CharField(max_length=1024, blank=True)

    def save(self, *args, **kwargs):
        """Obligamos a que solo haya una configuracion"""
        if not self.pk and Configuracion.objects.exists():
            raise ValueError("Solo puede existir una configuración")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Configuración global de la aplicación"
    
    def editar(self, data):
        try:
            for campo, valor in data.items():
                print(campo, valor)
                if hasattr(self, campo):
                    setattr(self, campo, valor)
            self.save()
            return True
        except Exception as e:
            print("Error al editar configuración:", e)
            return False