from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from django.db import models

from .constantes import RolAdministrador

def generar_codigo():
    return uuid.uuid4().hex[:8]

class User(AbstractUser):
    codigo_usuario = models.CharField(max_length=8, unique=True, default=generar_codigo, editable=False)

    @property
    def is_usuario_final(self):
        return hasattr(self, 'usuario_final')

    @property
    def is_monitor(self):
        return hasattr(self, 'monitor')

    @property
    def is_administrador(self):
        return hasattr(self, 'administrador')

    @property
    def is_administrador_raiz(self):
        return hasattr(self, 'administrador') and self.administrador.rol == RolAdministrador.RAIZ

    @property
    def is_administrador_espacios(self):
        return hasattr(self, 'administrador') and self.administrador.rol == RolAdministrador.ESPACIOS

    @property
    def is_administrador_usuarios(self):
        return hasattr(self, 'administrador') and self.administrador.rol == RolAdministrador.USUARIOS

    @property
    def is_administrador_tarifas(self):
        return hasattr(self, 'administrador') and self.administrador.rol == RolAdministrador.TARIFAS