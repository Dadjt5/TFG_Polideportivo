from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth import get_user_model

from .constantes import RolAdministrador

class Administrador(models.Model):
    """Modelo para representar a los administradores"""

    nombre = models.CharField(max_length=256, blank=True)
    DNI = models.CharField(max_length=9, blank=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="administrador")

    rol = models.CharField(default=RolAdministrador.USUARIOS, choices=RolAdministrador.choices)

    def __str__(self):
        return f'{self.nombre}, rol: {self.rol}'

    @classmethod
    def registrar_administrador(cls, *, nombre, dni, rol, email, password):
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
            if rol == RolAdministrador.USUARIOS:
                rolAdmin = RolAdministrador.USUARIOS
            elif rol == RolAdministrador.TARIFAS:
                rolAdmin = RolAdministrador.TARIFAS
            elif rol == RolAdministrador.ESPACIOS:
                rolAdmin = RolAdministrador.ESPACIOS
            elif rol == RolAdministrador.RAIZ:
                rolAdmin = RolAdministrador.RAIZ
            else:
                return {
                    "respuesta": "Rol de administrador inválido",
                    "error": True
                }
            
            auth_user = User.objects.create_user(
                username=dni,
                email=email,
                password=password
            )

            admin = cls.objects.create(
                user=auth_user,
                nombre=nombre,
                rol=rolAdmin,
                DNI=dni
            )

        return {
            "respuesta": admin,
            "error": False
        }

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()