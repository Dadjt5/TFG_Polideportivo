from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now, make_aware
from datetime import datetime, timedelta

from .user import generar_codigo
from .usuario import Usuario
from .favorito import Favorito
from .constantes import Sexo, Rol

DIA_MAP = {
    "Lunes": 0,
    "Martes": 1,
    "Miercoles": 2,
    "Jueves": 3,
    "Viernes": 4,
    "Sabado": 5,
    "Domingo": 6
}

class UsuarioFinal(Usuario):
    """Modelo para representar al usuario final"""

    fechaNacimiento = models.DateField()
    telefono = models.CharField(max_length=16, default="")
    provincia = models.CharField(max_length=64, default="")
    municipio = models.CharField(max_length=64, default="")
    localidad = models.CharField(max_length=64, default="")
    codigoPostal = models.CharField(max_length=64, default="")
    actividadesRealizadas = models.PositiveIntegerField(default=0)
    esUAM = models.BooleanField(default=False)
    tieneAbono = models.BooleanField(default=False)
    tieneTDA = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)

    deportesFavoritos = models.ManyToManyField('Deporte', blank=True, related_name="usuariosFinales")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usuario_final")

    sexo = models.CharField(default=Sexo.NINGUNO, choices=Sexo.choices)
    rol = models.CharField(default=Rol.EXTERNO, choices=Rol.choices)

    def save(self, *args, **kwargs):
        if not self.esUAM:
            self.rol == Rol.EXTERNO
        else:
            self.rol = Rol.ESTUDIANTE

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Usuario: {self.id}, nacido el {self.fechaNacimiento}'
    
    def revisarActividades(self):
        from .notificacion import Notificacion

        fecha_actual = now()

        for asistencia in self.asistencias.all():
            sesion = asistencia.sesion

            sesion.comprobarPeriodo(fecha_actual.month)

            hoy = fecha_actual.date()
            dia_actual = hoy.weekday()
            dia_sesion = DIA_MAP.get(sesion.dia)

            dias_hasta_sesion = (dia_sesion - dia_actual) % 7

            fecha_sesion_date = hoy + timedelta(days=dias_hasta_sesion)

            fecha_sesion = datetime.combine(fecha_sesion_date, sesion.horaInicio)
            fecha_sesion = make_aware(fecha_sesion)

            if 0 <= (fecha_sesion - fecha_actual).total_seconds() <= 3600:
                existe = Notificacion.objects.filter(usuario=self.user, actividad=sesion.actividad, sesion=sesion, fecha=hoy).exists()

                if not existe:
                    Notificacion.notificarActividadUsuarioFinal(sesion.actividad, sesion)
    
    def comprobarAbono(self):
        if self.abono.exists():
            self.tieneAbono = True
        else:
            self.tieneAbono = False

        self.save(update_fields=["tieneAbono"])

    def marcarAbono(self, abono):
        if abono:
            self.tieneAbono = True
            self.save(update_fields=["tieneAbono"])

    def cambiarFavorito(self, *, actividad=None, instalacion=None):
        if actividad and instalacion:
            raise ValueError("Solo puede haber actividad o instalación")

        favorito = Favorito.objects.filter(
            usuarioFinal=self,
            actividad=actividad,
            instalacion=instalacion
        ).first()

        if favorito:
            favorito.delete()
            return False

        Favorito.objects.create(
            usuarioFinal=self,
            actividad=actividad,
            instalacion=instalacion
        )
        return True

    @classmethod
    def contar(cls):
        return cls.objects.count()
    
    @classmethod
    def registrar_usuario(cls, *, nombre, apellidos, sexo, fechaNacimiento,
                          dni, telefono, email, provincia, municipio,
                          localidad, codigoPostal, password, esUAM):

        from .foro import Canal

        User = get_user_model()

        if dni and User.objects.filter(username=dni).exists():
            return {
                "respuesta": "Ya existe un usuario con ese DNI",
                "error": True
            }

        if User.objects.filter(email=email).exists():
            return {
                "respuesta": "Ya existe un usuario con ese email",
                "error": True
            }

        with transaction.atomic():
            codigo = generar_codigo()
    
            username = dni if dni else codigo

            auth_user = User.objects.create_user(
                username=username,
                email=email,
                codigo_usuario=codigo,
                password=password
            )

            usuarioFinal = cls.objects.create(
                user=auth_user,
                nombre=nombre,
                apellidos=apellidos,
                sexo=sexo,
                fechaNacimiento=fechaNacimiento,
                DNI=dni,
                telefono=telefono,
                provincia=provincia,
                municipio=municipio,
                localidad=localidad,
                codigoPostal=codigoPostal,
                esUAM=esUAM
            )

            for canal in Canal.objects.all():
                canal.añadirUsuario(usuarioFinal)

        return {
            "respuesta": usuarioFinal,
            "error": False
        }

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()