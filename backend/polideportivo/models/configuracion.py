from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Configuracion(models.Model):
    """Modelo para representar la configuracion interna de la aplicacion"""
    
    max_deportes_por_usuario = models.PositiveIntegerField(default=5)
    dias_minimo_alquiler = models.PositiveIntegerField(default=0)
    dias_maximo_alquiler = models.PositiveIntegerField(default=7)
    dias_minimo_cancelacion = models.PositiveIntegerField(default=1)
    horas_alquiler_consecutivas = models.PositiveIntegerField(default=2)
    porcentaje_maximo = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])

    titulo_cambios_cancelaciones = models.CharField(max_length=1024, blank=True)
    titulo_avisos_actividades = models.CharField(max_length=1024, blank=True)
    titulo_problemas_pago = models.CharField(max_length=1024, blank=True)
    titulo_salida_lista_espera = models.CharField(max_length=1024, blank=True)
    titulo_ausencias = models.CharField(max_length=1024, blank=True)
    titulo_material_especial = models.CharField(max_length=1024, blank=True)
    titulo_cambios_sesiones = models.CharField(max_length=1024, blank=True)
    titulo_avisos_sobre_actividades_usuarios = models.CharField(max_length=1024, blank=True)
    titulo_avisos_sobre_actividades_monitores = models.CharField(max_length=1024, blank=True)
    titulo_aviso_devolucion_dinero_alquiler = models.CharField(max_length=1024, blank=True)

    texto_cambios_cancelaciones = models.CharField(max_length=1024, blank=True)
    texto_avisos_actividades = models.CharField(max_length=1024, blank=True)
    texto_problemas_pago = models.CharField(max_length=1024, blank=True)
    texto_salida_lista_espera = models.CharField(max_length=1024, blank=True)
    texto_ausencias = models.CharField(max_length=1024, blank=True)
    texto_material_especial = models.CharField(max_length=1024, blank=True)
    texto_cambios_sesiones = models.CharField(max_length=1024, blank=True)
    texto_avisos_sobre_actividades_usuarios = models.CharField(max_length=1024, blank=True)
    texto_avisos_sobre_actividades_monitores = models.CharField(max_length=1024, blank=True)
    texto_aviso_devolucion_dinero_alquiler = models.CharField(max_length=1024, blank=True)

    # Función para sobreescribir el guardado y evitar crear mas de un objeto configuracion
    def save(self, *args, **kwargs):
        """Obligamos a que solo haya una configuracion"""
        if not self.pk and Configuracion.objects.exists():
            raise ValueError("Solo puede existir una configuración")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Configuración global de la aplicación"

    # Función para editar los campos de la configuracion
    def editar(self, data):
        try:
            valor_original_cancelacion = self.dias_minimo_cancelacion

            for campo, valor in data.items():
                if hasattr(self, campo):
                    setattr(self, campo, valor)

            self.save()

            if 'dias_minimo_cancelacion' in data and data['dias_minimo_cancelacion'] != valor_original_cancelacion:
                from .notificacion import Notificacion
                Notificacion.notificarCambioCancelacion()

            return True
        except Exception as e:
            print("Error al editar configuración:", e)
            return False