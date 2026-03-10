from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .configuracion import Configuracion
from .usuario_final import UsuarioFinal
from .monitor import Monitor
from .administrador import Administrador


class Notificacion(models.Model):
    """Modelo para representar una notificacion"""

    titulo = models.CharField(max_length=256, blank=True)
    descripcion = models.CharField(max_length=2048, blank=True)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    leido = models.BooleanField(default=False)
    fijado = models.BooleanField(default=False)
    debeMarcar = models.BooleanField(default=False)

    actividad = models.ForeignKey('Actividad', on_delete=models.RESTRICT, blank=True, null=True)
    instalacion = models.ForeignKey('Instalacion', on_delete=models.RESTRICT, blank=True, null=True)
    pabellon = models.ForeignKey('Pabellon', on_delete=models.RESTRICT, blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)

    class Meta:
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f'{self.titulo}'

    @classmethod
    def contar(cls):
        return cls.objects.count()

    @classmethod
    def cambiar_estado(cls, usuario, id, leido, fijado):
        cls.objects.filter(id=id, usuario=usuario).update(leido=leido, fijado=fijado)

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
            usuarios = User.objects.filter(id__in=UsuarioFinal.objects.filter(asistencia__sesion__actividad_id=complemento).values_list('user_id', flat=True)).distinct()

        elif tipoUsuarios == "INSTALACION":
            usuarios = User.objects.filter(id__in=UsuarioFinal.objects.filter(reservas__instalacion_id=complemento).values_list('user_id', flat=True)).distinct()

        elif tipoUsuarios == "PABELLON":
            usuarios = User.objects.filter(id__in=UsuarioFinal.objects.filter(reservas__instalacion__pabellon_id=complemento).values_list('user_id', flat=True)).distinct()

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

    @classmethod
    def notificarNuevoMaterial(cls, actividad):
        configuracion = Configuracion.objects.all().first()
        
        usuarios = UsuarioFinal.objects.filter(reserva__actividad=actividad).distinct()

        for usuario in usuarios:
            cls.objects.create(
                titulo=configuracion.titulo_material_especial,
                descripcion=configuracion.texto_material_especial,
                usuario=usuario.user,
                actividad=actividad
            )


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
    
    @classmethod
    def notificarAusencias(cls, usuario, actividad):
        configuracion = Configuracion.objects.all().first()
        
        cls.objects.create(
            titulo=configuracion.titulo_ausencias,
            descripcion=configuracion.texto_ausencias,
            usuario=usuario.user,
            actividad=actividad
        )


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
