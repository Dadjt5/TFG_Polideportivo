from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth import get_user_model
from django.conf import settings

from .usuario import Usuario
from .favorito import Favorito
from .constantes import Sexo, Rol

class UsuarioFinal(Usuario):
    """Modelo para representar al usuario final"""

    fechaNacimiento = models.DateField()
    telefono = models.CharField(max_length=16, default="")
    provincia = models.CharField(max_length=64, default="")
    municipio = models.CharField(max_length=64, default="")
    localidad = models.CharField(max_length=64, default="")
    codigoPostal = models.CharField(max_length=64, default="")
    cuentaBancaria = models.CharField(max_length=64, default="", blank=True)
    actividadesRealizadas = models.PositiveIntegerField(default=0)
    esUAM = models.BooleanField(default=False)
    tieneAbono = models.BooleanField(default=False)
    tieneTDA = models.BooleanField(default=False)

    deportesFavoritos = models.ManyToManyField('Deporte', blank=True, related_name="usuariosFinales")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usuario_final")

    sexo = models.CharField(default=Sexo.NINGUNO, choices=Sexo.choices)
    rol = models.CharField(default=Rol.EXTERNO, choices=Rol.choices)
    
    def save(self, *args, **kwargs):
        if self.rol == Rol.EXTERNO:
            esUAM = False
        else:
            esUAM = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Usuario: {self.id}, nacido el {self.fechaNacimiento}'
    
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
                          localidad, codigoPostal, password, cuentaBancaria=None):

        from .foro import Canal

        User = get_user_model()

        if User.objects.filter(username=dni).exists():
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
            auth_user = User.objects.create_user(
                username=dni,
                email=email,
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
                cuentaBancaria=cuentaBancaria
            )

            for canal in Canal.objects.all():
                canal.añadirUsuario(usuarioFinal)

        return {
            "respuesta": "Usuario registrado correctamente",
            "error": False
        }