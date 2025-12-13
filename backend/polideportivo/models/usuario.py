from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Usuario(models.Model):
    """Modelo para representar a los usuarios (clase abstracta)"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=256, blank=True)
    apellidos = models.CharField(max_length=256, blank=True, null=True)
    DNI = models.CharField(max_length=256, blank=True)
    contraseña = models.CharField(max_length=8)
    consentimiento = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'
    
    class Meta:
        abstract = True
