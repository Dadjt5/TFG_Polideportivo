from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .configuracion import Configuracion
from .usuario_final import UsuarioFinal
from .monitor import Monitor
from .administrador import Administrador
from .constantes import EstadoReserva


class Notificacion(models.Model):
    """Modelo para representar una notificacion"""

    titulo = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    leido = models.BooleanField(default=False)
    fijado = models.BooleanField(default=False)
    debeMarcar = models.BooleanField(default=False)

    actividad = models.ForeignKey('Actividad', on_delete=models.SET_NULL, blank=True, null=True)
    sesion = models.ForeignKey('Sesion', on_delete=models.SET_NULL, blank=True, null=True)
    instalacion = models.ForeignKey('Instalacion', on_delete=models.SET_NULL, blank=True, null=True)
    pabellon = models.ForeignKey('Pabellon', on_delete=models.SET_NULL, blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f'{self.titulo}'

    # Función para contar el número de notificaciones en el sistema
    @classmethod
    def contar(cls):
        return cls.objects.count()

    # Función para cambiar el estado de leído de la notificación
    @classmethod
    def cambiarEstado(cls, usuario, id, leido, fijado):
        cls.objects.filter(id=id, usuario=usuario).update(leido=leido, fijado=fijado)

    # Función para crear una nueva notificación por parte del administrador
    @classmethod
    def nuevaNotificacion(cls, titulo, descripcion, tipoUsuarios, complemento):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if tipoUsuarios == "TODOS":
            usuarios = User.objects.all()

        elif tipoUsuarios == "USUARIOS_FINALES":
            usuarios = User.objects.filter(id__in=UsuarioFinal.objects.values_list('user_id', flat=True))

        elif tipoUsuarios == "MONITORES":
            usuarios = User.objects.filter(id__in=Monitor.objects.values_list('user_id', flat=True))

        elif tipoUsuarios == "ADMINISTRADORES":
            usuarios = User.objects.filter(id__in=Administrador.objects.values_list('user_id', flat=True))

        elif tipoUsuarios == "ACTIVIDAD":
            # Trae todos los usuarios finales que tengan asistencia en alguna sesión de la actividad
            usuarios = User.objects.filter(id__in=UsuarioFinal.objects.filter(reservas_actividad__actividad_id=complemento, reservas_actividad__estado=EstadoReserva.CONFIRMADA).values_list('user_id', flat=True)).distinct()

        elif tipoUsuarios == "INSTALACION":
            usuarios = User.objects.filter(id__in=UsuarioFinal.objects.filter(alquileres__instalacion_id=complemento, alquileres__estado=EstadoReserva.CONFIRMADA).values_list('user_id', flat=True)).distinct()

        elif tipoUsuarios == "PABELLON":
            usuarios = User.objects.filter(id__in=UsuarioFinal.objects.filter(alquileres__instalacion__pabellon_id=complemento, alquileres__estado=EstadoReserva.CONFIRMADA).values_list('user_id', flat=True)).distinct()

        else:
            usuarios = User.objects.none()

        notificaciones = [
            cls(
                titulo=titulo,
                descripcion=descripcion,
                usuario=usuario,
                actividad_id=complemento if tipoUsuarios == "ACTIVIDAD" else None,
                instalacion_id=complemento if tipoUsuarios == "INSTALACION" else None,
                pabellon_id=complemento if tipoUsuarios == "PABELLON" else None,
            )
            for usuario in usuarios
        ]

        cls.objects.bulk_create(notificaciones)

    # Función para notificar automaticamente por cancelación de alquiler y devolución de dinero
    @classmethod
    def notificarCancelacionYDevolucionDinero(cls, usuarios, instalacion):
        configuracion = Configuracion.objects.all().first()

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_aviso_devolucion_dinero_alquiler,
                descripcion=configuracion.texto_aviso_devolucion_dinero_alquiler,
                usuario=usuario.user,
                instalacion=instalacion
            )

    # Función para notificar automaticamente a los usuarios finales que tiene una actividad próxima
    @classmethod
    def notificarActividadUsuarioFinal(cls, actividad, sesion):
        configuracion = Configuracion.objects.all().first()

        usuarios = UsuarioFinal.objects.filter(reservas_actividad__actividad=actividad, reservas_actividad__estado=EstadoReserva.CONFIRMADA).distinct()

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_avisos_sobre_actividades_usuarios,
                descripcion=configuracion.texto_avisos_sobre_actividades_usuarios,
                usuario=usuario.user,
                actividad=actividad,
                sesion=sesion
            )

    # Función para notificar automaticamente a los monitores que tiene una actividad próxima
    @classmethod
    def notificarActividadMonitor(cls, actividad, sesion):
        configuracion = Configuracion.objects.all().first()

        monitor = actividad.monitor

        cls.objects.create(
            titulo=configuracion.titulo_avisos_sobre_actividades_monitores,
            descripcion=configuracion.texto_avisos_sobre_actividades_monitores,
            usuario=monitor.user,
            actividad=actividad,
            sesion=sesion
        )

    # Función para notificar de una nueva actividad a los usuarios finales que lo tengan como favorito
    @classmethod
    def notificarNuevaActividad(cls, actividad):
        configuracion = Configuracion.objects.all().first()

        if not actividad.deportes:
            return

        usuarios = UsuarioFinal.objects.filter(
            deportesFavoritos=actividad.deportes
        )

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_avisos_actividades,
                descripcion=configuracion.texto_avisos_actividades,
                usuario=usuario.user,
                actividad=actividad
            )

    # Función para notificar a los usuarios automaticamente al cambiar el material
    @classmethod
    def notificarNuevoMaterial(cls, actividad):
        configuracion = Configuracion.objects.all().first()
        
        usuarios = UsuarioFinal.objects.filter(reservas_actividad__actividad=actividad, reservas_actividad__estado=EstadoReserva.CONFIRMADA).distinct()

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_material_especial,
                descripcion=configuracion.texto_material_especial,
                usuario=usuario.user,
                actividad=actividad
            )
    
    # Función para notificar automaticamente el cambio de sesiones
    @classmethod
    def notificarCambioSesiones(cls, actividad):
        configuracion = Configuracion.objects.all().first()
        
        usuarios = UsuarioFinal.objects.filter(reservas_actividad__actividad=actividad, reservas_actividad__estado=EstadoReserva.CONFIRMADA).distinct()

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_cambios_sesiones,
                descripcion=configuracion.texto_cambios_sesiones,
                usuario=usuario.user,
                actividad=actividad
            )

    # Función para notificar automaticamente los cambios de cancelaciones
    @classmethod
    def notificarCambioCancelacion(cls):
        configuracion = Configuracion.objects.all().first()

        usuarios = UsuarioFinal.objects.all()

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_cambios_cancelaciones,
                descripcion=configuracion.texto_cambios_cancelaciones,
                usuario=usuario.user
            )
    
    # Función para notificar automaticamente al llevar muchas ausencias
    @classmethod
    def notificarAusencias(cls, usuario, actividad):
        configuracion = Configuracion.objects.all().first()
        
        cls.objects.create(
            titulo=configuracion.titulo_ausencias,
            descripcion=configuracion.texto_ausencias,
            usuario=usuario.user,
            actividad=actividad
        )

    # Función para notificar automaticamente en caso de problemas de pago    
    @classmethod
    def notificarProblemasPago(cls, usuario):
        configuracion = Configuracion.objects.all().first()
        
        cls.objects.create(
            titulo=configuracion.titulo_problemas_pago,
            descripcion=configuracion.texto_problemas_pago,
            usuario=usuario,
        )

    # Función para notificar automaticamente la salida de la lista de espera c
    @classmethod
    def notificarSalidaListaDeEspera(cls, usuario, actividad):
        configuracion = Configuracion.objects.all().first()

        cls.objects.create(
            titulo=configuracion.titulo_salida_lista_espera,
            descripcion=configuracion.texto_salida_lista_espera,
            usuario=usuario.user,
            actividad=actividad,
            debeMarcar=True
        )

    # Función para notificar automaticamente la eliminacion de una actividad
    @classmethod
    def notificarEliminacionActividad(cls, actividad):
        configuracion = Configuracion.objects.all().first()
        
        usuarios = UsuarioFinal.objects.filter(reservas_actividad__actividad=actividad, reservas_actividad__estado=EstadoReserva.CONFIRMADA).distinct()

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_actividad_eliminada,
                descripcion=configuracion.texto_actividad_eliminada,
                usuario=usuario.user,
                actividad=actividad
            )

    # Función para notificar automaticamente la eliminacion de una instalacion
    @classmethod
    def notificarEliminacionInstalacion(cls, instalacion):
        configuracion = Configuracion.objects.all().first()

        usuarios = UsuarioFinal.objects.filter(alquileres__instalacion=instalacion, alquileres__estado=EstadoReserva.CONFIRMADA).distinct()

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_instalacion_eliminada,
                descripcion=configuracion.texto_instalacion_eliminada,
                usuario=usuario.user,
                instalacion=instalacion
            )
