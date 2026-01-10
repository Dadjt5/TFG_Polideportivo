from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .constantes import RolAdministrador

class Administrador(models.Model):
    """Modelo para representar a los administradores"""

    nombre = models.CharField(max_length=256, blank=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="administrador")

    rol = models.CharField(default=RolAdministrador.USUARIOS, choices=RolAdministrador.choices)

    def __str__(self):
        return f'{self.nombre}, rol: {self.rol}'
