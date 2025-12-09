from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    """Modelo para representar a los usuarios (clase abstracta)"""

    nombre = models.CharField(max_length=256, blank=True)
    apellidos = models.CharField(max_length=256, blank=True, null=True)
    DNI = models.CharField(max_length=256, blank=True)
    contraseña = models.CharField(max_length=8)
    consentimiento = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'
